import argparse

from github.get_repos_from_org import get_repos_from_org
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
    # print(args.path)
    # exit(1)

    # Load the organizations

    orgs = fromFilenametoLinesAsArray('.orgs')

    # Loop through the organizations and clone their repositories
    for org_name in orgs:
        # print(f"Fetching repos for org: {org}")
        repos = get_repos_from_org(org_name, headers)

        # new_organization_scenario(org_name, repos)
        update_organization_projects(api_token, org_name, repos, args.path)
        #create_project_in_org(org_name, args.path)


        exit()

    # python3 ./multigit.py ~/github
