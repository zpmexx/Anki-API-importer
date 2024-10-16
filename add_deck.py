import requests

# AnkiConnect URL (for desktop Anki with the plugin)
ANKICONNECT_URL = "http://localhost:8765"
deck_name = 'full talia'
model_name = 'Podstawowy'

# Define a new card
new_card = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": f"{deck_name}",   
            "modelName": f"{model_name}", 
            "fields": {
                "Przód": "Hellos",
                "Tył": "yes"
            },
        }
    }
}

# Function to add a new card via AnkiConnect
def add_new_card(card_data):
    response = requests.post(ANKICONNECT_URL, json=card_data)
    if response.status_code == 200 and response.json().get("error") is None:
        print("Card added successfully!")
    else:
        print(f"Error: {response.json()}")

add_new_card(new_card)