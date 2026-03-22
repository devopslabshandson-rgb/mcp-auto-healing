import subprocess
import time
import requests
import os

SLACK = os.getenv("SLACK_WEBHOOK")

CONTAINER_NAME = "my-app"
SCALED_CONTAINER = "my-app-2"

def get_cpu():
    try:
        output = subprocess.check_output(
            f"docker stats --no-stream --format '{{{{.CPUPerc}}}}' {CONTAINER_NAME}",
            shell=True
        ).decode().strip().replace("%", "")
        return float(output)
    except:
        return 0

def container_exists(name):
    result = subprocess.run(
        f"docker ps -a --format '{{{{.Names}}}}' | grep -w {name}",
        shell=True,
        stdout=subprocess.PIPE
    )
    return result.returncode == 0

def scale_up():
    if not container_exists(SCALED_CONTAINER):
        subprocess.run(f"docker run -d --name {SCALED_CONTAINER} nginx", shell=True)
        requests.post(SLACK, json={"text": "🚀 Auto-Scaled UP (High CPU detected)"})

def scale_down():
    if container_exists(SCALED_CONTAINER):
        subprocess.run(f"docker rm -f {SCALED_CONTAINER}", shell=True)
        requests.post(SLACK, json={"text": "📉 Auto-Scaled DOWN (Low CPU)"})

while True:
    cpu = get_cpu()
    print("CPU:", cpu)

    if cpu > 50:
        scale_up()
    elif cpu < 10:
        scale_down()

    time.sleep(10)
