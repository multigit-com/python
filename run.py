import subprocess
import sys

# python3 run.py TEST.md "sudo ./test.sh TEST_FOLDER "/home/$(logname) && open TEST.md

def run_command_with_sudo_and_save_results(command, output_file_path):
    try:
        # Run the command with sudo, capturing stdout and stderr
        completed_process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # Don't raise an exception on a non-zero exit
        )

        # Write the output and error (if any) to the specified output file
        with open(output_file_path, 'w') as file:
            file.write(f"Command: {' '.join(command)}\n")
            file.write(f"Return code: {completed_process.returncode}\n")
            out = completed_process.stdout
            out = out.replace("[1;33m", "")
            out = out.replace("[0m", "")
            out = out.replace("[0;31m", "- [ ]")
            out = out.replace("[0;32m", "+ [x]")
            file.write(f"--- STDOUT ---\n{out}\n")
            file.write(f"--- STDERR ---\n{completed_process.stderr}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run.py <output_file_path> <'command'>")
        sys.exit(1)

    # Output file path comes from the first script argument
    output_filepath = sys.argv[1]

    # The command to run comes from the second script argument
    # It is expected to be a single string, it will be split to form a list
    command_to_run = sys.argv[2].split(' ')

    # Run the command and save the results to the output file
    run_command_with_sudo_and_save_results(command_to_run, output_filepath)
