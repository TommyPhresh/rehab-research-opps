import requests
import pandas as pd
from io import StringIO

from constants import *

# parses user-entered comma-separated list into formatted user query
# Params:
    # user_query <class 'str'>: user-entered comma-separated list
# Return:
    # returns query string optimized for use with clinicaltrials.gov API
def create_trials_query(user_query):
    splits = user_query.split(",")
    result = ""
    for i in range(0, len(splits)):
        if i == 0:
            result += splits[i]
        else:
            if splits[i][0] == ' ':
                result += " OR"
                result += splits[i]
            else:
                result += " OR "
                result += splits[i]
    return result

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

    elif len(response.text) < empty_response_length:
        # Most likely result of an over-long user query
        # Or using "AND" when "OR" was desired
        # Send user back to query entry
        print("Your query returned 0 results. Please try a different query")
        return 2
        
    else:
        return response

# converts clinicaltrials.gov API response into dashboard universal format
# Params:
# response <class 'requests.models.Response'>
# Return:
# pandas df with universal format columns
def trials_to_universal_format(response):
    results = StringIO(response.text)
    data = pd.read_csv(results)
    data.rename(columns={"Study Title":"Award Name", "Sponsor":"Organization",
                         "Study URL":"Link", "Brief Summary":"Brief Description",
                         "Primary Completion Date":"Due Date"}, inplace=True)
    data = data.loc[:, data.columns.intersection(["Award Name","Organization",
                                                  "Link", "Brief Description","Due Date"])]
    data["Link"] = data["Link"].map(lambda s: "=HYPERLINK(" + s + ", 'Click here')")
    data["Specialty"] = "Processing needed"
    data["Funding Mechanism"] = "Clinical Trial"
    data["Award Amount"] = "Processing needed"
    data["Maximum Duration (Yr)"] = "Processing needed"
    data["Letter of Intent Required?"] = "Processing needed"
    data["Relevance"] = "Coming soon"
    data = data.loc[:, ["Award Name", "Specialty", "Funding Mechanism",
                        "Organization", "Link", "Brief Description",
                        "Award Amount", "Maximum Duration (Yr)",
                        "Letter of Intent Required?", "Due Date", "Relevance"]]
    return data
    


