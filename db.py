from duckdb.typing import VARCHAR, FLOAT

# params: 
    # conn: duckdb connection object
    # search_term: user-entered query (string)
def basic_query(conn, model, search_term):
    query = f"""
    SELECT "Award Name",
    array_inner_product(CAST(embedding AS FLOAT[1024]), vectorize('{str(search_term)}')) AS similarity,
    Organization, "Due Date", "Brief Description"
    FROM embedded_documents
    WHERE similarity > 0.5
    ORDER BY similarity DESC
    """
    return conn.execute(query).fetchall()
    