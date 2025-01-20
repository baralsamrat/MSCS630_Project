import os
import sys
from commands.built_in import execute_built_in
from commands.file_ops import execute_file_command
from commands.process_mgmt import execute_process_command
from utils.error_handling import handle_invalid_command

def shell():
    while True:
        try:
            current_dir = os.getcwd()
            command = input(f"{current_dir} $ ").strip()

            if not command:
                continue

            if command == "exit":
                print("Exiting the shell.")
                break

            execute_command(command)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the shell.")
        except Exception as e:
            print(f"Error: {e}")

def execute_command(command):
    parts = command.split()
    cmd = parts[0]

    # Delegate command execution
    if cmd in ["cd", "pwd", "echo", "clear"]:
        execute_built_in(parts)
    elif cmd in ["ls", "cat", "mkdir", "rmdir", "rm", "touch"]:
        execute_file_command(parts)
    elif cmd in ["kill", "jobs", "fg", "bg"]:
        execute_process_command(parts)
    else:
        handle_invalid_command(cmd)

if __name__ == "__main__":
    shell()
