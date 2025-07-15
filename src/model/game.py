from typing import List, Optional, Tuple
from model.player import Player
from model.dice import Dice
from state.game_state import GameState


class FarkleGame:
    """Classe principale pour gérer une partie de Farkle"""
    
    def __init__(self, player_names: List[str] = None):
        self.players = []
        self.current_player_index = 0
        self.dice = Dice()
        self.game_state = GameState()
        self.game_over = False
        self.winner = None
        self.turn_count = 1
        self.last_dice_roll = []
        self.shared_banked_dice = []  # Dés mis de côté partagés entre les joueurs
        self.last_player_banked = False  # True si le joueur précédent a banké sans lancer depuis
        self.turn_score_to_transfer = 0  # Score du tour à transférer au joueur suivant (piggy-back)
        self.final_round_started = False  # True si le dernier tour a commencé
        self.final_round_triggerer = None  # Joueur qui a déclenché le dernier tour
        self.final_round_players_remaining = 0  # Nombre de joueurs restants à jouer dans le dernier tour
        
        if player_names:
            self.setup_players(player_names)
    
    def setup_players(self, player_names: List[str]):
        """Initialise les joueurs pour une nouvelle partie"""
        if not (2 <= len(player_names) <= 8):
            raise ValueError("Le nombre de joueurs doit être entre 2 et 8")
        
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        self.turn_count = 1
        self.shared_banked_dice = []
        self.last_player_banked = False
        self.turn_score_to_transfer = 0
        self.final_round_started = False
        self.final_round_triggerer = None
        self.final_round_players_remaining = 0
    
    def get_current_player(self) -> Player:
        """Retourne le joueur actuel"""
        return self.players[self.current_player_index]
    
    def get_remaining_dice_count(self) -> int:
        """Retourne le nombre de dés restants à lancer (partagé entre tous les joueurs)"""
        return 6 - len(self.shared_banked_dice)
    
    def roll_dice(self) -> List[int]:
        """Lance les dés pour le joueur actuel"""
        remaining_dice = self.get_remaining_dice_count()
        
        if remaining_dice == 0:
            remaining_dice = 6  # Hot dice - relancer tous les dés
            self.shared_banked_dice = []
        
        # Dès qu'un joueur lance les dés, il peut banker à nouveau
        self.last_player_banked = False
        
        # Si il y a un score à transférer du joueur précédent (piggy-back)
        # Seuls les joueurs sur le plateau peuvent récupérer les points hérités
        current_player = self.get_current_player()
        if self.turn_score_to_transfer > 0 and current_player.is_on_board:
            current_player.turn_score += self.turn_score_to_transfer
            self.turn_score_to_transfer = 0
        elif self.turn_score_to_transfer > 0:
            # Si le joueur n'est pas sur le plateau, il perd les points hérités
            self.turn_score_to_transfer = 0
        
        self.last_dice_roll = self.dice.roll(remaining_dice)
        return self.last_dice_roll
    
    def get_possible_actions(self) -> List[Tuple[int, List[int]]]:
        """Retourne les actions possibles pour le lancé actuel"""
        return Dice.get_possible_combinations(self.last_dice_roll)
    
    def bank_dice(self, dice_to_bank: List[int]) -> bool:
        """
        Conserve des dés pour le joueur actuel
        
        Args:
            dice_to_bank: Liste des dés à conserver
            
        Returns:
            True si l'action est valide, False sinon
        """
        current_player = self.get_current_player()
        
        # Vérifier que les dés peuvent être conservés
        score, used_dice = Dice.calculate_score(dice_to_bank)
        if score == 0 or sorted(dice_to_bank) != sorted(used_dice):
            return False
        
        # Vérifier que les dés sont disponibles
        available_dice = self.last_dice_roll.copy()
        for die in dice_to_bank:
            if die in available_dice:
                available_dice.remove(die)
            else:
                return False
        
        # Conserver les dés au niveau du joueur ET au niveau du jeu
        current_player.add_turn_score(score, dice_to_bank)
        self.shared_banked_dice.extend(dice_to_bank)
        
        # Retirer les dés conservés du lancé actuel
        for die in dice_to_bank:
            self.last_dice_roll.remove(die)
        
        return True
    
    def can_stop_turn(self) -> bool:
        """Vérifie si le joueur actuel peut arrêter son tour (stop)"""
        current_player = self.get_current_player()
        
        # Un joueur ne peut pas s'arrêter s'il n'a pas de dés conservés dans CE tour
        if current_player.turn_score == 0:
            return False
        
        # Si le joueur n'est pas sur le plateau, il doit avoir au moins 800 points
        if not current_player.is_on_board and current_player.turn_score < 800:
            return False
        
        # Un joueur ne peut pas s'arrêter immédiatement après qu'un autre joueur ait banké sans lancer les dés
        if self.last_player_banked:
            return False
        
        return True
    
    def stop_turn(self) -> bool:
        """
        Arrête le tour du joueur actuel, garde son score et le transfère au joueur suivant (piggy-back)
        
        Returns:
            True si le tour peut être arrêté, False sinon
        """
        current_player = self.get_current_player()
        
        if not self.can_stop_turn():
            return False
        
        # Le joueur garde son score
        current_player.total_score += current_player.turn_score
        
        # Si le joueur n'était pas sur le plateau et qu'il a fait 800+ points ce tour
        if not current_player.is_on_board and current_player.turn_score >= 800:
            current_player.is_on_board = True
        
        # Vérifier si le joueur a atteint 10,000 points et déclencher le dernier tour
        if not self.final_round_started and current_player.total_score >= 10000:
            self.final_round_started = True
            self.final_round_triggerer = current_player
            # Tous les autres joueurs doivent avoir leur tour (nombre total - 1)
            self.final_round_players_remaining = len(self.players) - 1
        
        # Transférer le score du tour au joueur suivant
        self.turn_score_to_transfer = current_player.turn_score
        
        # Reset le tour du joueur actuel
        current_player.turn_score = 0
        current_player.banked_dice = []
        
        # Reset les dés partagés - nouveau tour avec 6 dés
        self.shared_banked_dice = []
        
        # Marquer qu'un joueur a "stoppé"
        self.last_player_banked = True
        
        # Vérifier si le jeu doit se terminer
        if self.should_end_game():
            self.end_game()
        else:
            self.next_player()
        
        return True
    
    def should_end_game(self) -> bool:
        """Vérifie si le jeu doit se terminer"""
        # Le jeu se termine si le dernier tour a commencé et que tous les autres joueurs ont joué
        if self.final_round_started:
            return self.final_round_players_remaining <= 0
        
        return False
    
    def farkle(self):
        """Gère un Farkle (aucun dé ne peut être conservé)"""
        current_player = self.get_current_player()
        current_player.reset_turn()
        
        # Reset les dés partagés - nouveau tour avec 6 dés
        self.shared_banked_dice = []
        self.last_player_banked = False
        
        # Perdre aussi le score transféré s'il y en a un
        self.turn_score_to_transfer = 0
        
        # Vérifier si le jeu doit se terminer
        if self.should_end_game():
            self.end_game()
        else:
            self.next_player()
    
    def next_player(self):
        """Passe au joueur suivant"""
        # Si on est dans le dernier tour, décrémenter le compteur des joueurs restants
        if self.final_round_started and self.final_round_players_remaining > 0:
            self.final_round_players_remaining -= 1
        
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Si on revient au premier joueur, incrémenter le tour
        if self.current_player_index == 0:
            self.turn_count += 1
    
    def end_game(self):
        """Termine la partie et détermine le gagnant"""
        self.game_over = True
        # Le gagnant est le joueur avec le score le plus élevé
        self.winner = max(self.players, key=lambda p: p.total_score)
    
    def is_farkle(self) -> bool:
        """Vérifie si le lancé actuel est un Farkle"""
        return Dice.is_farkle(self.last_dice_roll)
    
    def get_game_status(self) -> dict:
        """Retourne l'état actuel du jeu"""
        return {
            'current_player': self.get_current_player().name,
            'current_player_index': self.current_player_index,
            'turn_count': self.turn_count,
            'game_over': self.game_over,
            'winner': self.winner.name if self.winner else None,
            'players': [
                {
                    'name': player.name,
                    'total_score': player.total_score,
                    'turn_score': player.turn_score,
                    'banked_dice_count': len(player.banked_dice),
                    'is_on_board': player.is_on_board
                }
                for player in self.players
            ],
            'last_dice_roll': self.last_dice_roll,
            'shared_banked_dice': self.shared_banked_dice,
            'remaining_dice_count': self.get_remaining_dice_count(),
            'last_player_banked': self.last_player_banked,
            'turn_score_to_transfer': self.turn_score_to_transfer,
            'final_round_started': self.final_round_started,
            'final_round_triggerer': self.final_round_triggerer.name if self.final_round_triggerer else None,
            'final_round_players_remaining': self.final_round_players_remaining
        }
    
    def save_game(self, filename: str = None) -> str:
        """
        Sauvegarde la partie actuelle
        
        Args:
            filename: Nom du fichier (optionnel)
            
        Returns:
            Chemin du fichier de sauvegarde
        """
        game_data = self.game_state.export_game_data(self)
        return self.game_state.save_game(game_data, filename)
    
    def load_game(self, filename: str):
        """
        Charge une partie sauvegardée
        
        Args:
            filename: Nom du fichier à charger
        """
        data = self.game_state.load_game(filename)
        (self.players, self.current_player_index, self.game_over, 
         self.winner, self.turn_count, self.last_dice_roll,
         self.shared_banked_dice, self.last_player_banked, 
         self.turn_score_to_transfer, self.final_round_started,
         self.final_round_triggerer, self.final_round_players_remaining) = self.game_state.import_game_data(data)
    
    def get_leaderboard(self) -> List[Player]:
        """Retourne le classement des joueurs par score"""
        return sorted(self.players, key=lambda p: p.total_score, reverse=True)
    
    def can_continue_turn(self) -> bool:
        """Vérifie si le joueur actuel peut continuer son tour"""
        return (not self.game_over and 
                self.get_remaining_dice_count() > 0 and
                not self.is_farkle())
    
    def reset_game(self):
        """Remet à zéro la partie actuelle"""
        for player in self.players:
            player.total_score = 0
            player.turn_score = 0
            player.banked_dice = []
            player.is_on_board = False
        
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        self.turn_count = 1
        self.last_dice_roll = []
        self.shared_banked_dice = []
        self.last_player_banked = False
        self.turn_score_to_transfer = 0
        self.final_round_started = False
        self.final_round_triggerer = None
        self.final_round_players_remaining = 0 