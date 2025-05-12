import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
# Get current time for logging
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


def insert_to_notion(text):
    create_url = "https://api.notion.com/v1/pages"
    
    new_page_data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "first side": {
                "title": [
                    {
                        "text": {
                            "content": text
                        }
                    }
                ]
            },
            "second side": {
                "rich_text": []  # Empty initially
            }
        }
    }

    response = requests.post(create_url, headers=headers, json=new_page_data)
    if response.status_code == 200:
        print("✅ Entry added successfully.")
    else:
        print(f"❌ Failed to add entry: {response.status_code} {response.text}")
        
        
insert_to_notion("test")