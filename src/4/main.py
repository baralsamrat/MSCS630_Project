#!/usr/bin/env python3
import os
import sys
import shlex
import subprocess
import getpass
import time
import threading
import queue
import hashlib

# ==============================
# Process Scheduling Module
# ==============================
class ProcessScheduling:
    @staticmethod
    def round_robin_scheduler(commands, quantum):
        print(f"[Scheduling] Running Round-Robin Scheduling (quantum = {quantum} seconds)")
        processes = []
        for cmd in commands:
            print(f"[Scheduling] Executing: {cmd}")
            try:
                proc = subprocess.Popen(shlex.split(cmd))
                processes.append(proc)
                time.sleep(quantum)
                proc.terminate()
                print(f"[Scheduling] Terminated process: {cmd}")
            except Exception as e:
                print(f"[Scheduling] Error: {e}")
        for proc in processes:
            proc.wait()
            print(f"[Scheduling] Process {proc.pid} completed.")

    @staticmethod
    def priority_scheduler(command, priority):
        print(f"[Scheduling] Running Priority Scheduling (priority = {priority})")
        try:
            proc = subprocess.Popen(shlex.split(command))
            proc.wait()
            print(f"[Scheduling] Completed execution: {command}")
        except Exception as e:
            print(f"[Scheduling] Error: {e}")

# ==============================
# Memory Management Module (Improved)
# ==============================
class MemoryManagement:
    def __init__(self, frames=4, policy='FIFO'):
        self.frames = frames
        self.memory = {}
        self.page_faults = 0
        self.policy = policy
        self.page_order = []
        print("[Memory] Initialized with", frames, "frames and policy", policy)

    def allocate(self, pid, page):
        print(f"[Memory] Allocating {page} for process {pid}")
        if pid not in self.memory:
            self.memory[pid] = []
        if len(self.memory[pid]) >= self.frames:
            if self.policy == 'FIFO':
                removed = self.memory[pid].pop(0)
            elif self.policy == 'LRU':
                removed = self.page_order.pop(0)
                self.memory[pid].remove(removed)
            print(f"[Memory] Process {pid}: Replaced page {removed} ({self.policy})")
            self.page_faults += 1
        self.memory[pid].append(page)
        if self.policy == 'LRU':
            self.page_order.append(page)
        print(f"[Memory] Process {pid}: Allocated {page}")
        print(f"[Memory] Current State: {self.memory}")

    def status(self):
        print("[Memory] Current Allocation:")
        for pid, pages in self.memory.items():
            print(f"  Process {pid}: {pages}")
        print(f"  Total Page Faults: {self.page_faults}")

memory_manager = MemoryManagement()

def simulate_memory():
    print("[Memory] Running Memory Simulation")
    for i in range(6):
        print(f"[Memory] Iteration {i}")
        memory_manager.allocate(1, f"Page{i}")
        time.sleep(0.5)
    memory_manager.status()

# ==============================
# Process Synchronization (Improved)
# ==============================
def simulate_sync():
    print("[Sync] Running Producer-Consumer simulation.")
    buffer = queue.Queue(maxsize=3)
    condition = threading.Condition()

    def producer():
        for i in range(5):
            with condition:
                while buffer.full():
                    print("[Sync] Buffer full, producer waiting...")
                    condition.wait()
                item = f"Item{i}"
                buffer.put(item)
                print(f" Producer: Produced {item}")
                condition.notify()
            time.sleep(0.5)

    def consumer():
        for _ in range(5):
            with condition:
                while buffer.empty():
                    print("[Sync] Buffer empty, consumer waiting...")
                    condition.wait()
                item = buffer.get()
                print(f" Consumer: Consumed {item}")
                condition.notify()
            time.sleep(0.7)

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_prod.start()
    t_cons.start()
    t_prod.join()
    t_cons.join()
    print("[Sync] Simulation completed.")

# ==============================
# Security: User Authentication and File Permissions
# ==============================
# Simulated user database with hashed passwords for extra refinement.
USERS = {
    "admin": {"password": hashlib.sha256("adminpass".encode()).hexdigest(), "role": "admin"},
    "user": {"password": hashlib.sha256("userpass".encode()).hexdigest(), "role": "standard"}
}

FILE_PERMISSIONS = {
    "system.txt": {"read": ["admin", "standard"], "write": ["admin"], "execute": []},
    "user.txt": {"read": ["admin", "standard"], "write": ["admin", "standard"], "execute": []},
}

current_user = None

def authenticate():
    global current_user
    print("Welcome to the Secure Integrated Shell")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if username in USERS and USERS[username]["password"] == hashed:
        current_user = {"username": username, "role": USERS[username]["role"]}
        print(f"Login successful. Role: {current_user['role']}\n")
    else:
        print("Authentication failed.")
        sys.exit(1)

def check_permission(operation, filename):
    if filename in FILE_PERMISSIONS:
        allowed = FILE_PERMISSIONS[filename].get(operation, [])
        return current_user["role"] in allowed
    return True

# ==============================
# Command Execution (Enhanced with Piping and Custom Commands)
# ==============================
def execute_command(command):
    # Check for piping
    if "|" in command:
        execute_piped_commands(command)
        return

    print(f"[Execution] Received command: {command}")
    if command.startswith("schedule_rr"):
        parts = command.split()
        if len(parts) < 3:
            print("[Error] Invalid format. Usage: schedule_rr <quantum> <command1> ; <command2> ; ...")
            return
        try:
            quantum = float(parts[1])
            commands = [cmd.strip() for cmd in " ".join(parts[2:]).split(';') if cmd.strip()]
            ProcessScheduling.round_robin_scheduler(commands, quantum)
        except ValueError:
            print("[Error] Invalid quantum value.")
    elif command == "simulate_memory":
        simulate_memory()
    elif command == "simulate_sync":
        simulate_sync()
    else:
        # Check for file-modifying commands and enforce permissions.
        tokens = shlex.split(command)
        if tokens and tokens[0] in ["rm", "touch", "mkdir", "rmdir"]:
            if len(tokens) > 1:
                filename = tokens[1]
                if not check_permission("write", filename):
                    print(f"Permission denied: You do not have write access to '{filename}'.")
                    return
        print(f"[Execution] Running: {command}")
        subprocess.run(shlex.split(command))

def execute_piped_commands(command_line):
    commands = [cmd.strip() for cmd in command_line.split('|')]
    if not commands:
        return
    prev_process = None
    processes = []
    for idx, cmd in enumerate(commands):
        tokens = shlex.split(cmd)
        if not tokens:
            continue
        if idx == 0:
            proc = subprocess.Popen(tokens, stdout=subprocess.PIPE)
        elif idx == len(commands) - 1:
            proc = subprocess.Popen(tokens, stdin=prev_process.stdout)
        else:
            proc = subprocess.Popen(tokens, stdin=prev_process.stdout, stdout=subprocess.PIPE)
        processes.append(proc)
        prev_process = proc
    processes[-1].communicate()

# ==============================
# Main Shell Loop
# ==============================
def main():
    authenticate()
    while True:
        try:
            cmd_input = input(f"{current_user['username']}@integrated-shell> ")
            if not cmd_input.strip():
                continue
            if cmd_input.strip() == "exit":
                print("Exiting integrated shell.")
                break
            execute_command(cmd_input)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
