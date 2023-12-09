import sys
sys.path.append('../')
import requests
from github.getHeaders import getHeaders




def create_organization_on_github(api_token, org_name):
    url = f'https://api.github.com/user/orgs'
    print(url)
    data = {
        'name': org_name
    }

    # Make the request
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'created organization {org_name}.')
    else:
        print('Failed to create organization:', response.content)