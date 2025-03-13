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
    "FIC":[],
    "NCATS":[],
    "NCCIH":["Intvl Spine","Pain Mgmt","MSK"],
    "NCI":["Cancer"],
    "NEI":[],
    "NHGRI":[],
    "NHLBI":[],
    "NIA":["Geriatric"],
    "NIAAA":[],
    "NIAID":[],
    "NIAMS":["MSK","Pain Mgmt"],
    "NIBIB":["EMG","Ultrasound"],
    "NICHD":["Pediatrics"],
    "NIDA":["Neuropsych","Pain Mgmt"],
    "NIDCD":[],
    "NIDCR":[],
    "NIDDK":[],
    "NIEHS":[],
    "NIGMS":["Intvl Spine","Pain Mgmt","MSK","SCI","Spasticity","Limb Loss",
             "EMG","Ultrasound","TBI","Stroke","Sports Med","Neuropsych",
             "Cancer","Pediatrics","Geriatric","General"],
    "NIMH":["Neuropsych"],
    "NIMHD":["Neuropsych"],
    "NINDS":["TBI","Stroke","Neuropsych","Spasticity"],
    "NINR":["Intvl Spine","Pain Mgmt","MSK","SCI","Spasticity","Limb Loss",
             "EMG","Ultrasound","TBI","Stroke","Sports Med","Neuropsych",
             "Cancer","Pediatrics","Geriatric","General"],
    "NLM":[],
    "OD":["General"],
    "CLC":["Intvl Spine","Pain Mgmt","MSK","SCI","Spasticity","Limb Loss",
             "EMG","Ultrasound","TBI","Stroke","Sports Med","Neuropsych",
             "Cancer","Pediatrics","Geriatric","General"]
    }
