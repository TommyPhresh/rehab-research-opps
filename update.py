import pandas as pd
from datetime import datetime, timedelta
import logging, duckdb, os
from duckdb.typing import VARCHAR, FLOAT, INTEGER
from flask import current_app

from constants import REFRESH_INTERVAL, specialty_queries,
    LIVE_DB_LOCATION, LIVE_SPECIALTY_LOCATION, TMP_DB_LOCATION,
    TMP_DB_PATH, TMP_SPECIALTY_PATH, BACKUP_DB_PATH, BACKUP_SPECIALTY_PATH
from private_updaters import updaters as privates
from db import get_db
from gov_updaters import updaters as publics 


# FORMAT
    # name - award name
    # org - sponsoring organization
    # desc - brief description
    # deadline - due date
    # link - URL
    # grant - T/F 
# data pipeline
def update(app):
    if not is_fresh():
        with app.app_context():
            print('Not fresh')
            rebuild_data(app)
            update_last_refresh()
    else:
        print('Fresh')

# grabs all API results, computes embeddings
# memory optimized by using .duckdb file and batch processing
# once new parquet file created, then calls calculate_specialty_vectors
def rebuild_data(app, dest='new_data.parquet'):
    if os.path.exists(TMP_DB_LOCATION):
        print('removing deprecated tmp.duckdb')
        os.remove(TMP_DB_LOCATION)

    conn = duckdb.connect(database=TMP_DB_LOCATION, read_only=False)

    try:
        data = get_data()
        if not data:
            print('No data retrieved from pipeline. Aborting.')
            return

        # create new table & set up to receive embedding calculations
        df = pd.DataFrame(data).drop_duplicates(subset='name')
        conn.execute("""
            CREATE OR REPLACE TABLE documents
            AS SELECT * FROM df
            """)
        if 'embedding' not in conn.execute("PRAGMA table_info('documents');").fetchdf()['name'].values:
            conn.execute("""
                ALTER TABLE documents
                ADD embedding FLOAT[1024]
                """)
        else:
            conn.execute("UPDATE documents SET embedding NULL;")
        if 'rowid' not in conn.execute("PRAGMA table_info('documents');").fetchdf()['name'].values:
            conn.execute("CREATE SEQUENCE IF NOT EXISTS rowid_seq START 1")
            conn.execute("ALTER TABLE documents ADD rowid INTEGER DEFAULT nextval('rowid_seq')")
        conn.commit()

        BATCH_SIZE = 250
        db_size = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        rows_processed = 0
        print('Starting batched embedding calculation')

        while True:
            # grab batch
            batch_df = conn.execute(f"""
                SELECT rowid, name, desc
                FROM documents
                WHERE embedding IS NULL
                ORDER BY rowid
                LIMIT {BATCH_SIZE}
                """).fetchdf()
            if batch_df.empty:
                print('Embedding complete')
                break
            
            # calculate batch embeddings
            rows_processed += len(batch_df)
            batch_df['embedding'] = batch_df.apply(
                lambda row: app.model.encode(f"{row['name']}\n{row['desc']}")['dense_vecs'], 
                axis=1
            )
            print(f'Processed {len(batch_df)} rows.')
            print(f'{(rows_processed // db_size)*100}% done.')

            # update .duckdb file with new embeddings
            conn.execute("""
                CREATE OR REPLACE TEMPORARY TABLE batch_updates
                AS SELECT rowid, embedding 
                FROM batch_df
                """)
            conn.execute("""
                UPDATE documents
                SET embedding = batch.embedding
                FROM batch_updates AS batch
                WHERE documents.rowid = batch.rowid
                """)
            conn.commit()

        calculate_specialty_vectors(conn, app)
        
        # updating live db file with rollback thru robust atomic swap
        conn.execute(f"""
            COPY documents
            TO '{TMP_DB_PATH}' (FORMAT PARQUET);
        """)
        if os.path.exists(BACKUP_DB_PATH):
            os.remove(BACKUP_DB_PATH)
        if os.path.exists(LIVE_DB_LOCATION):
            shutil.move(LIVE_DB_LOCATION, BACKUP_DB_PATH)
        else:
            print('CRITICAL ERROR - no live db to back up')
        shutil.move(TMP_DB_PATH, LIVE_DB_LOCATION)
        
        # updating specialty db file the same way
        conn.execute(f"""
            COPY specialty_vectors 
            TO '{TMP_SPECIALTY_PATH}' (FORMAT PARQUET);
        """)
        if os.path.exists(BACKUP_SPECIALTY_PATH):
            os.remove(BACKUP_SPECIALTY_PATH)
        if os.path.exists(LIVE_SPECIALTY_LOCATION):
            shutil.move(LIVE_SPECIALTY_LOCATION, BACKUP_SPECIALTY_PATH)
        else:
            print('CRITICAL ERROR - no live specialty db to back up')
        shutil.move(TMP_SPECIALTY_PATH, LIVE_SPECIALTY_LOCATION)
        
        print('Data refresh complete')        

    except Exception as e:
        print(f'Error!' {e})
        import traceback
        traceback.print_exc()
        raise
    
    # clean up the tmp .duckdb file and the duckdb connection
    finally:
        if conn:
            conn.close()
        if os.path.exists(TMP_DB_LOCATION):
            os.remove(TMP_DB_LOCATION)

