#!/bin/bash
SQL_FOLDER=$1
[ -z $SQL_FOLDER ] && SQL_FOLDER=$(pwd)

HOME_FOLDER=$2
[ -z $HOME_FOLDER ] && HOME_FOLDER=~

# the configurartion is working with cdn-docker-compose and link11postgres projects
DB_PASS=$(cat $HOME_FOLDER/postgresql/.password)
DB_USER=$(cat $HOME_FOLDER/postgresql/.username)
DB_NAME=$(cat $HOME_FOLDER/postgresql/.database)
DB_PORT=$(cat $HOME_FOLDER/postgresql/.port)
DB_HOST=$(cat $HOME_FOLDER/postgresql/.host)

# connect to DB and run SELECT
export PGPASSWORD=$DB_PASS

# Check if no arguments provided 
if [ "$#" -lt 1 ] ; then
    echo "Usage: $0 sql_folder home_folder"
    exit 0
fi

# Iterate over each file name provided as argument
for SQL_FILES_DIR in "$SQL_FOLDER"
do
   # Check if file exists and is a regular file 
   if [ -d "$SQL_FILES_DIR" ]; then
      # Loop through every SQL file in the directory
      # List all files in the folder
      for SQL_FILE in $(ls $SQL_FILES_DIR)
      do
        SQL_FILE_PATH="$SQL_FILES_DIR/$SQL_FILE"
        if [ -f "$SQL_FILE_PATH" ];
        then
          echo $SQL_FILE_PATH
          # If $SQL_FILE is a file, import it
          psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $SQL_FILE_PATH
          #echo "Imported $SQL_FILE successfully"
          # check connection status
          if [ "$?" -eq "0" ]
          then
              echo "Successfully connected to the DB."
          else
              echo "Error in connecting to the DB."
          fi

        fi
      done
   else
      echo "$SQL_FILES_DIR does not exist or is not a regular folder"
   fi
done


# unset the PGPASSWORD
unset PGPASSWORD
