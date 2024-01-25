#!/bin/bash
# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default branches file
BRANCH_LIST=$1
[ -z $BRANCH_LIST ] && BRANCH_LIST=".branches"
# Array to keep track of paths
declare -a visited_folders

# Check if the branches file exists
if [ ! -f "$BRANCH_LIST" ]; then
    printf "\n${RED}Error: File $BRANCH_LIST does not exist.${NC}\n"
    exit 1
fi

# Add New Line
echo "" >> $BRANCH_LIST
BRANCH_FOLDER=$1
[ -z $BRANCH_FOLDER ] && BRANCH_FOLDER="./"
# Read the branches file line by line
printf "/n1.${GREEN}Switch the branch on each selected folder${NC}\n"
while IFS=' ' read -r folder_path branch_name; do
    # Skip empty lines
    [[ -z "$folder_path" || -z "$branch_name" ]] && continue

    # Check if the directory exists
    if [ -d "$folder_path" ]; then
        PROJECT_PATH="$BRANCH_FOLDER/$folder_path"
        [[ ! -d "$PROJECT_PATH" ]] && printf "${PROJECT_PATH}${NC}\n" && continue

        # Go to the directory
        pushd "$PROJECT_PATH" >/dev/null

        current_branch=$(git rev-parse --abbrev-ref HEAD)
        printf "\n${CYAN}$PROJECT_PATH${GREEN} ($current_branch)${NC}->${RED}($branch_name)${NC}\n"

        # Switch to the specified branch
        git reset --hard
        git pull
        git switch "$branch_name"
        git pull
        #git submodule update --init
        git submodule update --init --recursive


        if [ $? -ne 0 ]; then
            printf "\n ${YELLOW}Error: Failed to switch to branch $branch_name in $folder_path ${NC}\n"
            # Go back to the original directory
            popd >/dev/null
            continue # Continue with the next item
        fi

        # Go back to the original directory
        popd >/dev/null
    else
        printf "\n ${YELLOW}Warning: Directory $folder_path does not exist. Skipping. ${NC}\n"
    fi
done < "$BRANCH_LIST"


printf "\n2.${GREEN}List the branch name for each visited folder${NC}\n"
while IFS=' ' read -r folder branch_name; do
    if [ -d "$folder" ]; then
        #echo "Visiting $folder to list branch:"
        pushd "$folder" >/dev/null

        # Get the current branch name
        current_branch=$(git rev-parse --abbrev-ref HEAD)
        printf "\n${CYAN}$folder${GREEN} ($current_branch)${NC}->${RED}($branch_name)${NC}\n"

        git switch "$branch_name"
        # Load dependencies from submodules
        #git submodule update --init --recursive
        git submodule update --recursive --remote

        popd >/dev/null
    fi
done < "$BRANCH_LIST"
