import pandas as pd

# checks for update and converts to correct format
def nih_to_universal_format():
    df = pd.read_csv("NIH_Guide_Results.csv")
    df["Funding Mechanism"] = df["Activity_Code"] + " - Clinical Trials " + df["Clinical_Trials"]
    df["Brief Description"] = "Please click link."
    df["Award Amount"] = "Plesae click link."
    df["Maximum Duration (Yr)"] = "Plesae click link."
    df["Letter of Intent Required?"] = "Please click link."
    df["Relevance"] = "Coming soon."
    df["Specialty"] = "Processing required"
    df["Link"] = '=HYPERLINK("' + df["URL"] + ', "Click here")'
    df.rename(columns={"Title":"Award Name", "Expired_Date":"Due Date"},
              inplace=True)
    df = df.loc[:, ["Award Name","Specialty","Funding Mechanism",
                "Organization","Link","Brief Description","Award Amount",
                "Maximum Duration (Yr)","Letter of Intent Required?",
                "Due Date","Relevance"]]
    return df
