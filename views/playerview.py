"""Define player view"""
import re
from colorama import Fore

NATIONAL_IDENTIFIER_FORMAT = r"^[A-Z]{2}[0-9]{5}$"
BIRTHDAY_FORMAT = r"^[0-9]{1}[0-9]{1}/[0-9]{1}[0-9]{1}/[0-9]{4}$"
QUIT = "Q"


class PlayerView:
    def display_all_player_saved(self, players_saved):
        if len(players_saved) == 0:
            print(Fore.RED + "\nVous n'avez pas encore de joueur" + Fore.RESET)
        else:
            print(Fore.BLUE + "\nLes joueurs enregistrés sont:\n" + Fore.RESET)
            for player in players_saved:
                print(
                    "Le joueur "
                    + Fore.LIGHTGREEN_EX
                    + player.name
                    + Fore.RESET
                    + ", son prénom est "
                    + player.firstname
                    + " né(e) le "
                    + player.birthday
                    + ", avec l'identifiant: "
                    + Fore.LIGHTMAGENTA_EX
                    + player.identifiant
                    + Fore.RESET
                )
            if len(players_saved) == 1:
                print(Fore.RED + "Pour un total de 1 joueur\n" + Fore.RESET)
            elif len(players_saved) > 1:
                print(
                    Fore.BLUE
                    + "Pour un total de "
                    + str(len(players_saved))
                    + " joueurs\n"
                    + Fore.RESET
                )

    def add_again(self):
        again = ""
        while again != "N" or again != "Y":
            save_new_player = input(
                "Souhaitez-vous ajouter un nouveau joueur?(y/n)\n> "
            ).capitalize()
            if save_new_player == "Y":
                return True
            elif save_new_player == "N":
                return False
            else:
                print(
                    Fore.RED
                    + "'{}' n'est pas valide\n".format(save_new_player)
                    + Fore.RESET
                )

    def ask_for_name(self):
        name = ""
        while name != QUIT:
            name = input(
                "\nSaisissez le nom de famille du joueur ou 'q'"
                " pour quitter la création:\n> "
            ).upper()
            if name == "":
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif name == QUIT:
                print(Fore.RED + "Vous quittez la création\n" + Fore.RESET)
                return None
            else:
                name_confirmation = input(
                    Fore.GREEN
                    + "Ce nom: '{}'".format(name)
                    + " vous convient-il?\n(y/n)> "
                    + Fore.RESET
                ).upper()
                if name_confirmation == "Y":
                    return name
                elif name_confirmation == "N":
                    continue
                else:
                    print(
                        Fore.RED
                        + "Veuillez répondre en tapant 'y' pour oui,"
                        + " 'n' pour 'non'"
                        + Fore.RESET
                    )

    def ask_for_firstname(self):
        firstname = ""
        while firstname != QUIT:
            firstname = input(
                "Veuillez saisir le prénom du joueur "
                + " ou 'q' pour quitter la création :\n> "
            ).capitalize()
            if firstname == "":
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif firstname == QUIT:
                print(Fore.RED + "Vous quittez la création\n" + Fore.RESET)
                return None
            else:
                firstname_confirmation = input(
                    Fore.GREEN
                    + "Ce nom: '{}' ".format(firstname)
                    + "vous convient-il?\n(y/n)> "
                    + Fore.RESET
                ).upper()
                if firstname_confirmation == "Y":
                    return firstname
                elif firstname_confirmation == "N":
                    continue
                else:
                    print(
                        Fore.RED
                        + "Veuillez répondre en tapant 'y' pour oui,"
                        + " 'n' pour 'non'"
                        + Fore.RESET
                    )

    def ask_for_birthday(self):
        birthday = ""
        while birthday != QUIT:
            birthday = input(
                "Veuillez saisir la date de naissance du joueur.\n"
                + "Elle doit être au format"
                + Fore.LIGHTMAGENTA_EX
                + " '__/__/____' "
                + Fore.RESET
                + ", mais vous pouvez quitter la création"
                + " à tout moment en tapant 'q':\n> "
            ).capitalize()
            if birthday == "":
                print(Fore.RED + "Ce champ ne peut pas être vide" + Fore.RESET)
            elif birthday == QUIT:
                print(Fore.RED + "Vous quittez la création\n" + Fore.RESET)
                return None
            elif re.match(BIRTHDAY_FORMAT, birthday):
                return birthday
            else:
                print(
                    Fore.RED
                    + "La date doit être au format"
                    + Fore.LIGHTMAGENTA_EX
                    + " '__/__/____'"
                    + Fore.RESET
                )

    def ask_national_identification(self):
        identifiant = ""
        while identifiant != QUIT:
            identifiant = input(
                "Veuillez saisir l'identifiant national du joueur.\n"
                + "Il doit être au format"
                + Fore.LIGHTMAGENTA_EX
                + " 'AB12345'"
                + Fore.RESET
                + ", mais vous pouvez également quitter"
                + " la création en tapant 'q'.\n> "
            ).upper()
            if identifiant == "":
                print(Fore.RED + "Vous quittez la création\n" + Fore.RESET)
            elif identifiant == QUIT:
                print(Fore.RED + "Vous quittez la création\n" + Fore.RESET)
                return None
            elif re.match(NATIONAL_IDENTIFIER_FORMAT, identifiant):
                return identifiant
            else:
                print(
                    Fore.RED
                    + "Le format attendu est"
                    + Fore.LIGHTMAGENTA_EX
                    + " 'AB12345'\n"
                    + Fore.RESET
                )

    def display_creation_error(self, identifiant):
        print(
            Fore.RED
            + "L'indentifiant '"
            + Fore.LIGHTMAGENTA_EX
            + identifiant
            + Fore.RED
            + "' existe déjà dans la base de donnée.\n"
            + Fore.RESET
        )

    def display_creation(self):
        print(Fore.GREEN + "Le joueur à été créé" + Fore.RESET)
