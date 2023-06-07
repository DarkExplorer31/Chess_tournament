"""Define report views."""
from colorama import Fore


class ReportView:
    def display_empty(self):
        print(Fore.RED + "Vous n'avez aucune donnée enregistrée." + Fore.RESET)

    def display_import_error(self):
        print(Fore.RED + "Le tournoi saisi n'existe pas.\n" + Fore.RESET)

    def ask_type_report(self):
        end_selection = False
        while end_selection is False:
            selection = input(
                Fore.LIGHTCYAN_EX
                + "\nQuel type de rapport aimeriez-vous avoir?.\n"
                + "-Tapez 'p' liste de tous les joueurs.\n"
                + "-Tapez 't' pour une liste de tout les tournois.\n"
                + "-Tapez 'r' pour le nom et dates d'un tournoi donné.\n"
                + "-Tapez 'm' pour tout les tours/matchs d'un tournoi.\n"
                + "-Tapez 'pt' pour la liste de tout les joueurs d'un tournoi."
                + "\n-Ou tapez 'q' pour quitter.\n"
                + Fore.LIGHTGREEN_EX
                + "(p/t/r/m/pt/q)> "
                + Fore.RESET
            ).upper()
            if selection in ["T", "R", "M", "P", "PT"]:
                return selection
            elif selection == "Q":
                print(Fore.RED + "\nVous quittez la création de rapport." + Fore.RESET)
                return None
            else:
                print(Fore.RED + selection + " n'est pas valide" + Fore.RESET)

    def tournament_choice(self, all_tournaments):
        print("Voici les tournois sauvegardés: ")
        for tournament in all_tournaments:
            print(Fore.MAGENTA + "--> " + tournament + Fore.RESET)
        choice = input(
            "Taper le nom du tournoi dont vous souhaitez le rapport"
            + " ou tapez 'q' pour quitter.\n> "
        ).capitalize()
        if choice == "Q":
            return None
        return choice

    def display_create_report(self):
        print(Fore.GREEN + "Le rapport a bien été créé." + Fore.RESET)

    def display_create_error(self):
        print(Fore.RED + "Le rapport n'a pas pu être créé." + Fore.RESET)
