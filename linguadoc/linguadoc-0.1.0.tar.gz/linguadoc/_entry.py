from linguadoc import LinguaDoc
import click
import hashlib
import os
from linguadoc.lib import read_json, add_bracket, get_translation, write_json

def get_preproc_jsonfile_name(sourcejson, lang):
  name = hashlib.md5(sourcejson.encode()).hexdigest()[:8]
  temp_dir = "_".join([lang, "temp"])
  if not os.path.isdir(temp_dir):
    os.mkdir(temp_dir) 
  return os.path.join(temp_dir, name+".json")

@click.command()
@click.option("--sourcejson", prompt="source json file path", help="Specify the source json file path")
@click.option("--lang", prompt="language", help="Specify the language")
def preprocess_data(sourcejson, lang):
  output = get_preproc_jsonfile_name(sourcejson, lang)
  data = read_json(sourcejson)[:10]
  for d in data:
    analysis = d["analysis"]
    structure = " ".join([t["text"] + add_bracket(t["explanation"]) for t in analysis])
    d["structure"] = structure
    for t in analysis:
      if t["explanation"]:
        t["translation"] = get_translation(t["text"], from_lang=lang)
      else:
        t["translation"] = t["text"]
    d["translation"] = get_translation(d["sentence"], from_lang=lang)
  write_json(data, output)
  print(output)

@click.command()
@click.option("--sourcejson", prompt="source json file path", help="Specify the source json file path")
@click.option("--lang", prompt="language", help="Specify the language")
@click.option("--destdocx", prompt="destination docx file path", help="Specify the docx file path")
@click.option("--title", default="test", help="Specify doc title")
def gen_lingua_docx(sourcejson, lang, destdocx, title):
  doc = LinguaDoc(sourcejson, lang)
  doc.gen_doc(title, destdocx)
