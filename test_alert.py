import requests

# 1. Paste your secret URL inside the quotes
WEBHOOK_URL = "https://discord.com/api/webhooks/1481922757468885135/G2hEgHtGyrhvX6ZAonY2tST2xMVTqB6boda457dyHrwW7lj0hqS15rtIwl9OGDqQxZ_u"

def send_discord_alert(message_text):
    """Sends a push notification to the Heeramoti HQ Discord server."""

    # 2. Package the message exactly how Discord expects it
    payload = {
        "content" : message_text
    }

    # 3. Fire the POST request across the internet
    response = requests.post(WEBHOOK_URL, json=payload)

    # 4. Check if Discord accepted it (Discord returns 204 for a successful webhook)
    if response.status_code == 204:
        print("Success! Check your discord")
    else:
        print(f"Failed to send, Error code: {response.status_code}")

# Fire the test engine
send_discord_alert("🚨 **NEW LEAD ALERT:** The webhook engine is live!")