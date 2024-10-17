import requests
from datetime import datetime
import csv


# Function to add a new card via AnkiConnect
def add_new_card(card_data):
    response = requests.post(ANKICONNECT_URL, json=card_data)
    
    if response.status_code == 200 and response.json().get("error") is None:
        log_message = f"{formatDateTime} Card {new_card['params']['note']['fields']} added successfully!"
        with open('logfile.log', 'a') as file:
            file.write(log_message + "\n")
        print(f"{log_message}")
    else:
        error_message = f"{formatDateTime} Error: {response.json()}"
        with open('logfile.log', 'a') as file:
            file.write(error_message + "\n")
        print(f"Error: {response.json()}")

# Get current time for logging
now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open('logfile.log', 'a') as file:
        file.write(f"Date problem - {str(e)}\n")
    print(f"Date problem - {str(e)}")

# AnkiConnect URL (for desktop Anki with the plugin)
ANKICONNECT_URL = "http://localhost:8765"
# Change to correct deck name
deck_name = 'test'
# Change to correct model
model_name = 'Podstawowy'

words_dictionary = {}

with open('words_to_import.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    
    # Skip the header
    next(reader)

    for row in reader:
        try:
            key = row[0]   # First column as key
            value = row[1] # Second column as value
            words_dictionary[key] = value
        except Exception as e:
            with open('logfile.log', 'a') as file:
                file.write(f"Import problem for {row} - {str(e)}\n")
            print(f"Import problem for {row} - {str(e)}\n")

for front_side, back_side in words_dictionary.items():
    new_card = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": f"{deck_name}",
                "modelName": f"{model_name}",
                # Include chosen fields
                "fields": {
                    "Tył": f"{front_side}",
                    "Przód": f"{back_side}"
                },
            }
        }
    }
    add_new_card(new_card)




