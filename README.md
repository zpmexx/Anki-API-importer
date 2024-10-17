# Anki-Api-Importer

1. Download Anki desktop here [Anki download](https://apps.ankiweb.net/).

2. Add AnkiConnect [AnkiConnect](https://ankiweb.net/shared/info/2055492159) extension.

		2055492159 <- AnkiConnect code

3. Check settings of AnkiConnect (should be similar to the one below) 

		"apiKey": null,
		"apiLogPath": null,
		"ignoreOriginList": [],
		"webBindAddress": "127.0.0.1",
		"webBindPort": 8765,
		"webCorsOriginList": [
			"http://localhost"
		]

4. If there are any differences with AnkiConnect settings, replace them in python files.
	`manually_add_card.py - script to import single card, use this to tests`
	`check_models_fields.py - script to check models and fields for every deck`
	`import.py - script that automatically import cards into specific Anki deck (one way)`
	`import_other_way.py - same as above but import the other way`
5. First of all run check_models_fields.py file to get infomation about data to replace into code.

		{
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
	
6. Run script create_words_to_import_file.py to create import file with correct separator ';'.
7. Fill words_to_import.csv with cards to import (front side/back side separated by ;).
8. Run import.py or import_other_way.py scripts to import data into Anki deck.

### if any error occurs, it will be stored into .log file.