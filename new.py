import requests
import time
import json
import random
import os

# Constants
TAP_URL = "https://api.mokl.io/public/api/clicker/tap"
TASK_URL_TEMPLATE = "https://api.mokl.io/public/api/clicker/tasks/{}"
HEADERS_TEMPLATE = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://play.mokl.io",
    "priority": "u=1, i",
    "referer": "https://play.mokl.io/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
WAIT_TIME = 5 * 60  # 5 minutes
TASKS_FILE = "completed_tasks.json"

def read_authorizations(file_path):
    """Read authorization tokens from the file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def load_completed_tasks():
    """Load completed tasks from JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_completed_tasks(completed_tasks):
    """Save completed tasks to JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(completed_tasks, f)

def make_tap_request(auth_token):
    """Send the main tap request."""
    headers = HEADERS_TEMPLATE.copy()
    headers["authorization"] = f"Bearer {auth_token}"

    data = {
        "count": random.randint(270, 330),  # Random number between 270-330
        "energy": 500,
        "timestamp": int(time.time())  # Current timestamp
    }

    try:
        response = requests.post(TAP_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"[✔] Tap Success for token: {auth_token}")
        else:
            print(f"[✖] Tap Failed for token: {auth_token}, Status: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"[!] Tap Request error for token {auth_token}: {e}")

def make_task_requests_once(auth_token, completed_tasks):
    """Perform task requests from 1 to 100 once per account (only at script start)."""
    if auth_token in completed_tasks:
        return  # Tasks already completed for this account, skip

    completed_tasks[auth_token] = []

    for task_id in range(1, 101):
        headers = HEADERS_TEMPLATE.copy()
        headers["authorization"] = f"Bearer {auth_token}"
        headers["content-length"] = "0"  # Required for this request

        task_url = TASK_URL_TEMPLATE.format(task_id)

        try:
            response = requests.post(task_url, headers=headers)
            if response.status_code == 200:
                print(f"[✔] Task {task_id} completed for token: {auth_token}")
                completed_tasks[auth_token].append(task_id)
                save_completed_tasks(completed_tasks)  # Save progress
            else:
                print(f"[✖] Task {task_id} failed for token: {auth_token}, Status: {response.status_code}, Response: {response.text}")
        except requests.RequestException as e:
            print(f"[!] Task Request error for token {auth_token}: {e}")

def main():
    """Main script logic."""
    file_path = "datas.txt"
    completed_tasks = load_completed_tasks()

    authorizations = read_authorizations(file_path)
    if not authorizations:
        print("[!] No authorization tokens found. Exiting.")
        return

    # Perform tasks once at script start
    for token in authorizations:
        make_task_requests_once(token, completed_tasks)  # Tasks done once per account

    while True:
        for token in authorizations:
            make_tap_request(token)  # Keep doing the tap request every 5 minutes
            time.sleep(random.randint(2,5))

        print(f"[*] Waiting for {WAIT_TIME // 60} minutes before next cycle....Subscribe to DeepTV...")
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()
