"""
Système d'authentification et de logging pour le dashboard
"""
import streamlit as st
import hashlib
import datetime
import json
import os
from pathlib import Path

# Configuration des utilisateurs (dans un vrai système, utiliser une base de données)
# Les mots de passe sont hashés pour la sécurité
def hash_password(password):
    """Hash un mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Utilisateurs autorisés avec mots de passe hashés
AUTHORIZED_USERS = {
    "Julien": hash_password("jo0v2"),
    "Loic": hash_password("FNOA3SAfj*v5h%")
}

def create_log_entry(username, action, details=""):
    """Crée une entrée de log pour tracer les connexions"""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "username": username,
        "action": action,
        "details": details,
        "ip": st.session_state.get("client_ip", "Unknown")
    }
    
    # Créer le dossier logs s'il n'existe pas
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Nom du fichier de log du jour
    log_file = log_dir / f"access_{datetime.datetime.now().strftime('%Y%m%d')}.json"
    
    # Lire les logs existants ou créer une liste vide
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    else:
        logs = []
    
    # Ajouter la nouvelle entrée
    logs.append(log_entry)
    
    # Sauvegarder
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return log_entry

def check_password():
    """Vérifie les credentials et gère la session"""
    
    # CSS pour la page de connexion
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 2px solid #bee3f8;
            margin-top: 5rem;
        }
        
        .login-header {
            text-align: center;
            color: #1e3a5f;
            margin-bottom: 2rem;
        }
        
        .login-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .login-subtitle {
            color: #666;
            font-size: 0.9rem;
        }
        
        .stTextInput > div > div > input {
            border-radius: 4px;
        }
        
        .security-notice {
            background: #f8f9fa;
            padding: 0.8rem;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #666;
            margin-top: 1rem;
            border-left: 3px solid #bee3f8;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialiser l'état de session
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    
    # Si déjà connecté, afficher les infos de session
    if st.session_state["authentication_status"]:
        # Sidebar avec infos utilisateur
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **Utilisateur:** {st.session_state['username']}")
            st.markdown(f"🕐 **Connecté depuis:** {st.session_state.get('login_time', 'Unknown')}")
            
            if st.button("🚪 Déconnexion", use_container_width=True):
                # Logger la déconnexion
                create_log_entry(
                    st.session_state["username"],
                    "LOGOUT",
                    f"Session duration: {datetime.datetime.now() - datetime.datetime.fromisoformat(st.session_state.get('login_time_raw', datetime.datetime.now().isoformat()))}"
                )
                
                # Réinitialiser la session
                st.session_state["authentication_status"] = None
                st.session_state["username"] = None
                st.session_state["login_time"] = None
                st.session_state["login_time_raw"] = None
                st.rerun()
        
        return True
    
    # Formulaire de connexion
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-header">
            <div class="login-title">🔐 Authentification</div>
            <div class="login-subtitle">Dashboard Achats Cacao - BON PLEIN</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
            submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")
            
            if submit:
                # Vérifier les credentials
                if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == hash_password(password):
                    # Connexion réussie
                    st.session_state["authentication_status"] = True
                    st.session_state["username"] = username
                    st.session_state["login_time"] = datetime.datetime.now().strftime("%H:%M")
                    st.session_state["login_time_raw"] = datetime.datetime.now().isoformat()
                    
                    # Logger la connexion
                    create_log_entry(username, "LOGIN_SUCCESS", "Authentication successful")
                    
                    st.success("✅ Connexion réussie!")
                    st.balloons()
                    st.rerun()
                else:
                    # Échec de connexion
                    create_log_entry(
                        username if username else "Unknown",
                        "LOGIN_FAILED",
                        "Invalid credentials"
                    )
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect")
        
        st.markdown("""
        <div class="security-notice">
            🔒 <strong>Connexion sécurisée</strong><br>
            Toutes les connexions sont enregistrées et tracées.<br>
            Données confidentielles - Usage autorisé uniquement.
        </div>
        """, unsafe_allow_html=True)
    
    return False

def show_access_logs():
    """Affiche les logs d'accès pour les administrateurs"""
    if st.session_state.get("username") == "Julien":  # Admin uniquement
        with st.expander("📋 Logs d'accès (Admin)"):
            log_dir = Path("logs")
            if log_dir.exists():
                log_files = sorted(log_dir.glob("access_*.json"), reverse=True)
                
                if log_files:
                    # Sélectionner le fichier de log
                    selected_file = st.selectbox(
                        "Fichier de log",
                        log_files,
                        format_func=lambda x: x.stem.replace("access_", "")
                    )
                    
                    # Charger et afficher les logs
                    with open(selected_file, 'r') as f:
                        logs = json.load(f)
                    
                    # Convertir en DataFrame pour un meilleur affichage
                    import pandas as pd
                    df_logs = pd.DataFrame(logs)
                    
                    # Filtrer par type d'action
                    action_filter = st.multiselect(
                        "Filtrer par action",
                        ["LOGIN_SUCCESS", "LOGIN_FAILED", "LOGOUT"],
                        default=["LOGIN_SUCCESS", "LOGIN_FAILED", "LOGOUT"]
                    )
                    
                    if action_filter:
                        df_logs = df_logs[df_logs['action'].isin(action_filter)]
                    
                    # Afficher le tableau
                    st.dataframe(
                        df_logs[['timestamp', 'username', 'action', 'details']],
                        use_container_width=True
                    )
                    
                    # Statistiques
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total connexions", len(df_logs[df_logs['action'] == 'LOGIN_SUCCESS']))
                    with col2:
                        st.metric("Échecs connexion", len(df_logs[df_logs['action'] == 'LOGIN_FAILED']))
                    with col3:
                        st.metric("Utilisateurs uniques", df_logs['username'].nunique())
                else:
                    st.info("Aucun log disponible")
            else:
                st.info("Dossier de logs non trouvé")