import requests
import os

def send_slack(message):
    webhook = os.getenv("SLACK_WEBHOOK")

    if not webhook:
        print("❌ SLACK_WEBHOOK not set")
        return

    try:
        response = requests.post(
            webhook,
            json={"text": message},
            timeout=5
        )

        if response.status_code != 200:
            print(f"❌ Slack error: {response.text}")
        else:
            print("✅ Slack alert sent")

    except Exception as e:
        print(f"❌ Slack exception: {e}")
