import pandas as pd
from constants import nih_org_map

# Creates list of organizations to be mapped to PM&R specialties
    # Params:
        # row - Pandas series
    # Return:
        # list of organizations (possible duplicates)
def all_orgs(row):
    orgs = [row["Organization"]]
    if isinstance(row["Participating_Orgs"], str):
        participating = row["Participating_Orgs"].split(", ")
        for org in participating:
            orgs.append(org)
    return orgs

# Maps participating organizations to PM&R specialties
    # Params:
        # row - Pandas Series: list of organization abbreviations
    # Return:
        # set of specialties with no duplicates
def specialty_map(row):
    specialties = set()
    for org in nih_org_map:
        if (org in row):
            for specialty in nih_org_map[org]:
                specialties.add(specialty)
    if (len(specialties) != 0):
        s = str(list(specialties))
        return s[1:len(s)-1]
    else: return ""

# checks for update and converts to correct format
def nih_to_universal_format():
    df = pd.read_csv("NIH_Guide_Results.csv")
    df["Funding Mechanism"] = df["Activity_Code"] + " - Clinical Trials " + df["Clinical_Trials"]
    df["Brief Description"] = "Please click link."
    df["Award Amount"] = "Please click link."
    df["Maximum Duration (Yr)"] = "Please click link."
    df["Letter of Intent Required?"] = "Please click link."
    df["Relevance"] = "Coming soon."
    df["Link"] = '=HYPERLINK("' + df["URL"] + ', "Click here")'
    df.rename(columns={"Title":"Award Name", "Expired_Date":"Due Date"},
              inplace=True)
    df["All_Orgs"] = df.apply(all_orgs, axis=1)
    df["Specialty"] = df["All_Orgs"].map(lambda x: specialty_map(x))
    df = df.loc[:, ["Award Name","Specialty","Funding Mechanism",
                "Organization","Link","Brief Description","Award Amount",
                "Maximum Duration (Yr)","Letter of Intent Required?",
                "Due Date","Relevance"]]
    return df
