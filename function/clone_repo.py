import subprocess
import os
import sys
sys.path.append('../')
from function.folder_exist import folder_exist


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