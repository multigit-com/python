import argparse
import subprocess
import requests
import os
from urllib.parse import urlparse


def load_api_token(filename='.token'):
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            return file.readline().strip()


def fromFilenametoLinesAsArray(filename='.folders'):
    lines = None
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
    else:
        print(f"{filename} file does not exist")

    return lines


def create_path(path_folder):
    subprocess.run(['mkdir', '-p', path_folder])


# function to check if folder exist
def folder_exist(path_folder):
    return os.path.exists(path_folder)


def clone_repo(clone_url, repo_name, clone_path):
    # Create the directory if it doesn't exist.
    if not os.path.exists(clone_path):
        os.makedirs(clone_path)

    # Run git clone within the specified path.
    if folder_exist(clone_path + "/" + repo_name):
        result = subprocess.run(['git', 'pull'], cwd=clone_path + "/" + repo_name)
        print(f"Pull {repo_name} with exit code {result.returncode}")
    else:
        result = subprocess.run(['git', 'clone', clone_url], cwd=clone_path)
        print(f"Cloned {repo_name} with exit code {result.returncode}")


def flat_array(original_array, by_name='value'):
    return [element[by_name] for element in original_array]
    # return [element[by_name] for element in original_array if element.get('name') == 'text']


def get_repos_from_org(org_name, headers):
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(repos_url, headers=headers)
    return response.json() if response.status_code == 200 else None


# Function to compare two arrays
def arrayElementsAreIncluded(array_a, array_b):
    # Convert both lists to sets
    set_a = set(array_a)
    set_b = set(array_b)

    # Check if set A is a subset of set B
    return set_a.issubset(set_b)


# Function to compare two arrays and get elements of A not in B
def differenceElementsInArrays(array_a, array_b):
    # Convert both arrays to sets
    set_a = set(array_a)
    set_b = set(array_b)

    # Return the difference
    return list(set_a - set_b)


def generate_template(words, template_path, target_project_folder):
    if not os.path.exists(target_project_folder):
        os.makedirs(target_project_folder)
    # get list of file from path
    files = os.listdir(template_path)
    print(files)

    for template_file in files:
        template_path_file = template_path + "/" + template_file
        project_path_file = target_project_folder + "/" + template_file
        print('template_path_file', template_path_file)

        # get file and replace in the template each words from array by names and values {domain: value, organization: value}
        with open(template_path_file, 'r') as file:
            template = file.read()

        # list in for loop value and name from array elements
        for key, value in words.items():
            template = template.replace("{" + key + "}", value)

        print(f"Template {template_path_file}: {template}")
        # save the template in path
        with open(project_path_file, 'w') as file:
            file.write(template)


# to split up the url to domain name from subdomain
def get_subdomain_from_url(url):
    return url.split('/')[0]


# to split up the url to domain name without subdomain prefix oonly name and tld extension
def get_domain_from_url(url):
    return url.split('/')[2]


# Function to extract the domain name without subdomain but with the TLD
def extract_domain_name_from_url(url):
    domain_name = None
    if (url):
        # Parse the URL to get the netloc (network location part)
        netloc = urlparse(url).netloc

        # Split the netloc into parts by '.'
        netloc_parts = netloc.split('.')

        # Extract the last two parts for domain and TLD
        # This assumes a standard TLD; does not account for country-code TLDs like '.co.uk'
        domain_name = '.'.join(netloc_parts[-2:])

    return domain_name


def get_param_from_repo(repos, repo_name='homepage'):
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                if (repo['fork'] == False):
                    return repo[repo_name]
    return None


