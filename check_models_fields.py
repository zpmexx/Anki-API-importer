import requests

ANKICONNECT_URL = "http://localhost:8765"

# Function to get all available decks
def get_decks():
    response = requests.post(ANKICONNECT_URL, json={
        "action": "deckNames",
        "version": 6
    })
    if response.status_code == 200:
        return response.json().get("result")
    else:
        print(f"Error retrieving decks: {response.json()}")  # Print error response
        return None

# Function to get note IDs from a specific deck
def get_notes_from_deck(deck_name):
    response = requests.post(ANKICONNECT_URL, json={
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'deck:"{deck_name}"'
        }
    })
    if response.status_code == 200:
        return response.json().get("result")
    else:
        print(f"Error retrieving notes for deck '{deck_name}': {response.json()}")  # Print error response
        return None

# Function to get detailed note information
def get_note_info(note_ids):
    response = requests.post(ANKICONNECT_URL, json={
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    })
    if response.status_code == 200:
        return response.json().get("result")
    else:
        print(f"Error retrieving note info: {response.json()}")  # Print error response
        return None

# Main function to check fields and model names in all decks
def check_fields_in_decks():
    decks = get_decks()
    if decks:
        for deck in decks:
            print(f"Checking deck: {deck}")
            note_ids = get_notes_from_deck(deck)
            if note_ids:
                note_info = get_note_info(note_ids)
                if note_info:
                    fields_set = set()  # Using a set to avoid duplicates
                    model_names = set()  # Set to collect unique model names
                    for note in note_info:
                        fields_set.update(note['fields'].keys())
                        model_names.add(note['modelName'])
                    
                    print(f"Fields in '{deck}': {', '.join(fields_set)}")
                    print(f"Model names in '{deck}': {', '.join(model_names)}\n")
                else:
                    print(f"Unable to retrieve note information for '{deck}'.\n")
            else:
                print(f"No notes found in '{deck}' or unable to retrieve notes.\n")
    else:
        print("Unable to retrieve decks.")

# Run the function
check_fields_in_decks()
