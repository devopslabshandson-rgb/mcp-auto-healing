# AI Auto-Healing DevOps System

## Features
- AI-based log analysis
- Auto Kubernetes scaling
- Slack notification

## Run

docker build -t autoheal .

docker run -d -p 9000:9000 \
-e OPENAI_API_KEY=your_key \
-e SLACK_WEBHOOK=your_webhook \
autoheal
