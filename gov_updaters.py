import requests, pandas as pd
from io import StringIO
from constants import trials_url, trials_format, trials_statuses, trials_pagesize, empty_response_length, search_conditions, search_interventions


updaters = [clinical_trials]

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
    
