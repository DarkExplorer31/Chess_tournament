"""Round Model"""
import json
import os
import re
from datetime import datetime

TOURNAMENT_FILES = "data/tournaments"


class Round:
    """Define a Round as an object"""

    def __init__(
        self,
        tournament_name,
        round_nb,
        match_list,
        end_of_the_round=False,
    ):
        self.tournament_name = tournament_name
        self.round_nb = round_nb
        self._match_list = match_list
        self._end_of_the_round = end_of_the_round
        self.starting_round = None
        self.ending_round = None
        self.save_round_data()

    def __repr__(self):
        """Define the representation for a round object"""
        representation = (
            "Round(tournament_name='"
            + self.tournament_name
            + "', round_nb='"
            + str(self.round_nb)
            + "', match_list={},".format(self.match_list)
            + "matches_result={})".format(self._match_list)
        )
        return representation

    def __str__(self):
        representation = (
            "Le tour numéro: "
            + str(self.round_nb)
            + "du tournoi: '"
            + self.tournament_name
            + "', les matchs qui le compose sont: {}".format(self.match_list)
        )
        return representation

    def to_dict(self):
        return {
            "tournament_name": self.tournament_name,
            "round_nb": self.round_nb,
            "match_list": self._match_list,
        }

    def save_round_data(self):
        new_round = self.to_dict()
        self.tournament_name = self.tournament_name.replace(" ", "")
        all_information = new_round
        if self.starting_round is None:
            self.starting_round = datetime.now()
            all_information.update({"start": str(self.starting_round)})
        else:
            all_information["start"] = str(self.starting_round)
        if self.ending_round:
            all_information["end"] = str(self.ending_round)
        else:
            all_information.update({"end": None})
        file_name = "{}/{}_round{}.json".format(
            TOURNAMENT_FILES, self.tournament_name, self.round_nb
        )
        with open(file_name, "w") as file:
            json.dump(all_information, file, default=lambda x: x.to_dict())

    @classmethod
    def get_all_round_files(cls, tournament_name):
        round_file = rf"^data/tournaments/{tournament_name}_round[0-9]{{0,99}}.json$"
        file_list = []
        for root, _, files in os.walk(TOURNAMENT_FILES):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path.replace("\\", "/")
                if re.match(round_file, file_path):
                    file_list.append(file_path)
        return file_list

    @classmethod
    def restore_round(cls, round_to_restore):
        path_control = os.path.exists(round_to_restore)
        if path_control is True:
            with open(round_to_restore, "r") as file:
                all_infos = json.load(file)
            t_name = all_infos["tournament_name"]
            round_nb = all_infos["round_nb"]
            match_list = all_infos["match_list"]
            round_to_return = cls(t_name, round_nb, match_list)
            round_to_return.starting_round = all_infos["start"]
            if all_infos["end"]:
                round_to_return.ending_round = all_infos["end"]
        else:
            round_to_return = None
        return round_to_return

    @property
    def match_list(self):
        return self._match_list

    @match_list.setter
    def match_list(self, value):
        self._match_list = value
        self.save_round_data()

    @property
    def end_of_the_round(self):
        return self._end_of_the_round

    @end_of_the_round.setter
    def end_of_the_round(self, value):
        self._end_of_the_round = value
        self.ending_round = datetime.now()
        self.save_round_data()
