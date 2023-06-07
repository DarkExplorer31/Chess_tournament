"""Player Model"""
import os
import json
import re

SEARCHING_IDENT = r"\((.*)\)"


class Player:
    """Define player as an object:
    A player has a name, a firstname, a birthday and a national identifiant"""

    PLAYER_DATA = "data/player/player_data.json"

    def __init__(self, name, firstname, birthday, identifiant, score=0):
        self.name = name
        self.firstname = firstname
        self.birthday = birthday
        self.identifiant = identifiant
        self.score = score

    def __repr__(self):
        """Define the representation for a player object"""
        representation = (
            "Player(name='"
            + self.name
            + "', firstname='"
            + self.firstname
            + "', birthday='"
            + self.birthday
            + "', identifiant='"
            + self.identifiant
            + "')"
        )
        return representation

    def __str__(self):
        return "Le joueur {} (score: {})".format(self.name, self.score)

    def __lt__(self, other):
        return self.score < other.score

    def to_dict(self):
        return {
            "name": self.name,
            "firstname": self.firstname,
            "birthday": self.birthday,
            "national_identification": self.identifiant,
        }

    def save_new_player(self):
        new_player = self.to_dict()
        path_control = os.path.exists(self.PLAYER_DATA)
        if path_control is True:
            with open(self.PLAYER_DATA, "r") as file:
                all_players = json.load(file)
                all_players["players"].append(new_player)
        else:
            all_players = {"players": [new_player]}
        with open(self.PLAYER_DATA, "w") as file:
            json.dump(all_players, file)

    @classmethod
    def identifiant_exists(cls, identifiant):
        """Return existing identifiant or None if not exist"""
        players_saved = cls.get_players_saved()
        for player in players_saved:
            if identifiant == player.identifiant:
                return identifiant
        return None

    @classmethod
    def get_players_saved(cls):
        all_players_saved = {}
        players_saved = []
        path_control = os.path.exists(cls.PLAYER_DATA)
        if path_control is True:
            with open(cls.PLAYER_DATA, "r") as file:
                all_players_saved = json.load(file)
            for player in all_players_saved["players"]:
                name = player["name"]
                firstname = player["firstname"]
                birthday = player["birthday"]
                identifiant = player["national_identification"]
                players_to_return = cls(name, firstname, birthday, identifiant)
                players_saved.append(players_to_return)
            return players_saved
        else:
            return players_saved

    @classmethod
    def get_player_by_ident(cls, player_ident):
        path_control = os.path.exists(cls.PLAYER_DATA)
        if path_control is True:
            with open(cls.PLAYER_DATA, "r") as file:
                all_players_saved = json.load(file)
            for player in all_players_saved["players"]:
                ident = player["national_identification"]
                if player_ident == ident:
                    name = player["name"] + " (" + ident + ")"
                    firstname = player["firstname"]
                    birthday = player["birthday"]
                    player_to_return = cls(name, firstname, birthday, ident)
        return player_to_return

    @classmethod
    def restore_player(cls, player):
        identifiant = re.search(SEARCHING_IDENT, player)
        identifiant = identifiant.group(1)
        all_players = cls.get_players_saved()
        for player in all_players:
            if player.identifiant == identifiant:
                player_to_return = player
                player_to_return.name = player.name + " (" + identifiant + ")"
                break
        return player_to_return
