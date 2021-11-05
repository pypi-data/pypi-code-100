from pathlib import Path
import json

class Translator:

    def __init__(self):
        self.translations = { str: dict }
        self.languages_path = Path(__file__).parent.resolve()
        self.loadLangages()

    def loadLangages(self):
        languages = [ lang for lang in self.languages_path.iterdir() if lang.name.endswith('json') ]
        print('Detecting languages...')
        for lang in languages:
            print(f"Language {lang.name} detected")
            path = lang.name.split('\\')
            code = path[-1].split('.')[0]
            with open(lang, encoding='utf-8') as f:
                self.translations[code] = json.load(f)