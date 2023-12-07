import requests
import sys
sys.path.append('../')
from github.getHeaders import getHeaders


def update_repo_on_github(api_token, org_name, repo_name, description, domain):
    # Endpoint to create a repo within an organization
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    print(url)
    # Data for the new repo
    data = {
        'name': repo_name,
        'description': description,
        'homepage': "http://" + repo_name + "." + domain,
        #'html_url': "http://" + repo_name + "." + domain,
        #'private': False  # Set to True if you want a private repository
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }

    # Make the request
    response = requests.patch(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'updated repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to update repo:', response.content)