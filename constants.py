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

search_terms = [
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

nsf_link = "https://new.nsf.gov/funding/opps/csvexport?page&_format=csv"
nsf_path = "C:\\Users\\Student\\Downloads\\nsf_funding.csv"

specialty_queries = {
    "Neuropsych": {"threshold": 0.52, "definition": "Neuropsychology is a specialty that focuses on brain functioning. A neuropsychologist is a licensed psychologist with expertise in how behavior and skills are related to brain structures and systems. Neuropsychology evaluates brain function by testing memory and thinking skills.Individuals who suffer from cognitive difficulties may feel overwhelmed, disorganized, and frustrated because of reduced information-processing abilities. "},
    "MSK": {"threshold": 0.58, "definition": "Musculoskeletal diseases and injuries can limit your day-to-day activities by limiting your movement and strength. Our goal is to help you eliminate or reduce musculoskeletal pain so you can return to the activities you need and want to do. Our physiatrists specialize in conservative, non-surgical treatment of diseases and injuries. Some of our treatments include: prescription of non-narcotic medications, injections to relieve pain and inflammation, such as cortisone injections for the hip, knee, and shoulder, viscosupplementation (gel injections) for the knee, non-surgical treatments such as Coolief (nerve ablation) for the knee, trigger point injections for myofascial neck pain, use of braces and other orthotic devices, physical and occupational therapy."},
    "Pain Mgmt": {"threshold": 0.59, "definition": "There are chronic conditions that are recalcitrant to standard non-operative rehabilitative and surgical treatment. We offer patients a multidisciplinary and in-depth means of managing their conditions. We treat the following conditions: disc herniation and degenerative disc disease, sciatica, spinal stenosis, scoliosis, brain and spine tumors, among other chronic pain-causing conditions."},
    "TBI": {"threshold": 0.60, "definition": "Meeting the inpatient rehabilitation needs of patients with both traumatic and non-traumatic acquired brain injuries including medical conditions, hemorrhage, cancer or infection causing temporary or permanent disabilities. The team is comprised of rehabilitation nurses, physical therapists, occupational therapists, speech and language pathologists, recreational therapists, care managers, dietitians, and psychologists."},
    "Stroke": {"threshold": 0.58, "definition": "The Stroke Specialty Program accepts all types of strokes including thrombotic, embolic, hemorrhagic, and subarachnoid hemorrhage. We accept patients 6 years of age and older, and patients 5 years or younger will be considered on a case-by-case basis. The program is designed to: build strength, improve function and build skills needed to complete daily activities, improve balance, mobility, and safety awareness, improve speech, cognition, and swallowing, prevent future stroke by promoting lifestyle changes to reduce modifiable risk factors and secondary complications, facilitate community inclusion and participation in life roles and interests, introduce resources for assistive technology, community support, advocacy, aging with disability, wellness, driving, promote health coping and adaptation skills."},
    "SCI": {"threshold": 0.63, "definition": "Spinal cord injury/disease is life-altering, usually resulting in either paraplegia or quadriplegia. Patients face the loss of sensory function, motor strength, bowel and bladder control, sexual function, and more. We provide both acute inpatient and follow-up outpatient rehabilitation services for spinal cord injury patients. This group includes patients with trauma, multiple sclerosis, tumors (either primary or metastatic), herniated intervertebral discs with significant neurologic deficit, spontaneous vascular accidents, and spinal cord compression secondary to osteomyelitis or degenerative changes."},
    "Sports Med": {"threshold": 0.60, "definition": "Recovering from a sports injury requires strength and conditioning work, as well as the right mindset. In addition to helping you recover from injury and reduce pain, sports rehabilitation utilizes exercises, movements, and therapeutic interventions to help you get back in the game. Services offered are: fitness science training, active release technique, acupuncture, performance psychology, dry needling, and more."},
    "Cancer": {"threshold": 0.64, "definition": "Cancer rehabilitation is a supportive service that aims to prevent, relieve, and reduce symptoms at any point during your cancer treatment. It will get you ready for treatment, along with the following: balance issues, difficulty swallowing, fatigue, incontinence, constipation, peripheral neuropathy, pain, sexual dysfunction, lymphedema, brain fog, mood disorders, anxiety, and panic attacks."},
    "Limb Loss": {"threshold": 0.604, "definition": "Provision of amputation management including: prevention of contractures, limb edema management, skin complications, evaluation and monitoring of physical therapy and occupational therapy needs, assessment of need for an assistive device or durable medical equipment, on-site work with a prosthetist for customized prosthesis design and evaluation for proper fit and gait, montoring and treatment of related issues such as phantom pain and neuromas, help connecting with community resources"},
    "EMG": {"threshold": 0.64, "definition": "An electrodiagnostic study (EMG study) consists of nerve conduction studies and electromyography. Nerve conduction studies stimulate the nerves with small amounts of electricity to evaluate the electrical properties and function of nerves to help detect diseases or injury. Electromyography studies consist of the insertion of a needle through the skin into a muscle to examine electrical properties and function. Will help diagnose individual nerve or nerve root entrapments, generalized neuropathies, inflammatory demyelinating neuropathies, small fiber sensory neuropathies, myotonia in myotonic myopathies, and disorders of muscles."},
    "Ultrasound": {"threshold": 0.60, "definition": "Rehabilitative ultrasound imaging is a non-invasive tool that can be used to visualize muscles and more accurately assess the origin of musculoskeletal pain and dysfunction. It can successfully evaluate morphologic characteristics of muscles and tendons, muscle activation patterns, outcomes of rehabilitation, pathologic conditions, muscle or tendon stiffness, and biofeedback for muscle retraining."},
    "Intvl Spine": {"threshold": 0.60, "definition": "Spine treatments: education (spine biomechanics), activity modification, orthotics/braces, topical treatments (ultrasound, electrical stimulation), spine-specific physical therapy, spinal manipulation and manual treatments, pain psychology, corticosteroid injections, radiofrequency ablation, vertebral body ablation, spinal cord stimulator implantation, discectomy (relieve pressure on spinal nerve), foraminotomy (treat spinal stenosis, disc herniations, facet arthritis), laminotomy and laminectomy, and spinal fusion (treat degenerative disc disease, spondylolisthesis, scoliosis, spinal tumors, and spinal trauma)."},
    "Spasticity": {"threshold": 0.63, "definition": "Spasticity is an abnormal increase in muscle tone due to a central nervous system disease. Symptoms include: abnormal increase in muscle tone (stiff, tight, painful), difficulty moving joints or relaxing muscles, overactive reflexes, muscle spasms or abnormal movements, limited or loss of range of motion. Treatments include physical or occupational therapy, bracing/orthotics, oral medication, botulinum toxin injections, adult intrathecal baclofen pump, and surgical interventions such as tendon lengthening."},
    "General": {"threshold": 0.61, "definition": "These are general administrative or non-specific awards which provide funding for researchers to put where most needed. Examples may include: upgrading technology available to researchers, funding for increased support staff for researchers, and more. These are specifically to assist researchers in their projects, but are not tied down to any one project."}
}
