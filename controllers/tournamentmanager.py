"""Define controller about tournament"""
import random

from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match

from views.playerview import PlayerView
from views.tournamentview import TournamentView
from views.roundview import RoundView
from views.matchview import MatchView

COLOR = ["Blanc", "Noir"]


class TournamentManager:
    """Define Tournament Manager"""

    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.roundview = RoundView()
        self.matchview = MatchView()
        self.tournament = None

    def create_tournament(self, players_saved):
        """We create a new tournament, a tournament has:
        a name, a location (place), a list of players and
        a nummber of rounds"""
        all_tournaments_names = Tournament.get_all_tournament_names()
        name = self.tournament_view.ask_for_name(all_tournaments_names)
        control_name = Tournament.control_name_exist(name)
        if name is None:
            return None
        elif control_name is True:
            self.tournament_view.display_saving_error()
            return None
        place = self.tournament_view.ask_for_place()
        if place is None:
            return None
        players = self.create_player_list(players_saved)
        if not players:
            return None
        empty_list = []
        self.tournament = Tournament(
            name, place, players, ranking=empty_list, round_list=empty_list
        )
        nb_round = self.tournament_view.ask_for_nb_round(players)
        if nb_round is None:
            return None
        self.tournament.nb_round = nb_round
        return self.tournament

    def create_player_list(self, players_saved):
        players = []
        while len(players) < 2:
            players = self.tournament_view.select_players(players_saved)
            if players is None:
                return None
            elif len(players) % 2 == 0 and len(players) >= 2:
                break
        for player in players:
            renamed_player = "{} ({})".format(player.name, player.identifiant)
            player.name = renamed_player
        return players

    def define_first_round(self):
        restored_round = self.restore_round(self.tournament.name)
        if restored_round:
            return restored_round
        tournament_players = self.tournament.players.copy()
        random.shuffle(tournament_players)
        first_match_list = []
        while len(tournament_players) != 0:
            player = tournament_players[0]
            opponent = tournament_players[1]
            match = Match(player, opponent)
            first_match_list.append(match)
            tournament_players.remove(player)
            tournament_players.remove(opponent)
        first_round = Round(
            self.tournament.name, self.tournament.round, first_match_list
        )
        return first_round

    def randomize_color(self, round):
        """Define a color for one player per match"""
        result = {}
        for match in round.match_list:
            player_color = random.choice(COLOR)
            result.update({match.player: player_color})
        self.matchview.display_size(result)

    def draft_match_result(self, existing_round):
        """Take and return the result from matches"""
        match_list = existing_round.match_list.copy()
        match_index = 0
        for match in match_list:
            if match.match_result:
                self.matchview.display_already_played(match)
            else:
                match_list[match_index] = self.matchview.ask_result(match)
                if not match_list[match_index]:
                    return None
                existing_round.match_list = match_list
            match_index += 1
        return existing_round.match_list

    def define_player_list(self, match_result):
        """Return a list of player with theirs score to sorting them"""
        player_list = []
        for match in match_result:
            player = match.player
            player.score = match.player_score
            player_list.append(player)
            opponent = match.opponent
            opponent.score = match.opponent_score
            player_list.append(opponent)
        return player_list

    def sorting_by_score(self, current_round):
        matches = self.draft_match_result(current_round)
        if not matches:
            return None
        player_list = self.define_player_list(matches)
        players_name_sorted = sorted(player_list, reverse=True)
        self.tournament.ranking = players_name_sorted
        self.roundview.display_matchmacking(self.tournament)
        return current_round

    def all_previous_matches(self):
        """take all previous matches to avoid a
        second match between two players"""
        previous_matches = []
        for existing_round in self.tournament.round_list:
            previous = ()
            for match in existing_round.match_list:
                previous = (match.player, match.opponent)
                previous_matches.append(previous)
        return previous_matches

    def next_match_list(self, new_match_list):
        """Make match list for next confrontations"""
        next_match_list = []
        for new_match in new_match_list:
            player = new_match[0]
            opponent = new_match[1]
            player_score = player.score
            opponent_score = opponent.score
            next_match = Match(player, opponent, player_score, opponent_score)
            next_match_list.append(next_match)
        return next_match_list

    def define_match_list(self):
        """Define next confrontation, after first round of tournament"""
        previous_matches = self.all_previous_matches()
        ranking = self.tournament.ranking.copy()
        new_match_list = []
        while len(ranking) != 0:
            opponent_position = 1
            if len(ranking) == 0:
                break
            for player in ranking:
                next_versus = ()
                try:
                    opponent = ranking[opponent_position]
                # that means he has played with everyone else
                except IndexError:
                    previous_matches = []
                next_versus = (player, opponent)
                if player == opponent:
                    opponent_position += 1
                    continue
                if next_versus in previous_matches:
                    opponent_position += 1
                    continue
                elif (next_versus[1], next_versus[0]) in previous_matches:
                    opponent_position += 1
                    continue
                else:
                    new_match_list.append(next_versus)
                    ranking.remove(player)
                    ranking.remove(opponent)
        matches = self.next_match_list(new_match_list)
        new_round = Round(self.tournament.name, self.tournament.round, matches)
        return new_round

    def select_tournament(self):
        """Allow to resume an unfinished tournament"""
        all_path = Tournament.get_all_tournament_names()
        choice = self.tournament_view.select_previous_tournament(all_path)
        if choice is None:
            return None
        path_control = Tournament.control_name_exist(choice)
        if path_control:
            restored = self.restore_tournament(choice)
            if not restored:
                return None
        else:
            self.tournament_view.display_import_error()
            return None
        return restored

    def restore_tournament(self, tournament_name):
        t_restored = Tournament.get_tournament_info(tournament_name)
        if t_restored.ending_date:
            self.tournament_view.display_tournament_error()
            return None
        tournament_player = []
        for player in t_restored.players:
            player_founded = Player.get_player_by_ident(player)
            tournament_player.append(player_founded)
        t_restored.players = tournament_player
        tournament_ranking = []
        for player in t_restored.ranking:
            player_restored = Player.restore_player(player)
            tournament_ranking.append(player_restored)
        t_restored.ranking = tournament_ranking
        if t_restored.round > 1:
            round_list = self.restore_round(t_restored.name, listing=True)
            t_restored.round_list = round_list
        return t_restored

    def restore_round(self, tournament_name, listing=False):
        restored_round = Round.get_all_round_files(tournament_name)
        if restored_round and not listing:
            for round in restored_round:
                round_saved = Round.restore_round(round)
                match_list = self.restore_matches(round_saved.match_list)
                round_saved.match_list = match_list
        elif restored_round and listing:
            all_restored_round = []
            for round in restored_round:
                round_saved = Round.restore_round(round)
                match_list = self.restore_matches(round_saved.match_list)
                round_saved.match_list = match_list
                all_restored_round.append(round_saved)
            return all_restored_round
        else:
            round_saved = None
        return round_saved

    def restore_matches(self, matches_to_restore):
        matches = []
        for match in matches_to_restore:
            match_restored = Match.restore_match(match)
            player = Player.restore_player(match_restored.player)
            opponent = Player.restore_player(match_restored.opponent)
            match_restored.player = player
            match_restored.opponent = opponent
            matches.append(match_restored)
        return matches

    def run_tournament(self):
        self.tournament = None
        players_saved = Player.get_players_saved()
        if not players_saved:
            self.tournament_view.ask_for_players()
            return None
        ask_for_new = self.tournament_view.ask_to_continue()
        if ask_for_new:
            self.tournament = self.create_tournament(players_saved)
        elif ask_for_new is None:
            return None
        elif not ask_for_new:
            self.tournament = self.select_tournament()
        else:
            return None
        if not self.tournament:
            return None
        for _ in range(self.tournament.round, self.tournament.nb_round + 1):
            if self.tournament.round == 1:
                starting_round = self.define_first_round()
            else:
                starting_round = self.define_match_list()
            self.roundview.display_match_list(starting_round)
            self.randomize_color(starting_round)
            ending_round = self.sorting_by_score(starting_round)
            if ending_round is None:
                return None
            ending_round.end_of_the_round = True
            self.tournament.round_list.append(ending_round)
            if self.tournament.round < self.tournament.nb_round:
                self.tournament.round = self.tournament.round + 1
        comment = self.tournament_view.ask_to_comment()
        self.tournament.comment = comment
        self.tournament.finished = True
