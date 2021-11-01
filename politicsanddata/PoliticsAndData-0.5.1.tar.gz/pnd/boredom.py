from __future__ import annotations

import datetime
import json
import os

import requests
import zipfile
import io
import csv
import time
import pytz
import re


time.timezone = pytz.UTC


class Boredom:

    def __init__(self, thing_type, fs="filespace"):
        self.type = thing_type
        self.file = f"{fs}/{thing_type}.json"
        self.filespace = fs
        self.url = f"https://politicsandwar.com/data/{thing_type}"
        self.cache = {"timeline": {}, "latest": None}
        self.load()
        self.collected = {}
        self.length = None
        self.total = tuple()
        self.match = tuple()
        self.if_then_total = {}

    def init_db(self, reset=False):
        try:
            os.mkdir(self.filespace)
        except FileExistsError:
            pass
        try:
            with open(self.file, "x") as f:
                f.write('{"timeline": {}, "latest": null}')
        except FileExistsError:
            if not reset:
                raise

    def date_conv(self, date: str | float) -> float | str:
        if type(date) == str:
            return time.mktime(time.strptime(date, "%Y-%m-%d"))
        elif type(date) == float:
            return time.strftime("%Y-%m-%d", datetime.datetime.fromtimestamp(date).timetuple())
        else:
            raise TypeError

    def load(self):
        try:
            with open(self.file) as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.init_db()
            self.load()

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.cache, f)

    def day(self, date: str) -> list[dict]:
        with requests.get(f"{self.url}/{self.type}-{date}.csv.zip") as dl:
            opened = zipfile.ZipFile(io.BytesIO(dl.content))
            with io.TextIOWrapper(opened.open(f"{self.type}-{date}.csv"), encoding="utf-8-sig") as f:
                data = csv.DictReader(f)
                out = []
                for line in data:
                    out.append(line)
            return out

    def get_day(self, date: str, ignore=False):
        data = self.day(date)
        self.spec_collection(data, ignore)
        if "error" not in self.collected.keys():
            self.cache[self.date_conv(date)] = self.collected
        self.save()

    def latest(self):
        self.load()
        return self.cache

    def get_dates(self):
        with requests.get(self.url) as page:
            text = page.text
        times = list(set(re.findall("\\d\\d\\d\\d-\\d\\d-\\d\\d.csv.zip", text)))
        for t in range(len(times)):
            times[t] = self.date_conv(times[t].strip(".csv.zip"))
        times.sort()
        offset = 0
        for i in range(1, len(times)):
            if times[i-offset]-times[i-1-offset] != 86400:
                del times[i-1-offset]
                offset += 1
        for t in range(len(times)):
            times[t] = self.date_conv(times[t])
        return times

    def data_sample(self, date: str, th=0):
        day = self.day(date)[th]
        out = []
        for e in enumerate(day.items()):
            i = e[0]
            key, value = e[1]
            if type(key) == str:
                out.append(f"{str(i).zfill(2)}|{key.rjust(48)} | {value}")
        return "\n".join(out)

    def run(self, force_new=False, ignore=False):
        todo = self.get_dates()
        if self.cache["latest"] is None or force_new:
            day = 0
        else:
            day = todo.index(self.date_conv(self.cache["latest"])) + 1
        while True:
            if day == len(todo):
                print("Completed!")
                return

            self.get_day(todo[day], ignore)
            self.cache["latest"] = self.date_conv(todo[day])
            self.save()
            print(f"{self.type.rjust(10)} - {todo[day]} Complete")

            day += 1

    def spec_collection(self, data: list[dict], ignore=False):
        self.collected = {}

        if self.length is not None:
            self.collected[self.length] = len(data)

        for item in self.total+list(self.if_then_total.keys()):
            self.collected[item[0]] = item[2]()

        for item in self.match:
            self.collected[item[0]] = 0

        try:
            for line in data:
                extra = []
                for condition, extras in if_then_total:
                    if type(condition[1]) == int and list(line.values())[condition[1]] == item[2]:
                        extra += extras
                    elif type(condition[1]) == str and self.collected[item[0]] += int(line[condition[1]] == condition[2]):
                        extra += extras
                for item in self.total+extra:
                    if type(item[1]) == int:
                        self.collected[item[0]] += item[2](list(line.values())[item[1]])
                    elif type(item[1]) == str:
                        self.collected[item[0]] += item[2](line[item[1]])
                    else:
                        raise TypeError
                for item in self.match:
                    if type(item[1]) == int:
                        self.collected[item[0]] += int(list(line.values())[item[1]] == item[2])
                    elif type(item[1]) == str:
                        self.collected[item[0]] += int(line[item[1]] == item[2])
                    else:
                        raise TypeError
        except KeyError:
            if ignore:
                self.collected = {"error": True}
            else:
                raise
