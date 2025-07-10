import duckdb
from duckdb.typing import VARCHAR, FLOAT
from flask import g, current_app


# checks for existing duckdb connection. if found, closes it 
def close_db(e=None):
    conn = g.pop('db', None)
    if conn is not None:
        conn.close()

# checks for existing duckdb connection. if none found, opens one
def get_db():
    if 'db' not in g:
        conn = duckdb.connect()
        conn.create_function("vectorize",
                lambda sentence: current_app.model.encode(sentence)["dense_vecs"],
                [VARCHAR], 'FLOAT[1024]')
        g.db = conn
        return g.db

# params:
    # conn - duckdb connection object
    # search_term - user-entered query (string)
def basic_query(conn, search_term):
    query = f"""
    SELECT name, org, "desc", deadline,
    array_inner_product(CAST(embedding AS FLOAT[1024]), vectorize('{str(search_term)}')) AS similarity,
    link, isGrant
    FROM {app.db}
    WHERE similarity > 0.5
    ORDER BY similarity DESC
    """
    return conn.execute(query).fetchall()
    
