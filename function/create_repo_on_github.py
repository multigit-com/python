import requests
import os
import sys
sys.path.append('../')
from function.getHeaders import getHeaders

def create_repo_on_github(api_token, org_name, repo_name, local_path, description, domain):
    # Endpoint to create a repo within an organization
    url = f'https://api.github.com/orgs/{org_name}/repos'
    print(url)
    # Data for the new repo
    data = {
        'name': repo_name,
        'description': description,
        'homepage': "http://" + repo_name + "." + domain,
        'html_url': "http://" + repo_name + "." + domain,
        'private': False  # Set to True if you want a private repository
    }

    # Make the request
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'Successfully created repo {repo_name} under organization {org_name}.')
        repo_info = response.json()

        # Navigate to the local path
        os.chdir(local_path)

        # Initialize the local repository and add the remote
        os.system(f'git init')
        os.system(f'git remote add origin {repo_info["ssh_url"]}')
        os.system(f'git push --set-upstream origin main')
        os.system(f'git pull')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial commit"')
        os.system(f'git push')

        print(f'Initialized local git repository and added remote origin.')

    else:
        print('Failed to create repo:', response.content)