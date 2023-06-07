"""Define Player Manager"""
from models.player import Player
from views.playerview import PlayerView


class PlayerManager:
    def __init__(self):
        self.player_view = PlayerView()
        self.all_players = []

    def new_player(self):
        another_add = True
        new_player = None
        while another_add:
            self.all_players = Player.get_players_saved()
            self.player_view.display_all_player_saved(self.all_players)
            if self.all_players:
                another_add = self.player_view.add_again()
                if not another_add:
                    break
            name = self.player_view.ask_for_name()
            if not name:
                return None
            firstname = self.player_view.ask_for_firstname()
            if not firstname:
                return None
            birthday = self.player_view.ask_for_birthday()
            if not birthday:
                return None
            create_identifiant = True
            while create_identifiant:
                identifiant = self.player_view.ask_national_identification()
                if not identifiant:
                    return None
                control_ident = Player.identifiant_exists(identifiant)
                if control_ident:
                    self.player_view.display_creation_error(control_ident)
                elif not control_ident:
                    self.player_view.display_creation()
                    create_identifiant = False
            new_player = Player(name, firstname, birthday, identifiant)
            new_player.save_new_player()
            self.all_players = Player.get_players_saved()
        return new_player

    def player_management(self):
        all_player_saved = []
        self.new_player()
        all_player_saved = Player.get_players_saved()
        return all_player_saved
