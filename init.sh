#!/bin/bash
gituser=$1
[ -z $gituser ] && gituser=git
#echo "init [gitusername]" && exit 1
touch .projects .orgs .branches .token
python3 -m pip install requests
# SSH
cat $HOME/.ssh/authorized_keys
ssh-keygen -t ed25519 -C "$gituser@github.com" -f $HOME/.ssh/github
ls $HOME/.ssh/
cat $HOME/.ssh/github.pub
open https://github.com/settings/keys
# add the ssh pub key
chmod 600  $HOME/.ssh/*
chmod 755  $HOME/.ssh/*.pub
eval "$(ssh-agent -s)"
ssh-add $HOME/.ssh/github
ssh -i ~/.ssh/github -T "$gituser@github.com"
# TOKEN
open https://github.com/settings/tokens
git remote set-url origin git@github.com:hexagonalsandbox/book.git
git remote show origin
