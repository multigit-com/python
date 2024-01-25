#!/bin/bash
TICKET_FOLDER=$1
HOME_PATH=$2
[ -z $HOME_PATH ] && HOME_PATH=$(pwd)
PROJECT_PATH="$HOME_PATH/$TICKET_FOLDER"
## Color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
## Check Inputs
[ $# -eq 0 ] && printf "No TICKET parameter provided, example: \n${YELLOW}./project.sh\n" && exit 0
mkdir -p $PROJECT_PATH
echo $PROJECT_PATH


# Default projects
PROJECT_LIST="$PROJECT_PATH/.projects"
# Check if the branches file exists
if [ ! -f "$PROJECT_LIST" ]; then
    printf "\n${RED}Error: File $PROJECT_LIST does not exist.${NC}\n"
    exit 1
fi
# Function to extract the repository name from a Git URL
extract_repo_name() {
  local git_url="$1"
  # Use basename to get the last part of the URL, then strip off the .git suffix
  local repo_name=$(basename -s .git "$git_url")
  echo "$repo_name"
}
#
printf "\n${GREEN}List of folders: ${NC}\n"
cd $PROJECT_PATH
ls -ls
#
# Add New Line
echo "" >> $PROJECT_LIST
printf "\n${GREEN}List the projects for each visited folder from the file: ${PROJECT_LIST}${NC}\n"
while IFS=' ' read -r git_url; do
    if [[ -n "$git_url" ]]; then
        folder_name=$(extract_repo_name "$git_url")
        git clone $git_url $folder_name
    fi
done < "$PROJECT_LIST"

cd $HOME_PATH

# Update branches
./branches/info.sh $TICKET_FOLDER
./branches/init.sh $TICKET_FOLDER
./branches/update.sh $TICKET_FOLDER
# Load submodules and update rights
while IFS=' ' read -r git_url; do
    if [[ -n "$git_url" ]]; then
        folder_name=$(extract_repo_name "$git_url")
        BRANCH_FOLDER="$PROJECT_PATH/$folder_name"
        [[ ! -d "$BRANCH_FOLDER" ]] && printf "${RED}${PROJECT_PATH}${NC}\n" && continue
        printf "${YELLOW}$BRANCH_FOLDER ${NC}\n"
        cd $BRANCH_FOLDER
        #git submodule update --init --recursive --remote
        chmod +x *.sh
        chmod +x *.py
    fi
done < "$PROJECT_LIST"
# The last one repo in  .projects must be docker compose project
#printf "${YELLOW}Start docker environment${NC}\n"
#bash ../../docker_rebuild.sh
