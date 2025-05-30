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

---

# Notion update
### If you want add new cards from diffrent devices and automate import (via cron or windows task scheduler) you could use external site like [Notion](https://www.notion.so/) to store data, connect automatically via API and manage AndkiDroid new cards.

1. Create account [Notion](https://www.notion.so/)
2. Create table with 2 columns similar to ->> **example.png**
3. Create  [Notion integration](https://developers.notion.com/docs/create-a-notion-integration) and save NOTION_API_KEY (Integral Integration Secret)
4. Connect created integration to notion table (on notion's table site **...** -> connect to)
5. Fill into .env file NOTION_API_KEY and DATABASE_ID (notion's table site -> share -> copy link (from first / till ? < database id) for example in link:
``https://www.notion.so/1123casad801sa6ds75dasdae91c39asd?v=dsad8as6asndasd&pvs=4``  
database id is
``1123casad801sa6ds75dasdae91c39asd``
6. Update notion_import.py the same way as import.py to include yours deck's name, model's name and fields
7. Set in notion_import.py variable INCLUDE_REVERSE to True if you want to insert into the same deck both sides, False otherwise
8. Set CRON or Task scheduler to run those scripts automatically
9. The file words_history.txt will contain all cards imported into the AnkiDroid deck, separated by commas. You can share or use this file to push cards back into Notion (e.g., to share with another user). Simply run the export_to_notion.py script to export the data to the Notion database.
### if any error occurs, it will be stored into .log file as well.

# Beeware app to add word to notion's db
1. The ankinotion folder contains the source code for a BeeWare Toga application that you can install on your Android phone. It allows you to quickly send words to your Notion database, making it easier than using the Notion app itself and serving as a convenient alternative.
2. You may need to install the required modules using the re.txt file:
`pip install -r re.txt`.
3. You need to create a passwords.txt file in \ankinotion\src\ankinotion\resources with the same data as in the .env file, separated by commas, as shown below:

`NOTION_API_KEY,<your NOTION_API_KEY from .env file`

`DATABASE_ID,<your DATABASE_ID from .env file>`

4. To run the script from your PC, type `briefcase dev` in the terminal.
5. If you want to create an Android app, run the following commands:
	
	* briefcase create 
	* briefcase build
	* briefcase create android 
	* briefcase build android

6. The app file will be stored in ankinotion\build\ankinotion\android\gradle\app\build\outputs\apk\debug
7. Copy the .apk file to your phone and install it.
8. Information about a successful import or any errors will be stored below the Add button.

![App Image](notionanki.jpg)
