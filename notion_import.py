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

# Funkcja do pobierania słów i wyjaśnień
def get_words_from_notion():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    response_data = response.json()
    notion_d = {}

    # Loop through each page in the results
    for page in response_data.get("results", []):
        # Extract the "first side" content
        page_id = page["id"]
        
        first_side_title = page["properties"]["first side"]["title"]
        
        first_side_content = first_side_title[0]["plain_text"] if first_side_title else None

        second_side_text = page["properties"]["second side"]["rich_text"]
        second_side_content = second_side_text[0]["plain_text"] if second_side_text else None

        # Save only correct cards (both side filled in)
        if page and first_side_content and second_side_content:
            notion_d[page_id] = (first_side_content,second_side_content)
            
  
    return(notion_d)



# Delete specific page (anki deck from notion)
def delete_entry(page_id):
    delete_url = f"https://api.notion.com/v1/blocks/{page_id}"
    delete_response = requests.delete(delete_url, headers=headers)
    

def add_new_card(card_data, page_id, reverse):
    response = requests.post(ANKICONNECT_URL, json=card_data)
    
    if response.status_code == 200 and response.json().get("error") is None:
        log_message = f"{formatDateTime} Card {new_card['params']['note']['fields']} added successfully!"
        with open('logfile.log', 'a') as file:
            file.write(log_message + "\n")
        print(f"{log_message}")
        
        #include reversed
        if reverse == True:
            reversed_card = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": f"{deck_name}",
                    "modelName": f"{model_name}",
                    # Include chosen fields
                    "fields": {
                        "Przód": f"{back_side}",
                        "Tył": f"{front_side}"
                     },
                 }
             }
            }
            response = requests.post(ANKICONNECT_URL, json=reversed_card)
            if response.status_code == 200 and response.json().get("error") is None:
                log_message = f"{formatDateTime} Card {new_card['params']['note']['fields']} in reverse added successfully!"
                with open('logfile.log', 'a') as file:
                    file.write(log_message + "\n")
                print(f"{log_message}")
            else:
                error_message = f"{formatDateTime} Error: {response.json()}"
                with open('logfile.log', 'a') as file:
                    file.write(error_message + "\n")
                print(f"Error: {response.json()}")
                
        #delete from Notion
        delete_entry(page_id)
    else:
        error_message = f"{formatDateTime} Error: {response.json()}"
        with open('logfile.log', 'a') as file:
            file.write(error_message + "\n")
        print(f"Error: {response.json()}")


if __name__ == "__main__":
    INCLUDE_REVERSE = True # set false to import also reverse to the same deck
    ANKICONNECT_URL = "http://localhost:8765"
    # Change to correct deck name
    deck_name = 'full talia'
    # Change to correct model
    model_name = 'Podstawowy'
    words_dictionary = get_words_from_notion()
    for page_id, (front_side, back_side) in words_dictionary.items():
    
        new_card = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": f"{deck_name}",
                "modelName": f"{model_name}",
                # Include chosen fields
                "fields": {
                    "Przód": f"{front_side}",
                    "Tył": f"{back_side}"
                },
            }
        }
    }
        try:
            add_new_card(new_card, page_id, INCLUDE_REVERSE)
        except Exception as e:
            with open('logfile.log', 'a') as file:
                file.write(f"Import problem for {page_id}, {front_side}, {back_side} - {str(e)}\n")
    
            
    sync_payload = {
        "action": "sync",
        "version": 6
    }

    # Send the request to AnkiConnect
    response = requests.post(ANKICONNECT_URL, json=sync_payload)

    # Check the response
    if response.json().get("error") is None:
        print("Sync successful!")
    else:
        with open('logfile.log', 'a') as file:
            file.write(f'Sync error:", {response.json()["error"]}')
        