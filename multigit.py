import argparse
import subprocess
import requests
import os
from urllib.parse import urlparse

from local.load_api_token import load_api_token
from local.fromFilenametoLinesAsArray import fromFilenametoLinesAsArray
from local.create_path import create_path
from local.folder_exist import folder_exist
from local.clone_repo import clone_repo
from function.flat_array import flat_array
from github.get_repos_from_org import get_repos_from_org
from function.arrayElementsAreIncluded import arrayElementsAreIncluded
from function.differenceElementsInArrays import differenceElementsInArrays
from local.generate_template import generate_template
from function.get_subdomain_from_url import get_subdomain_from_url
from function.get_domain_from_url import get_domain_from_url
from function.extract_domain_name_from_url import extract_domain_name_from_url
from github.get_param_from_repo import get_param_from_repo
from github.create_repo_on_github import create_repo_on_github
from github.update_repo_on_github import update_repo_on_github
from local.load_file import load_file
from github.create_notexisting_folder import create_notexisting_folder
from github.configure_github_pages_domain import configure_github_pages_domain
from github.configure_github_pages_branch import configure_github_pages_branch
from github.set_github_pages_domain import set_github_pages_domain
from local.non_git_folders_in_path import non_git_folders_in_path
from local.git_folders_in_path import git_folders_in_path
from github.create_repo_on_not_git_repo_folder import create_repo_on_not_git_repo_folder
from local.pull_all_repos import pull_all_repos
from local.init_local_repo import init_local_repo
from local.push_local_repo import push_local_repo
from local.clone_repos_from_org import clone_repos_from_org
from github.update_github_pages import update_github_pages
from github.enable_github_pages import enable_github_pages
from github.getHeaders import getHeaders
from github.getHeaders2 import getHeaders2
from github.get_repository_list_wtih_github_pages import get_repository_list_wtih_github_pages
from github.change_default_branch import change_default_branch
from github.create_project_in_org import create_project_in_org
from github.update_organization_projects import update_organization_projects
from github.clone_repo_from_org import clone_repo_from_org



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
