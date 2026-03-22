import sys
import subprocess

action = sys.argv[1]

if action == "up":
    subprocess.run(["kubectl", "scale", "deployment", "my-app", "--replicas=5"])
elif action == "down":
    subprocess.run(["kubectl", "scale", "deployment", "my-app", "--replicas=2"])
