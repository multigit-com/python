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
from local.create_repo_on_not_git_repo_folder import create_repo_on_not_git_repo_folder
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


def delete_branch_on_github(api_token, org_name, repo_name, branch):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/git/refs/heads/{branch}'
    print(url)
    response = requests.delete(url, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 204:
        print(f'deleted branch {branch} on repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to delete branch:', response.content)



        branch='master'
        delete_branch_on_github(api_token, org_name, repo_name, branch)


def update_default_branch_on_github(api_token, org_name, repo_name, branch):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}'
    print(url)
    data = {
        'default_branch': branch
    }

    # Make the request
    response = requests.patch(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 200:
        print(f'updated default branch {branch} on repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to update default branch:', response.content)



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


def rename_branch_on_github(api_token, org_name, repo_name, branch, new_name):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/branches/{branch}/rename'
    print(url)
    data = {
        'new_name': new_name
    }

    # Make the request
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 200:
        print(f'renamed branch {branch} on repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to rename branch:', response.content)


def new_organization_scenario(org_name, repos):
    # print(repos)
    path_name = args.path
    # path_name = "~/github"
    local_path = path_name + "/" + org_name
    create_path(local_path)

    # domain = org_name + '.com'
    domain = 'legacycode.info'
    # branch = 'master'
    branch = 'main'
    repo_name = 'identity'
    # exit()
    homepage = ''
    # homepage = get_param_from_repo(repos, 'homepage')
    # print(homepage)

    if homepage:
        # set_github_pages_domain(api_token, org_name, domain)
        # homepage = f'{org_name}.github.io/{repo_folder}'
        domain = extract_domain_name_from_url(homepage)

    # print(domain)
    # exit()
    if not homepage:
        homepage = 'http://www.' + domain

    description = repo_name + ', ' + homepage

    print(org_name, domain, homepage, description)
    change_default_branch(api_token, org_name)

    root_path = os.path.dirname(os.path.realpath(__file__))
    #create_notexisting_folder(api_token, org_name, repos, local_path, domain, root_path)
    exit()
    create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain)



    # push_all_repos(api_token, org_name, repos, local_path)
    # pull_all_repos(local_path)
    init_local_repo(local_path)
    push_local_repo(local_path)

    # configure_github_pages_branch(api_token, org_name, 'main')
    # configure_github_pages_domain(api_token, org_name, domain)
    # print(f'{org_name} / {repo_name} / {branch}..')
    set_github_pages_domain(api_token, org_name, domain)
    set_github_pages_domain(api_token, org_name, domain)


def update_organization_projects(org_name, repos):
    # print(repos)
    path_name = args.path
    # path_name = "~/github"
    local_path = path_name + "/" + org_name
    create_path(local_path)

    # domain = org_name + '.com'
    domain = 'legacycode.info'
    # branch = 'master'
    branch = 'main'
    repo_name = 'identity'
    # exit()
    homepage = ''
    # homepage = get_param_from_repo(repos, 'homepage')
    # print(homepage)

    if homepage:
        # set_github_pages_domain(api_token, org_name, domain)
        # homepage = f'{org_name}.github.io/{repo_folder}'
        domain = extract_domain_name_from_url(homepage)

    # print(domain)
    # exit()
    if not homepage:
        homepage = 'http://www.' + domain

    description = repo_name + ', ' + homepage

    print(org_name, domain, homepage, description)
    set_github_pages_domain(api_token, org_name, domain)
    exit()

    # update_repo_on_github(api_token, org_name, repo_name, description, domain)
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                #update_default_branch_on_github(api_token, org_name, repo['name'], branch)
                rename_branch_on_github(api_token, org_name, repo['name'], 'master', 'main')
    exit()

    # change_default_branch(api_token, org_name, repo_name, description, homepage)

    # clone_repos_from_org(org_name, repos, path_name, local_path)
    root_path = os.path.dirname(os.path.realpath(__file__))
    create_notexisting_folder(api_token, org_name, repos, local_path, domain, root_path)
    # exit()
    create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain)

    change_default_branch(api_token, org_name)

    # push_all_repos(api_token, org_name, repos, local_path)
    # pull_all_repos(local_path)
    init_local_repo(local_path)
    push_local_repo(local_path)

    # configure_github_pages_branch(api_token, org_name, 'main')
    # configure_github_pages_domain(api_token, org_name, domain)
    # print(f'{org_name} / {repo_name} / {branch}..')
    set_github_pages_domain(api_token, org_name, domain)
    set_github_pages_domain(api_token, org_name, domain)


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

        #new_organization_scenario(org_name, repos)
        update_organization_projects(org_name, repos)

        exit()

    # python3 ./multigit.py ~/github
