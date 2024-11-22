import json
from pathlib import Path

def load_categories():
    file_path = Path(__file__).resolve().parent / 'categories.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data