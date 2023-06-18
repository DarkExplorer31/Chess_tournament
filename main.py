import os
from colorama import Fore

from controllers.tournamentmanager import TournamentManager
from controllers.playermanager import PlayerManager
from controllers.reportmanager import ReportManager


def main_menu():
    tournament = TournamentManager()
    player = PlayerManager()
    report = ReportManager()

    try:
        os.path.exists("data")
    except FileNotFoundError:
        os.mkdir("data")
        os.mkdir("data/player")
        os.mkdir("data/report")
        os.mkdir("data/tournaments")

    menu = ""
    while menu != "Q":
        menu = input(
            Fore.BLUE
            + "\n#1: Gestion des joueurs\n"
            + Fore.GREEN
            + "#2: Le Tournoi\n"
            + Fore.CYAN
            + "#3: La Gestion des rapports\n"
            + Fore.RESET
            + "ou tapez 'q' pour quitter.\n"
            "Quel menu souhaitez-vous sélectionner ?(1/2/3)> "
        ).upper()
        if menu == "1":
            player.player_management()
        elif menu == "2":
            tournament.run_tournament()
        elif menu == "3":
            report.execute()
        elif menu == "Q":
            break
        else:
            print(Fore.RED + "Votre réponse est invalide." + Fore.RESET)


if __name__ == "__main__":
    main_menu()
