#!/usr/bin/env python3
"""
Farkle 10000 - Jeu de dés en Python
Point d'entrée principal de l'application
"""

import sys
from view.cli import FarkleCLI


def main():
    """Fonction principale"""
    try:
        # Créer et lancer l'interface CLI
        cli = FarkleCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nAu revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 