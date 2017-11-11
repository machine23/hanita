import subprocess
from sys import platform


def run():
    commands = ["python3 client.py -w", "python3 client.py -r"]
    for command in commands:
        if platform == "linux":
            subprocess.call(command, shell=True)

if __name__ == "__main__":
    run()
