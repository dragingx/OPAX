
import random
import string
import requests
import threading
import time
from datetime import datetime

# Discord webhook URL (replace with the actual webhook URL)
WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

# Function to send a test message to Discord webhook
def send_test_message():
    embed = {
        "color": 0x00ff00,  # Green color
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "Opax Username Search"
        },
        "description": "//////////Welcome to opax username search//////////\n" + "————————————\n" + "Test message sent successfully."
    }
    payload = {
        "embeds": [embed]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Test message sent successfully.")
    except requests.RequestException as e:
        print(f"Error sending test message to Discord: {e}")

# Send test message at the start
send_test_message()

# Function to generate a random 3-4 character username
def generate_username():
    length = random.choice([3, 4])
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to check Roblox username availability
def check_roblox_username(username):
    url = 'https://users.roblox.com/v1/usernames/validate'
    payload = {
        'username': username,
        'birthday': '2000-01-01'
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get('isAvailable', False)
    except requests.RequestException as e:
        print(f"Error checking Roblox username {username}: {e}")
        return False

# Function to send message to Discord webhook
def send_to_discord(usernames):
    embed_description = "//////////Welcome to opax username search made by @4j63//////////\n" + "————————————\n"
    for index, username in enumerate(usernames, start=1):
        embed_description += f"User {index}: {username} → AVAILABLE ✅\n"

    embed = {
        "color": 0x00ff00,  # Green color
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "Opax Username Search"
        },
        "description": embed_description
    }
    payload = {
        "embeds": [embed]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending to Discord: {e}")

# Function to run in each thread
def username_thread():
    while True:
        username = generate_username()
        if check_roblox_username(username):
            with lock:
                available_usernames.append(username)
                print(f"Available Roblox username found: {username}")
                send_to_discord(available_usernames)

# List to store available usernames
available_usernames = []
lock = threading.Lock()

# Create and start threads
threads = []
num_threads = 30
for _ in range(num_threads):
    thread = threading.Thread(target=username_thread)
    thread.start()
    threads.append(thread)

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the script.")
finally:
    for thread in threads:
        thread.join()
