import json
from googletrans import Translator

def read_json(jsonfile):
  data = []
  with open(jsonfile) as f:
    data = json.load(f)
  return data

def write_json(content, filename):
  with open(filename, 'w') as outfile:
    json.dump(content, outfile) 

def add_bracket(ex):
  return " (" + ex + ")" if ex!=None else "" 


def get_translation(p, from_lang, to_lang="zh-CN"):
  translator = Translator()
  result = translator.translate(p, src=from_lang, dest=to_lang)
  print(result)
  return result.text

