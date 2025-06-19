from private_updaters import updaters as privates
from gov_updaters import *
from functools import reduce

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
    # Name - award name
    # Org - sponsoring organization
    # Desc - brief description
    # 
# 
def update():
    data = get_data()

def get_data():
    data = []
    for api in privates:
        api(data)
    publics = gov_updaters_all
    result = reduce(lambda f, func: func(f), privates, data)
    return reduce(lambda f, func: func(f), publics, result)


