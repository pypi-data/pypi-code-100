#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 15:22:10 2021

@author: siddharthvenkatesh

This script aims to construct a class with  methods for scraping and storing data from the 18xx.games api for 1830 games.
"""

import requests
import bs4
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


class Scraper1830:
    def __init__(self, ID):
        # ID is a string representing the game ID on 18xx.games

        # General api url for website
        api_url = "https://18xx.games/api/game/"
        # Game ID number
        self.id = ID
        # Link to the API for the game
        self.api = api_url + self.id
        # Json file consisting of the players, results and game actions.
        self.log = requests.get(self.api).json()

        # URL for finished game page
        self.url = "https://18xx.games/game/" + self.id

        # Game Title
        self.title = self.log["title"]

        # Raise error if game id belongs to a game not in scope of scraper
        if self.title != "1830":
            raise ValueError(
                "Game ID must belong to a finished 1830 game, the scraper is not designed for other games or unfinished games."
            )

        # List of the privates in increasing order of base price.
        self.privates = ["SV", "CS", "DH", "MH", "CA", "BO"]

        # List of players in initial turn order
        self.players = self.log["players"]
        self.player_count = len(self.log["players"])

        # Attribute to record the player score history
        self.player_history = None

    def get_player_dict(self):
        """
        This function takes a scraper, parses the log and returns a dictionary whose 
         keys are player id numbers as ints and whose values are player name strings.

        """

        players = dict([d.values() for d in self.players])

        return players

    def get_initial_player_order(self):
        """
        This functions takes a scraper and returns a list of player ids ordered based on the initial turn order of the game.

        """
        order_list = []
        for i in range(0, self.player_count):
            order_list.append(self.get_player_dict()[self.log["actions"][i]["user"]])

        return order_list

    def get_private_auction(self):
        """
        This function takes a scraper and returns a dictionary whose keys are the 
         private companies in the game and whose values are tuples (player name string, int representing price paid).


        """

        prices = {}

        # The next block of code iterates through the 'actions' field of the game log. Any time it encounters a 'bid' action
        # representing a bid on a private company, it updates that company's price with the new bid and updates the person
        # winning the bid . Since the last 'bid' action records the final purchase of the private, the tuple at the end
        # records the winner and the price paid.

        for action in self.log["actions"]:
            if action["type"] != "bid":
                continue
            prices[action["company"]] = (
                self.get_player_dict()[action["entity"]],
                action["price"],
            )

        return prices

    def get_remaining_cash(self):
        """
        This function uses the get_private_auction function to compute the cash remaining for each player after the auction. 
         It returns a dictionary with keys = player name strings and values = cash remaining as integer.

        """
        cash = {}
        # Initialize the cash dictionary.
        for player in self.get_initial_player_order():
            cash[player] = 2400 / self.player_count
        # Iterate over the get_private_auction dictionary to compute remaining cash.
        for entry in self.get_private_auction().values():
            cash[entry[0]] = cash[entry[0]] - entry[1]

        return cash

    def get_priority(self):
        """
        This function takes a scraper and returns the player name string of the player who had priority in stock round 1. 

        """

        action_counter = 0
        for action in self.log["actions"]:

            if not (action["type"] == "par" and action["corporation"] == "B&O"):
                action_counter += 1
                continue
            else:
                action_counter += 1
                break

        priority_id = self.log["actions"][action_counter]["entity"]

        return self.get_player_dict()[priority_id]

    def get_result(self):
        """
        This funtion takes a scraper and returns a dictionary whose keys are player ids and
         returns a dictionary whose keys are player name strings and whose values are their final scores as ints.

        """

        result = self.log["result"]

        return result

    def get_player_history(self):
        """
         This function takes a scraper and returns a dictionary with keys strings representing player names and round numbers and values
          representing the player names and their scores at the end of each round.

         """
        if self.player_history:
            return self.player_history
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver import Firefox
        from selenium.webdriver.firefox.options import Options

        def start_firefox_driver():
            """
             This function loads a headless copy of Firefox in Python. It is needed to load the javascript on a webpage to scrape 
              html output.
             """

            options = Options()
            options.add_argument("-headless")
            firefox = Firefox(options=options)
            return firefox

        def ready(driver):
            """
             Driver is a firefox driver loaded via Selenium. This function tests that a particular table "player_table" has 
             loaded on self.url and returns a boolean (true if the table has loaded and false if not).

             """
            return driver.execute_script(
                "return !!document.querySelector('#player_or_history');"
            )

        print("Firefox Driver Loading:")

        # Initialize driver
        firefox = start_firefox_driver()

        print("Driver loaded, loading game page:")

        # Get the page on self.url
        firefox.get(self.url)
        # Wait till the javascript on the page runs and loads the tables.
        WebDriverWait(firefox, 5).until(ready)
        # Grab the body of the game page
        html_string = firefox.execute_script("return document.body.outerHTML")

        print("Page loaded, parsing html")

        # Use Beautiful Soup to parse the html.
        soup = bs4.BeautifulSoup(html_string, "lxml")

        # Write entries into a dictionary
        dictionary = {}
        # Find the table containing the player names.
        table = soup.select("#player_table")[0]
        # Find the player names and write them to the dictionary
        names = [
            entry.get_text() for entry in table.find_all("th", {"class": "name nowrap"})
        ]
        dictionary["player_order"] = names
        # Find the table containing the player score history
        score_table = soup.select("#player_or_history")[0]
        # Enter the player scores into the dictionary
        for row in score_table.children:
            if isinstance(row, bs4.NavigableString):
                continue
            else:
                key = row.select("th")[0].get_text()
                value = [c.get_text() for c in row.select("td")]
                dictionary[key] = value

        self.player_history = dictionary

        return dictionary

    def player_history_table(self):
        """
         Returns the result from get_player_history as a pandas dataframe with the keys as the row index.

         """
        dictionary = self.get_player_history()

        return pd.DataFrame.from_dict(dictionary, orient="index")

    def plot_player_history(self):
        """
        This function returns a lineplot of the player score history.


        """

        # Styling via seaborn
        sns.set_theme()
        sns.set(rc={"figure.dpi": 300, "savefig.dpi": 300})
        sns.set_style("ticks")

        # Color choices
        colors = [
            "tab:blue",
            "tab:orange",
            "tab:red",
            "tab:purple",
            "tab:pink",
            "tab:gray",
        ]

        # Reverse the player history dataframe so it follows in increasing order of round number.
        full_data = self.player_history_table()
        data = self.player_history_table()[1:]
        data = data[::-1]

        # Cleaning up the data dataframe by converting strings representing scores to integers.
        data = data.applymap(lambda x: int(x.strip("$")))

        # The x-variable are the indices of the dataframe data.
        x = data.index.values

        # Set the size of the plot
        axs = plt.figure(figsize=(15, 15), dpi=1000)

        # We need to plot different y values for each player
        for i in full_data.columns:
            y = data.iloc[:, i]
            plt.plot(x, y, color=colors[i], label=full_data.loc["player_order", i])

        axs.legend()

        plt.savefig(f"1830-{self.id}.png")

        return plt

    # The last method is built to enable easy entry of the game state after the private auction as a row of a pandas dataframe.
    # This will be important for building a dataset and then running a classifier on it.
