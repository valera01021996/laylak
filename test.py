import os
import json

LOCALES_DIR = "locale"
locales = {}

for filename in os.listdir(LOCALES_DIR):
    if filename.endswith(".json"):
        with open(os.path.join(LOCALES_DIR, filename), 'r', encoding='utf-8') as f:
            locales[filename.split('.')[0]] = json.load(f)


def get_locale_text(lang, text_key):
    return locales.get(lang, {}).get(text_key, '')
