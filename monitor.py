import requests
import json
import time

# CONFIGURATION
# Replace with the URL you want to monitor (e.g., your project's Flask app URL or a test site)
TARGET_URL = "https://google.com"
# Replace with your actual Discord Webhook URL
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK"

def check_website():
    try:
        # Send a request with a 5-second timeout
        response = requests.get(TARGET_URL, timeout=5)
        
        # If the status code is not 200, trigger an incident alert
        if response.status_code != 200:
            send_alert(f"🚨 **INCIDENT ALERT:** {TARGET_URL} returned status code {response.status_code}!")
        else:
            print(f"[HEALTHY] {TARGET_URL} is online. Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        # Trigger an alert if the site is completely unreachable/down
        send_alert(f"💥 **CRITICAL CRASH:** Cannot reach {TARGET_URL}. Error: {e}")

def send_alert(message):
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        if res.status_code == 204:
            print("[ALERT SENT] Incident notification pushed to Discord successfully.")
    except Exception as e:
        print(f"Failed to send alert: {e}")

if __name__ == "__main__":
    check_website()
