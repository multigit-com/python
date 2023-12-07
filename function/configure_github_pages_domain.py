import sys
sys.path.append('../')
from function.getHeaders import getHeaders
import requests



def configure_github_pages_domain(api_token, org_name, domain):
    # List all repositories in the organization
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(repos_url, headers=getHeaders(api_token))

    if response.status_code != 200:
        print('Failed to retrieve repositories:', response.content)
        return

    for repo in response.json():
        # If GitHub Pages API allows enabling Pages, the code would be similar to this:
        pages_url = repo['url'] + '/pages'
        pages_data = {
            'source': {
                'branch': 'main',  # Assuming the branch with your site content is named 'gh-pages'
                'path': '/'  # The root path where your site is located
            },
            'cname': domain,  # Set your custom domain (must be configured in your DNS)
            # Any additional settings...
        }
        pages_response = requests.post(pages_url, json=pages_data, headers=headers)

        if pages_response.status_code == 200 or pages_response.status_code == 201:
            print(f"Configured GitHub Pages for repo: {repo['name']}")
        elif pages_response.status_code == 409:
            print(f"GitHub Pages is already set up for repo: {repo['name']}")
        else:
            print(f"Failed to configure GitHub Pages for repo: {repo['name']}")