# Farkle 10000 - Jeu de dés en Python 🎲

Implémentation complète du jeu de dés Farkle (10000) en Python avec interface CLI, démarré le 15.07.2025.

**Implémenté par Malik, pour les copains de chez Badger !**

## 🎯 Fonctionnalités

- ✅ **Gestion de 2-8 joueurs** avec noms personnalisés
- ✅ **Sauvegarde/Chargement** de parties en cours
- ✅ **Règles intégrées** consultables dans le jeu, et dans le fichier `game-rules.pdf`

## 🎮 Règles du Farkle

### Objectif
Être le premier joueur à atteindre 10 000 points.


### Déroulement
1. Lancez 6 dés
2. Conservez des dés qui rapportent des points
3. Continuez avec les dés restants ou "bankez" votre score
4. **FARKLE** = aucun dé ne peut être conservé → perte du tour
5. Il faut **800 points minimum** pour être "sur le plateau"

## 🚀 Installation

1. Clonez le repository :
```bash
git clone <votre-repo-url>
cd dice-game-10000
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez le jeu :
```bash
python src/main.py
```

## 📁 Structure du projet

```
dice-game-10000/src/
├── main.py              # Point d'entrée principal
├── model/
│   ├── player.py        # Gestion des joueurs
│   ├── dice.py          # Gestion des dés et scoring
│   ├── game.py          # Logique principale du jeu
├── state/
│   ├── game_state.py    # Sauvegarde/chargement des parties en JSON
├── view/
│   ├── cli.py           # Interface utilisateur CLI
├── saves/               # Dossier des sauvegardes (auto-créé)
├── requirements.in      # Dépendances sources
└── requirements.txt     # Dépendances générées (pip-compile)
```

## 🎯 Utilisation

### Menu principal
1. **Nouvelle partie** - Créer une nouvelle partie
2. **Charger une partie** - Reprendre une partie sauvegardée
3. **Règles du jeu** - Consulter les règles
4. **Quitter** - Fermer l'application

### Pendant le jeu
- **Lancer les dés** - Lance les dés disponibles
- **Banker le score** - Transfère le score du tour au total, potentiellement relancé par le prochain joueur
- **Sauvegarder** - Sauvegarde la partie actuelle
- **Voir le classement** - Affiche le classement des joueurs
- **Quitter** - Quitte la partie

### Sauvegardes
Les parties sont automatiquement sauvegardées dans le dossier `saves/` au format JSON avec horodatage.

## 🛠️ Développement

### Dépendances
- `colorama` - Couleurs dans le terminal
- `click` - Interface CLI

## 📝 Exemples d'utilisation

### Nouveau jeu
```bash
python main.py
# Sélectionnez "1" pour nouvelle partie
# Entrez les noms des joueurs (2-8)
# Jouez !
```

### Charger une partie
```bash
python main.py
# Sélectionnez "2" pour charger
# Choisissez la sauvegarde à charger
```


## Bonne chance et que le meilleur gagne ! 🎲🏆
