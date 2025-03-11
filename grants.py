import requests, json
import pandas as pd

from constants import *

# grants.gov API not very useful but should keep it as an option anyways
# NOTE: can only handle one keyword at a time (NO LISTS)
def grants_search(user_query):
    json_data = {
        "keyword":user_query,
        "oppStatuses":"forecasted|posted"
        }
    response = requests.post(grants_URL, headers={}, json=json_data)
    if (response.status_code == 200):
        data = json.loads(response.text)
        if (data['data']['hitCount'] == 0):
            print("No results found. Please try a different search.")
            return -1
        else:
            return data
    else:
        data = json.loads(response.text)
        print("ERROR - ", response.status_code, " ", data['message'])
        return -1

# converts grants.gov API response into dashboard universal format
# Params:
    # response <class 'requests.models.Response'>
# Return:
    # pandas df with universal format columns 
def grants_to_universal_format(data):
    dict_list = data['data']['oppHits']
    df = pd.DataFrame(dict_list)
    df.rename(columns={"title":"Award Name",
                       "closeDate":"Due Date",
                       "agencyCode":"Organization"}, inplace=True)
    df["Specialty"] = "Processing needed"
    df["Funding Mechanism"] = "Discretionary grant"
    df['Award Amount'] = "Processing needed"
    df['Maximum Duration (Yr)'] = "Processing needed"
    df["Letter of Intent Required?"] = "Processing needed"
    df["Relevance"] = "Coming soon"
    df["Link"] = "grants.gov does not include links; please search award name"
    df['Brief Description'] = "grants.gov does not include links; please search award name"
    df = df.loc[:, ["Award Name", "Specialty", "Funding Mechanism",
                        "Organization", "Link", "Brief Description",
                        "Award Amount", "Maximum Duration (Yr)",
                        "Letter of Intent Required?", "Due Date", "Relevance"]]
    return df
                       

