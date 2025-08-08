# Version optimisée pour Streamlit Cloud
import streamlit as st
from analyse_cacao import main

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Achats Cacao - Côte d'Ivoire",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# Exécuter l'application
if __name__ == "__main__":
    main()