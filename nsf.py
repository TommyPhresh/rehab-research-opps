import webbrowser
from constants import nsf_link, nsf_path


# Downloads ALL available NSF opportunities to user's Downloads folder
def scrape_nsf():
    webbrowser.open(nsf_link)
    # Please click 'Save' on the Download for nsf_funding.csv

# Converts downloaded csv to universal/dashboard format
def nsf_to_universal_format():
    df = pd.read_csv(nsf_path)
    # we only want NaN (N/A) or Cleared statuses
    # NOT Current but no longer receiving proposals
    # OR Waiting for new publication
    df["Status"] = df["Status"].map(lambda x: x if isinstance(x, str) else "N/A")
    df = df[(df["Status"] == "Cleared") | (df["Status"] == "N/A")]
    # WES - We only want types of 'Program', not 'Dear Colleague Letter'
    df = df[(df["Type"] == "Program")]
    # WES - What types of award types do we want?
    # Standard, Continuing, Coop, Fellow, Other, DROP nan
    # create non-obvious columns
    df["Link"] = '=HYPERLINK("' + df["URL"] + ', "Click here")'
    df["Due Date"] = df["Next due date (Y-m-d)"].map(lambda x: x if
                                                     isinstance(x,str) else "Click link")
    df["Due Date"] = df["Due Date"].map(lambda x: x if
                                        (x == "Click link") else x.split(", ")[0])
    df = df[df["Award Type"].notnull()]
    df["Funding Mechanism"] = df["Award Type"].map(lambda x: "NIH " + x)
                                                     
    # renaming & reorganizing
    df.rename(columns={"Title":"Award Name", "Synopsis":"Brief Description",
                       }, inplace=True)
    df = df.loc[:, ["Award Name","Specialty","Funding Mechanism",
                "Organization","Link","Brief Description","Award Amount",
                "Maximum Duration (Yr)","Letter of Intent Required?",
                "Due Date","Relevance"]]
