import os
import sys
from typing import List, Optional
from colorama import init, Fore, Back, Style
from model.game import FarkleGame
from state.game_state import GameState


# Initialiser colorama
init()


class FarkleCLI:
    """Interface en ligne de commande pour le jeu Farkle"""
    
    def __init__(self):
        self.game = FarkleGame()
        self.game_state = GameState()
    
    def clear_screen(self):
        """Efface l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
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
    
    def print_dice(self, dice_values: List[int]):
        """Affiche les dés avec des caractères Unicode"""
        dice_faces = {
            1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣"
        }
        
        print(f"{Fore.YELLOW}Dés lancés: {Style.RESET_ALL}", end="")
        for i, value in enumerate(dice_values):
            print(f"{Fore.WHITE}{dice_faces[value]} ({i+1}){Style.RESET_ALL}", end="  ")
        print()
    
    def print_game_status(self):
        """Affiche l'état actuel du jeu"""
        status = self.game.get_game_status()
        
        # Ligne colorée pour séparer les tours
        print(f"\n{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Tour {status['turn_count']} - Joueur: {Fore.YELLOW}{status['current_player']}{Style.RESET_ALL}")
        # Ligne colorée pour séparer les tours
        print(f"{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}")
        
        # Afficher le score de tous les joueurs
        print(f"\n{Fore.GREEN}📊 SCORES:{Style.RESET_ALL}")
        for player_info in status['players']:
            board_status = "" if player_info['is_on_board'] else "✗ pas encore dans le jeu (-800)"
            color = Fore.GREEN if player_info['name'] == status['current_player'] else Fore.WHITE
            print(f"{color}  {player_info['name']}: {player_info['total_score']} pts "
                  f"(tour: {player_info['turn_score']}) {f'[{board_status}]' if board_status else ''}{Style.RESET_ALL}")
        
        # Afficher le score à transférer (piggy-back)
        if status['turn_score_to_transfer'] > 0:
            current_player = self.game.get_current_player()
            if current_player.is_on_board:
                print(f"\n{Fore.YELLOW}🎁 Score hérité (piggy-back): {status['turn_score_to_transfer']} points{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}   Ce score sera ajouté à vos points dès que vous lancerez les dés!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}❌ Score hérité perdu: {status['turn_score_to_transfer']} points{Style.RESET_ALL}")
                print(f"{Fore.RED}   Vous devez être sur le plateau pour récupérer les points hérités.{Style.RESET_ALL}")
        
        # Afficher les dés partagés mis de côté
        if status['shared_banked_dice']:
            print(f"\n{Fore.YELLOW}🎲 Dés mis de côté: {status['shared_banked_dice']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Dés restants à lancer: {status['remaining_dice_count']}{Style.RESET_ALL}")
        
        # Afficher les dés du joueur actuel dans ce tour
        current_player = self.game.get_current_player()
        if current_player.banked_dice:
            print(f"\n{Fore.CYAN}🎯 Dés gardés par {current_player.name} ce tour: {current_player.banked_dice}{Style.RESET_ALL}")
        
        # Afficher qui a banké en dernier
        if status['last_player_banked']:
            print(f"\n{Fore.MAGENTA}💰 Dernier joueur a stoppé (doit lancer avant de restopper){Style.RESET_ALL}")
    
    def print_possible_actions(self, actions: List[tuple]):
        """Affiche les actions possibles"""
        if not actions:
            print(f"{Fore.RED}💥 FARKLE! Aucun dé ne peut être conservé.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.BLUE}🎯 Actions possibles:{Style.RESET_ALL}")
        for i, (score, dice) in enumerate(actions, 1):
            print(f"{Fore.BLUE}  {i}. Garder {dice} → {score} points{Style.RESET_ALL}")
    
    def get_player_names(self) -> List[str]:
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
                name = input(f"{Fore.CYAN}Nom du joueur {i+1}: {Style.RESET_ALL}").strip()
                if name and name not in player_names:
                    player_names.append(name)
                    break
                elif name in player_names:
                    print(f"{Fore.RED}Ce nom est déjà pris.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Veuillez entrer un nom valide.{Style.RESET_ALL}")
        
        return player_names
    
    def show_main_menu(self):
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
    
    def show_game_rules(self):
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
        print("  • Pour chaque nombre au-delà de trois identiques, doublez le montant (par exemple, trois 6 = 600, quatre 6 = 1200, cinq 6 = 2400, six 6 = 4800).")
        print("  • Straight (1, 2, 3, 4, 5, 6) = 1000 points")
        print("  • Trois paires = 1000 points")
        print("  Note : Trois d'une sorte doivent tous être lancés ensemble. Lancer un 1, puis un autre 1 et encore un 1 vaut 300. Lancer 3 1 d'un coup vaut 1000.")
        
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
        
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    def show_load_menu(self):
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
    
    def show_turn_menu(self):
        """Affiche le menu du tour de jeu"""
        current_player = self.game.get_current_player()
        
        print(f"\n{Fore.CYAN}🎯 ACTIONS DISPONIBLES:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lancer les dés{Style.RESET_ALL}")
        
        # Afficher l'option stopper selon le contexte
        if current_player.turn_score == 0:
            print(f"{Fore.YELLOW}2. Stopper le tour (⚠️ aucun point à transférer){Style.RESET_ALL}")
        elif current_player.is_on_board:
            print(f"{Fore.WHITE}2. Stopper le tour (garder + transférer {current_player.turn_score} pts){Style.RESET_ALL}")
        elif current_player.turn_score >= 800:
            print(f"{Fore.WHITE}2. Stopper le tour (entrer sur le plateau + transférer {current_player.turn_score} pts){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}2. Stopper le tour (⚠️ besoin de 800 pts, vous avez {current_player.turn_score}){Style.RESET_ALL}")
        
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
    
    def handle_dice_roll(self):
        """Gère le lancé de dés et la sélection des dés à conserver"""
        dice_values = self.game.roll_dice()
        self.print_dice(dice_values)
        
        # Vérifier si c'est un Farkle
        if self.game.is_farkle():
            print(f"{Fore.RED}💥 FARKLE! Votre tour est terminé.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            self.game.farkle()
            return
        
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
                        break
                    else:
                        print(f"{Fore.RED}Erreur lors de la conservation des dés.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Choix invalide.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
    
    def show_leaderboard(self):
        """Affiche le classement"""
        leaderboard = self.game.get_leaderboard()
        
        print(f"\n{Fore.CYAN}🏆 CLASSEMENT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*30}{Style.RESET_ALL}")
        
        for i, player in enumerate(leaderboard, 1):
            color = Fore.YELLOW if i == 1 else Fore.WHITE
            board_status = "✓" if player.is_on_board else "✗"
            print(f"{color}{i}. {player.name}: {player.total_score} points [{board_status}]{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    def save_game_menu(self):
        """Menu de sauvegarde"""
        filename = input(f"\n{Fore.CYAN}Nom du fichier (laissez vide pour auto): {Style.RESET_ALL}").strip()
        
        try:
            filepath = self.game.save_game(filename if filename else None)
            print(f"{Fore.GREEN}✓ Partie sauvegardée: {filepath}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erreur lors de la sauvegarde: {e}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    def play_game(self):
        """Boucle principale du jeu"""
        while not self.game.game_over:
            self.clear_screen()
            self.print_title()
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
                        print(f"{Fore.RED}❌ Vous devez garder au moins un dé avant de pouvoir stopper!{Style.RESET_ALL}")
                    elif not current_player.is_on_board and current_player.turn_score < 800:
                        print(f"{Fore.RED}❌ Vous devez faire au moins 800 points EN UN SEUL TOUR pour entrer sur le plateau!{Style.RESET_ALL}")
                        print(f"{Fore.RED}   Votre score actuel du tour: {current_player.turn_score} points{Style.RESET_ALL}")
                    elif self.game.last_player_banked:
                        print(f"{Fore.RED}❌ Vous ne pouvez pas stopper immédiatement après qu'un joueur ait stoppé!{Style.RESET_ALL}")
                        print(f"{Fore.RED}   Vous devez d'abord lancer les dés.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Vous ne pouvez pas stopper pour une raison inconnue.{Style.RESET_ALL}")
                else:
                    score_to_transfer = current_player.turn_score
                    if self.game.stop_turn():
                        print(f"{Fore.GREEN}✓ Tour stoppé! Score gardé et transféré: {score_to_transfer} points{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}   Le joueur suivant héritera de ce score s'il est sur le plateau.{Style.RESET_ALL}")
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
        
        # Fin de partie
        self.clear_screen()
        self.print_title()
        print(f"\n{Fore.GREEN}🎉 PARTIE TERMINÉE!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🏆 Gagnant: {self.game.winner.name} avec {self.game.winner.total_score} points!{Style.RESET_ALL}")
        
        self.show_leaderboard()
    
    def run(self):
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