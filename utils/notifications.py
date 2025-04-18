import requests

def send_slack_message(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        print("✅ Slack message sent:", response.status_code)
        return response.status_code == 200
    except Exception as e:
        print("❌ Slack error:", e)
        return False
