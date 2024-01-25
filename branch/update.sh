#!/bin/bash
## Color
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
# Default branches file
BRANCH_FOLDER=$1
[ -z $BRANCH_FOLDER ] && BRANCH_FOLDER="./"
#
BRANCH_FILE=$2
[ -z $BRANCH_FILE ] && BRANCH_FILE=".branches"
#
BRANCH_LIST="$BRANCH_FOLDER/$BRANCH_FILE"
# Check if the branches file exists
if [ ! -f "$BRANCH_LIST" ]; then
    echo "\n${RED}Error: File $BRANCH_LIST does not exist.${NC}\n"
    exit 1
fi

# Add New Line
echo "" >> $BRANCH_LIST
printf "\n${GREEN}List the branch-names for each visited folder from the file: ${CYAN}${BRANCH_LIST}${NC}\n"
#
while IFS=' ' read -r folder branch_name; do
    if [ -n "$folder" ]; then
        PROJECT_PATH="$BRANCH_FOLDER/$folder"
        [[ ! -d "$PROJECT_PATH" ]] && printf "${RED}${PROJECT_PATH}${NC}\n" && continue

        #echo "Visiting $folder to list branch:"
        pushd "$PROJECT_PATH" >/dev/null

        # Get the current branch name
        current_branch=$(git rev-parse --abbrev-ref HEAD)
        printf "\n${CYAN}$PROJECT_PATH${GREEN} ($current_branch)${NC}->${RED}($branch_name)${NC}\n"

        git switch "$branch_name"
        git pull
        #git submodule update --init --recursive
        git submodule update --init --recursive --remote

        # Load dependencies from submodules
        popd >/dev/null
    fi
done < "$BRANCH_LIST"