# saves batch df to tmp parquet file
def save_batch(batch, batch_num):
    batch.to_parquet(f'C:\\Users\\trich6\\Desktop\\rehab_frontend\\batches\\batch_{batch_num}.parquet')              
       
# updates last refresh timestamp
def update_last_refresh(filename='last_refresh.txt'):
    with open(filename, 'w') as f:
        f.write(datetime.now().isoformat())

# reads last refresh timestamp if available
def get_last_refresh(filename='last_refresh.txt'):
    try: 
        with open(filename, 'r') as f:
            return datetime.fromisoformat(f.read().strip())
    except Exception: 
        return datetime.min

# checks time since last refresh
def is_fresh(interval=REFRESH_INTERVAL):
    last_refresh = get_last_refresh()
    return (datetime.now() - last_refresh) < interval

# converts list of dicts to parquet file 
# for compressed storage on server
def save_to_parquet(conn, filename='new_data.parquet'):
    conn.execute(f"""COPY (
                 SELECT name, org, "desc", deadline, link, isGrant
                 FROM documents
                 )
                 TO '{filename}' (FORMAT 'parquet');""")

# calls all updaters, public and private, then appends
# their results into one list of dicts
def get_data():
    data = []
    for api in privates:
        try: 
            api(data)
            print(f'{api.__name__}')
        except Exception as e:
            print(f'{api.__name__} failed: {e}')
    for api in publics: 
        try:
            api(data)
            print(f'{api.__name__}')
        except Exception as e:
            print(f'{api.__name__} failed: {e}')
    return data

# calculates vector similarity for each specialty on refresh
# replaces live calculation upon user interaction with specialty button
# saves results to specialty_vectors.parquet file
# Args: 
    # conn: duckdb connection 
    # app: Flask app created in the create_app() function in app.py
    # specialty_queries: dict containing pre-defined specialty queries
def calculate_specialty_vectors(conn, app):
    conn.execute("""
        CREATE OR REPLACE TABLE specialty_vectors (
            specialty_name VARCHAR,
            doc_rowid INTEGER,
            similarity FLOAT
        );    
    """)
    conn.commit()
    
    # compute similarities for each specialty query
    for specialty in specialty_queries.keys():
        query_vector = app.model.encode(specialty_queries[specialty]['definition'])['dense_vecs']
        specialty_df = conn.execute("""
            SELECT 
                documents.rowid AS doc_rowid, 
                array_inner_product(?, documents.embedding) AS similarity
            FROM documents
            WHERE documents.embedding IS NOT NULL AND similarity > 0.5
            ORDER BY similarity DESC
        """, (query_vector,)).fetchdf()
        specialty_df['specialty_name'] = specialty
        conn.execute("""
            INSERT INTO specialty_vectors
            SELECT specialty_name, doc_rowid, similarity 
            FROM specialty_df
        """)
        conn.commit()
        print(f'Completed calculations for {specialty}')


