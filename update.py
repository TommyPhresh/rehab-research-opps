import pandas as pd
from datetime import datetime, timedelta
import logging, duckdb
from duckdb.typing import VARCHAR, FLOAT
from flask import current_app

from constants import REFRESH_INTERVAL
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

# grabs all API results, computes embeddings, and 
# writes results to a Parquet file on server
def rebuild_data(app, dest='data.parquet'):
    conn = duckdb.connect()
    conn.create_function('vectorize',
                         lambda sentence: app.model.encode(sentence)['dense_vecs'],
                         [VARCHAR],
                         'FLOAT[1024]')
                         
    # grab all API results
    data = get_data()
    # compute embeddings
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset='name')
    try:
        conn.execute("DROP TABLE IF EXISTS documents")
    except Exception as e:
        pass
    conn.execute("CREATE TABLE documents AS SELECT * FROM df")
    conn.execute("ALTER TABLE documents ADD embedding FLOAT[1024]")
    conn.execute("""
    UPDATE documents
    SET embedding = vectorize(name || ' ' || "desc")
    WHERE embedding IS NULL
    """)

    # save to Parquet
    try:
        save_to_parquet(conn, dest)
    finally:
        conn.close()

    
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
def save_to_parquet(conn, filename='data.parquet'):
    conn.execute(f"COPY documents TO '{filename}' (FORMAT 'parquet');")

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
        api(data)
    return data
