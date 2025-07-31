import os
import sys
from typing import List

from colorama import init, Fore, Style

from src.model.dice import Dice
from src.model.game import FarkleGame
from src.state.game_state import GameState

# Initialiser colorama
init()


class FarkleCLI:
    """Interface en ligne de commande pour le jeu Farkle"""

    def __init__(self) -> None:
        self.game = FarkleGame()
        self.game_state = GameState()

    @staticmethod
    def clear_screen() -> None:
        """Efface l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_title() -> None:
        """Affiche le titre du jeu"""
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("╔════════════════════════════════════════╗")
        print("║            Jeu du Farkle               ║")
        print("║            Codé en Python              ║")
        print("║        Par Malik, pour Badger          ║")
        print("╚════════════════════════════════════════╝")
        print("       .-------.    ______")
        print("      /   o   /|   /\\     \\")
        print("     /_______/o|  /o \\  o  \\")
        print("     | o     | | /   o\\_____\\")
        print("     |   o   |o/ \\o   /o    /")
        print("     |     o |/   \\ o/  o  /")
        print("     '-------'     \\/____o/")

        print(f"{Style.RESET_ALL}")

    @staticmethod
    def print_dice(dice_values: List[int]) -> None:
        """Affiche les dés avec des caractères Unicode"""
        dice_faces = {
            1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣"
        }

        print(f"{Fore.YELLOW}Dés lancés: {Style.RESET_ALL}", end="")
        for i, value in enumerate(dice_values):
            print(f"{Fore.WHITE}{dice_faces[value]} ({i + 1}){Style.RESET_ALL}", end="  ")
        print()

    def print_game_status(self) -> None:
        """Affiche l'état actuel du jeu"""
        status = self.game.get_game_status()

        # Ligne colorée pour séparer les tours
        print(f"\n{Fore.MAGENTA}{'=' * 50}{Style.RESET_ALL}")

        # Afficher si c'est le dernier tour
        if status['final_round_started']:
            remaining_players = status['final_round_players_remaining']
            if remaining_players > 0:
                print(
                    f"{Fore.RED}{Style.BRIGHT}🚨 DERNIER TOUR - {status['final_round_triggerer']} a atteint 10,000 points!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}   Joueurs restants: {remaining_players}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{Style.BRIGHT}🏁 DERNIER TOUR TERMINÉ - Calcul du gagnant...{Style.RESET_ALL}")
            print(
                f"{Fore.CYAN}Tour {status['turn_count']} - Joueur: {Fore.YELLOW}{status['current_player']}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.CYAN}Tour {status['turn_count']} - Joueur: {Fore.YELLOW}{status['current_player']}{Style.RESET_ALL}")

        # Ligne colorée pour séparer les tours
        print(f"{Fore.MAGENTA}{'=' * 50}{Style.RESET_ALL}")

        # Afficher le score de tous les joueurs
        print(f"\n{Fore.GREEN}📊 SCORES:{Style.RESET_ALL}")
        for player_info in status['players']:
            board_status = "" if player_info['is_on_board'] else "✗ pas encore dans le jeu (-800)"
            color = Fore.GREEN if player_info['name'] == status['current_player'] else Fore.WHITE

            # Marquer le joueur qui a déclenché le dernier tour
            if status['final_round_started'] and player_info['name'] == status['final_round_triggerer']:
                winner_mark = "👑 "
            else:
                winner_mark = "  "

            print(f"{color}{winner_mark}{player_info['name']}: {player_info['total_score']} pts "
                  f"(tour: {player_info['turn_score']}) {f'[{board_status}]' if board_status else ''}{Style.RESET_ALL}")

        # Afficher le score à transférer (piggy-back)
        if status['turn_score_to_transfer'] > 0:
            current_player = self.game.get_current_player()
            if current_player.is_on_board:
                print(
                    f"\n{Fore.YELLOW}🎁 Score hérité (piggy-back): {status['turn_score_to_transfer']} points{Style.RESET_ALL}")
                print(
                    f"{Fore.YELLOW}   Ce score sera ajouté à vos points dès que vous lancerez les dés!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}❌ Score hérité perdu: {status['turn_score_to_transfer']} points{Style.RESET_ALL}")
                print(
                    f"{Fore.RED}   Vous devez être sur le plateau pour récupérer les points hérités.{Style.RESET_ALL}")

        # Afficher les dés partagés mis de côté
        if status['shared_banked_dice']:
            print(f"\n{Fore.YELLOW}🎲 Dés mis de côté: {status['shared_banked_dice']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Dés restants à lancer: {status['remaining_dice_count']}{Style.RESET_ALL}")

        # Afficher les dés du joueur actuel dans ce tour
        current_player = self.game.get_current_player()
        if current_player.banked_dice:
            print(
                f"\n{Fore.CYAN}🎯 Dés gardés par {current_player.name} ce tour: {current_player.banked_dice}{Style.RESET_ALL}")

        # Afficher qui a banké en dernier
        if status['last_player_banked']:
            print(f"\n{Fore.MAGENTA}💰 Dernier joueur a stoppé (doit lancer avant de restopper){Style.RESET_ALL}")

    @staticmethod
    def print_possible_actions(actions: List[tuple]) -> None:
        """Affiche les actions possibles"""
        if not actions:
            print(f"{Fore.RED}💥 FARKLE! Aucun dé ne peut être conservé.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.BLUE}🎯 Actions possibles:{Style.RESET_ALL}")
        for i, (score, dice) in enumerate(actions, 1):
            print(f"{Fore.BLUE}  {i}. Garder {dice} → {score} points{Style.RESET_ALL}")

    @staticmethod
    def get_player_names() -> List[str]:
        """Demande les noms des joueurs"""
        while True:
            try:
                num_players = int(input(f"\n{Fore.CYAN}Nombre de joueurs (2-8): {Style.RESET_ALL}"))
                if 2 <= num_players <= 8:
                    break
                else:
                    print(f"{Fore.RED}Le nombre de joueurs doit être entre 2 et 8.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")

        player_names = []
        for i in range(num_players):
            while True:
                name = input(f"{Fore.CYAN}Nom du joueur {i + 1}: {Style.RESET_ALL}").strip()
                if name and name not in player_names:
                    player_names.append(name)
                    break
                elif name in player_names:
                    print(f"{Fore.RED}Ce nom est déjà pris.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Veuillez entrer un nom valide.{Style.RESET_ALL}")

        return player_names

    def show_main_menu(self) -> int:
        """Affiche le menu principal"""
        self.clear_screen()
        self.print_title()

        print(f"\n{Fore.CYAN}🎮 MENU PRINCIPAL{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Nouvelle partie{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Charger une partie{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Règles du jeu{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. Quitter{Style.RESET_ALL}")

        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}Votre choix: {Style.RESET_ALL}"))
                if 1 <= choice <= 4:
                    return choice
                else:
                    print(f"{Fore.RED}Choix invalide. Veuillez choisir entre 1 et 4.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")

    def show_game_rules(self) -> None:
        """Affiche les règles du jeu"""
        self.clear_screen()
        self.print_title()

        print(f"\n{Fore.CYAN}📋 RÈGLES DU FARKLE{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}🎯 Objectif:{Style.RESET_ALL}")
        print("  Être le premier à atteindre 10 000 points")

        print(f"\n{Fore.YELLOW}🎲 Scoring:{Style.RESET_ALL}")
        print("  • 1 = 100 points")
        print("  • 5 = 50 points")
        print("  • Trois 1 = 1000 points")
        print("  • Trois 2 = 200 points")
        print("  • Trois 3 = 300 points")
        print("  • Trois 4 = 400 points")
        print("  • Trois 5 = 500 points")
        print("  • Trois 6 = 600 points")
        print(
            "  • Pour chaque nombre au-delà de trois identiques, doublez le montant (par exemple, trois 6 = 600, quatre 6 = 1200, cinq 6 = 2400, six 6 = 4800).")
        print("  • Straight (1, 2, 3, 4, 5, 6) = 1000 points")
        print("  • Trois paires = 1000 points")
        print(
            "  Note : Trois d'une sorte doivent tous être lancés ensemble. Lancer un 1, puis un autre 1 et encore un 1 vaut 300. Lancer 3 1 d'un coup vaut 1000.")

        print(f"\n{Fore.YELLOW}🎮 Déroulement:{Style.RESET_ALL}")
        print("  • Lancez 6 dés")
        print("  • Conservez des dés qui rapportent des points")
        print("  • FARKLE = aucun dé ne peut être conservé → perte du tour")
        print("  • Il faut 'payer' 800 points pour entrer 'sur le plateau'")

        print(f"\n{Fore.YELLOW}💰 Stopper le tour:{Style.RESET_ALL}")
        print("  • Garde votre score du tour et l'ajoute à votre total")
        print("  • Transfère aussi ce score au joueur suivant (piggy-back)")
        print("  • Conditions pour stopper :")
        print("    - Soit être déjà sur le plateau")
        print("    - Soit avoir 800+ points ce tour (pour entrer sur le plateau)")

        print(f"\n{Fore.YELLOW}🎁 Système Piggy-Back:{Style.RESET_ALL}")
        print("  • Quand un joueur stoppe, son score est transféré au suivant")
        print("  • MAIS seuls les joueurs sur le plateau peuvent récupérer les points hérités")
        print("  • Si le joueur suivant n'est pas sur le plateau → points perdus")
        print("  • En cas de FARKLE, le joueur perd tout (y compris le score hérité)")
        print("  • Le score hérité est ajouté dès que le joueur lance les dés")

        print(f"\n{Fore.YELLOW}🏁 Dernier Tour:{Style.RESET_ALL}")
        print("  • Dès qu'un joueur atteint/dépasse 10,000 points, le dernier tour commence")
        print("  • Tous les autres joueurs ont droit à un tour supplémentaire")
        print("  • Le dernier tour ne se déclenche qu'une seule fois")
        print("  • Même si plusieurs joueurs dépassent 10,000 pendant le dernier tour")
        print("  • À la fin du dernier tour, le joueur avec le score le plus élevé gagne")
        print("  • Les joueurs peuvent se rattraper grâce au piggy-back!")

        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def show_load_menu(self) -> str | None:
        """Affiche le menu de chargement"""
        saves = self.game_state.list_saves()

        if not saves:
            print(f"{Fore.RED}Aucune sauvegarde disponible.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            return None

        self.clear_screen()
        self.print_title()

        print(f"\n{Fore.CYAN}💾 CHARGER UNE PARTIE{Style.RESET_ALL}")
        print(f"{Fore.WHITE}0. Retour au menu principal{Style.RESET_ALL}")

        for i, save in enumerate(saves, 1):
            players_str = ", ".join(save['players'])
            print(f"{Fore.WHITE}{i}. {save['filename']} - {players_str} ({save['saved_at']}){Style.RESET_ALL}")

        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}Votre choix: {Style.RESET_ALL}"))
                if choice == 0:
                    return None
                elif 1 <= choice <= len(saves):
                    return saves[choice - 1]['filename']
                else:
                    print(f"{Fore.RED}Choix invalide.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")

    def show_turn_menu(self) -> int:
        """Affiche le menu du tour de jeu"""
        current_player = self.game.get_current_player()

        print(f"\n{Fore.CYAN}🎯 ACTIONS DISPONIBLES:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lancer les dés{Style.RESET_ALL}")

        # Afficher l'option stopper selon le contexte
        if current_player.turn_score == 0:
            print(f"{Fore.YELLOW}2. Stopper le tour (⚠️ aucun point à transférer){Style.RESET_ALL}")
        elif current_player.is_on_board:
            print(
                f"{Fore.WHITE}2. Stopper le tour (garder + transférer {current_player.turn_score} pts){Style.RESET_ALL}")
        elif current_player.turn_score >= 800:
            print(
                f"{Fore.WHITE}2. Stopper le tour (entrer sur le plateau + transférer {current_player.turn_score} pts){Style.RESET_ALL}")
        else:
            print(
                f"{Fore.YELLOW}2. Stopper le tour (⚠️ besoin de 800 pts, vous avez {current_player.turn_score}){Style.RESET_ALL}")

        print(f"{Fore.WHITE}3. Sauvegarder{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. Voir le classement{Style.RESET_ALL}")
        print(f"{Fore.WHITE}5. Quitter{Style.RESET_ALL}")

        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}Votre choix: {Style.RESET_ALL}"))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print(f"{Fore.RED}Choix invalide.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")

    def handle_dice_roll(self) -> None:
        """Gère le lancé de dés et la sélection des dés à conserver"""
        dice_values = self.game.roll_dice()
        self.print_dice(dice_values)

        # Vérifier si c'est un Farkle
        if Dice.is_farkle(self.game.last_dice_roll):
            print(f"{Fore.RED}💥 FARKLE! Votre tour est terminé.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            self.game.farkle()
            return None

        # Afficher les actions possibles
        actions = self.game.get_possible_actions()
        self.print_possible_actions(actions)

        # Demander au joueur de choisir une action
        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}Choisissez une action (1-{len(actions)}): {Style.RESET_ALL}"))
                if 1 <= choice <= len(actions):
                    score, dice_to_bank = actions[choice - 1]
                    if self.game.bank_dice(dice_to_bank):
                        print(f"{Fore.GREEN}✓ Dés conservés: {dice_to_bank} → +{score} points{Style.RESET_ALL}")
                        return None
                    else:
                        print(f"{Fore.RED}Erreur lors de la conservation des dés.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Choix invalide.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")

    def show_leaderboard(self) -> None:
        """Affiche le classement"""
        leaderboard = self.game.get_leaderboard()

        print(f"\n{Fore.CYAN}🏆 CLASSEMENT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'=' * 30}{Style.RESET_ALL}")

        for i, player in enumerate(leaderboard, 1):
            color = Fore.YELLOW if i == 1 else Fore.WHITE
            board_status = "✓" if player.is_on_board else "✗"
            print(f"{color}{i}. {player.name}: {player.total_score} points [{board_status}]{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def save_game_menu(self) -> None:
        """Menu de sauvegarde"""
        filename = input(f"\n{Fore.CYAN}Nom du fichier (laissez vide pour auto): {Style.RESET_ALL}").strip()

        try:
            filepath = self.game.save_game(filename if filename else None)
            print(f"{Fore.GREEN}✓ Partie sauvegardée: {filepath}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erreur lors de la sauvegarde: {e}{Style.RESET_ALL}")

        input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def play_game(self) -> None:
        """Boucle principale du jeu"""
        final_round_message_shown = False

        while not self.game.game_over:
            self.clear_screen()
            self.print_title()

            # Afficher un message spécial quand le dernier tour commence
            if self.game.final_round_started and not final_round_message_shown:
                print(f"\n{Fore.RED}{Style.BRIGHT}🚨 DERNIER TOUR DÉCLENCHÉ!{Style.RESET_ALL}")
                print(
                    f"{Fore.YELLOW}   {self.game.final_round_triggerer.name} a atteint 10,000 points!{Style.RESET_ALL}")
                print(
                    f"{Fore.YELLOW}   Tous les autres joueurs ont droit à un tour pour le rattraper.{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   Attention: Le dernier tour ne se déclenchera qu'une seule fois!{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
                final_round_message_shown = True

            self.print_game_status()

            current_player = self.game.get_current_player()

            # Vérifier si le joueur peut continuer son tour
            if current_player.turn_score > 0 and self.game.get_remaining_dice_count() == 0:
                print(f"\n{Fore.GREEN}🔥 HOT DICE! Tous les dés ont été utilisés.{Style.RESET_ALL}")
                print(f"{Fore.GREEN}   Vous pouvez relancer tous les dés!{Style.RESET_ALL}")

            choice = self.show_turn_menu()

            if choice == 1:  # Lancer les dés
                self.handle_dice_roll()
            elif choice == 2:  # Stopper le tour
                current_player = self.game.get_current_player()
                if not self.game.can_stop_turn():
                    if current_player.turn_score == 0:
                        print(
                            f"{Fore.RED}❌ Vous devez garder au moins un dé avant de pouvoir stopper!{Style.RESET_ALL}")
                    elif not current_player.is_on_board and current_player.turn_score < 800:
                        print(
                            f"{Fore.RED}❌ Vous devez faire au moins 800 points EN UN SEUL TOUR pour entrer sur le plateau!{Style.RESET_ALL}")
                        print(
                            f"{Fore.RED}   Votre score actuel du tour: {current_player.turn_score} points{Style.RESET_ALL}")
                    elif self.game.last_player_banked:
                        print(
                            f"{Fore.RED}❌ Vous ne pouvez pas stopper immédiatement après qu'un joueur ait stoppé!{Style.RESET_ALL}")
                        print(f"{Fore.RED}   Vous devez d'abord lancer les dés.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Vous ne pouvez pas stopper pour une raison inconnue.{Style.RESET_ALL}")
                else:
                    score_to_transfer = current_player.turn_score

                    if self.game.stop_turn():
                        # Vérifier si le joueur vient de déclencher le dernier tour
                        if self.game.final_round_started and self.game.final_round_triggerer == current_player and not final_round_message_shown:
                            print(
                                f"{Fore.GREEN}✓ Tour stoppé! Score gardé: {score_to_transfer} points{Style.RESET_ALL}")
                            print(
                                f"{Fore.RED}{Style.BRIGHT}🎉 FÉLICITATIONS! Vous avez atteint 10,000 points!{Style.RESET_ALL}")
                            print(
                                f"{Fore.RED}   Votre score final: {current_player.total_score} points{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}   Le dernier tour commence maintenant!{Style.RESET_ALL}")
                        else:
                            print(
                                f"{Fore.GREEN}✓ Tour stoppé! Score gardé et transféré: {score_to_transfer} points{Style.RESET_ALL}")
                            print(
                                f"{Fore.YELLOW}   Le joueur suivant héritera de ce score s'il est sur le plateau.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Erreur lors de l'arrêt du tour.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            elif choice == 3:  # Sauvegarder
                self.save_game_menu()
            elif choice == 4:  # Classement
                self.show_leaderboard()
            elif choice == 5:  # Quitter
                confirm = input(f"{Fore.YELLOW}Voulez-vous vraiment quitter? (o/n): {Style.RESET_ALL}")
                if confirm.lower() in ['o', 'oui', 'y', 'yes']:
                    return

        # Fin de partie - Affichage du classement final
        self.clear_screen()
        self.print_title()
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 PARTIE TERMINÉE!{Style.RESET_ALL}")
        print(
            f"{Fore.RED}🏆 GAGNANT: {self.game.winner.name} avec {self.game.winner.total_score} points!{Style.RESET_ALL}")

        # Afficher le classement final complet
        print(f"\n{Fore.CYAN}🏆 CLASSEMENT FINAL:{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'=' * 40}{Style.RESET_ALL}")

        leaderboard = self.game.get_leaderboard()
        for i, player in enumerate(leaderboard, 1):
            if i == 1:
                color = Fore.YELLOW
                medal = "🥇"
            elif i == 2:
                color = Fore.WHITE
                medal = "🥈"
            elif i == 3:
                color = Fore.RED
                medal = "🥉"
            else:
                color = Fore.WHITE
                medal = f"{i}."

            board_status = "✓" if player.is_on_board else "✗"
            print(f"{color}{medal} {player.name}: {player.total_score} points [{board_status}]{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Merci d'avoir joué au Farkle!{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def run(self) -> None:
        """Lance l'application"""
        while True:
            choice = self.show_main_menu()

            if choice == 1:  # Nouvelle partie
                player_names = self.get_player_names()
                self.game.setup_players(player_names)
                self.play_game()
            elif choice == 2:  # Charger une partie
                filename = self.show_load_menu()
                if filename:
                    try:
                        self.game.load_game(filename)
                        print(f"{Fore.GREEN}✓ Partie rechargée avec succès!{Style.RESET_ALL}")
                        input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
                        self.play_game()
                    except Exception as e:
                        print(f"{Fore.RED}Erreur lors du chargement: {e}{Style.RESET_ALL}")
                        input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            elif choice == 3:  # Règles
                self.show_game_rules()
            elif choice == 4:  # Quitter
                print(f"{Fore.CYAN}Merci d'avoir joué au Farkle ! A tout bientôt chez Badger !{Style.RESET_ALL}")
                sys.exit(0)
