import requests

ANKICONNECT_URL = "http://localhost:8765"

# Function to get all deck names
def get_decks():
    response = requests.post(ANKICONNECT_URL, json={
        "action": "deckNames",
        "version": 6
    })
    if response.status_code == 200:
        return response.json().get("result")
    return None

decks = get_decks()
if decks:
    print("Available decks:", decks)
else:
    print("Could not retrieve decks.")