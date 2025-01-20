import subprocess
import os
import time

def run_shell_command(input_commands):
    """Run shell.py with specified commands and return its output."""
    process = subprocess.run(
        ["python3", "shell.py"],
        input=input_commands,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process.stdout, process.stderr

def test_built_in_commands():
    """Test built-in shell commands."""
    print("Testing built-in commands...")

     # Test `pwd`
    print("Expected working directory:", os.getcwd())  # Debug expected output
    commands = "pwd\nexit\n"
    stdout, stderr = run_shell_command(commands)
    print("Debug stdout:", repr(stdout))  # Debug actual output
    assert os.getcwd() in stdout.strip(), "pwd command failed"
    print("pwd command passed!")


    # Test `echo`
    commands = "echo Hello, World!\nexit\n"
    stdout, stderr = run_shell_command(commands)
    assert "Hello, World!" in stdout, "echo command failed"

    # Test `clear`
    # Skipping output validation since it just clears the screen.

    # Test `cd`
    test_dir = "test_directory"
    os.mkdir(test_dir)
    commands = f"cd {test_dir}\npwd\nexit\n"
    stdout, stderr = run_shell_command(commands)
    assert test_dir in stdout, "cd command failed"
    os.rmdir(test_dir)  # Clean up

    print("Built-in commands passed all tests!")

def test_file_operations():
    """Test file-related shell commands."""
    print("Testing file operations...")

    # Test `ls`
    open("test_file.txt", "w").close()
    commands = "ls\nexit\n"
    stdout, stderr = run_shell_command(commands)
    assert "test_file.txt" in stdout, "ls command failed"
    os.remove("test_file.txt")  # Clean up

    # Test `touch`
    commands = "touch new_file.txt\nls\nexit\n"
    stdout, stderr = run_shell_command(commands)
    assert "new_file.txt" in stdout, "touch command failed"
    os.remove("new_file.txt")  # Clean up

    # Test `rm`
    open("to_remove.txt", "w").close()
    commands = "rm to_remove.txt\nls\nexit\n"
    stdout, stderr = run_shell_command(commands)
    assert "to_remove.txt" not in stdout, "rm command failed"

    print("File operations passed all tests!")

def test_process_management():
    """Test process management commands."""
    print("Testing process management...")

    # Test background execution and `jobs`
    commands = "sleep 5 &\njobs\nexit\n"
    stdout, stderr = run_shell_command(commands)
    assert "Running" in stdout, "jobs command failed"

    print("Process management passed all tests!")

def main():
    """Run all tests."""
    print("Starting tests for shell...")
    test_built_in_commands()
    test_file_operations()
    test_process_management()
    print("All tests completed successfully!")

if __name__ == "__main__":
    main()
