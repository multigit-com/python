import argparse
import subprocess
import requests
import os


def load_api_token(filename='.token'):
    with open(filename, 'r') as file:
        return file.readline().strip()


def create_path(path_folder):
    subprocess.run(['mkdir', '-p', path_folder])


def clone_repo(clone_url, repo_name, clone_path):
    # Create the directory if it doesn't exist.
    if not os.path.exists(clone_path):
        os.makedirs(clone_path)

    # Run git clone within the specified path.
    result = subprocess.run(['git', 'clone', clone_url], cwd=clone_path)
    print(f"Cloned {repo_name} with exit code {result.returncode}")


def get_repos_from_org(org_name, headers):
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(repos_url, headers=headers)
    return response.json() if response.status_code == 200 else None


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
    if os.path.isfile('.orgs'):
        with open('.orgs', 'r') as file:
            orgs = file.read().splitlines()
    else:
        print(".orgs file does not exist")
        exit(-1)

    # Loop through the organizations and clone their repositories
    for org in orgs:
        # print(f"Fetching repos for org: {org}")
        repos = get_repos_from_org(org, headers)
        path_name = args.path
        # path_name = "~/github"
        path_folder = path_name + "/" + org
        create_path(path_folder)

        if repos:
            for repo in repos:
                if 'clone_url' in repo:
                    print(f"Cloning {repo['name']} from {org}")
                    clone_repo(repo['clone_url'], repo['name'], path_folder)
        else:
            print(f"Failed to fetch repositories for organization: {org}")