# create repository on github by api call
def create_repo_on_github(api_token, org_name, repo_name, local_path, description, domain):
    # Endpoint to create a repo within an organization
    url = f'https://api.github.com/orgs/{org_name}/repos'
    print(url)
    # Data for the new repo
    data = {
        'name': repo_name,
        'description': description,
        'homepage': "http://" + repo_name + "." + domain,
        'private': False  # Set to True if you want a private repository
    }

    # Make the request
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'Successfully created repo {repo_name} under organization {org_name}.')
        repo_info = response.json()

        # Navigate to the local path
        os.chdir(local_path)

        # Initialize the local repository and add the remote
        os.system(f'git init')
        os.system(f'git remote add origin {repo_info["ssh_url"]}')
        os.system(f'git push --set-upstream origin main')
        os.system(f'git pull')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial commit"')
        os.system(f'git push')

        print(f'Initialized local git repository and added remote origin.')

    else:
        print('Failed to create repo:', response.content)


def load_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        print(f"{filename} file does not exist")


def create_notexisting_folder(api_token, org_name, repos, path_folder, domain):
    expected_folders = fromFilenametoLinesAsArray('.folders')
    repos_in_orgs = flat_array(repos, 'name')
    print(repos_in_orgs)
    # Call the function with your arrays
    # result = arrayElementsAreIncluded(expected_folders, repos_in_orgs)
    # print(result)
    not_existing_folder = differenceElementsInArrays(expected_folders, repos_in_orgs)
    print(not_existing_folder)
    if not_existing_folder:
        for repo_folder in not_existing_folder:
            words = {
                'domain': domain,
                'homepage': "http://" + repo_folder + "." + domain,
                'repository': repo_folder,
                'organization': org_name,
                'branch': get_param_from_repo(repos, 'default_branch')
            }
            template_path = os.path.dirname(os.path.realpath(__file__)) + "/templates/" + repo_folder
            print(template_path)
            target_path=path_folder + "/" + repo_folder
            generate_template(words, template_path, target_path)
            description = load_file(target_path + "/description.txt")
            # create repository on github by api call
            create_repo_on_github(api_token, org_name, repo_folder, target_path, description, domain)


# Function to configure GitHub Pages within a repo of an organization
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


# Function to configure GitHub Pages to use the main/master branch
def configure_github_pages_branch(api_token, org_name, branch='main'):
    # List all repositories in the organization
    url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(url, headers=getHeaders(api_token))

    if response.status_code != 200:
        print('Failed to retrieve repositories:', response.content)
        return

    for repo in response.json():
        repo_name = repo['name']
        pages_url = repo['url'] + '/pages'

        # Get the current GitHub Pages configuration
        pages_config_response = requests.get(pages_url, headers=getHeaders(api_token))

        if pages_config_response.status_code == 200:
            # Update the existing GitHub Pages configuration
            pages_data = {
                'source': {
                    'branch': branch,
                    'path': '/'
                }
            }
            # Send the PATCH request to update the configuration
            update_response = requests.patch(pages_url, json=pages_data, headers=getHeaders(api_token))

            if update_response.status_code == 200:
                print(f"Updated GitHub Pages source branch to '{branch}' for repo: {repo_name}")
            else:
                print(f"Failed to update GitHub Pages configuration for repo: {repo_name}")
        elif pages_config_response.status_code == 404:
            print(f"GitHub Pages is not enabled for repo: {repo_name}, skipping...")
        else:
            print(f"Failed to retrieve GitHub Pages configuration for repo: {repo_name}")


# Function to set the domain for all projects in an organization on GitHub
def set_github_pages_domain(api_token, org_name, domain):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    # Iterate over all pages of repositories
    while url:
        response = requests.get(url, headers=getHeaders(api_token))
        print(url)

        if response.status_code != 200:
            print('Failed to retrieve repositories:', response.content)
            return

        # Loop over each repo and set the GitHub Pages domain
        for repo in response.json():
            if repo['name'] == '.github':
                subdomain = "www" + "." + domain
                continue
            else:
                subdomain = repo['name'] + "." + domain

            print("0", repo['name'])

            result = get_repository_list_wtih_github_pages(api_token, org_name, repo['name'])
            print("1", result)
            # repo['default_branch']
            branch = 'main'

            if not result:
                result = enable_github_pages(api_token, org_name, repo['name'], branch, subdomain)

            print('2', result)

            if result and not result['cname']:
                result = update_github_pages(api_token, org_name, repo['name'], branch, subdomain)

            print('3', result)

            # if (result['status'] == 'built'):

            # update_github_pages(api_token, org_name, repo['name'], repo['default_branch'], subdomain)

        # Fetch the next page of repositories, if available
        url = response.links.get('next', {}).get('url', None)


