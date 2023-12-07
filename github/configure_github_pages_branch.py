import sys
sys.path.append('../')
from github.getHeaders import getHeaders
import requests



def configure_github_pages_branch(api_token, org_name, branch='main'):
    # List all repositories in the organization
    url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(url, headers=getHeaders(api_token))

    if response.status_code != 200:
        print('Failed to retrieve repositories:', response.content)
        return

    for repo in response.json():
        repo_name = repo['name']
        pages_url = repo['url'] + '/pages'

        # Get the current GitHub Pages configuration
        pages_config_response = requests.get(pages_url, headers=getHeaders(api_token))

        if pages_config_response.status_code == 200:
            # Update the existing GitHub Pages configuration
            pages_data = {
                'source': {
                    'branch': branch,
                    'path': '/'
                }
            }
            # Send the PATCH request to update the configuration
            update_response = requests.patch(pages_url, json=pages_data, headers=getHeaders(api_token))

            if update_response.status_code == 200:
                print(f"Updated GitHub Pages source branch to '{branch}' for repo: {repo_name}")
            else:
                print(f"Failed to update GitHub Pages configuration for repo: {repo_name}")
        elif pages_config_response.status_code == 404:
            print(f"GitHub Pages is not enabled for repo: {repo_name}, skipping...")
        else:
            print(f"Failed to retrieve GitHub Pages configuration for repo: {repo_name}")