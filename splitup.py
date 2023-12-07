import argparse
import os
import ast


# Get a list of all the refactored function files
def main(source_file, output_dir):
    # The name/path of your large Python source file
    source_file = 'multigit.py'

    # The directory where the function files will be stored
    output_dir = 'function'
    os.makedirs(output_dir, exist_ok=True)

    # The main file with the imports
    main_py_content = []

    # Parse the source file
    with open(source_file, 'r') as fp:
        source_code = fp.read()
        module = ast.parse(source_code)

    # Process the functions in the source file
    for node in ast.iter_child_nodes(module):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            # The start and end line numbers of the function
            start_line = node.lineno - 1
            end_line = node.end_lineno
            output_file_path = os.path.join(output_dir, f'{function_name}.py')

            # Extract the function source code
            function_source_lines = source_code.splitlines()[start_line:end_line]
            function_source = '\n'.join(function_source_lines)

            # Handle imports by adding them to each function's source
            imports = [line for line in source_code.splitlines() if
                       line.strip().startswith('import') or line.strip().startswith('from')]
            function_source_with_imports = '\n'.join(imports + ['\n\n'] + function_source_lines)

            # Write the function source code to its file
            with open(output_file_path, 'w') as func_fp:
                func_fp.write(function_source_with_imports)

            # Prepare the import line for the main.py content
            main_py_content.append(f'from {output_dir}.{function_name} import {function_name}')

    return main_py_content


# Command line interface
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resolve dependencies and add imports to refactored function files.')
    parser.add_argument('file', help='The file to refactor containing functions to split up into files.')
    parser.add_argument('directory', help='The directory containing the refactored function files.')

    args = parser.parse_args()
    output_dir = args.directory
    main_py_content = main(args.file, output_dir)

    # Write the main.py file
    main_py_file_path = os.path.join(output_dir, 'main.py')
    with open(main_py_file_path, 'w') as main_fp:
        main_fp.write('\n'.join(main_py_content))

print('Refactoring completed successfully.')