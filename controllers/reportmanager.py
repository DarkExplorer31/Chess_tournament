"""Define report manager"""
import csv
import os

from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match

from views.reportview import ReportView

REPORT_FILE = "data/report/report.csv"


class ReportManager:
    def __init__(self):
        self.reportview = ReportView()

    def all_tournaments_name(self):
        all_tournaments = Tournament.get_all_tournament_names()
        if all_tournaments == []:
            self.reportview.display_empty()
            return None
        return all_tournaments

    def report_control(self):
        path_control = os.path.exists(REPORT_FILE)
        if path_control:
            self.reportview.display_create_report()
        else:
            self.reportview.display_create_error()

    def get_chosen_tournament(self):
        all_tournaments = self.all_tournaments_name()
        if not all_tournaments:
            return None
        choice_control = False
        while not choice_control:
            choice = self.reportview.tournament_choice(all_tournaments)
            if not choice:
                return None
            choice_control = Tournament.control_name_exist(choice)
            if not choice_control:
                self.reportview.display_import_error()
                continue
            tournament = Tournament.get_tournament_info(choice)
        return tournament

    def get_round_list(self, tournament_name):
        restored_round = Round.get_all_round_files(tournament_name)
        if restored_round:
            all_restored_round = []
            for round in restored_round:
                round_list_saved = Round.restore_round(round)
                match_list = self.get_matches(round_list_saved.match_list)
                round_list_saved.match_list = match_list
                all_restored_round.append(round_list_saved)
            return all_restored_round
        else:
            round_list_saved = None
        return round_list_saved

    def get_matches(self, matches_to_restore):
        matches = []
        for match in matches_to_restore:
            match_restored = Match.restore_match(match)
            player = Player.restore_player(match_restored.player)
            opponent = Player.restore_player(match_restored.opponent)
            match_restored.player = player
            match_restored.opponent = opponent
            matches.append(match_restored)
        return matches

    def all_tournaments_report(self):
        """Export a list of all tournaments"""
        all_tournaments = self.all_tournaments_name()
        if not all_tournaments:
            return None
        title = [
            "Name",
            "Place",
            "Tournaments_players",
            "Starting_date",
            "Ending_date",
            "Comment",
        ]
        exctraction = []
        for tournament in all_tournaments:
            current = Tournament.get_tournament_info(tournament)
            if current is None:
                break
            exctraction.append(
                [
                    current.name,
                    current.place,
                    current.players,
                    current.starting_date,
                    current.ending_date,
                    current.comment,
                ]
            )
        with open(REPORT_FILE, "w") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(title)
            writer.writerows(exctraction)
        self.report_control()

    def name_and_time_tournament(self):
        """Export a list with names and dates from a chosen tournament."""
        tournament = self.get_chosen_tournament()
        if not tournament:
            return None
        data = [
            "Name",
            "Place",
            "starting_date",
            "ending_date",
            "players_identifiant",
            "ranking",
        ]
        from_tournament = [
            tournament.name,
            tournament.place,
            tournament.starting_date,
            tournament.ending_date,
        ]
        data_from_list = zip(tournament.players, tournament.ranking)
        with open(REPORT_FILE, "w") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(data)
            i = 0
            for player, rank in data_from_list:
                if i == 0:
                    writer.writerow(from_tournament + [player] + [rank])
                else:
                    writer.writerow([""] * 4 + [player] + [rank])
                i += 1
        self.report_control()

    def all_matches_and_rounds(self):
        """Export a list of all matches from all rounds
        from a selected tournament"""  # A Finir
        tournament = self.get_chosen_tournament()
        if not tournament:
            return None
        tournament.round_list = self.get_round_list(tournament.name)
        title = ["Tournament_name", ""]

    def all_players_report(self):
        """Export a list of all players saved"""
        all_players = Player.get_players_saved()
        title = ["Name", "Firstname", "Birthday", "Identifiant"]
        data = []
        for player in all_players:
            player_extract = [
                player.name,
                player.firstname,
                player.birthday,
                player.identifiant,
            ]
            data.append(player_extract)
        with open(REPORT_FILE, "w") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(title)
            writer.writerows(data)
        self.report_control()

    def all_players_tournament_report(self):
        """Export a list of players from a selected tournament
        in alphabetic order"""
        tournament = self.get_chosen_tournament()
        if not tournament:
            return None
        title = [
            "Tournament_name",
            "tournament_players",
        ]
        all_tournament_player = []
        for player_ident in tournament.players:
            player_restored = Player.get_player_by_ident(player_ident)
            all_tournament_player.append(player_restored.name)
        sorted_player = sorted(all_tournament_player, reverse=True)
        with open(REPORT_FILE, "w") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(title)
            i = 0
            for player_name in sorted_player:
                if i == 0:
                    writer.writerow([tournament.name] + [player_name])
                else:
                    writer.writerow([""] + [player_name])
                i += 1
        self.report_control()

    def execute(self):
        end_execution = False
        while end_execution is False:
            selection = self.reportview.ask_type_report()
            if selection is None:
                end_execution = True
            elif selection == "T":
                self.all_tournaments_report()
            elif selection == "R":
                self.name_and_time_tournament()
            elif selection == "M":
                self.all_matches_and_rounds()
            elif selection == "P":
                self.all_players_report()
            elif selection == "PT":
                self.all_players_tournament_report()
