import requests
import time
import json
import random


# Constants
URL = "https://api.mokl.io/public/api/clicker/tap"
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
WAIT_TIME = 5 * 60  # 5 minutes in seconds

def read_authorizations(file_path):
    """Read authorization tokens from the file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def make_request(auth_token):
    """Send the request for a specific authorization token."""
    headers = HEADERS_TEMPLATE.copy()
    headers["authorization"] = f"Bearer {auth_token}"

    # Get current timestamp
    timestamp = int(time.time())

    data = {
        "count": random.randint(270, 330),
        "energy": 500,
        "timestamp": timestamp
    }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"[✔] Success for token: {auth_token}")
        else:
            print(f"[✖] Failed for token: {auth_token}, Status: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"[!] Request error for token {auth_token}: {e}")

def main():
    """Main script logic."""
    file_path = "datas.txt"

    while True:
        authorizations = read_authorizations(file_path)
        if not authorizations:
            print("[!] No authorization tokens found. Exiting.")
            break

        for token in authorizations:
            make_request(token)

        print(f"[*] Waiting for {WAIT_TIME // 60} minutes before next cycle...")
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()
