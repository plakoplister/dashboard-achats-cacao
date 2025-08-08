# Point d'entrée pour Streamlit Cloud
# Ce fichier permet à Streamlit Cloud de détecter automatiquement l'application

import streamlit as st
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Importer et exécuter l'application principale
if __name__ == "__main__":
    from analyse_cacao import main
    main()