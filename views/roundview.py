"""Define Round View"""
from colorama import Fore


class RoundView:
    def display_match_list(self, round):
        print(
            Fore.GREEN
            + "\n#####################################################\n"
            + "Voici le round {}:\n".format(round.round_nb)
            + "Voici la liste des joueurs qui vont s'affronter:\n"
            + Fore.RESET
        )
        for match in round.match_list:
            print(
                Fore.BLUE
                + "{} VS {}\n".format(match.player, match.opponent)
                + Fore.RESET
            )
        print("Et c'est parti pour le round {}:".format(round.round_nb))

    def display_matchmacking(self, tournament_data):
        round_nb = tournament_data.round
        print(
            Fore.LIGHTGREEN_EX
            + "\nNous voici donc à la fin du round {}:".format(round_nb)
            + Fore.RESET
        )
        print("\nVoici le classement actuel: ")
        sorted_player = tournament_data.ranking
        for player in sorted_player:
            print(
                Fore.MAGENTA
                + player.name
                + " avec "
                + str(player.score)
                + " points"
                + Fore.RESET
            )
