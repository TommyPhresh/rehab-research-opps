import pandas as pd
from datetime import datetime, timedelta
import logging, duckdb, os
from duckdb.typing import VARCHAR, FLOAT, INTEGER
from flask import current_app

from constants import REFRESH_INTERVAL, DB_LOCATION, NEW_DB_LOCATION, TMP_DB_LOCATION
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
        
        # save embeddings to parquet file
        conn.execute(f"""
            COPY documents TO 
            '{NEW_DB_LOCATION}'
            (FORMAT PARQUET)
        """)
        print('Saved all updates to {NEW_DB_LOCATION}')

        # atomic swap that ho
        if os.path.exists(DB_LOCATION):
            os.remove(DB_LOCATION)
        shutil.move(NEW_DB_LOCATION, DB_LOCATION)
        print('Data refresh complete')

    # exception handling
    except Exception as e:
        print(f'Error! {e}')
        import traceback
        traceback.print_exc()
        raise

    # clean up tmp files
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
