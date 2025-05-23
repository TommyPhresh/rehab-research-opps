import pandas as pd
import os, time
from constants import *
import trials, grants, nih, nsf, specialty_model

# returns dataframe with all clinical trials retrieved from PM&R-specific
# search terms in dashboard format
def update_clinical_trials():
    df = pd.DataFrame()
    for condition in search_conditions:
        df = df._append(
            trials.trials_to_universal_format(
                trials.search_clinical_trials(
                    condition, True)))
    for intervention in search_interventions:
        df = df._append(trials.trials_to_universal_format(trials.search_clinical_trials(intervention, False)))

    return df

# returns dataframe with all grants retrieved from PM&R-specific
# search terms in dashboard format 
def update_grants():
    df = pd.DataFrame()
    for term in search_terms:
        data = grants.grants_search(term)
        if (not isinstance(data, int)):
            df = df._append(grants.grants_to_universal_format(data))

    return df


def update_nih():
    os.chdir("C:\\Users\\Student\\Documents\\Projects\\rehab-research-opps")
    if os.path.isfile("NIH_Guide_Results.csv"):
        os.remove("NIH_Guide_Results.csv")

    print("Navigate to the following URL: https://grants.nih.gov/funding/nih-guide-for-grants-and-contracts")

# returns dataframe with all NIH opportunities retrieved in dashboard format
def update_nih2():
    return nih.nih_to_universal_format()

# returns dataframe with all NSF opportunities retrieved in dashboard format
def update_nsf():
    os.chdir("C:\\Users\\Student\\Downloads")
    if os.path.isfile("nsf_funding.csv"):
        os.remove("nsf_funding.csv")

    nsf.scrape_nsf()
    print("Click 'Save' on the download in top right")
    time.sleep(10)
    return nsf.nsf_to_universal_format()

# combines all 4 sources into one CSV for clinician processing    
def update():
    # create one central csv
    df = update_clinical_trials()
    df = df._append(update_grants())
    update_nih()
    time.sleep(120)
    df = df._append(update_nih2())
    df = df._append(update_nsf())
    df = df.drop_duplicates()
    # get specialty column created 
    labeled_df = specialty_model.begin_model(df)

