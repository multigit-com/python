
![obraz](https://github.com/multigit-com/python/assets/5669657/5364d20a-ad03-49b2-9251-142613975347)

# [python.multigit.com](http://python.multigit.com)

+ [www.multigit.com](http://www.multigit.com)
+ [identity](http://identity.multigit.com)



**MultiGit** project facilitate the process of cloning multiple repositories across different organizations, branches, and projects on GitHub.

**MultiGit** is designed for software developers managing or contributing to large-scale projects with complex structures. 
The project operates by reading specified .orgs, .projects, and .branches files to determine which repositories need to be cloned or pulled. 
This approach allows for an automated, organized, and efficient workflow, reducing the manual effort of dealing with each repository individually.

### Key features include

- Automatic cloning or pulling of repositories based on lists provided in .orgs, .projects, and .branches files.
- Skips cloning forked repositories to focus on original content.
- Verifies if each project adheres to a predefined structure as specified in a .structure file, offering to create a repository in the organization if it doesn't exist.
- Provides installation and configuration instructions to ensure proper setup, including upgrading pip, installing dependencies via a requirements.txt file, and executing shell commands for git operations.

### How it works

The scripts included, particularly `multigit.py`, enable execution of git clone commands for each repository, emphasizing the need for git configurations and appropriate permissions. Given its sensitivity, the project also stresses the importance of securely managing the GitHub API token used in the cloning process.

Overall, this GitHub project represents a practical utility for developers working in large-scale, multi-repository environments, streamlining the management of such projects through automation and structured checks.


multigit cloning for many different organization, branches, projects on github
+ load projects from `.projects` file
+ load branches from `.branches` file
+ load all project from each organization on `.orgs` file list
  
options:
  + if repo is existing, trying to pull
  + don't clone forked repo
  + check if each project has correct structure, projects, files inside, based on `.structure` file
    + if they don't have create a repo in org and clone 


## Init
python update
```bash
python -m pip install --upgrade pip
```

init requirements
```bash
pip freeze > requirements.txt
```

install dependencies
```bash
pip install -r requirements.txt
```

clone
```bash
git clone https://github.com/multigit-com/python.git
```

configuration
```bash
chmod +x ./init.sh
./init.sh github-username
```

packages
```shell
python -m pip install requests      # for Python 2.x (if still used)
python3 -m pip install requests     # for Python 3.x
```


## refactoring

```shell
python3 splitup.py multigit.py function
python3 depend.py function
```


## How to start

The script [multigit.py](multigit.py) executes a shell command (`git clone`) for each repository. This command requires that you have git installed and properly configured on your system.
Please note that you should have appropriate permissions to clone the repositories that you're trying to access, otherwise, you may run into authentication issues. Additionally, GitHub API tokens are sensitive and should be kept secure. If you accidentally expose your token, make sure to revoke it immediately and generate a new one.

+ [ ] Before running the script, ensure you have Git installed on your system and that the script has execute permissions.
+ To use this script, you must have:
  + [ ] A file named `.orgs` in the same directory as the script, containing a list of organization names, each on a new line.
  + [ ] A file named `.token` in the same directory as the script, containing your [GitHub API token](https://github.com/settings/tokens)
 
```bash
python3 ./multigit.py ~/github
```

check list of folders (organizations) and included subfolders (projects)
```bash
cd  ~/github
find . -maxdepth 1 -mindepth 1 -type d -exec sh -c 'echo "{}: $(find "{}" -maxdepth 1 -mindepth 1 -type d | wc -l)"' \;
```




# ? optional parameter
# ! mandatory parameter
# : equivalent name of function parameter
# Object: repo_descr="description of github repository"
# Example: Update description "Description for my " on gitHub repository myrepo on GitHub
# Update description !description on gitHub repository !name:repo_name
update_repo_on_github(api_token, org_name, repo_name, description, domain):


# Text To Service

+ by voice
+ by shell
+ by web app
+ 

## API handler

## Test framework


## More

API documentation
+ [Pages - GitHub Docs](https://docs.github.com/en/rest/pages/pages?apiVersion=2022-11-28#create-a-apiname-pages-site)

## Another solution
+ [git-repo - Git at Google](https://gerrit.googlesource.com/git-repo)


---

+ [edit](https://github.com/multigit-com/python/edit/main/README.md)
+ [git](https://github.com/multigit-com/) 
