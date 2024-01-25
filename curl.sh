#!/bin/bash

# Check if an input file was provided
if [[ "$#" -lt 1 ]]; then
    echo "Usage: $0 <input_csv_file>"
    echo "Usage: $0 <input_csv_file> <input_type>"
    echo "*input_type: status, response"
    exit 1
fi

# Config
INPUT_FILE=$1
INPUT_TYPE=$2
#echo $INPUT_TYPE
[ -z $INPUT_TYPE ] && INPUT_TYPE=status
## Files
OUTPUT_FILE="${INPUT_FILE}.valid.csv"
ERROR_OUTPUT_FILE="${INPUT_FILE}.error.csv"
## Request
HOST_DOMAIN="demo.com"
HOST_IP=$3
[ -z $HOST_IP ] && HOST_IP="1.1.1.1"
## Colors
RED='\033[0;31m'
GREEN='\033[0;32m'

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File ${INPUT_FILE} does not exist."
    exit 1
fi

# Write the headers to the output file
echo "URL,EXPECTED_STATUS,CURL_STATUS" > "$OUTPUT_FILE"
#echo "URL,EXPECTED_STATUS,CURL_STATUS" > "$ERROR_OUTPUT_FILE"
[ -f "$ERROR_OUTPUT_FILE" ] && rm $ERROR_OUTPUT_FILE

# Read the input file line by line
while IFS=, read -r URL expected_status; do
    # Skip headers
    if [ "$URL" = "URL" ]; then
        continue
    fi

    # Use curl to get the HTTP status code
    # --silent: hide progress meter
    # --output: discard the document fetched
    # --write-out: specify what to display after transaction
    # --max-time: maximum time in seconds for the entire operation to take
    # --fail: fail silently on server errors
    # --location: follow redirects
    if [ $INPUT_TYPE == "status" ]; then
        curl_status=$(curl --silent --output /dev/null --write-out '%{http_code}' --max-time 10 --fail --location -H "Host: ${HOST_DOMAIN}" -H "X-Forwared-For: ${HOST_IP}" ${URL})
    else
        curl_status=$(curl -sb -H "Host: ${HOST_DOMAIN}" -H "X-Forwared-For: ${HOST_IP}" ${URL})
    fi


    # If curl failed for reasons other than HTTP errors (e.g., network issues), it will return an empty string.
    # In such cases, we'll set curl_status to 0 to indicate an error.
    if [ -z "$curl_status" ]; then
        curl_status=0
    fi

    # Append the result to the output file
    if [ ${expected_status} != ${curl_status} ]; then
        printf "${RED} ${URL} ${curl_status} Expected: ${expected_status}\n"
        echo "${URL},${expected_status},${curl_status}" >> "$ERROR_OUTPUT_FILE"
    else
        printf "${GREEN} ${URL} ${expected_status}\n"
        echo "${URL},${expected_status},${curl_status}" >> "$OUTPUT_FILE"
    fi

done < "$INPUT_FILE"

#echo "Results saved to $OUTPUT_FILE"
