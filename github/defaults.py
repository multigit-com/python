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


def defaults(domain = 'legacycode.info', branch = 'main', repo_name = 'identity', homepage = ''):
    # domain = org_name + '.com'
    # homepage = get_param_from_repo(repos, 'homepage')
    # print(homepage)
    if homepage:
        # set_github_pages_domain(api_token, org_name, domain)
        # homepage = f'{org_name}.github.io/{repo_folder}'
        domain = extract_domain_name_from_url(homepage)

    if not homepage:
        homepage = 'http://www.' + domain

    description = repo_name + ', ' + homepage

    return domain, homepage, description
