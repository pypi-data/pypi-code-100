import re
import sys

from .TournamentParticipant import TournamentParticipant
from .TournamentMatch import TournamentMatch

import pandas as pd

CHALLONGE_URL = "https://api.challonge.com/v1/tournaments/"

class Tournament:
    def __init__(self, source, meta, participants=None, matches=None, to_dataframe=True):
        # meta fields
        self.url = None
        self.tournament_id = None
        self.tournament_name = None
        self.description = None
        self.tournament_type = None
        self.started_at = None
        self.completed_at = None
        self.created_at = None
        self.state = None
        self.game_name = None
        self.participants_count = None
        self.teams = None
        self.start_at = None

        # participants and matches
        self.participants = []
        self.matches = []

        # challonge branch
        if source.startswith("c"):
            try:
                # checks for error in JSON download
                meta = meta["tournament"]
            except KeyError:
                print("TournamentAPI: Something went wrong, please check your URL and try again.")
                sys.exit(1)

            # proceeds to tournament construction
            self.build_challonge_tournament(meta, participants, matches, to_dataframe)  

        # smashgg branch
        elif source.startswith("s"):
            pass

    def tournament(self, url, subdomain=False):
        if "challonge" in url:
            return self.fetch_challonge_tournament(url, subdomain, self.challonge_auth)
        elif "smash.gg" in url:
            return self.fetch_smashgg_tournament(url)
        else:
            print("TournamentAPI: invalid URL.")

    def fetch_challonge_tournament(self, url, subdomain, challonge_auth):
        # TODO: finding a regex to replace the subdomain parameter
        if subdomain == False:
            # extracting id from url
            url_params = re.search(r'https://challonge.com/(.*)', url)
            groups = url_params.groups()

            # prepares data urls
            tournament_url = CHALLONGE_URL + f"{groups[0]}.json"
            participants_url = CHALLONGE_URL + f"{groups[0]}/participants.json"
            matches_url = CHALLONGE_URL + f"{groups[0]}/matches.json"
        else:
            # extracting id and subdomain from url
            url_params = re.search(r'https://(.*).challonge.com/(.*)', url)
            groups = url_params.groups()

            # prepares data urls
            tournament_url = CHALLONGE_URL + f"{groups[0]}-{groups[1]}.json"
            participants_url = CHALLONGE_URL + f"{groups[0]}-{groups[1]}/participants.json"
            matches_url = CHALLONGE_URL + f"{groups[0]}-{groups[1]}/matches.json"

        # downloads data from Challonge
        try:
            meta_data = self.fetch_raw_data(tournament_url, challonge_auth)
            participants_data = self.fetch_raw_data(participants_url, challonge_auth)
            matches_data = self.fetch_raw_data(matches_url, challonge_auth)
        except TypeError:
            print("TournamentAPI: Challonge API key is not set.")
            sys.exit(1)

        # returns Tournament object after processing data from Challonge
        return Tournament("c", meta_data, participants_data, matches_data)

    def fetch_smashgg_tournament(self, url):
        pass

    def build_challonge_tournament(self, meta, participants, matches, to_dataframe):
        self.url = meta["full_challonge_url"]
        self.tournament_id = meta["id"]
        self.tournament_name = meta["name"]
        self.description = meta["description"]
        self.tournament_type = meta["tournament_type"]
        self.started_at = meta["started_at"]
        self.completed_at = meta["completed_at"]
        self.created_at = meta["created_at"]
        self.state = meta["state"]
        self.game_name = meta["game_name"]
        self.participants_count = meta["participants_count"]
        self.teams = meta["teams"]
        self.start_at = meta["start_at"]

        meta_fields = [
            "url", "id", "name", "description", "tournament_type", 
            "started_at", "completed_at", "created_at", "state", 
            "game_name", "participants_count", "teams", "start_at"
        ]

        # retrieves meta data from json file
        self.meta = {}
        for f in meta_fields:
            self.meta[f] = meta[f]

        # retrieves participants, creates and appends object for each
        for p in participants:
            self.participants.append(TournamentParticipant(p["participant"]))

        # retrieves matches, creates and appends object for each
        for m in matches:
            self.matches.append(TournamentMatch(m["match"]))
            
        # transforms each collection into a DataFrame, unless disabled
        if to_dataframe:
            self.meta = self.data_to_pandas(self.meta)
            self.matches = self.data_to_pandas(self.matches)
            self.participants = self.data_to_pandas(self.participants)

            # enhances matches dataframe by adding nicknames
            nicknames = dict(self.participants[["id", "display_name"]].values)
            self.matches["player1_nickname"] = self.matches["player1_id"].map(nicknames)
            self.matches["player2_nickname"] = self.matches["player2_id"].map(nicknames)
            self.matches["winner_nickname"] = self.matches["winner_id"].map(nicknames)
            self.matches["loser_nickname"] = self.matches["loser_id"].map(nicknames)

            # TODO: add per-player scores
            # matches["player1_score"] = 
            # matches["player2_score"] = 

    def __str__(self) -> str:
        return (
            f"url: {self.url}, id: {self.tournament_id}, name: {self.tournament_name}, " 
            f"tournament_type: {self.tournament_type}, state: {self.state}, "
            f"game_name: {self.game_name}, participants_count: {self.participants_count}, "
            f"teams: {self.teams}"
        )

    def __repr__(self) -> str:
        return f"<Tournament id: {self.tournament_id}>"

    def data_to_pandas(self, data):
        # handles participants and matches
        if isinstance(data, list): 
            df = pd.DataFrame(columns=vars(data[0]))

            for p in data:
                df = df.append(pd.Series(vars(p)), ignore_index=True)

            return df
        # handles meta data
        elif isinstance(data, dict):
            df = pd.DataFrame([pd.Series(data)])
            return df
