import requests
import pandas as pd

from constants import *

# grabs up to 1000 clinical trial opportunities from clinicaltrials.gov
# Params:
    # user_query <class 'str'>: pre-processed user-entered list
    #                                      of conditions or interventions                                        
    # is_condition <class 'bool'>: True if user is searching by condition
# Return:
    # returns HTTP response to be processed if well-formed
    # returns error code 1 if response status is not 200
    # returns error code 2 if response is empty (no matching opportunities)
def search_clinical_trials(user_query, is_condition):
    query_type = "query.cond" if is_condition else "query.intr"
    response = requests.get(trials_url, params=
                            {"format":trials_format,
                             "filter.overallStatus":trials_statuses,
                             "pageSize":trials_pagesize,
                             query_type: user_query})
    
    if response.status_code != 200:
        # malformed request - should never be reached
        print("HTTP QUERY ERROR: ", response.text)
        return 1

    elif len(response.text < empty_response_length):
        # Most likely result of an over-long user query
        # Or using "AND" when "OR" was desired
        # Send user back to query entry
        print("Your query returned 0 results. Please try a different query")
        return 2
        
    else:
        return response


