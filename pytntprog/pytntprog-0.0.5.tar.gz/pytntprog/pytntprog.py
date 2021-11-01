"""
pytntprog use case
"""

import argparse
import sys
import requests
import urllib.request
import xml.etree.ElementTree as ET
import os
import time
from pytntprog.args import compute_args
import datetime
import tempfile
import colorama
from termcolor import colored

def find():
    alll = compute_args().all
    idd = compute_args().id
    ffilter = compute_args().filter
    ccurrent = compute_args().current
    nocolor = compute_args().nocolor

    colorama.init()

    url = "https://xmltv.ch/xmltv/xmltv-tnt.xml"
    if compute_args().nocache or not os.path.exists(tempfile.gettempdir()+"/tnt.xml") or (
        time.time() - os.stat(tempfile.gettempdir()+"/tnt.xml").st_mtime > 86400
    ):
        print("download the distant xml file...")
        urllib.request.urlretrieve(url, tempfile.gettempdir()+"/tnt.xml")
        print("download is finished")
    tree = ET.parse(tempfile.gettempdir()+"/tnt.xml")
    root = tree.getroot()
    T = []
    i = 1
    for neighbor in root.iter("programme"):
        start = neighbor.get("start")
        stop = neighbor.get("stop")
        channel = neighbor.get("channel")
        for c in root.iter("channel"):
            if c.get("id") == channel:
                channel = c.find("display-name").text
                break
        title = neighbor.find("title").text
        subtitle = ""
        if neighbor.find("sub-title") != None:
            subtitle = neighbor.find("sub-title").text
        desc = ""
        if neighbor.find("desc") != None:
            desc = neighbor.find("desc").text
        category = ""
        if neighbor.find("category") != None:
            category = neighbor.find("category").text
        date = ""
        if neighbor.find("date") != None:
            date = neighbor.find("date").text
        episode = ""
        if neighbor.find("episode-num") != None:
            episode = neighbor.find("episode-num").text
        age = ""
        if neighbor.find("rating") != None:
            age = neighbor.find("rating").find("value").text
        T.append(
            {
                "time": start,
                "time_end": stop,
                "day": start[0:8],
                "start": start[8:10] + ":" + start[10:12],
                "end": stop[8:10] + ":" + stop[10:12],
                "channel": channel,
                "title": title,
                "id": str(i).zfill(5),
                "subtitle": subtitle,
                "description": desc,
                "category": category,
                "age": age,
                "episode": episode,
                "date": date,
            }
        )

        i = i + 1
    T.sort(key=lambda x: x["time"])
    
    if idd:
        for w in T:
            if w["id"] == idd.zfill(5):
                print(
                    "titre       : "
                    + w["title"]
                    + " "
                    + w["subtitle"]
                )
                print("chaine      : " + w["channel"])
                print("jour        : " + w["day"])
                print("heure debut : " + w["start"])
                print("heure fin   : " + w["end"])
                print("resume      : " + w["description"])
                print("episode     : " + w["episode"])
                print("date        : " + w["date"])
                print("categorie   : " + w["category"])
                print("age         : " + w["age"])
                break
    else:
        for w in T:

            if alll:
                resume = (
                    my_colored("["+ w["id"]+ "] ","red",nocolor)
                    + " "
                    + w["day"]
                    + " "
                    + my_colored(w["start"],"gree",nocolor)
                    + " "
                    + my_colored(w["channel"],"yellow",nocolor)
                    + " "
                    + my_colored(w["title"]
                    + " "
                    + w["subtitle"],"cyan",nocolor)
                )
            else:
                resume = (
                    my_colored("["+ w["id"] + "] ","red",nocolor)
                    + " "
                    + my_colored(w["start"],"green",nocolor)
                    + " "
                    + my_colored(w["channel"],"yellow",nocolor)
                    + " "
                    + my_colored(w["title"]
                    + " "
                    + w["subtitle"],"cyan",nocolor)
                )
            trouve = False
            
            if not ffilter:
                trouve = True
            else:
                trouve = True
                for search in ffilter:
                    if search.lower() not in resume.lower():
                        trouve = False
                        break
            
            if ccurrent:
                until = datetime.datetime(int(w["time"][0:4]),int(w["time"][4:6]),int(w["time"][6:8]),int(w["time"][8:10]),int(w["time"][10:12]),0).timestamp()-time.time()
                since = datetime.datetime(int(w["time_end"][0:4]),int(w["time_end"][4:6]),int(w["time_end"][6:8]),int(w["time_end"][8:10]),int(w["time_end"][10:12]),0).timestamp()-time.time()
                if (until>3600) or (since < 0):
                    trouve = False
                if (until>3600):
                    break   
            if alll:
                if trouve:
                    print(resume)
            else:
                if w["day"] == datetime.date.today().strftime(
                    "%Y%m%d") and trouve:
                    print(resume)
                if w["day"] > datetime.date.today().strftime(
                    "%Y%m%d"
                ):
                    break

def my_colored(message,color,nocolor):
    if nocolor:
        return message
    return colored(message,color)   