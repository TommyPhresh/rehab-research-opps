import pandas as pd
from datetime import datetime, timedelta
import logging, duckdb
from duckdb.typing import VARCHAR, FLOAT, INTEGER
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
def rebuild_data(app, dest='new_data.parquet'):
    conn = duckdb.connect()
    conn.create_function('vectorize',
                         lambda sentence: app.model.encode(sentence)['dense_vecs'],
                         [VARCHAR],
                         'FLOAT[1024]')
                         
    # grab all API results
    data = get_data()
    # compute embeddings
    print('retrieved all data')
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset='name')
    try:
        conn.execute("DROP TABLE IF EXISTS documents")
    except Exception as e:
        pass
    conn.execute("CREATE TABLE documents AS SELECT * FROM df")
    conn.execute("ALTER TABLE documents ADD embedding FLOAT[1024]")
    conn.execute("CREATE SEQUENCE rowid_seq START 1")
    conn.execute("ALTER TABLE documents ADD rowid INTEGER DEFAULT nextval('rowid_seq')")
    # the big one - batched for log-ability & pause-ability
    # save {BATCH_SIZE} rows to new parquet in background (no effect on
    # prod db), repeated {len(documents)} times until complete,
    # then change the name of the new file to 'data.parquet' once 100%
    i = 1
    batch_size = 250
    table_size = len(df)
    while True:
        batch = conn.execute(f"""
                SELECT rowid, name, org, "desc", deadline, link, isGrant
                FROM documents
                WHERE embedding IS NULL
                LIMIT {batch_size}
                """).fetchdf()

        if batch.empty:
            print("DONE")
            break
        
        print("Batch:", i, "of", table_size / batch_size + 1)
        for _, row in batch.iterrows():
            conn.execute(f"""
                UPDATE documents
                SET embedding = vectorize(? || ' ' || ?)
                WHERE rowid = ?
                """,(row['name'], row['desc'], row['rowid']))
            
        save_batch(batch, i)
        i += 1       
    # the final save to data.parquet
    try:
        save_to_parquet(conn, dest)
    finally:
        conn.close()

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
