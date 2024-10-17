import requests
from datetime import datetime

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
deck_name = 'full talia'
model_name = 'Podstawowy'

front_side = "Hello"
back_side = "Helloback"

# Define a new card
new_card = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": f"{deck_name}",
            "modelName": f"{model_name}",
            "fields": {
                "Przód": f"{front_side}",
                "Tył": f"{back_side}"
            },
        }
    }
}

# Function to add a new card via AnkiConnect
def add_new_card(card_data):
    response = requests.post(ANKICONNECT_URL, json=card_data)
    
    if response.status_code == 200 and response.json().get("error") is None:
        log_message = f"{formatDateTime} Card added successfully!"
        with open('logfile.log', 'a') as file:
            file.write(log_message + "\n")
        print("Card added successfully!")
    else:
        error_message = f"{formatDateTime} Error: {response.json()}"
        with open('logfile.log', 'a') as file:
            file.write(error_message + "\n")
        print(f"Error: {response.json()}")

add_new_card(new_card)
