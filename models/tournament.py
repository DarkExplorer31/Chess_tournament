"""Define Tournament"""
import os
import json
import re
from datetime import datetime

TOURNAMENT_FILES = "data/tournaments"
TOURNAMENT_FILES_NAME = r"^data/tournaments/[A-Za-z0-9]{0,99}.json$"


class Tournament:
    """Define a tournament as an object,
    has a name, the place where it takes place,
    and a number total of round, by default on four"""

    def __init__(
        self,
        name,
        place,
        players,
        nb_round=4,
        round=1,
        round_list=None,
        ranking=None,
        save=True,
        comment=None,
        finished=False,
    ):
        self.name = name
        self.place = place
        self.players = players
        self.nb_round = nb_round
        self._round = round
        self.round_list = round_list
        self._ranking = ranking
        self.comment = comment
        self._finished = finished
        self.starting_date = None
        self.ending_date = None
        if save:
            self.save_tournament()

    def __repr__(self):
        """Define the representation of a tournament object"""
        player_list = []
        if self.players:
            for player in self.players:
                player_list.append(player.name)
        representation = (
            "Tournament(name='"
            + self.name
            + "', place='"
            + self.place
            + "', players={}, nb_round='".format(player_list)
            + str(self.nb_round)
            + "', round='"
            + str(self.round)
            + "', round_list={})".format(self.round_list)
        )
        return representation

    def to_dict(self):
        return {
            "name_of_tournament": self.name,
            "place": self.place,
            "round": self._round,
            "tournament_players": [p.identifiant for p in self.players],
            "total_of_round": self.nb_round,
            "ranking": [p.name for p in self._ranking],
            "comment": self.comment,
        }

    def save_tournament(self):
        new_tournament = self.to_dict()
        tournament_name = self.name
        all_information = new_tournament
        if not self.starting_date:
            self.starting_date = datetime.now()
            all_information.update({"starting_date": str(self.starting_date)})
        else:
            all_information["starting_date"] = str(self.starting_date)
        if self.ending_date:
            all_information.update({"ending_date": str(self.ending_date)})
        else:
            all_information.update({"ending_date": None})
        tournament_file = TOURNAMENT_FILES + "/" + tournament_name + ".json"
        tournament_file = tournament_file.replace(" ", "")
        with open(tournament_file, "w") as file:
            json.dump(all_information, file)

    @classmethod
    def control_finished(cls, tournament):
        path_control = os.path.exists(tournament)
        if path_control is True:
            with open(tournament, "r") as file:
                all_infos = json.load(file)
                if all_infos["ending_date"]:
                    return tournament
                else:
                    return None
        else:
            return None

    @classmethod
    def get_all_tournament_names(cls, with_finished=False):
        file_list = []
        for root, _, files in os.walk(TOURNAMENT_FILES):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path.replace("\\", "/")
                if re.match(TOURNAMENT_FILES_NAME, file_path):
                    file_path = file_path.replace(TOURNAMENT_FILES + "/", "")
                    file_path = file_path.replace(".json", "")
                    file_list.append(file_path)
        final_list = []
        if with_finished:
            for tournament in file_list:
                tournament_control = cls.control_finished(tournament)
                if not tournament_control:
                    final_list.append(tournament)
            return final_list
        else:
            return file_list

    @classmethod
    def control_name_exist(cls, tournament_name):
        tournaments_saved = cls.get_all_tournament_names()
        if tournament_name in tournaments_saved:
            return True
        else:
            return False

    @classmethod
    def get_tournament_info(cls, name):
        tournament_file = TOURNAMENT_FILES + "/" + name + ".json"
        path_control = os.path.exists(tournament_file)
        if path_control is True:
            with open(tournament_file, "r") as file:
                all_infos = json.load(file)
            name = all_infos["name_of_tournament"]
            place = all_infos["place"]
            players = all_infos["tournament_players"]
            nb_round = all_infos["total_of_round"]
            ranking = all_infos["ranking"]
            round = all_infos["round"]
            round_list = []
            saved_tournament = cls(
                name=name,
                place=place,
                players=players,
                nb_round=nb_round,
                round=round,
                round_list=round_list,
                ranking=ranking,
                save=False,
            )
            saved_tournament.starting_date = all_infos["starting_date"]
            if all_infos["ending_date"]:
                saved_tournament.ending_date = all_infos["ending_date"]
                saved_tournament.comment = all_infos["comment"]
        else:
            return None
        return saved_tournament

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, value):
        self._round = value
        self.save_tournament()

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = value
        self.save_tournament()

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value
        if self._finished:
            self.ending_date = datetime.now()
        self.save_tournament()
