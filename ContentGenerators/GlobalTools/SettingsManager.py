import json
import os

settings_file_name = 'settings.json'

default_values = {
    "LANGUAGE_MODEL": {
        "OPENAI": True,
        "MODEL": "llama3.2",
        "BASE_URL": "http://localhost:11434/",
        "API_KEY": "?"
    },
    "DOCUMENT_SETTINGS": {
        "WATERMARK_PDF_LOCATION": "---"
    }
}


class Settings:
    def __init__(self):
        # Check if the file exists
        if not os.path.exists(settings_file_name):
            # Create the file if it does not exist
            open(settings_file_name, 'w').close()
        try:
            # Load the existing values from the file
            with open(settings_file_name, 'r') as file:
                self.data = json.load(file)
            if self.data == {}:
                raise Exception(f"Your Settings File is Empty. Please go through {settings_file_name} and fill in the missing values.")
        except (json.JSONDecodeError, FileNotFoundError):
            with open(settings_file_name, 'w') as file:
                json.dump(default_values, file, indent=4)
            raise Exception(f"Your Settings File has been Created. Please go through {settings_file_name} and fill in the missing values.")
