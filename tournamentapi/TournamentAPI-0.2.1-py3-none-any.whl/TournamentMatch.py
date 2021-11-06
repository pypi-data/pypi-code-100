#!/usr/bin/python
#-*- coding: utf-8 -*-

class TournamentMatch:
    def __init__(self, data):
        self.id = data["id"]
        self.tournament_id = data["tournament_id"]
        self.state = data["state"]
        self.player1_id = data["player1_id"]
        self.player2_id = data["player2_id"]
        self.winner_id = data["winner_id"]
        self.loser_id = data["loser_id"]
        self.started_at = data["started_at"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.completed_at = data["completed_at"]
        self.identifier = data["identifier"]
        self.round = data["round"]
        self.scores_csv = data["scores_csv"]

    def __str__(self) -> str:
        return (
            f"id: {self.id}, tournament_id:{self.tournament_id}, "
            f"state: {self.state}, p1_id: {self.player1_id}, p2:id {self.player2_id}, "
            f"winner_id: {self.winner_id}, loser_id: {self.loser_id}, started_at: {self.started_at}, "
            f"created_at: {self.created_at}, updated_at: {self.updated_at}, "
            f"completed_at: {self.completed_at}, identifier: {self.identifier}, "
            f"round: {self.round}, scores_csv: {self.scores_csv}"
        )

    def __repr__(self) -> str:
        return self.identifier
