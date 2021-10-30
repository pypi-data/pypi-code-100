import json
import logging
import os

import ndjson
from jschon import JSON, JSONSchema, create_catalog

logger = logging.getLogger(__name__)

create_catalog("2020-12", default=True)


class LoadError(Exception):
    pass


class Format(object):
    def __init__(self):
        self.d = f"{os.path.dirname(__file__)}/data"
        self.schema = None

    def load(self, filename):
        return json.load(open(filename))

    def save(self, filename, data):
        json.dump(data, open(filename, "w"))

    def validate(self, data):
        j = JSON(data)
        r = self.schema.evaluate(j)
        if r.valid:
            return True
        logger.error(r.output("detailed"))
        raise LoadError(j.path)


class FormatCollection(Format):
    def load(self, filename, create_from_json):
        format = self.format()
        count = 0
        with open(filename) as f:
            for j in ndjson.reader(f):
                format.validate(j)
                create_from_json(j)
                count += 1
        return count

    def save(self, filename, data):
        count = 0
        with open(filename, "w") as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for i in data:
                writer.writerow(i.to_json())
                count += 1
        return count


class FormatProject(Format):
    def __init__(self):
        super().__init__()
        self.schema = JSONSchema.loadf(f"{self.d}/project.json")


class FormatIssue(Format):
    def __init__(self):
        super().__init__()
        JSONSchema.loadf(f"{self.d}/comment.json")
        self.schema = JSONSchema.loadf(f"{self.d}/issue.json")


class FormatIssues(FormatCollection):
    @property
    def format(self):
        return FormatIssue


class FormatUser(Format):
    def __init__(self):
        super().__init__()
        self.schema = JSONSchema.loadf(f"{self.d}/user.json")


class FormatUsers(FormatCollection):
    @property
    def format(self):
        return FormatUser


class FormatIdentities(Format):
    def __init__(self):
        super().__init__()
        self.schema = JSONSchema.loadf(f"{self.d}/identities.json")


class FormatFederation(Format):
    def __init__(self):
        super().__init__()
        self.schema = JSONSchema.loadf(f"{self.d}/federation.json")
