import re
from abc import ABC
from datetime import date
from typing import List
from urllib import request
from babel.dates import format_date
from bs4 import BeautifulSoup
from .event import Event


class Source(ABC):
    def __init__(self) -> None:
        self.today = date.today()

    def parse(self) -> List[Event]:
        pass  # interface method

    @staticmethod
    def _get_soup(url: str) -> BeautifulSoup:
        # Validate URL before opening it
        if url.lower().startswith("https"):
            req = request.Request(url)
        else:
            raise ValueError("Not going to get resource from unsecure URL")

        with request.urlopen(req) as body:  # skipcq: BAN-B310
            return BeautifulSoup(body, "html.parser")


class Wikipedia(Source):
    URL_PREFIX = "https://it.wikipedia.org/wiki"

    @staticmethod
    def _sanitize(text: str) -> str:
        return re.sub(r"\[\d+]", "", text)

    def _to_event(self, year: str, title: str) -> Event:
        title = self._sanitize(title)

        if "a.C." in year:
            year = int(re.sub(r"a\.C\.", "", year))
            return Event(year=year, title=title, bc=True)

        return Event(year=int(year), title=title)

    def parse(self) -> List[Event]:
        day = format_date(self.today, "d_MMMM", locale="it")
        url = f"{self.URL_PREFIX}/{day}"

        soup = self._get_soup(url)

        event_title = soup.find(id="Eventi").parent
        event_list = event_title.find_next_sibling().find_all("li", recursive=False)

        res = []

        for event in event_list:

            if subevents := event.find("ul"):
                # Multiline event
                year = event.a.text
                for subevent in subevents.find_all("li"):
                    res.append(self._to_event(year, subevent.text))
            else:
                # Simple event
                year, title = re.split("-|–", event.text, maxsplit=1)
                res.append(self._to_event(year, title))

        return res


class AccaddeOggi(Source):
    URL = "https://www.accaddeoggi.it"

    @staticmethod
    def _to_event(year: str, title: str) -> Event:
        return Event(year=int(year.strip()), title=title.strip())

    def parse(self) -> List[Event]:
        soup = self._get_soup(self.URL)

        stop_tag = soup.find(text="Sono nati oggi")

        event_list = stop_tag.find_all_previous("div", class_="entry")

        res = []
        for event in event_list:
            text = event.find("a").text
            year, title = re.split(" - | – ", text, maxsplit=1)
            res.append(self._to_event(year, title))

        res.reverse()

        return res