def non_git_folders_in_path(path_folder):
    files = os.listdir(path_folder)
    # print(files)
    folders = []
    for file in files:
        current_path = os.path.join(path_folder, file)
        if folder_exist(current_path + "/" + ".git"):
            print(f"GIT Exist: {current_path}")
        else:
            folders.append(f"{current_path}")
    return folders


def git_folders_in_path(path_folder):
    files = os.listdir(path_folder)
    folders = []
    for file in files:
        current_path = os.path.join(path_folder, file)
        if folder_exist(current_path + "/" + ".git"):
            folders.append(f"{current_path}")
    return folders


# api_token, repos, org_name, path_name
def create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain):
    # Git not exist, check if exist the remote repo on github
    remote_repos = flat_array(repos, 'name')
    print(remote_repos)
    print(local_path)
    non_git_local_repos = non_git_folders_in_path(local_path)
    # print('non_git_local_repos', non_git_local_repos)
    not_expected_folders = [local_path + '/.idea']
    # print('not_expected_folders', not_expected_folders)
    # remove from array existing elements from another array
    filtered_non_git_folders = differenceElementsInArrays(non_git_local_repos, not_expected_folders)
    print(filtered_non_git_folders)
    # not_existing_folder = differenceElementsInArrays(expected_folders, repos_in_orgs)
    for repo_folder in filtered_non_git_folders:
        # get last folder from path
        repo_name = repo_folder.split('/')[-1]
        print(repo_name)
        # create repository on github by api call
        description = load_file(repo_folder + "/description.txt")
        create_repo_on_github(api_token, org_name, repo_name, repo_folder, description, domain)


def pull_all_repos(local_path):
    # Git not exist, check if exist the remote repo on github
    git_local_repos = git_folders_in_path(local_path)
    # print(git_local_repos)
    not_expected_folders = [local_path + '/.idea']
    # remove from array existing elements from another array
    filtered_non_git_folders = differenceElementsInArrays(git_local_repos, not_expected_folders)
    print(filtered_non_git_folders)
    # not_existing_folder = differenceElementsInArrays(expected_folders, repos_in_orgs)
    for repo_folder in filtered_non_git_folders:
        # get last folder from path
        repo_name = repo_folder.split('/')[-1]
        print(repo_name)
        # create repository on github by api call

        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        # os.system(f'git push --set-upstream origin main')
        os.system(f'git pull')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial commit"')
        os.system(f'git push')


def init_local_repo(local_path):
    git_local_repos = git_folders_in_path(local_path)
    for repo_folder in git_local_repos:
        repo_name = repo_folder.split('/')[-1]
        org_name = repo_folder.split('/')[-2]

        ssh_url = f"git@github.com:{org_name}/{repo_name}.git"
        # print(repo_folder)
        # print(ssh_url)
        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        # os.system(f'git init')
        # os.system('eval "$(ssh-agent -s)"')
        os.system(f'ssh-add ~/.ssh/github')
        # os.system(f'ssh -T git@github.com')
        os.system(f'ssh -i ~/.ssh/github -T git@github.com')
        os.system(f'git remote set-url origin {ssh_url}')
        os.system(f'git remote rm origin')
        os.system(f'git remote add origin {ssh_url}')
        os.system(f'git config advice.setUpstreamFailure false"')
        os.system(f'git branch -m master main')
        os.system(f'git fetch origin')
        os.system(f'git branch -u origin/main main')
        os.system(f'git remote set-head origin -a')
        os.system(f'git config --global push.default current')
        os.system(f'git branch --set-upstream-to=origin/main main')
        # os.system(f'git push --set-upstream origin main')
        os.system('git pull')
        #os.system(f'git pull origin main')

        # os.system(f'git add .')
        # os.system(f'git commit -m "Initial commit"')
        # os.system(f'git push')
        # exit()


