import os

from googleapiclient.discovery import build
from googleapiclient.errors import Error

client_service = build('jobs', 'v3')

def basic_keyword_search(client_service, company_name, keyword):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'query': keyword}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'search_mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'job_query': job_query,
    }

    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
    
def run_sample():
    try:
        project_id = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
        response = client_service.projects().companies().list(
            parent=project_id).execute()
        print('Request Id: %s' %
              response.get('metadata').get('requestId'))
        print('Companies:')
        if response.get('companies') is not None:
            for company in response.get('companies'):
                print('%s' % company.get('name'))
        print('')

    except Error as e:
        print('Got exception while listing companies')
        raise e


if __name__ == '__main__':
    run_sample()