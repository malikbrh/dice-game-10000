import json
import os
from datetime import datetime
from typing import Dict, List, Any

from src.model.player import Player


class GameState:
    """Classe pour gérer la sauvegarde et le chargement de l'état du jeu"""

    SAVE_DIR = "saves"

    def __init__(self) -> None:
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)

    def save_game(self, game_data: Dict[str, Any], filename: str = None) -> str:
        """
        Sauvegarde l'état du jeu dans un fichier JSON
        
        Args:
            game_data: Données du jeu à sauvegarder
            filename: Nom du fichier (optionnel)
        
        Returns:
            Chemin du fichier de sauvegarde
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"farkle_save_{timestamp}.json"

        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.SAVE_DIR, filename)

        # Ajouter timestamp à la sauvegarde
        game_data['saved_at'] = datetime.now().isoformat()

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_data, f, indent=2, ensure_ascii=False)

        return filepath

    def load_game(self, filename: str) -> Dict[str, Any]:
        """
        Charge l'état du jeu depuis un fichier JSON
        
        Args:
            filename: Nom du fichier à charger
        
        Returns:
            Données du jeu
        """
        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Fichier de sauvegarde non trouvé: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_saves(self) -> List[Dict[str, str]]:
        """
        Liste toutes les sauvegardes disponibles
        
        Returns:
            Liste des informations sur les sauvegardes
        """
        saves = []

        if not os.path.exists(self.SAVE_DIR):
            return saves

        for filename in os.listdir(self.SAVE_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(self.SAVE_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    save_info = {
                        'filename': filename,
                        'filepath': filepath,
                        'saved_at': data.get('saved_at', 'Inconnu'),
                        'current_player': data.get('current_player_index', 0),
                        'players': [p['name'] for p in data.get('players', [])]
                    }
                    saves.append(save_info)
                except (json.JSONDecodeError, IOError):
                    continue

        # Trier par date de sauvegarde (plus récent en premier)
        saves.sort(key=lambda x: x['saved_at'], reverse=True)
        return saves

    def delete_save(self, filename: str) -> bool:
        """
        Supprime une sauvegarde
        
        Args:
            filename: Nom du fichier à supprimer
        
        Returns:
            True si suppression réussie, False sinon
        """
        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.SAVE_DIR, filename)

        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except IOError:
            pass

        return False

    @staticmethod
    def export_game_data(game) -> Dict[str, Any]:
        """
        Exporte les données du jeu vers un dictionnaire
        
        Args:
            game: Instance du jeu à exporter
        
        Returns:
            Dictionnaire contenant toutes les données du jeu
        """
        return {
            'players': [
                {
                    'name': player.name,
                    'total_score': player.total_score,
                    'turn_score': player.turn_score,
                    'banked_dice': player.banked_dice,
                    'is_on_board': player.is_on_board
                }
                for player in game.players
            ],
            'current_player_index': game.current_player_index,
            'game_over': game.game_over,
            'winner': game.winner.name if game.winner else None,
            'turn_count': game.turn_count,
            'last_dice_roll': game.last_dice_roll,
            'shared_banked_dice': game.shared_banked_dice,
            'last_player_banked': game.last_player_banked,
            'turn_score_to_transfer': game.turn_score_to_transfer,
            'final_round_started': game.final_round_started,
            'final_round_triggerer': game.final_round_triggerer.name if game.final_round_triggerer else None,
            'final_round_players_remaining': game.final_round_players_remaining,
            'version': '1.5'
        }

    @staticmethod
    def import_game_data(
            data: Dict[str, Any]
    ) -> tuple[List[Player], int, bool, Player, int, List[int], List[int], bool, int, int, Player, int]:
        """
        Importe les données du jeu depuis un dictionnaire
        
        Args:
            data: Dictionnaire contenant les données du jeu
        
        Returns:
            Tuple (players, current_player_index, game_over, winner, turn_count, last_dice_roll, shared_banked_dice, last_player_banked, turn_score_to_transfer, final_round_started, final_round_triggerer, final_round_players_remaining)
        """

        players = []
        for player_data in data['players']:
            player = Player(player_data['name'])
            player.total_score = player_data['total_score']
            player.turn_score = player_data['turn_score']
            player.banked_dice = player_data['banked_dice']
            player.is_on_board = player_data['is_on_board']
            players.append(player)

        current_player_index = data['current_player_index']
        game_over = data['game_over']
        winner = None
        if data['winner'] and players:
            winner = next((p for p in players if p.name == data['winner']), None)

        turn_count = data.get('turn_count', 1)
        last_dice_roll = data.get('last_dice_roll', [])
        shared_banked_dice = data.get('shared_banked_dice', [])
        last_player_banked = data.get('last_player_banked', False)
        turn_score_to_transfer = data.get('turn_score_to_transfer', 0)
        final_round_started = data.get('final_round_started', False)

        final_round_triggerer = None
        if data.get('final_round_triggerer') and players:
            final_round_triggerer = next((p for p in players if p.name == data['final_round_triggerer']), None)

        final_round_players_remaining = data.get('final_round_players_remaining', 0)

        return players, current_player_index, game_over, winner, turn_count, last_dice_roll, shared_banked_dice, \
            last_player_banked, turn_score_to_transfer, final_round_started, final_round_triggerer, \
            final_round_players_remaining
