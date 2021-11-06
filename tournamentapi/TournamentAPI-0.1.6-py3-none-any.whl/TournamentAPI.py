#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import sys
import requests

import Tournament

CHALLONGE_URL = "https://api.challonge.com/v1/tournaments/"

class TournamentAPI:
    def __init__(self, challonge_auth=None, smashgg_auth=None):
        try:
            self.challonge_auth = challonge_auth
            self.smashgg_key = smashgg_auth
        except TypeError:
            pass

    def tournament(self, url, subdomain=False):
        if "challonge" in url:
            return self.fetch_challonge_tournament(url, subdomain, self.challonge_auth)
        elif "smash.gg" in url:
            return self.fetch_smashgg_tournament(url)
        else:
            print("TournamentAPI: invalid URL.")

    def fetch_challonge_tournament(self, url, subdomain, challonge_auth):
        if subdomain == False:
            url_params = re.search(r'https://challonge.com/(.*)', url)
            groups = url_params.groups()

            tournament_url = CHALLONGE_URL + f"{groups[0]}.json"
            participants_url = CHALLONGE_URL + f"{groups[0]}/participants.json"
            matches_url = CHALLONGE_URL + f"{groups[0]}/matches.json"

            try:
                meta_data = self.fetch_raw_data(tournament_url, challonge_auth)
                participants_data = self.fetch_raw_data(participants_url, challonge_auth)
                matches_data = self.fetch_raw_data(matches_url, challonge_auth)
            except TypeError:
                print("TournamentAPI: Challonge API key is not set.")
                sys.exit(1)
        else:
            url_params = re.search(r'https://(.*).challonge.com/(.*)', url)
            groups = url_params.groups()

            tournament_url = CHALLONGE_URL + f"{groups[0]}-{groups[1]}.json"
            participants_url = CHALLONGE_URL + f"{groups[0]}-{groups[1]}/participants.json"
            matches_url = CHALLONGE_URL + f"{groups[0]}-{groups[1]}/matches.json"

            try:
                meta_data = self.fetch_raw_data(tournament_url, challonge_auth)
                participants_data = self.fetch_raw_data(participants_url, challonge_auth)
                matches_data = self.fetch_raw_data(matches_url, challonge_auth)
            except TypeError:
                print("TournamentAPI: Challonge API key is not set.")
                sys.exit(1)

        return Tournament(
            "challonge", 
            meta_data, 
            participants_data, 
            matches_data
        )

    def fetch_smashgg_tournament(self, url):
        pass

    def fetch_raw_data(self, api_url, api_credentials):
        response = requests.get(
            api_url, 
            auth=(api_credentials["nickname"], api_credentials["api_key"]), 
            headers={'User-Agent': ''}
        )

        raw_data = response.json()

        return raw_data
