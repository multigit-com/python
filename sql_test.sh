#!/bin/bash
HOME_PATH=/home/$(logname)
YELLOW='\033[1;33m'
[ $# -eq 0 ] && printf "No TICKET parameter provided, example: \n${YELLOW}./test.sh\n" && exit 0
TICKET=$1
PATH_SQL=$2
[ -z $PATH_SQL ] && PATH_SQL=1/sql
#echo $PATH_SQL
#
PROJECT_PATH=$(pwd)
SQL_PATH=$PROJECT_PATH/$TICKET/$PATH_SQL
echo "load SQL: $SQL_PATH for: $TICKET"
sh ./sql_folder.sh $SQL_PATH $HOME_PATH
