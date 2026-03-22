import requests
import os

def send_slack(message):
    webhook = os.getenv("SLACK_WEBHOOK")
    requests.post(webhook, json={"text": message})
