import random
from collections import Counter
from typing import List, Tuple, Dict


class Dice:
    """Classe pour gérer les dés et les règles de scoring du Farkle"""
    
    def __init__(self, num_dice: int = 6):
        self.num_dice = num_dice
        self.dice_values = []
        
    def roll(self, num_dice: int = None) -> List[int]:
        """Lance les dés"""
        if num_dice is None:
            num_dice = self.num_dice
        self.dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        return self.dice_values
    
    def get_dice_values(self) -> List[int]:
        """Retourne les valeurs actuelles des dés"""
        return self.dice_values.copy()
    
    @staticmethod
    def calculate_score(dice_values: List[int]) -> Tuple[int, List[int]]:
        """
        Calcule le score pour des dés donnés et retourne les dés utilisés pour le score
        
        
        Règles de scoring Farkle:
        - 1 = 100 points
        - 5 = 50 points
        - Trois 1 = 1000 points
        - Trois 2 = 200 points
        - Trois 3 = 300 points
        - Trois 4 = 400 points
        - Trois 5 = 500 points
        - Trois 6 = 600 points
        - Pour chaque nombre au-delà de trois identiques, doublez le montant (par exemple, trois 2 = 200, quatre 2 = 400, cinq 2 = 800, six 2 = 1600).
        - Paires et Straights :
            - Lorsqu'un joueur lance 1, 2, 3, 4, 5, 6 en lançant les 6 dés, c'est un Straight.
            - Lorsqu'un joueur obtient 3 paires en lançant 6 dés, ce sont des paires.
            - Les paires et les Straights valent 1000 points.
        Note : Trois d'une sorte doivent tous être lancés ensemble. Lancer un 1, puis un autre 1 et encore un 1 vaut 300. Lancer 3 1 d'un coup vaut 1000.
        
        """
        if not dice_values:
            return 0, []
        
        # Vérifier d'abord les cas spéciaux (seulement si on a exactement 6 dés)
        if len(dice_values) == 6:
            # Vérifier le straight (1,2,3,4,5,6)
            if sorted(dice_values) == [1, 2, 3, 4, 5, 6]:
                return 1000, sorted(dice_values)
            
            # Vérifier les 3 paires (exemple : 22 33 44)
            counter = Counter(dice_values)
            if len(counter) == 3 and all(count == 2 for count in counter.values()):
                return 1000, sorted(dice_values)
        
        counter = Counter(dice_values)
        score = 0
        used_dice = []
        
        # Traiter les groupes de 3 ou plus d'abord
        for value, count in counter.items():
            if count >= 3:
                base_score = 1000 if value == 1 else value * 100
                # Appliquer le multiplicateur correct : 3=1x, 4=2x, 5=4x, 6=8x (doubler à chaque fois)
                multiplier = 2 ** (count - 3)
                score += base_score * multiplier
                used_dice.extend([value] * count)
                
        # Traiter les 1 et 5 restants (seulement s'ils n'ont pas été utilisés dans un groupe de 3+)
        for value in [1, 5]:
            remaining_count = counter[value] if counter[value] < 3 else 0
            if remaining_count > 0:
                if value == 1:
                    score += remaining_count * 100
                else:  # value == 5
                    score += remaining_count * 50
                used_dice.extend([value] * remaining_count)
        
        return score, sorted(used_dice)
    
    @staticmethod
    def get_possible_combinations(dice_values: List[int]) -> List[Tuple[int, List[int]]]:
        """
        Retourne toutes les combinaisons possibles de dés qui peuvent être conservés
        """
        if not dice_values:
            return []
        
        combinations = []
        counter = Counter(dice_values)
        
        # Génère toutes les combinaisons possibles de dés.
        # Chaque nombre i de 1 à 2**len(dice_values) - 1 représente une combinaison unique.
        # La représentation binaire de i indique quels dés sont inclus dans la combinaison.
        # Exemple concret avec les dés [1, 2, 3] :
        # i = 1 (binaire: 001) → combo = [1] (seulement le premier dé)
        # i = 2 (binaire: 010) → combo = [2] (seulement le deuxième dé)
        # i = 3 (binaire: 011) → combo = [1, 2] (premier et deuxième dés)
        # i = 4 (binaire: 100) → combo = [3] (seulement le troisième dé)
        # etc.
        for i in range(1, 2**len(dice_values)):
            combo = [dice_values[j] for j in range(len(dice_values)) if (i >> j) & 1]
            
            score, used_dice = Dice.calculate_score(combo)
            if score > 0 and sorted(combo) == sorted(used_dice):
                combinations.append((score, combo))
        
        # Supprimer les doublons et trier par score
        unique_combinations = []
        seen = set()
        for score, combo in combinations:
            # tuple, pour regrouper les dés, sorted pour n'avoir que des combinaisons uniques, 3 1 2 est identique à 1 2 3
            combo_key = tuple(sorted(combo))
            if combo_key not in seen:
                seen.add(combo_key)
                unique_combinations.append((score, combo))
        # trier par score, le plus haut score en premier pour suggérer les meilleures options
        return sorted(unique_combinations, reverse=True)
    
    @staticmethod
    def is_farkle(dice_values: List[int]) -> bool:
        """Vérifie si c'est un Farkle (aucun dé ne peut être conservé)"""
        score, _ = Dice.calculate_score(dice_values)
        return score == 0 