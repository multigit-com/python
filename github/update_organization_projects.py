import os
import sys

from github.create_repo_on_not_git_repo_folder import create_repo_on_not_git_repo_folder

sys.path.append('../')
from function.flat_array import flat_array

from function.extract_domain_name_from_url import extract_domain_name_from_url
from github.change_default_branch import change_default_branch
from github.get_domain_from_page import get_domain_from_page
from github.create_notexisting_folder import create_notexisting_folder
from github.get_param_from_repo import get_param_from_repo
from github.defaults import defaults
from github.set_github_pages_domain import set_github_pages_domain
from local.create_path import create_path
from local.init_local_repo import init_local_repo
from local.push_local_repo import push_local_repo
from local.clone_repo import clone_repo
from github.set_domain_on_github_org_pages import set_domain_on_github_org_pages


# url: https://developer.github.com/v3/repos/#create-a-repository
# Connect to Github by {API token|api_token|GITHUB_API_TOKEN}
# Connect to Github by:
## human: API token
## code: api_token
## env: GITHUB_API_TOKEN
#
def update_organization_projects(api_token, org_name, repos, domain_name, path_name, root_path):
    # print(repos)
    branch = get_param_from_repo(repos, 'default_branch')

    if branch != 'main':
        change_default_branch(api_token, org_name,'main')

    branch = get_param_from_repo(repos, 'default_branch')
    if not branch:
        branch = 'main'
        change_default_branch(api_token, org_name, 'main')

    print('branch: ' + branch)
    #exit()

    local_path = path_name + "/" + org_name
    create_path(local_path)
    #print(local_path, path_name)

    domain, homepage, description = defaults(domain_name, 'main', 'identity','')

    #print(org_name, domain, homepage, description)
    #create_repo_on_github(api_token, org_name, repo_name, description, domain)

    #exit()
    #set_domain_on_github_org_pages(api_token, org_name, domain)
    #set_github_pages_domain(api_token, org_name, domain)
    #exit()
    #print(repos)
    # update_repo_on_github(api_token, org_name, repo_name, description, domain)
    repo_list = []
    if repos:
        for repo in repos:
            print('repo',repo)
            #page_domain = get_domain_from_page(api_token, org_name, repo)
            #print(page_domain)
            # exit()

            if 'clone_url' in repo:
                # update_default_branch_on_github(api_token, org_name, repo['name'], branch)
                #rename_branch_on_github(api_token, org_name, repo['name'], 'master', 'main')
                clone_repo(repo['clone_url'], repo['name'], local_path)
                # repo_list.append(repo['name'])

    #exit()


    # clone_repos_from_org(org_name, repos, path_name, local_path)
    #create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain)
    # print('----')
    # print(repos)
    # print(repo_list)
    repos_in_orgs = flat_array(repos, 'name')
    print(repos_in_orgs)
    print('----')

    # exit()

    create_notexisting_folder(api_token, org_name, repos_in_orgs, local_path, domain, root_path, branch)
    #configure_github_pages_branch(api_token, org_name, 'main')



    set_github_pages_domain(api_token, org_name, domain, branch)
    exit()
    # push_all_repos(api_token, org_name, repos, local_path)
    # pull_all_repos(local_path)
    init_local_repo(local_path)
    push_local_repo(local_path)

    # configure_github_pages_branch(api_token, org_name, 'main')
    # configure_github_pages_domain(api_token, org_name, domain)
    # print(f'{org_name} / {repo_name} / {branch}..')
    set_github_pages_domain(api_token, org_name, domain)
    #set_github_pages_domain(api_token, org_name, domain)