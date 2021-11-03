
import io
import os 
from collections import namedtuple
import json 

DatabaseEntry = namedtuple("DatabaseEntry", [
    "title",
    "authors",
    "publicationYear",
    "path",
    "url",
    "status",
    "field", 
    "category"
])

class Database:
    def __init__(self, location = os.path.join(os.environ["HOME"], ".papertrack/metadata.json")):
        self.location = location
    
    def save(self, entry: DatabaseEntry):
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        data = [] 
        try:
            f = open(self.location, "r")
            data = json.loads(f.read())
            f.close()
        except FileNotFoundError:
            data = []
        data.append(dict(
            title = entry.title,
            authors = entry.authors,
            publicationYear = entry.publicationYear,
            path = entry.path,
            url = entry.url,
            status = entry.status,
            field = entry.field,
            category = entry.category
        ))
        with open(self.location, "w") as f:
            f.write(json.dumps(data))
    def list(self):
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        try:
            with open(self.location) as f:
                try:
                    data = json.loads(f.read())
                except io.UnsupportedOperation:
                    data = []
                finally:
                    return list(DatabaseEntry(
                        title = x["title"],
                        authors = x["authors"],
                        publicationYear = x["publicationYear"],
                        path = x["path"],
                        url = x["url"],
                        status = x["status"],
                        field = x["field"],
                        category = x["category"]
                    ) for x in data)
        except FileNotFoundError:
            return []