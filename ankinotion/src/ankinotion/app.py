import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

class AnkiNotionApp(toga.App):
    def startup(self):
        # --- Main container ---
        main_box = toga.Box(
            style=Pack(direction=COLUMN, padding=20, background_color="#f5f5f5")
        )

        # --- Text input ---
        self.text_input = toga.TextInput(
            placeholder="Enter your word...",
            style=Pack(padding=(0, 0, 10, 0), font_size=14, background_color="white")
        )

        # --- Submit button ---
        self.button = toga.Button(
            "➕ Add to Notion",
            on_press=self.on_button_click,
            style=Pack(
                padding=10,
                background_color="#3366cc",  # Blue
                color="white",
                font_size=14
            )
        )

        # --- Result display area ---
        self.results_box = toga.Box(style=Pack(direction=COLUMN, padding_top=15))
        self.container = toga.ScrollContainer(content=self.results_box, style=Pack(flex=1))

        # --- Layout ---
        main_box.add(self.text_input)
        main_box.add(self.button)
        main_box.add(self.container)

        # --- Main window ---
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def on_button_click(self, widget):
        text = self.text_input.value.strip()

        if not text:
            self.display_message("⚠️ Please enter some text.", color="orange")
            return

        try:
            success, message = self.add_entry_to_notion(text)
            self.display_message(f"✅ {message}", color="green" if success else "red")
        except Exception as e:
            self.display_message(f"❌ Error: {e}", color="red")

        self.text_input.value = ""

    def add_entry_to_notion(self, text):
        NOTION_API_KEY = os.getenv("NOTION_API_KEY")
        DATABASE_ID = os.getenv("DATABASE_ID")

        if not NOTION_API_KEY or not DATABASE_ID:
            raise ValueError("Missing NOTION_API_KEY or DATABASE_ID in .env")

        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "first side": {
                    "title": [{"text": {"content": text}}]
                },
                "second side": {
                    "rich_text": []
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return True, f"'{text}' added to Notion."
        else:
            return False, f"Failed ({response.status_code}): {response.text}"

    def display_message(self, message, color="black"):
        self.results_box.clear()
        self.results_box.add(
            toga.MultilineTextInput(
                value=message,
                readonly=True,
                style=Pack(
                    font_size=13,
                    color=color,
                    padding=8,
                    height=100,
                    #width=400
                )
            )
        )

        
def main():
    return AnkiNotionApp()
