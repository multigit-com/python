#  Copyright (c) 2023.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import csv
import re


def extract_function_details(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    details = []
    current_description = None
    for line in lines:
        description_match = re.match(r'^\s*#(.*)', line)
        function_match = re.match(r'^\s*def\s+(\w+)\((.*?)\):', line)

        if description_match:
            current_description = description_match.group(1).strip()

        if function_match:
            function_name = function_match.group(1).strip()
            inputs = function_match.group(2).strip()
            details.append({'FUNCTION': function_name, 'DESCRIPTION': current_description, 'INPUT': inputs})
            current_description = None

    # Scan for outputs within the functions
    for detail in details:
        function_name = detail['FUNCTION']
        function_regex = r'def\s+' + function_name + r'\([^)]*\):\s*(.*?)(?:return (.*?))?\s*$'
        for line in lines:
            output_match = re.search(function_regex, line, re.DOTALL)
            if output_match:
                detail['OUTPUT'] = output_match.group(2).strip() if output_match.group(2) else None
                break

    return details


def create_csv_from_folder(folder_path, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=['PATH', 'FUNCTION', 'DESCRIPTION', 'INPUT', 'OUTPUT'])
        csv_writer.writeheader()

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.py'):
                    full_path = os.path.join(root, filename)
                    function_details = extract_function_details(full_path)
                    for detail in function_details:
                        csv_writer.writerow({
                            'PATH': full_path,
                            'FUNCTION': detail['FUNCTION'],
                            'DESCRIPTION': detail['DESCRIPTION'],
                            'INPUT': detail['INPUT'],
                            'OUTPUT': detail['OUTPUT']
                        })

# Replace 'selected_folder_path' with the path to your folder
# Replace 'output_csv_file' with the path where you want to save the CSV output
selected_folder_path = 'function'
output_csv_file = 'ops.csv'
create_csv_from_folder(selected_folder_path, output_csv_file)
#python3 ops.py