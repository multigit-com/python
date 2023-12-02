# [python.multigit.com](http://python.multigit.com)

+ load projects from `.projects` file
+ load branches from `.branches` file
+ load all project from list `.orgs` file

## Init

clone
```bash
git clone https://github.com/multigit-com/python.git
```

configuration
```bash
chmod +x ./init.sh
./init.sh
```

packages
```shell
python -m pip install requests      # for Python 2.x (if still used)
python3 -m pip install requests     # for Python 3.x
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

---

+ [edit](https://github.com/multigit-com/python/edit/main/README.md)
+ [git](https://github.com/multigit-com/) 