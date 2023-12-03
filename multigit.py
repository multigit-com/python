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
    # get list of file from path
    template_path = "templates/" + template_folder
    files = os.listdir(template_path)
    print(files)

    for template_file in files:
        template_path_file = template_path + "/" + template_file
        print(template_path_file)
        # remove.template file
        # if '.template' in files:
        #    files.remove('.template')
        # get file and replace in the template each words from array by names and values {domain: value, organization: value}
        with open(template_path_file, 'r') as file:
            template = file.read()

        # create example array with name and values {domain: value, organization: value}
        # list in for loop value and name from array elements



        for key, value in words.items():
            template = template.replace("{" + key + "}", value)

        print(f"Template {template_path_file}: {template}")

    # save the template in path
    # with open(target_project_folder + "/.template", 'w') as file:
    #    file.write(template)


# to split up the url to domain name from subdomain
def get_subdomain_from_url(url):
    return url.split('/')[0]


# to split up the url to domain name without subdomain prefix oonly name and tld extension
def get_domain_from_url(url):
    return url.split('/')[2]


# Function to extract the domain name without subdomain but with the TLD
def extract_domain_name(url):
    # Parse the URL to get the netloc (network location part)
    netloc = urlparse(url).netloc

    # Split the netloc into parts by '.'
    netloc_parts = netloc.split('.')

    # Extract the last two parts for domain and TLD
    # This assumes a standard TLD; does not account for country-code TLDs like '.co.uk'
    domain_name = '.'.join(netloc_parts[-2:])

    return domain_name






def get_param_from_repo(repos, repo_name = 'home_page'):
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                if (repo['fork'] == False):
                    return repo[repo_name]
    return None


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
    for org in orgs:
        # print(f"Fetching repos for org: {org}")
        repos = get_repos_from_org(org, headers)
        # get from array repos of object the 'homepage' value


        print(repos)

        path_name = args.path
        # path_name = "~/github"
        path_folder = path_name + "/" + org
        create_path(path_folder)

        expected_folders = fromFilenametoLinesAsArray('.folders')
        repos_in_orgs = flat_array(repos, 'name')
        print(repos_in_orgs)
        # Call the function with your arrays
        # result = arrayElementsAreIncluded(expected_folders, repos_in_orgs)
        # print(result)
        not_existing_folder = differenceElementsInArrays(expected_folders, repos_in_orgs)
        print(not_existing_folder)
        print("---")
        if not_existing_folder:
            for repo_folder in not_existing_folder:
                homepage = get_param_from_repo(repos, 'homepage')
                words = {'domain': extract_domain_name(homepage), 'homepage': homepage + ".com", 'repository': repo_folder, 'organization': org}
                generate_template(words, repo_folder, path_folder + "/" + repo_folder)
        exit()
        # print(f"Expected folders: {folders} in {org}/{repo['name']}")
        # exit(1)

        # if not os.path.exists(clone_path):
        #    os.makedirs(clone_path)
        #    create project online on github
        continue
        if repos:
            for repo in repos:
                if 'clone_url' in repo:

                    if (repo['fork'] == False):
                        print(f"C: {org}/{repo['name']}")
                        # clone_repo(repo['clone_url'], repo['name'], path_folder)
                    else:
                        print(f"F: {org}/{repo['name']}")
                        # if(remove_fork) remove
        else:
            print(f"Failed to fetch repositories for organization: {org}")

# python3 ./multigit.py ~/github
