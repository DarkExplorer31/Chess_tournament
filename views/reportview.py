"""Define report views."""
from colorama import Fore


class ReportView:
    def display_empty(self):
        print(Fore.RED + "Vous n'avez aucune donnée enregistrée." + Fore.RESET)

    def display_import_error(self):
        print(Fore.RED + "Le tournoi saisi n'existe pas.\n" + Fore.RESET)

    def ask_type_report(self):
        end_selection = False
        while not end_selection:
            selection = input(
                Fore.LIGHTCYAN_EX
                + "\nQuel type de rapport aimeriez-vous créer?\n"
                + "-Tapez 'p' liste de tous les joueurs.\n"
                + "-Tapez 't' pour une liste de tout les tournois.\n"
                + "-Tapez 'r' pour le nom et dates d'un tournoi donné.\n"
                + "-Tapez 'm' pour tout les tours/matchs d'un tournoi.\n"
                + "-Tapez 'pt' pour la liste de tout les joueurs d'un tournoi."
                + Fore.LIGHTBLUE_EX
                + "\n\n-Ou tapez 'q' pour quitter.\n"
                + Fore.LIGHTGREEN_EX
                + "(p/t/r/m/pt/q)> "
                + Fore.RESET
            ).upper()
            if selection in ["T", "R", "M", "P", "PT"]:
                return selection
            elif selection == "Q":
                print(
                    Fore.RED
                    + "\nVous quittez maintenant la gestion de rapport."
                    + Fore.RESET
                )
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

    def ask_to_open(self):
        asking = True
        while asking:
            to_open = input(
                Fore.GREEN
                + "\nSouhaitez-vous visualiser le "
                + "contenu de ce rapport? (y/n)\n> "
                + Fore.RESET
            ).upper()
            if to_open == "Y":
                return True
            elif to_open == "N":
                return False
            else:
                print(Fore.RED + to_open + " n'est pas valide.\n" + Fore.RESET)

    def open_error(self):
        print(Fore.RED + "Le rapport n'a pas pu être trouvé." + Fore.RESET)

    def display_content(self, line_to_visualized):
        for element in line_to_visualized:
            element = element.replace(" ", "Vide")
            print(element.replace(";", ", "))
