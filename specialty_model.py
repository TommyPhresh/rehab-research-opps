import duckdb, FlagEmbedding, torch, pyarrow, numpy
from duckdb.typing import VARCHAR, FLOAT

# turn csv of text descriptions into embeddings
def embed_all(data, record_batch_size=100, batch_size=16):
    conn = duckdb.connect()
    # pull in all data from sources
    conn.execute("""
    CREATE TABLE corpus
    FROM data
    """)

    # set up where embeddings will go
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = FlagEmbedding.BGEM3FlagModel('BAAI/bge-m3', use_fp16=True, device=device)
    conn.execute("""
    CREATE TABLE embeddings(
        text VARCHAR,
        embedding FLOAT[1024]
    )    
    """)
    reader = conn.execute("""
    SELECT corpus."Award Name" || corpus."Brief Description" as text 
    FROM corpus
    LEFT JOIN embeddings ON "Award Name" || "Brief Description" = embeddings.text
    WHERE embeddings.text IS NULL
    """).fetch_record_batch(record_batch_size)

    # embed all documents (will take some time)
    i = 0
    for batch in reader: 
        try: 
            batch_text = [x.as_py() for x in batch["text"]]
            embeddings = model.encode(batch_text, batch_size=batch_size)["dense_vecs"].astype(numpy.asfloat32)
            print("converted batch", i)
            batch = batch.add_column(0, "embedding", list(embeddings))
            batch_table = pyarrow.Table.from_batches([batch])
            conn.cursor().execute("""
            INSERT INTO embeddings
            FROM (FROM batch_table SELECT text, embedding)
            """)
            i += 1
        except: 
            batch_text = [x.as_py() for x in batch["text"]]
            embeddings = model.encode(batch_text, batch_size=batch_size)["dense_vecs"].astype(numpy.asfloat32)
            print("converted batch", i)
            batch = batch.add_column(0, "embedding", list(embeddings))
            batch_table = pyarrow.Table.from_batches([batch])
            conn.cursor().execute("""
            INSERT INTO embeddings
            FROM (FROM batch_table SELECT text, embedding)
            """)
            i += 1

    # register vectorize with duckdb connection
    conn.create_function("vectorize", lambda sentence: model.encode(sentence)["dense_vecs"], [VARCHAR], 'FLOAT[1024]')

    # merge text and embeddings into one
    conn.execute("""
    CREATE TABLE merged_table 
    AS SELECT corpus.*, embeddings.embedding
    FROM corpus
    LEFT JOIN embeddings ON "Award Name" || "Brief Description" = embeddings.text
    """)
    value = conn.execute("SELECT * FROM merged_table").fetchdf()
    conn.close()
    return value

# turn one row of embeddings into its specialty column
def classify(embedding):
    specialties = ""
    for specialty in specialty_queries: 
        if (numpy.inner(
            embedding,
            model.encode(specialty_queries[specialty]["definition"])["dense_vecs"]
            ) > specialty_queries[specialty]["threshold"]):
            specialties += specialty + ", "
    return specialties.strip(", ")


# turn df of embeddings into specialty column
def label_specialties(data, dest_path, batch_size=50):
    # set up tables in duckdb
    conn = duckdb.connect()
    conn.execute("""
    CREATE TABLE merged_table 
    FROM data
    """)
    conn.create_function("classify", classify, ['FLOAT[1024]'], VARCHAR)
    # label all columns with their specialties (takes 4-5 hours on a GPU [parallelized])
    offset = 0
    while True: 
        query = """
        SELECT "Award Name", "Brief Description", Specialty, embedding 
        FROM merged_table
        LIMIT {batch_size} OFFSET {offset}
        """
        batch_df = conn.execute(query).fetchdf()
        if batch_df.empty: break
        batch_df["Specialty"] = batch_df["embedding"].apply(classify)
        update_query = """
        UPDATE merged_table
        SET Specialty = ? 
        WHERE "Award Name" = ? AND "Brief Description" = ?
        """
        for _, row in batch_df.iterrows():
            conn.execute(update_query, (row["Specialty"], row["Award Name"], row["Brief Description"]))
        print(offset + batch_size, " completed rows")
        offset += batch_size
    # output to somewhere
    merged_tables = conn.execute("""
    SELECT * 
    FROM merged_table
    """).fetchdf()
    conn.close()
    return merged_tables

# main function
def begin_model(data):
    return label_specialties(embed_all(data))
