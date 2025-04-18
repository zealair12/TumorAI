import requests

def send_slack_message(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        print("✅ Slack status:", response.status_code)
        print("➡️ Slack response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print("❌ Slack error:", e)
        return False

