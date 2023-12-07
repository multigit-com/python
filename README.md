# [python.multigit.com](http://python.multigit.com)

+ [www.multigit.com](http://www.multigit.com)
+ [identity](http://identity.multigit.com)


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


## More

API documentation
+ [Pages - GitHub Docs](https://docs.github.com/en/rest/pages/pages?apiVersion=2022-11-28#create-a-apiname-pages-site)

## Another solution
+ [git-repo - Git at Google](https://gerrit.googlesource.com/git-repo)


---

+ [edit](https://github.com/multigit-com/python/edit/main/README.md)
+ [git](https://github.com/multigit-com/) 