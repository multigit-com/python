import requests
import os
import sys
sys.path.append('../')
from github.create_repo_on_github import create_repo_on_github

def create_repo_on_github_and_local(api_token, org_name, repo_folder, local_path, description, domain):
    # Endpoint to create a repo within an organization
    response = create_repo_on_github(api_token, org_name, repo_folder, description, domain)
    # Check the response from GitHub
    if response.status_code == 201:
        print(f'Successfully created repo {repo_folder} under organization {org_name}.')
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