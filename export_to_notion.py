import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open('logfile.log', 'a') as file:
        file.write(f"Date problem - {str(e)}\n")
    print(f"Date problem - {str(e)}")


# Load env variables
try:
    load_dotenv()
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')
    DATABASE_ID = os.getenv('DATABASE_ID')
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with loading .env variables - {str(e)}\n""")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def post_words_to_notion(first_side, second_side):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "first side": {
                "title": [{"text": {"content": first_side}}]
            },
            "second side": {
                "rich_text": [{"text": {"content": second_side}}]
            },
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        log_message = f"{formatDateTime} Data {first_side} - {second_side} exported successfully to notion"
        with open('export_logfile.log', 'a') as file:
            file.write(log_message + "\n")
    else:
        log_message = f"{formatDateTime} Data {first_side} - {second_side} not exported successfully to notion. Error code: {response.status_code}"
        with open('export_logfile.log', 'a') as file:
            file.write(log_message + "\n")

if __name__ == "__main__":
    words_dict = {}
    try:
        with open('words_history.txt', 'r') as file:
            for line in file:
                parts = line.split(',', maxsplit=1)
                if len(parts) == 2:  # Ensure the line has both parts
                    key, value = parts[0].strip(), parts[1].strip()
                    words_dict[key] = value
        for k,v in words_dict.items():
            post_words_to_notion(k,v)
    except Exception as e:
        with open ('logfile.log', 'a') as file:
            file.write(f"""{formatDateTime} Problem with sending data to notion - {str(e)}\n""")
