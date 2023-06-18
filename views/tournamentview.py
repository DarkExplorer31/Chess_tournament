"""Define Tournament view"""
import re
from colorama import Fore

TOURNAMENT_NAME = r"^[A-Za-z0-9]{0,99}$"
NB_ROUND_FORMAT = r"^[0-9]{1,2}$"


class TournamentView:
    def __init__(self):
        self.demande = (
            Fore.BLUE
            + "\nVeuillez saisir le nom du joueur que vous souhaitez "
            + "sélectionner pour participer à ce tournoi.\n Vous pouvez"
            + " taper l'identification du joueur ou "
            + " utiliser les options suivantes : \n"
            + " -Taper 'a' pour afficher la liste en cours d'entrée.\n"
            + " -Taper 't' pour sélectionner tous les joueurs.\n"
            + " -Taper 'f' pour finalisé la liste\n"
            + " -Enfin, taper 'q' pour quitter la création.\n> "
            + Fore.RESET
        )

    def ask_for_players(self):
        return (
            Fore.RED
            + "Vous n'avez pas encore de joueur.\n"
            + " Veuillez entrer des joueurs à enregistrer"
            + " sur le menu de gestion des joueurs avant"
            + " de démarrer un tournoi.\n"
            + Fore.RESET
        )

    def ask_for_name(self, all_existing_tournament):
        name_confirmation = ""
        name = ""
        while name_confirmation != "Y" or name != "Q":
            if not all_existing_tournament:
                print(
                    Fore.RED
                    + "Vous n'avez pas encore enregistré de tournoi\n"
                    + Fore.RESET
                )
            else:
                print("Voici les noms de tournoi déjà créés:\n")
                for tournament in all_existing_tournament:
                    print(Fore.RED + tournament + Fore.RESET)
            name = input(
                "Quel est le nom de ce tournoi?"
                + " (tapez 'q' pour revenir au menu)\n> "
            ).capitalize()
            name = name.replace(" ", "")
            if not name:
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif re.match(TOURNAMENT_NAME, name):
                if name == "Q":
                    return None
                name_confirmation = input(
                    Fore.GREEN
                    + "'{}' ce nom vous convient-il?(y/n)\n> ".format(name)
                    + Fore.RESET
                ).capitalize()
                if name_confirmation == "Y":
                    return name
                elif name_confirmation == "N":
                    continue
                else:
                    print(
                        Fore.RED
                        + "'{}' n'est pas valide".format(name_confirmation)
                        + Fore.RESET
                    )
            else:
                print(
                    Fore.RED
                    + "'{}' n'est pas valide".format(name_confirmation)
                    + " car il ne doit pas contenir de caractères spéciaux"
                    + Fore.RESET
                )

    def ask_for_place(self):
        place_confirmation = ""
        place = ""
        while place_confirmation != "Y" or place != "Q":
            place = input(
                "Ou se passe ce tournoi? (tapez 'q' pour revenir au menu)\n> "
            ).capitalize()
            if not place:
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif place == "Q":
                return None
            else:
                place_confirmation = input(
                    Fore.GREEN
                    + place
                    + " cet endroit vous convient-il?(y/n)\n> "
                    + Fore.RESET
                ).capitalize()
                if place_confirmation == "Y":
                    return place
                elif place_confirmation == "N":
                    continue
                else:
                    print(
                        Fore.RED
                        + "'{}' n'est pas valide".format(place_confirmation)
                        + Fore.RESET
                    )

    def ask_for_nb_round(self, players):
        perfect_choice = int(len(players) / 2)
        nb_confirmation = ""
        rounds = ""
        final_round_nb = 0
        while nb_confirmation != "Y" or rounds != "Q":
            rounds = input(
                "Combien de tours compte ce tournoi?\n-tapez 'd',"
                + " pour laisser le chiffre par défaut (4 tours)"
                + " (idéal: {} tours)\n".format(perfect_choice)
                + " et tapez 'q' pour quitter,\n"
                + " mais le chiffre 4 sera utilisé par défaut.\n> "
            ).capitalize()
            if not rounds:
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif rounds == "D":
                final_round_nb = 4
                return final_round_nb
            elif rounds == "Q":
                return None
            elif re.match(NB_ROUND_FORMAT, rounds):
                try:
                    final_round_nb = int(rounds)
                except ValueError:
                    print(
                        Fore.RED
                        + "'{}' n'est pas valide".format(final_round_nb)
                        + Fore.RESET
                    )
                nb_confirmation = input(
                    Fore.GREEN
                    + "'{}' ce nombre de tour vous".format(rounds)
                    + " convient-il?(y/n)\n> "
                    + Fore.RESET
                ).capitalize()
                if nb_confirmation == "Y":
                    return final_round_nb
                elif nb_confirmation == "N":
                    continue
            else:
                print(Fore.RED + rounds + "'' n'est pas valide" + Fore.RESET)

    def list_enumeration(self, player_list):
        if not player_list:
            print(
                Fore.RED
                + "Votre liste de joueurs sélectionnés est vide."
                + Fore.RESET
            )
        elif len(player_list) == 1:
            print("Votre liste comporte 1 joueur.")
        elif len(player_list) > 1:
            print(
                "Votre liste de joueurs sélectionnés: {} joueurs".format(
                    len(player_list)
                )
            )

    def display_tournament_players(self, players_saved):
        print("Les joueurs déjà enregistrés sont: ")
        for player in players_saved:
            print(
                "Voici '{}', son prénom est {}"
                ", il est né le {} et son identifiant: ".format(
                    player.name,
                    player.firstname,
                    player.birthday,
                )
                + Fore.LIGHTMAGENTA_EX
                + player.identifiant
                + Fore.RESET
            )

    def display_current_list(self, current_list):
        print("La liste en cours d'entrée actuelle est :")
        if not current_list:
            print(Fore.RED + "Votre liste est vide" + Fore.RESET)
        else:
            print(Fore.GREEN + "Votre liste actuelle: ")
            for player in current_list:
                print(player)
            print(
                Fore.BLUE
                + "Pour un total de: "
                + str(len(current_list))
                + " joueur(s)\n"
                + Fore.RESET
            )

    def quit_select_current(self, current_list):
        if current_list:
            print("Votre liste est actuellement constituée de: ")
            for player in current_list:
                print(player)
            print("\nPour un Total de: {}".format(len(current_list)))
            if len(current_list) % 2 != 0:
                print(
                    Fore.RED
                    + "Votre liste n'est pas paire, veuillez reprendre\n"
                    + Fore.RESET
                )
        else:
            print(
                Fore.RED
                + "Votre liste est vide, elle ne peux pas être vide"
                + Fore.RESET
            )

    def select_players(self, players_saved):
        player_list = []
        decision = False
        while not decision:
            self.list_enumeration(player_list)
            self.display_tournament_players(players_saved)
            current_player = input(self.demande).upper()
            if current_player == "":
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif current_player == "A":
                self.display_current_list(player_list)
                continue
            elif current_player == "T":
                player_list = players_saved
                if len(player_list) % 2 != 0:
                    print(
                        Fore.RED
                        + "La liste de tous les joueurs n'est pas paire.\n"
                        + Fore.RESET
                    )
                else:
                    return player_list
            elif current_player == "F":
                self.quit_select_current(player_list)
                return player_list
            elif current_player == "Q":
                return None
            elif current_player in player_list:
                print(
                    Fore.RED
                    + "{} est déjà dans la liste".format(current_player)
                    + Fore.RESET
                )
            else:
                player_exist = False
                for player in player_list:
                    if current_player in player.identifiant:
                        print(
                            Fore.RED
                            + "Le joueur est déjà enregistré.\n"
                            + Fore.RESET
                        )
                        player_exist = True
                        break
                if player_exist:
                    continue
                for player in players_saved:
                    if current_player == player.identifiant:
                        player_list.append(player)
                        break

    def ask_to_continue(self):
        while True:
            ask_to_new = input(
                "\nVoulez-vous créer un nouveau tournoi (tapez '1'),\n"
                + "reprendre un tournoi en cours (tapez '2')\n"
                + "ou tapez 'q' pour quitter?\n> "
            ).upper()
            if ask_to_new == "1":
                return True
            elif ask_to_new == "2":
                return False
            elif ask_to_new == "Q":
                return None
            else:
                print(Fore.RED + ask_to_new + " n'est pas valide" + Fore.RESET)

    def select_previous_tournament(self, tournament_saved):
        if not tournament_saved:
            print(
                Fore.RED
                + "Il n'y a aucun tournoi commencé ou sauvegardé.\n"
                + Fore.RESET
            )
            return None
        selected = ""
        while selected not in tournament_saved:
            print("\nVoici la liste de tous les tournois précédents :")
            for tournament in tournament_saved:
                print(Fore.LIGHTMAGENTA_EX + "--> " + tournament + Fore.RESET)
            selected = input(
                "\nTapez le nom d'un tournoi ou 'q' pour quitter.\n> "
            ).capitalize()
            if selected in tournament_saved:
                return selected
            elif selected == "Q":
                return None
            else:
                print(Fore.RED + selected + " n'est pas valide" + Fore.RESET)

    def display_saving_error(self):
        print(
            Fore.RED
            + "Le tournoi n'a pas pu être enregistré: le nom est déjà pris.\n"
            + Fore.RESET
        )

    def display_import_error(self):
        print(
            Fore.RED
            + "Nous n'arrivons pas à importer le tournoi sélectionné.\n"
            + Fore.RESET
        )

    def ask_to_comment(self):
        comment_confirm = ""
        while comment_confirm != "Y" or comment_confirm != "N":
            comment = input(
                Fore.BLUE
                + "Le tournoi étant terminé, avez-vous un commentaire"
                + " général sur le tournoi?\n> "
                + Fore.RESET
            ).capitalize()
            if comment:
                comment_confirm = input(
                    Fore.GREEN
                    + "Voulez-vous enregistrer ce commentaire ?"
                    + " \n'{}'".format(comment)
                    + Fore.RESET
                    + "\n(y/n)> "
                    + Fore.RESET
                ).capitalize()
                if comment_confirm == "Y":
                    return comment
            elif not comment:
                comment_confirm = input(
                    Fore.RED
                    + "Vous n'avez rien rentré comme commentaire."
                    + " Voulez-vous laisser cette partie vide ?\n(y\n)> "
                    + Fore.RESET
                ).capitalize()
                if comment_confirm == "Y":
                    return None
