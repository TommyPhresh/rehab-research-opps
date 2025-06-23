import pandas as pd
from datetime import datetime, timedelta

from constants import REFRESH_INTERVAL
from private_updaters import updaters as privates
from main import conn, model
# from gov_updaters import updaters as publics 


"""
Cache using parquet
create is_fresh fn to check if its been enough time to update again
create rebuild_cache fn to refresh cache
create get_data fn to return a new list of dicts every time period

call the get_data fn (which has cache check in it)
this is super cheap 99% of the time

use scheduler and add a job such that each period cache is refreshed

call inside duckdb with original query 
"CREATE TABLE_NAME VIEW table AS SELECT ..."
"REFRESH TABLE_NAME VIEW table

Pass to Jinja the same way I've been doing except Parquet not csv
"""

# FORMAT
    # name - award name
    # org - sponsoring organization
    # desc - brief description
    # deadline - due date
    # link - URL
    # grant - T/F 
# 
def update():
    if not is_fresh():
        logging.log(logging.INFO, 'Not fresh')
        rebuild_data()
        update_last_refresh()
    else:
        logging.log(logging.INFO, 'Fresh')

# grabs all API results, computes embeddings, and 
# writes results to a Parquet file on server
def rebuild_data(dest='data.parquet'):
    # grab all API results
    data = get_data()
    # compute embeddings
    df = pd.DataFrame(data)
    conn.execute("DROP TABLE documents")
    conn.execute("CREATE TABLE documents AS SELECT * FROM df")
    conn.execute("ALTER TABLE documents ADD embedding FLOAT[1024]")
    conn.execute("""
    UPDATE documents
    SET embedding = vectorize(name || ' ' || "desc")
    WHERE embedding IS NULL
    """)

    # save to Parquet
    save_to_parquet(dest)

    
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
def save_to_parquet(filename='data.parquet'):
    conn.execute(f"COPY documents TO '{filename}' (FORMAT 'parquet');")

# calls all updaters, public and private, then appends
# their results into one list of dicts
def get_data():
    data = []
    for api in privates:
        try: 
            api(data)
        except: pass
    # for api in publics: 
        # api(data)
    return data

