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


def generate_template(words, template_folder, target_project_folder):
    if not os.path.exists(target_project_folder):
        os.makedirs(target_project_folder)
    # get list of file from path
    template_path = "templates/" + template_folder
    files = os.listdir(template_path)
    # print(files)

    for template_file in files:
        template_path_file = template_path + "/" + template_file
        project_path_file = target_project_folder + "/" + template_file
        print(template_path_file)

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
    # Parse the URL to get the netloc (network location part)
    netloc = urlparse(url).netloc

    # Split the netloc into parts by '.'
    netloc_parts = netloc.split('.')

    # Extract the last two parts for domain and TLD
    # This assumes a standard TLD; does not account for country-code TLDs like '.co.uk'
    domain_name = '.'.join(netloc_parts[-2:])

    return domain_name


def get_param_from_repo(repos, repo_name='home_page'):
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                if (repo['fork'] == False):
                    return repo[repo_name]
    return None


# create repository on github by api call
def create_repo_on_github(api_token, org_name, repo_name, local_path):
    # Endpoint to create a repo within an organization
    url = f'https://api.github.com/orgs/{org_name}/repos'
    print(url)
    # Headers for the request, including the authorization token
    headers = {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    # Data for the new repo
    data = {
        'name': repo_name,
        'private': False  # Set to True if you want a private repository
    }

    # Make the request
    response = requests.post(url, json=data, headers=headers)

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


def create_notexisting_folder(api_token, org_name, repos, path_name, path_folder):
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
            homepage = get_param_from_repo(repos, 'homepage')
            words = {'domain': extract_domain_name_from_url(homepage), 'homepage': homepage + ".com",
                     'repository': repo_folder,
                     'organization': org_name}
            generate_template(words, repo_folder, path_folder + "/" + repo_folder)
            # create repository on github by api call
            create_repo_on_github(api_token, org_name, repo_folder, path_folder + "/" + repo_folder)

    # print(f"Expected folders: {folders} in {org}/{repo['name']}")
    # exit(1)

    # if not os.path.exists(clone_path):
    #    os.makedirs(clone_path)
    #    create project online on github


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
def create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path):
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
        create_repo_on_github(api_token, org_name, repo_name, repo_folder)


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
        #print(repo_folder)
        #print(ssh_url)
        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        #os.system(f'git init')
        #os.system('eval "$(ssh-agent -s)"')
        os.system(f'ssh-add ~/.ssh/github')
        #os.system(f'ssh -T git@github.com')
        os.system(f'ssh -i ~/.ssh/github -T git@github.com')
        os.system(f'git remote set-url origin {ssh_url}')
        os.system(f'git remote rm origin')
        os.system(f'git remote add origin {ssh_url}')
        os.system(f'git config advice.setUpstreamFailure false"')
        os.system(f'git config --global push.default current')
        #os.system(f'git branch --set-upstream-to=origin/main main')
        #os.system(f'git push --set-upstream origin main')
        os.system('git pull')
        #os.system(f'git add .')
        #os.system(f'git commit -m "Initial commit"')
        #os.system(f'git push')
        #exit()



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
        #exit()

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

        # clone_repos_from_org(org_name, repos, path_name, local_path)
        # create_notexisting_folder(api_token, org_name, repos, path_name, local_path)
        # create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path)
        # push_all_repos(api_token, org_name, repos, local_path)
        #pull_all_repos(local_path)
        #init_local_repo(local_path)
        push_local_repo(local_path)
        exit()

# python3 ./multigit.py ~/github
