"""Define Match view"""
from colorama import Fore


class MatchView:
    def display_size(self, match_list_with_color):
        print(
            "\nLa décision est prise, voici les joueurs"
            + " et leurs couleurs pour ce tour: "
        )
        for player, color in match_list_with_color.items():
            print("Le Joueur : '{}' jouera ".format(player))
            if color == "Blanc":
                print(Fore.WHITE + "Blanc" + Fore.RESET)
            else:
                print(Fore.BLACK + "Noir" + Fore.RESET)

    def display_already_played(self, match):
        print(
            Fore.LIGHTCYAN_EX
            + "\n--> Le match {} VS {}".format(match.player, match.opponent)
            + " a déjà été joué pour ce round, on rappelle le résultat :\n"
            + " Le joueur: {} à un score de : {}\n".format(
                match.player, match.player_score
            )
            + "et le joueur: {} un score de {}\n".format(
                match.opponent, match.opponent_score
            )
            + Fore.RESET
        )

    def ask_result(self, match):
        print("\n" + str(match))
        end_turn = False
        while end_turn is False:
            match_result = input(
                Fore.GREEN
                + "\nQui est le vainceur?"
                + " ({} vs {}) ".format(match.player, match.opponent)
                + " '1' pour {}, ".format(match.player)
                + "'2' pour {} et ".format(match.opponent)
                + "'e' pour déclarer une égalité. "
                + "Vous pouvez taper 'q' pour quitter.\n(1/2/e/q)> "
                + Fore.RESET
            ).upper()
            if match_result == "1":
                print(
                    Fore.LIGHTBLUE_EX
                    + str(match.player)
                    + " est le vainceur\n"
                    + Fore.RESET
                )
                match.player_score += 1
                end_turn = True
            elif match_result == "2":
                print(
                    Fore.LIGHTBLUE_EX
                    + str(match.opponent)
                    + " est le vainceur\n"
                    + Fore.RESET
                )
                match.opponent_score += 1
                end_turn = True
            elif match_result == "E":
                print(Fore.LIGHTBLUE_EX + "c'est un égalité!\n" + Fore.RESET)
                match.player_score += 0.5
                match.opponent_score += 0.5
                end_turn = True
            elif match_result == "Q":
                print(Fore.RED + "Vous quitter le tournoi" + Fore.RESET)
                return None
            else:
                print(Fore.RED + match_result + " est invalide" + Fore.RESET)
            match.match_result = (
                [match.player, match.player_score],
                [match.opponent, match.opponent_score],
            )
        return match
