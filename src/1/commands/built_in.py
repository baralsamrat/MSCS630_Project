import os

def execute_built_in(parts):
    cmd = parts[0]
    args = parts[1:]

    if cmd == "cd":
        change_directory(args)
    if cmd == "pwd":
        print("Expected working directory:", os.getcwd())
    elif cmd == "echo":
        print(" ".join(args))
    elif cmd == "clear":
        os.system("clear")  # Use "cls" on Windows
    else:
        print(f"{cmd}: Command not recognized.")

def change_directory(args):
    if not args:
        print("cd: missing argument")
    else:
        try:
            os.chdir(args[0])
        except FileNotFoundError:
            print(f"cd: no such directory: {args[0]}")
