import os
import time
import requests
import json

# Configuration
webhook_url = 'https://hooks.slack.com/services/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'
directory_to_watch = '/Users/jcran/work/mallory/local/mallory/tmp/vulnerability_analysis'
check_interval = 10  # seconds

# Create directory if it doesn't exist
if not os.path.exists(directory_to_watch):
    os.makedirs(directory_to_watch)

# List to keep track of filenames
known_files = set(os.listdir(directory_to_watch))

def send_notification_to_slack(message):
    payload = {"text": message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to send notification to Slack: {response.text}")

def read_and_send_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            
            content = file.read()
            content_json = json.loads(content)

            message = f"New item:\n```{content_json}```"
            send_notification_to_slack(message)

    except Exception as e:
        print(f"Could not read {file_path}: {str(e)}")

# Informing that the script is listening for new files
print("Listening for messages in", directory_to_watch)

while True:
    current_files = set(os.listdir(directory_to_watch))
    new_files = current_files - known_files
    
    for new_file in new_files:
        full_file_path = os.path.join(directory_to_watch, new_file)
        read_and_send_file_content(full_file_path)
        
    known_files = current_files
    time.sleep(check_interval)
