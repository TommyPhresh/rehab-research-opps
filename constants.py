# clinical trials constants 
trials_url = "https://clinicaltrials.gov/api/v2/studies"
trials_format = "csv"
trials_statuses = "NOT_YET_RECRUITING,RECRUITING,AVAILABLE,ENROLLING_BY_INVITATION"
trials_pagesize = 1000
empty_response_length = 407
# see datadictionary.txt for column definitions
columns = ["Award Name", "Specialty", "Funding Mechanism",
                  "Organization", "Link", "Brief Description", "Award Amount",
                  "Maximum Duration (Yr)", "Letter of Intent Required?",
                  "Due Date", "Relevance"]

grants_URL = "https://api.grants.gov/v1/api/search2"

nih_org_map = {
    "FIC":["Any"],
    "NCATS":["General"],
    "NCCIH":["Intvl Spine","Pain Mgmt","MSK"],
    "NCI":["Cancer"],
    "NEI":[],
    "NHGRI":[],
    "NHLBI":[],
    "NIA":["Any"],
    "NIAAA":[],
    "NIAID":[],
    "NIAMS":["MSK","Pain Mgmt"],
    "NIBIB":["EMG","Ultrasound", "MSK"],
    "NICHD":["Pediatrics"],
    "NIDA":["Neuropsych","Pain Mgmt"],
    "NIDCD":[],
    "NIDCR":[],
    "NIDDK":[],
    "NIEHS":[],
    "NIGMS":["Any"],
    "NIMH":["Neuropsych"],
    "NIMHD":["Neuropsych"],
    "NINDS":["TBI","Stroke","Neuropsych","Spasticity"],
    "NINR":["Any"],
    "NLM":[],
    "OD":["General"],
    "CLC":["Any"]
    }

nsf_link = "https://new.nsf.gov/funding/opps/csvexport?page&_format=csv"
nsf_path = "C:\\Users\\Student\\Downloads\\nsf_funding.csv"
