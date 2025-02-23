#!/bin/bash
# main.sh
# This script creates a Python virtual environment, installs dependencies,
# and then demonstrates the fully integrated shell functionalities:
# - Piping: chaining commands (e.g., ls | grep txt).
# - User Authentication: logging in as admin and as a standard user.
# - File Permissions: restricting file modifications based on user roles.
# - Process Scheduling, Memory Management, and Process Synchronization simulations.

VENV_DIR="venv"

# Create the virtual environment if it doesn't exist.
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment.
source "$VENV_DIR/bin/activate"

# Install dependencies (if any) from requirements.txt.
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

# Ensure current directory is in PYTHONPATH.
export PYTHONPATH=$(pwd)

# Check if 'expect' is installed.
if ! command -v expect &> /dev/null; then
    echo "Expect tool is not installed. Please install it (e.g., sudo apt-get install expect) and re-run the script."
    deactivate
    exit 1
fi

SHELL_CMD="python3 main.py"

echo "=== Admin User Demonstration ==="
expect <<EOF
log_user 1
spawn $SHELL_CMD
expect "Username: "
send "admin\r"
expect "Password: "
send "adminpass\r"
expect "admin@shell> "
send "ls | grep txt\r"
expect "admin@shell> "
send "touch system.txt\r"
expect "admin@shell> "
send "schedule_rr 1 ls ; pwd\r"
expect "admin@shell> "
send "simulate_memory\r"
expect "admin@shell> "
send "simulate_sync\r"
expect "admin@shell> "
send "exit\r"
expect eof
EOF

echo "Admin demonstration completed."
echo "-----------------------------------------"

echo "=== Standard User Demonstration ==="
expect <<EOF
log_user 1
spawn $SHELL_CMD
expect "Username: "
send "user\r"
expect "Password: "
send "userpass\r"
expect "user@shell> "
send "ls | grep txt\r"
expect "user@shell> "
send "touch system.txt\r"
expect {
    "Permission denied" { send_user "\nPermission restriction verified for standard user.\n" }
    timeout { send_user "\nPermission check failed.\n" }
}
expect "user@shell> "
send "exit\r"
expect eof
EOF

echo "Standard user demonstration completed."

deactivate
echo "Virtual environment deactivated."
