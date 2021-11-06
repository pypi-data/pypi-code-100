#!/usr/bin/python
#-*- coding: utf-8 -*-

class TournamentParticipant:
    def __init__(self, data):
        self.id = data["id"]
        self.tournament_id = data["tournament_id"]
        self.nickname = data["name"]
        self.challonge_username = data["challonge_username"]
        self.username = data["username"]
        self.display_name = data["display_name"]
        self.seed = data["seed"]
        self.placement = data["final_rank"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.checked_in_at = data["checked_in_at"]
        self.checked_in = data["checked_in"]
        self.profile_picture = data["attached_participatable_portrait_url"]

    def __str__(self) -> str:
        return (
            f"id: {self.id}, tournament_id: {self.tournament_id}, nickname: {self.nickname}, "
            f"challonge_username: {self.challonge_username}, username: {self.username}, "
            f"display_name: {self.display_name}, seed: {self.seed}, final_rank: {self.final_rank}, "
            f"created_at: {self.created_at}, updated_at: {self.updated_at}, checked_in_at: {self.checked_in_at}, " 
            f"checked_in: {self.checked_in}, profile_picture: {self.profile_picture}"
        )
    
    def __repr__(self) -> str:
        return self.challonge_username
