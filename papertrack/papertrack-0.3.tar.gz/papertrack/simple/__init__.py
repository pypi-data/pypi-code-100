


from collections import UserList
import collections
from genericpath import exists
from typing import List
from easy_widgets.Application import Application

from easy_widgets.Menu import Menu
from papertrack.core import *
import os 
from papertrack.core import Database, DatabaseEntry, Configuration, Field, get_configuration

@register_downloader
class SimpleDownloader:
    name = "simple"
    params = {
        "url": {
            "type": "string",
            "description": "URL to download PDF from"
        },
        "location": {
            "type": "string",
            "default": os.path.join("/tmp", "papertrack-downloads"),
            "description": "Location where PDF are going to be downloaded at."
        }
    }
    def __init__(self, url, location):
        self.url = url
        self.download_location = location
    
    def _download(self, url, output):
        import urllib.request
        urllib.request.urlretrieve(url, output)
    
    def download(self):
        print("Downloading from %s" % self.url)
        import datetime 
        name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.pdf")
        os.makedirs(self.download_location, exist_ok=True)
        output = os.path.join(self.download_location, name)
        self._download(self.url, output)
        return output


@register_collector
class SimpleCollector:
    name = "simple"
    params = {
        "author": {
            "type": "list",
            "description": "Specify list of authors"
        },
        "title": {
            "type": "string",
            "description": "Specify title"
        },
        "year": {
            "type": "int",
            "description": "Specify year of publication"
        },
        "field": {
            "type": "string",
            "description": "Select field of study (e.g. Computer Science) and category (format field/category)",
            "choices": list("%s/%s" % (field.name, cat) 
                for field in get_configuration(name).get_fields() for cat in field.categories
            ),
            "default": get_configuration(name).get_default_field().name + "/" + get_configuration(name).get_default_field().default_category,
        },
        "location": {
            "type": "string",
            "description": "Path where the papers are stored (with categories as subdirs and fields as their subdirs)",
            "default": get_configuration(name).get_storage_location()
        }
    }
    def __init__(self, author: list, title: str, year: int, field, location):
        self.authors = author
        self.title = title 
        self.year = year
        self.field = field.split("/")[0]
        self.category = field.split("/")[1]
        self.location = location
    
    def _convert_author(self, author):
        return "".join(x[0] + ". " for x in author.split()[:-1]) + author.split()[-1]
    
    def _convert_authors(self, authors):
        return " ".join(self._convert_author(x) for x in authors)

    def collect(self, location):
        import shutil
        print("Collecting from %s" % location)
        os.makedirs(os.path.join(self.location, self.field, self.category), exist_ok=True)
        destination = os.path.join(
            self.location,
            self.field,
            self.category,
            f"{self._convert_authors(self.authors)} - {self.title} ({self.year}).pdf"
        )
        shutil.move(location, destination)
        return DatabaseEntry(
            title=self.title,
            authors=self.authors,
            publicationYear=self.year,
            path=destination,
            url="",
            status=get_configuration(self.name).get_default_document_state(),
            field=self.field,
            category=self.category
        )

@register_viewer
class SimpleViewer:
    name = "simple"
    params = {
        "location": {
            "type": "string",
            "description": "Path where PDFs are stored",
            "default": get_configuration(name).get_storage_location()
        },
    }
    def __init__(self, location: str):
        self.location = location
    
    def view(self, entries: List[DatabaseEntry]):
        import easy_widgets
        import subprocess
        easy_widgets.Application.init()
        fields = get_configuration(self.name).get_fields()
        field_menu = easy_widgets.Menu("Fields")
        def open_paper(btn, p):
            entry: DatabaseEntry = p[0]
            print("Opening %s" % entry.path)
            process = subprocess.Popen(["xdg-open", entry.path])
            ret = process.wait()
            if ret != 0:
                print("Viewer exited with status: %d" % ret)
            easy_widgets.Application.exit()
        def show_papers(btn, params):
            field = params[0]
            category = params[1]
            paper_menu = easy_widgets.Menu("Papers")
            for entry in entries:
                if entry.field == field.name and entry.category == category:
                    paper_menu.addOption(entry.title, open_paper, params=[entry])
            paper_menu.addOption("Back", show_categories, params=[field])
            paper_menu.show()
        def show_categories(btn, params):
            field: Field = params[0]
            category_menu = easy_widgets.Menu("Categories")
            for category in field.categories:
                category_menu.addOption(category, show_papers, params=[field, category])
            category_menu.addOption("Quit", lambda b, p: easy_widgets.Application.exit())
            category_menu.show()
        for field in fields:
            field_menu.addOption(field.name, show_categories, params=[field] )
        field_menu.addOption("Quit", lambda b, p: easy_widgets.Application.exit())
        field_menu.show()
        easy_widgets.Application.run()

