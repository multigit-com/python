import sys
sys.path.append('../')
from function.extract_domain_name_from_url import extract_domain_name_from_url
from local.clone_repo import clone_repo
from local.create_path import create_path


def create_project_in_org(org_name, path_name):
    # print(repos)
    # path_name = "~/github"
    local_path = path_name + "/" + org_name
    create_path(local_path)

    # domain = org_name + '.com'
    domain = 'legacycode.info'
    # branch = 'master'
    branch = 'main'
    repo_name = 'python'
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
    #create_repo_on_github_and_local(api_token, org_name, repo_name, description, domain)
    #rename_branch_on_github(api_token, org_name, repo_name, 'master', 'main')
    clone_url = 'https://github.com/' + org_name + '/' + repo_name + '.git'
    clone_repo(clone_url, repo_name, local_path)