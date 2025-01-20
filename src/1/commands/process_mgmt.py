import os
import subprocess
import signal

background_jobs = {}  # Dictionary to store background jobs with job_id as key

def execute_process_command(parts):
    cmd = parts[0]
    args = parts[1:]

    if cmd == "kill":
        kill_process(args)
    elif cmd == "jobs":
        list_jobs()
    elif cmd == "fg":
        bring_to_foreground(args)
    elif cmd == "bg":
        resume_in_background(args)
    elif "&" in " ".join(parts):
        run_background_command(parts)
    else:
        run_foreground_command(parts)

def run_background_command(parts):
    try:
        process = subprocess.Popen(parts[:-1])
        job_id = len(background_jobs) + 1
        background_jobs[job_id] = process
        print(f"[{job_id}] {process.pid}")
    except FileNotFoundError:
        print(f"{parts[0]}: command not found")

def run_foreground_command(parts):
    try:
        subprocess.run(parts)
    except FileNotFoundError:
        print(f"{parts[0]}: command not found")

def list_jobs():
    for job_id, process in background_jobs.items():
        print(f"[{job_id}] {process.pid} Running")

def bring_to_foreground(args):
    if not args:
        print("fg: missing job ID")
        return
    job_id = int(args[0])
    if job_id not in background_jobs:
        print(f"fg: no such job {job_id}")
        return
    process = background_jobs.pop(job_id)
    process.wait()
    print(f"[{job_id}] {process.pid} Done")

def resume_in_background(args):
    if not args:
        print("bg: missing job ID")
        return
    job_id = int(args[0])
    if job_id not in background_jobs:
        print(f"bg: no such job {job_id}")
        return
    process = background_jobs[job_id]
    print(f"[{job_id}] {process.pid} Resumed")
