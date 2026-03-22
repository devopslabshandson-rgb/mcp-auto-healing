from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import subprocess
from slack import send_slack

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LogRequest(BaseModel):
    logs: str

@app.post("/auto-heal")
def auto_heal(req: LogRequest):

    prompt = f"""
You are a senior DevOps engineer.

Analyze logs and respond in JSON:

- root_cause
- action (scale_up / scale_down / none)

Logs:
{req.logs}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content

    if "scale_up" in result:
        subprocess.run(["python3", "scale.py", "up"])
        action = "Scaled UP"
    elif "scale_down" in result:
        subprocess.run(["python3", "scale.py", "down"])
        action = "Scaled DOWN"
    else:
        action = "No scaling"

    send_slack(f"Auto-Healing Triggered 🚀\n\n{result}\n\nAction: {action}")

    return {"analysis": result, "action": action}
