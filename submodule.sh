#!/bin/bash

show_help() {
cat << EOF
Usage: ${0##*/} COMMAND

Available commands are:
    init:         Initialize the git submodule - 'git submodule update --init --recursive --remote'
    add PATH:     Add a new submodule at the specified path, with the branch defaulting to 'master'. Pass branch name as third argument if different.
    del PATH:     Delete the submodule at the specified path

Examples:
    ${0##*/} info
    ${0##*/} init
    ${0##*/} update
    ${0##*/} add ../../submodule
    ${0##*/} add ../../submodule branchname
    ${0##*/} del submodule
    ${0##*/} switch submodule develop
EOF
}

command=$1
path=$2
branch=$3

if [ -z "$command" ]; then
    show_help
    exit 1
fi

case $command in
    info)
        git submodule
        cat .gitmodules
        ;;
    init)
        git submodule update --init --recursive --remote
        ;;

    update)
        git submodule update --recursive --remote
        ;;

    add)
        if [ -n "$path" ]; then
            if [ -z "$branch" ]; then
                git submodule add --force "$path"
            else
                git submodule add -b "$branch" "$path"
            fi
            git submodule update --init --recursive --remote
            #git status
            cat .gitmodules
            git add "$path"
            git add .gitmodules            
            git commit -m "Added submodule: $path"
            git push
        else
            echo "Path is required for add command"
        fi
        ;;
    switch)
        if [ -n "$path" ]; then            
            cat .gitmodules
            cd "$path"
            switch "$branch"
            git pull
            cd ..
            git submodule set-branch -b "$branch" "$path"
            git submodule sync            
            git submodule update --init --recursive --remote
            cat .gitmodules            
            git add "$path"
            git add .gitmodules
            git commit -m "Switched branch: '$branch' in submodule: '$path'" 
            git push

        else
            echo "Path is required for add command"
        fi
        ;;        
    del)
        if [ -n "$path" ]; then
            git submodule deinit -f -- "$path"
            rm -rf ".git/modules/$path"
            git rm -f "$path"
            cat .gitmodules
            git add "$path"
            git add .gitmodules
            git commit -m "Deleted submodule: $path"
            git push
        else
            echo "Path is required for del command"
        fi
        ;;

    *)
        echo "Invalid command"
        show_help
        exit 1
        ;;
esac
