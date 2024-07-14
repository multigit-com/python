#!/bin/bash
gituser=$1
#[ -z $gituser ] && gituser=git
[ -z $gituser ] && gituser=$(git config user.name)
#echo "init [gitusername]" && exit 1
# generate private cert
cat $HOME/.ssh/authorized_keys
ls $HOME/.ssh/
cat $HOME/.ssh/github.pub
xdg-open https://github.com/settings/keys
# add the ssh pub key
chmod 600  $HOME/.ssh/*
chmod 755  $HOME/.ssh/*.pub
eval "$(ssh-agent -s)"
ssh-add $HOME/.ssh/github
ssh -i ~/.ssh/github -T "$gituser@github.com"
# TOKEN
open https://github.com/settings/tokens
#git remote set-url origin git@github.com:hexagonalsandbox/book.git
#git remote set-url origin git@github.com:multigit-com/python.git
git remote show origin
