from datetime import datetime
import os
import json
from flask import current_app
from typing import Any


def get_current_time():
    # Get the current time
    now = datetime.now()
    
    # Format the time as a string
    current_time = now.strftime("%H:%M:%S")
    
    return current_time

def load_translation_file(locale_id: int, filename: str) -> Any:
    # Define the file name and construct the file path
    file_name_translations = filename +'.json'
    file_path_translations = os.path.join(
        current_app.root_path, 'static', 'translations', str(locale_id), file_name_translations
    )
    
    # Read and parse the JSON data
    with open(file_path_translations, 'r', encoding='utf-8') as file:
        json_translations = json.load(file)
    
    return json_translations

