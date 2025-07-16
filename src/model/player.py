from typing import List


class Player:
    """Classe pour représenter un joueur du jeu Farkle"""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.total_score = 0
        self.turn_score = 0
        self.banked_dice = []
        self.is_on_board = False  # Joueur doit faire au moins 800 points pour être "sur le plateau"
        
    def add_turn_score(self, score: int, dice_used: List[int]) -> None:
        """Ajoute des points au score du tour actuel"""
        self.turn_score += score
        self.banked_dice.extend(dice_used)
        
    def reset_turn(self) -> None:
        """Remet à zéro le score du tour et les dés conservés"""
        self.turn_score = 0
        self.banked_dice = []
        
    def get_remaining_dice_count(self) -> int:
        """Retourne le nombre de dés restants à lancer"""
        return 6 - len(self.banked_dice)
    
    def can_win(self) -> bool:
        """Vérifie si le joueur peut gagner (score total >= 10000)"""
        # Un joueur ne peut gagner que s'il est sur le plateau
        if not self.is_on_board:
            return False
        return self.total_score >= 10000
    
    def __str__(self) -> str:
        return f"{self.name}: {self.total_score} points (tour: {self.turn_score})"
    
    def __repr__(self) -> str:
        return f"Player(name='{self.name}', total_score={self.total_score}, turn_score={self.turn_score})" 