import os
import sys
sys.path.append('../')
from function.extract_domain_name_from_url import extract_domain_name_from_url
from github.change_default_branch import change_default_branch
from github.create_notexisting_folder import create_notexisting_folder
from github.create_repo_on_github import create_repo_on_github
from github.set_github_pages_domain import set_github_pages_domain
from local.create_path import create_path
from local.init_local_repo import init_local_repo
from local.push_local_repo import push_local_repo
from local.clone_repo import clone_repo


def update_organization_projects(api_token, org_name, repos, path_name):
    # print(repos)
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
    #create_repo_on_github(api_token, org_name, repo_name, description, domain)
    #exit()
    set_github_pages_domain(api_token, org_name, domain)
    exit()

    # update_repo_on_github(api_token, org_name, repo_name, description, domain)
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                # update_default_branch_on_github(api_token, org_name, repo['name'], branch)
                #rename_branch_on_github(api_token, org_name, repo['name'], 'master', 'main')
                clone_repo(repo['clone_url'], repo['name'], local_path)
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