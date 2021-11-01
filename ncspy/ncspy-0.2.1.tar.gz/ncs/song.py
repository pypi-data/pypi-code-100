import typing
from datetime import datetime


class Song:
    def __init__(self, **data):
        if not data:
            raise LookupError("No data was given.")

        self.data = data

    # variables, adding them as properties so they can't be changed
    @property
    def title(self) -> str:
        return self.data["title"]

    @property
    def name(self) -> str:
        return self.title

    @property
    def artists(self) -> typing.List[str]:
        return self.data["artists"]

    @property
    def versions(self) -> typing.List[str]:
        return self.data["versions"]

    @property
    def release_date(self) -> datetime:
        ret = self.data["release_date"]

        return datetime.strptime(ret, "%d %b %Y")

    @property
    def artwork(self) -> str:
        return self.data["artwork"]

    def __repr__(self):
        return f'<{type(self).__name__} title="{self.title}">'


class SearchResults:
    def __init__(self, pages: int, items: typing.List[dict]):
        self.pages = pages
        self.items: typing.List[Song] = []
        for item in items:
            self.items.append(Song(**item))

    def __repr__(self):
        return f"<{type(self).__name__} items={len(self.items)} pages={self.pages}>"
