import requests
from datetime import datetime

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open('logfile.log', 'a') as file:
        file.write(f"""Date problem - {str(e)}\n""")
    print(f"Date problem - {str(e)}")

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
        with open('logfile.log', 'a') as file:
            file.write(f"{formatDateTime} Error retrieving decks: {response.json()}\n")
        print(f"{formatDateTime} Error retrieving decks: {response.json()}")
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
        with open('logfile.log', 'a') as file:
            file.write(f"{formatDateTime} Error retrieving notes for deck '{deck_name}': {response.json()}\n")
        print(f"{formatDateTime} Error retrieving notes for deck '{deck_name}': {response.json()}")
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
        with open('logfile.log', 'a') as file:
            file.write(f"{formatDateTime} Error retrieving note info: {response.json()}\n")
        print(f"{formatDateTime} Error retrieving note info: {response.json()}")
        return None

# Main function to check fields and model names in all decks
def check_fields_in_decks():
    decks = get_decks()
    if decks:
        for deck in decks:
            log_message = f"Checking deck: {deck}"
            with open('logfile.log', 'a') as file:
                file.write(f"{formatDateTime} {log_message}\n")
            print(log_message)

            note_ids = get_notes_from_deck(deck)
            if note_ids:
                note_info = get_note_info(note_ids)
                if note_info:
                    fields_set = set()  # Using a set to avoid duplicates
                    model_names = set()  # Set to collect unique model names
                    for note in note_info:
                        fields_set.update(note['fields'].keys())
                        model_names.add(note['modelName'])

                    fields_message = f"Fields in '{deck}': {', '.join(fields_set)}"
                    models_message = f"Model names in '{deck}': {', '.join(model_names)}\n"
                    
                    with open('logfile.log', 'a') as file:
                        file.write(f"{formatDateTime} {fields_message}\n")
                        file.write(f"{formatDateTime} {models_message}\n")
                    
                    print(fields_message)
                    print(models_message)
                else:
                    log_message = f"Unable to retrieve note information for '{deck}'."
                    with open('logfile.log', 'a') as file:
                        file.write(f"{formatDateTime} {log_message}\n")
                    print(log_message)
            else:
                log_message = f"No notes found in '{deck}' or unable to retrieve notes."
                with open('logfile.log', 'a') as file:
                    file.write(f"{formatDateTime} {log_message}\n")
                print(log_message)
    else:
        log_message = "Unable to retrieve decks."
        with open('logfile.log', 'a') as file:
            file.write(f"{formatDateTime} {log_message}\n")
        print(log_message)

# Run the function
check_fields_in_decks()
