import requests

ANKICONNECT_URL = "http://localhost:8765"

def get_models():
    response = requests.post(ANKICONNECT_URL, json={
        "action": "modelNames",
        "version": 6
    })
    if response.status_code == 200:
        return response.json().get("result")
    return None

models = get_models()

if models:
    print("Available models:", models)
else:
    print("Could not retrieve models.")