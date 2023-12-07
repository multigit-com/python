import argparse
import subprocess
import requests
import os
from urllib.parse import urlparse

from function.load_api_token import load_api_token
from function.fromFilenametoLinesAsArray import fromFilenametoLinesAsArray
from function.create_path import create_path
from function.folder_exist import folder_exist
from function.clone_repo import clone_repo
from function.flat_array import flat_array
from function.get_repos_from_org import get_repos_from_org
from function.arrayElementsAreIncluded import arrayElementsAreIncluded
from function.differenceElementsInArrays import differenceElementsInArrays
from function.generate_template import generate_template
from function.get_subdomain_from_url import get_subdomain_from_url
from function.get_domain_from_url import get_domain_from_url
from function.extract_domain_name_from_url import extract_domain_name_from_url
from function.get_param_from_repo import get_param_from_repo
from function.create_repo_on_github import create_repo_on_github
from function.update_repo_on_github import update_repo_on_github
from function.load_file import load_file
from function.create_notexisting_folder import create_notexisting_folder
from function.configure_github_pages_domain import configure_github_pages_domain
from function.configure_github_pages_branch import configure_github_pages_branch
from function.set_github_pages_domain import set_github_pages_domain
from function.non_git_folders_in_path import non_git_folders_in_path
from function.git_folders_in_path import git_folders_in_path
from function.create_repo_on_not_git_repo_folder import create_repo_on_not_git_repo_folder
from function.pull_all_repos import pull_all_repos
from function.init_local_repo import init_local_repo
from function.push_local_repo import push_local_repo
from function.clone_repos_from_org import clone_repos_from_org
from function.update_github_pages import update_github_pages
from function.enable_github_pages import enable_github_pages
from function.getHeaders import getHeaders
from function.getHeaders2 import getHeaders2
from function.get_repository_list_wtih_github_pages import get_repository_list_wtih_github_pages
from function.change_default_branch_to_main import change_default_branch_to_main

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
    # print(repos)

        path_name = args.path
        # path_name = "~/github"
        local_path = path_name + "/" + org_name
        create_path(local_path)

        domain = org_name + '.com'
        #domain = 'finofficer.com'
        # branch = 'master'
        branch = 'main'
        repo_name = 'identity'
        # exit()
        homepage=''
        #homepage = get_param_from_repo(repos, 'homepage')
        #print(homepage)

        if homepage:
            # set_github_pages_domain(api_token, org_name, domain)
            # homepage = f'{org_name}.github.io/{repo_folder}'
            domain = extract_domain_name_from_url(homepage)

        #print(domain)
        #exit()
        if not homepage:
            homepage = 'http://www.' + domain

        description = repo_name + ', ' + homepage

        print(org_name, domain, homepage, description)

        update_repo_on_github(api_token, org_name, repo_name, description, domain)
        exit()

        #change_default_branch_to_main(api_token, org_name, repo_name, description, homepage)
        set_github_pages_domain(api_token, org_name, domain)
        # clone_repos_from_org(org_name, repos, path_name, local_path)
        create_notexisting_folder(api_token, org_name, repos, local_path, domain)
        # exit()
        create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain)

        change_default_branch_to_main(api_token, org_name)

        # push_all_repos(api_token, org_name, repos, local_path)
        # pull_all_repos(local_path)
        init_local_repo(local_path)
        push_local_repo(local_path)

        # configure_github_pages_branch(api_token, org_name, 'main')
        # configure_github_pages_domain(api_token, org_name, domain)
        # print(f'{org_name} / {repo_name} / {branch}..')
        set_github_pages_domain(api_token, org_name, domain)
        set_github_pages_domain(api_token, org_name, domain)

        #exit()

    # python3 ./multigit.py ~/github
