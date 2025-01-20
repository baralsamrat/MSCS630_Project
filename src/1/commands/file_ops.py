import os

def execute_file_command(parts):
    cmd = parts[0]
    args = parts[1:]

    if cmd == "ls":
        list_files()
    elif cmd == "cat":
        display_file(args)
    elif cmd == "mkdir":
        create_directory(args)
    elif cmd == "rmdir":
        remove_directory(args)
    elif cmd == "rm":
        remove_file(args)
    elif cmd == "touch":
        touch_file(args)
    else:
        print(f"{cmd}: Command not recognized.")

def list_files():
    for item in os.listdir():
        print(item)

def display_file(args):
    if not args:
        print("cat: missing filename")
    else:
        try:
            with open(args[0], 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f"cat: {args[0]}: No such file or directory")

def create_directory(args):
    if not args:
        print("mkdir: missing directory name")
    else:
        try:
            os.mkdir(args[0])
        except FileExistsError:
            print(f"mkdir: {args[0]}: Directory already exists")

def remove_directory(args):
    if not args:
        print("rmdir: missing directory name")
    else:
        try:
            os.rmdir(args[0])
        except FileNotFoundError:
            print(f"rmdir: {args[0]}: No such directory")
        except OSError:
            print(f"rmdir: {args[0]}: Directory not empty")

def remove_file(args):
    if not args:
        print("rm: missing filename")
    else:
        try:
            os.remove(args[0])
        except FileNotFoundError:
            print(f"rm: {args[0]}: No such file")

def touch_file(args):
    if not args:
        print("touch: missing filename")
    else:
        try:
            with open(args[0], 'a'):
                os.utime(args[0], None)
        except Exception as e:
            print(f"touch: {e}")