def push_local_repo(local_path):
    git_local_repos = git_folders_in_path(local_path)
    for repo_folder in git_local_repos:
        repo_name = repo_folder.split('/')[-1]
        org_name = repo_folder.split('/')[-2]

        ssh_url = f"git@github.com:{org_name}/{repo_name}.git"
        print(repo_folder)
        print(ssh_url)
        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        os.system(f'git pull origin main')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial commit"')
        os.system(f'git push')
        # exit()


def clone_repos_from_org(org_name, repos, path_name, path_folder):
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                if folder_exist(path_folder + "/" + repo['name']):
                    print(f"Exist: {org_name}/{repo['name']}")
                    continue
                if (repo['fork'] == False):
                    print(f"Clone: {org_name}/{repo['name']}")
                    # clone_repo(repo['clone_url'], repo['name'], path_folder)
                else:
                    print(f"Fork: {org_name}/{repo['name']}")
                    # if(remove_fork) remove
    else:
        print(f"Failed to fetch repositories for organization: {org_name}")


def update_github_pages(api_token, org_name, repo_name, branch='main', domain=None, path='/'):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    data = {
        "cname": domain,
        "source": {
            "branch": branch,
            "path": path
        }
        # 'https_enforced': False,
        # 'protected_domain_state': 'verified'
    }
    print('data', data)
    response = requests.put(url, json=data, headers=getHeaders2(api_token))

    if response.status_code in (200, 201):
        print(f"GitHub Pages configuration updated for repository: {repo_name}")
    else:
        print(f"Failed to update GitHub Pages configuration. Status code: {response.status_code}")
        #print(f"Response: {response.json()}")


def enable_github_pages(api_token, org_name, repo_name, branch='main', domain=None, path='/'):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    data = {
        'source': {
            'branch': branch,
            'path': path
        },
        'cname': domain
    }
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    if response.status_code == 201:
        print(f"GitHub Pages enabled for {repo_name} with branch '{branch}'.")
        if domain:
            print("Custom domain set to:", domain)
    else:
        print("Failed to enable GitHub Pages. Status code:", response.status_code)
        print("Response:", response.json())


# Headers for the request, including the authorization token
def getHeaders(api_token):
    return {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/vnd.github.v+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }


def getHeaders2(api_token):
    return {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json',
    }


def get_repository_list_wtih_github_pages(api_token, org_name, repo_name):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    response = requests.get(url, headers=getHeaders(api_token))

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch GitHub Pages. Status code:", response.status_code)
        print("Response:", response.json())



# Function to change the default branch to 'main' for all organization repos
def change_default_branch_to_main(api_token, org_name, name = '', description = '', homepage = ''):
    # Retrieve a list of all repositories within the organization
    repos_url = f'https://api.github.com/orgs/{org_name}/repos?per_page=100'
    repos_response = requests.get(repos_url, headers=getHeaders(api_token))

    if repos_response.status_code != 200:
        print(f"Failed to retrieve repositories: {repos_response.content}")
        return

    for repo in repos_response.json():
        repo_name = repo['name']
        repo_url = f"https://api.github.com/repos/{org_name}/{repo_name}"

        # Change the default branch
        data = {
            #"name": repo_name,
            #"description": repo_name,
            #"homepage": homepage,
            "default_branch": "main",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }
        patch_response = requests.patch(repo_url, headers=getHeaders(api_token), json=data)

        if patch_response.status_code in (200, 202):
            print(f"Default branch updated to 'main' for repo: {repo_name}")
        else:
            print(f"Failed to update default branch for repo: {repo_name}")
        print(f"Status code: {patch_response.status_code}, Response: {patch_response.json()}")


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
        #domain = 'ndof.org'
        # branch = 'master'
        branch = 'main'
        repo_name = 'identity'
        # exit()
        homepage = get_param_from_repo(repos, 'homepage')
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
        #exit()
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

        exit()

    # python3 ./multigit.py ~/github
