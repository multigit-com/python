import argparse
# Importing required module
# import subprocess
import os

from github.has_valid_credentials import has_valid_credentials
from github.get_repos_from_org import get_repos_from_org
from github.get_owner_json import get_owner_json
from github.get_domain_from_page import get_domain_from_page
from github.update_organization_on_github import update_organization_on_github
from github.update_organization_projects import update_organization_projects
from local.fromFilenametoLinesAsArray import fromFilenametoLinesAsArray
from local.load_api_token import load_api_token

"""
Enable GitHub Pages for a repository and optionally set a custom domain.
:param token: str. Your GitHub token with the appropriate permissions.
:param org_name: str. The name of your organization.
:param repo_name: str. The name of your repository.
:param branch: str. The name of the branch to publish (e.g., 'main', 'gh-pages').
:param domain: str. Optional custom domain for GitHub Pages.
"""

if __name__ == "__main__":
    # Load the GitHub API token
    api_token = load_api_token()
    headers = {'Authorization': f'token {api_token}'}

    # parameterize the command line arguments
    parser = argparse.ArgumentParser(description='Clone GitHub repositories')
    # parser.add_argument('-o', '--org', type=str, required=True, help='Organization name')
    # parser.add_argument('-p', '--path', type=str, required=True, help='Path')
    # argument without prefix
    # parser.add_argument('org', type=str, help='Organization name')
    parser.add_argument('path', type=str, help='Path ~/github')
    args = parser.parse_args()
    root_path = os.path.dirname(os.path.realpath(__file__))
    # print(root_path)
    # exit()

    # print(args.path)
    # exit(1)

    # Load the organizations

    orgs = fromFilenametoLinesAsArray('.orgs')
    data = get_owner_json("owner/telemonit.json")

    # print(orgs)
    # Loop through the organizations and clone their repositories
    for row in orgs:
        org_name = row.split(' ')[0]
        domain = row.split(' ')[1]
        print(row, org_name, domain)
        print(f"!!! Fetching repos for org: {org_name}")
        if has_valid_credentials(org_name, headers):
            repos = get_repos_from_org(org_name, headers)
            # print(repos)
            # new_organization_scenario(org_name, repos)
            if not org_name:
                print("!!! Error: org_name cannot be empty.")

            # Update the 'name' value with the provided org_name
            data['name'] = org_name
            data['description'] = data['company'] + " " + org_name,

            update_organization_on_github(api_token, org_name, data)
            # exit()

            update_organization_projects(api_token, org_name, repos, domain, args.path, root_path)
            # repos_url = f'https://api.github.com/orgs/{org_name}/repos'
            repos_url = f'https://github.com/orgs/{org_name}/repositories'
            os.system(f'xdg-open {repos_url}')
            # create_project_in_org(org_name, args.path)

        exit()

    # python3 ./multigit.py ~/github
