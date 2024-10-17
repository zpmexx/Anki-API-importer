import csv
import os
from datetime import datetime

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open('logfile.log', 'a') as file:
        file.write(f"""Date problem - {str(e)}\n""")
    print(f"Date problem - {str(e)}")


file_path = 'words_to_import.csv'

if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';') 

        # Dodanie nagłówków do pliku
        writer.writerow(['first side', 'second side'])
else:
    print()
    with open('logfile.log', 'a') as file:
        file.write(f"{formatDateTime} File '{file_path}' already exists. No new file was created.")
        print(f"{formatDateTime} File '{file_path}' already exists. No new file was created.")
