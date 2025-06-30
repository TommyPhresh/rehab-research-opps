from datetime import timedelta

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

grants_url = "https://api.grants.gov/v1/api/search2"

grants_search_terms = [
    "Interventional Spine", "Pain Management", "Electromyography", "Electrodiagnostics", "Radiculopathy",
    "Musculoskeletal Rehabilitation", "Ultrasound", "Pediatric Rehabilitation", "Neuropsychology",
    "Rehabilitation Psychology", "Traumatic Brain Injury", "Stroke Rehabilitation", "Spasticity",
    "Physical Therapy", "Occupational Therapy", "Rehabilitation", "Limb Loss",
    ]

search_conditions = [
    "Limb Loss", "Arthritis", "Osteoarthritis", "Herniated Disc", "Scoliosis", "Spinal Stenosis",
    "Traumatic Brain Injury", "Stroke", "Balance Disorder", "Parkinson's Disease",
    "Spinal Cord Injury", "Brain Tumor", "Spine Tumor", "Multiple Sclerosis",
    "Pelvic Floor Disorder", "Concussion", "Developmental Disability", "Ataxia",
    "Functional Neurologic Disorder", "Heart Failure", "Heart Attack", "Angioplasty",
    "Aortic Aneurysm", "Aortic Dissection", "Angina", "Aortic Stenosis", "Arrythmia",
    "Atrial Fibrillation", "Bradycardia", "Cardiomyopathy", "Carotid Artery Disease",
    "Coronary Artery Disease", "Heart Valve Disease", "Hypertrophic Cardiomyopathy",
    "Adult Congenital Heart Disease", "Alzheimer's Disease", "Dementia", "Hand Pain",
    "Wrist Pain", "Lymphedema", "Major Multiple Trauma", "Cerebral Palsy",
    "Guillain-Barre Syndrome", "Amyotrophic Lateral Sclerosis", "Cancer", "Spasticity",
    "Chronic Obstructive Pulmonary Disease", "Coronavirus", "Bronchiectasis",
    "Nontuberculous Mycobacteria", "Speech Disorder", "Swallowing Disorder",
    "Dysphagia", "Dysarthria", "Neurodegenerative Speech Disorder", "Aphasia",
    "Tendonitis", "High Cholesterol", "Sickle Cell Disease", "Facial Paralysis",
    "Trigeminal Neuralgia", "Left Atrial Appendage Occlusion", "Radiculopathy"
    ]

search_interventions = [
    "Lower Extremity Reconstruction", "Limb-Saving Care", "Joint Replacement Surgery",
    "Hip Replacement", "Knee Replacement", "Shoulder Replacement", "Elbow Replacement",
    "Neurological Rehabilitation", "Neurosurgery", "Neuromedicine Pain Management",
    "Neuroradiology", "Vestibular Testing", "Acute Rehabilitation", "Vestibular Rehabilitation",
    "Neurorehabilitation", "Spinal Cord Injury Rehabilitation", "Cardiac Rehabilitation", "Stenting",
    "Coronary Artery Bypass Grafting", "Heart Valve Repair", "Heart Valve Replacement",
    "Minimally Invasive Cardiac Surgery", "Minimally Invasive Valve Surgery",
    "Open Heart Surgery", "Transcatheter Aortic Valve Replacement","Ventricular Assist Device",
    "Heart Transplant", "Cardiac Surgery", "Cognitive Rehabilitation", "Electrodiagnostic Study",
    "Hand Rehabilitation", "Wrist Rehabilitation", "Plastic Surgery", "Reconstructive Surgery",
    "Performing Arts Medicine", "Medically Complex Rehabilitation", "Inpatient Acute Rehabilitation",
    "Physical Therapy", "Occupational Therapy", "Vascular Care", "Cancer Rehabilitation",
    "Pediatric Rehabilitation", "Prosthesis", "Pulmonary Rehabilitation", "Neuromodulation",
    "Botox Therapy", "Speech Therapy", "Sports Injury Rehabilitation", "Aquatic Therapy",
    "Sport Psychology", "Balance Training", "Neuropsychology", "Palliative Care",
    "Spinal Injection"
    ]

nih_url =  "https://vtbgfslh0k.execute-api.us-east-1.amazonaws.com/prod/export_csv"
nih_params = {
    'perpage': 10000,
    'sort': 'reldate:desc',
    'from': 0,
    'type': 'active',
    'parentic': 'all',
    'primaryic': 'all',
    'activitycodes': 'all',
    'doctype': 'all',
    'parentfoa': 'all',
    'clinicaltrials': 'all',
    'fields': 'all',
    'spons': 'true'
    }

nsf_landing = (
    "https://www.nsf.gov/funding/opportunities"
    f"?query=&sort=search_api_relevance_DESC"
    )
nsf_ajax_views = "https://www.nsf.gov/views/ajax?query=&sort=search_api_relevance_DESC&_wrapper_format=drupal_ajax&archived_toggle=current&view_name=funding&view_display_id=all&view_args=&view_path=%2Ffunding%2Fopportunities&view_base_path=funding%2Fopportunities&view_dom_id=45b346671040be2a973595c2df8cf1d31d388d5ecf3567f14e7991c80b898a47&pager_element=0&exposed_form_display=1&_drupal_ajax=1"
nsf_ajax_facets = "https://www.nsf.gov/facets-block-ajax?_wrapper_format=drupal_ajax"
nsf_export = "https://www.nsf.gov/funding/opps/csvexport"

REFRESH_INTERVAL = timedelta(weeks=4)
