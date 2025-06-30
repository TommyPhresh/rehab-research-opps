import requests, pandas as pd, json, csv, time
from io import StringIO
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constants import trials_url, trials_format, trials_statuses, trials_pagesize,
                      empty_response_length, search_conditions,
                      search_interventions, grants_search_terms, nih_url,
                      nih_params, nsf_landing

updaters = [clinical_trials, grants, nih, nsf]


###################
# CLINICAL TRIALS #
###################

# queries clinical trials db for relevant & active trials
def search_clinical_trials(user_query, is_condition):
    query_type = 'query.cond' if is_condition else 'query.intr'
    response = requests.get(trials_url, params={
        'format': trials_format,
        'filter.overallStatus': trials_statuses,
        'pageSize': trials_pagesize,
        query_type: user_query})
    # error handling: empty response or unsuccessful request
    if response.status_code != 200:
        print('HTTP error:', response.text)
        return 1
    elif len(response.text) < empty_response_length:
        print('Your search returned 0 results. Please try again.')
        return 2
    else: return response

# converts API output to webpage format
def trials_formatter(response):
    results = StringIO(response.text)
    data = pd.read_csv(results)
    data.rename(columns={
        'Study Title': 'name',
        'Sponsor': 'org',
        'Brief Summary': 'desc',
        'Primary Completion Date': 'deadline',
        'Study URL': 'link'
        }, inplace=True)
    data = data.loc[:, data.columns.intersection(['name', 'org', 'desc', 'deadline',
                                     'link'])]
    data['grant'] = False
    return data
        
# return updated clinical trials related to PM&R
def clinical_trials(data):
    df = pd.DataFrame()
    for condition in search_conditions:
        df = df._append(trials_formatter(search_clinical_trials(condition, True)))
    for intervention in search_interventions:
        df = df._append(trials_formatter(search_clinical_trials(intervention, False)))
    for item in df.to_dict('records'):
        data.append(item)

##################
#     GRANTS     #
##################

# grants.gov API    
def grants_search(user_query):
    json_data = {
        'keyword': user_query,
        'oppStatuses': 'forecasted|posted'
        }
    response = requests.post(grants_url, headers={}, json=json_data)
    if (response.status_code == 200):
        data = json.loads(response.text)
        if (data['data']['hitCount'] == 0):
            print('No results found.')
            return 1
        else:
            return data
    else:
        data = json.loads(response.text)
        print('HTTP ERROR:', data['message'])
        return 2

# convert grants.gov API response to webpage format        
def grants_formatter(data):
    dict_list = data['data']['oppHits']
    L, res = [], []
    for D in dict_list:
        L.append({k: D[k] for k in ('id', 'title', 'agency', 'closeDate')})

    def date_stripper(date):
        if date != '':
            return datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
        else: return 'No deadline listed.'
        
    for row in L:
        res.append({
            'name': row['title'],
            'org': row['agency'],
            'desc': 'No description.',
            'deadline': date_stripper(row['closeDate']),
            'link': f"https://www.grants.gov/search-results-detail/{row['id']}",
            'grant': True
            })
    return res        

# grants API handler
def grants(data):
    for term in grants_search_terms:
        response = grants_search(term)
        if not isinstance(response, int):
            res_set = grants_formatter(response)
            for item in res_set:
                data.append(item)

###########
#   NIH   #                
###########

# Formats NIH API response to match webpage format
def nih_formatter(response):
    text = StringIO(response.text)
    df = pd.read_csv(text)
    df.rename(columns={
        'Title': 'name',
        'Organization': 'org',
        'Expired_Date': 'deadline',
        'URL': 'link'
        }, inplace=True)
    df = df.loc[:, df.columns.intersection(['name', 'org', 'deadline', 'link'])]
    df['deadline'] = df['deadline'].map(lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d'))
    df['grant'] = True
    df['desc'] = 'No description given.'
    return df.to_dict('records')

# NIH API
def nih(data):
    params = nih_params
    params['daterange'] = f"01011991-{datetime.now().strftime('%m%d%Y')}"
    response = requests.get(nih_url, params=params)
    if response.status_code == 200:
        res_set = nih_formatter(response)
        for item in res_set:
            data.append(item)

###########
#   NSF   #                
###########

# nsf formatting
def nsf_formatter(response):
    df = pd.read_csv(StringIO(response.text))
    df['Status'] = df['Status'].map(lambda x: x if isinstance(x, str) else 'N/A')
    df = df[(df['Status'] == 'Cleared') | (df['Status'] == 'N/A')]
    df = df[(df['Type'] == 'Program')]
    df.rename(columns={
        'Title': 'name',
        'Synopsis': 'desc',
        'Next due date (Y-m-d)': 'deadline',
        'URL': 'link'}, inplace=True)
    df['deadline'] = df['deadline'].map(lambda x: x if isinstance(x, str) else '')
    df['deadline'] = df['deadline'].map(lambda x: x if (x == '') else x.split(', ')[0])
    df['grant'] = True
    df['org'] = 'NSF'
    df = df.loc[:, df.columns.intersection(['name', 'org', 'deadline', 'desc', 'link', 'grant'])]
    return df.to_dict('records')
    

# NSF API
def nsf(data):
    # solve challenge from AWS
    options = Options()
    options.add_argument('--headless')
    options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0')
    driver = webdriver.Chrome(options=options)
    driver.get(nsf_landing)
    time.sleep(2)

    # get all the cookies before closing the driver
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'],
                            domain=cookie['domain'], path=cookie['path'])
    driver.quit()

    # inject headers 
    session.headers.update({
        'User-Agent': ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"),
        'Referer': nsf_landing,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        })

    # poll export endpoint until CSV complete
    start = time.time()
    while True:
        response = session.get(nsf_export, params=nsf_params)
        if response.status_code == 200:
            break
        if response.status_code not in (202,) or (time.time() - start) > 45:
            response.raise_for_status()
        time.sleep(1)

    # finish off
    res_set = nsf_formatter(response)
    for item in res_set:
        data.append(item)
    