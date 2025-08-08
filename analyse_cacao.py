import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
from auth import check_password, show_access_logs

st.set_page_config(
    page_title="Dashboard Achats Cacao - Côte d'Ivoire",
    page_icon="📊",
    layout="wide"
)

# Styles CSS BON PLEIN
st.markdown("""
<style>
    /* Variables CSS BON PLEIN */
    :root {
        --bleu-principal-fonce: #1e3a5f;
        --bleu-principal-moyen: #2c5282;
        --bleu-clair-accent: #bee3f8;
    }
    
    /* Header principal avec cadre élégant */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
        padding: 2rem !important;
        margin: -1rem -1rem 2rem -1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3) !important;
        border: 2px solid #bee3f8 !important;
        display: block !important;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .main-title {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 300 !important;
        margin: 0 !important;
        text-align: center;
        font-family: Arial, sans-serif !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: #bee3f8 !important;
        font-size: 1.2rem !important;
        text-align: center;
        margin: 0.5rem 0 0 0 !important;
        font-weight: 300 !important;
        font-family: Arial, sans-serif !important;
    }
    
    /* Métriques avec style BON PLEIN */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #bee3f8;
        padding: 1rem;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] > div > div {
        color: #1e3a5f !important;
        font-weight: 600 !important;
    }
    
    /* Footer */
    .footer {
        background: #f8f9fa;
        padding: 1rem;
        text-align: center;
        color: #666;
        margin-top: 2rem;
        border-top: 1px solid #bee3f8;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path, sheet_name='dB ACHAT'):
    """Charge les données depuis le fichier Excel"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Utiliser la première ligne comme en-têtes de colonnes
        new_columns = df.iloc[0].astype(str).tolist()
        df.columns = new_columns
        
        # Supprimer la première ligne qui contenait les en-têtes
        df = df.iloc[1:].reset_index(drop=True)
        
        # Pour dB EXPORT, renommer les colonnes pour cohérence
        if sheet_name == 'dB EXPORT':
            rename_map = {
                'ABJ': 'ABIDJAN',
                'SP': 'SAN PEDRO',
                'Total général': 'Total Exporté'
            }
            df = df.rename(columns=rename_map)
            # Ajouter colonne INTERIEUR si elle n'existe pas
            if 'INTERIEUR' not in df.columns:
                df['INTERIEUR'] = 0
        
        # Nettoyer les colonnes numériques
        numeric_cols = ['Volume livré (kg)', 'ABIDJAN', 'INTERIEUR', 'SAN PEDRO', 'Volume exporté (kg)', 'Total Exporté']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Nettoyer les colonnes texte
        text_cols = ['Code fournisseur', 'Nom fournisseur', 'Exportateurs', 'EXPORTATEUR SIMPLE', 'Region activité']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', 'Non renseigné').fillna('Non renseigné')
        
        # Pour la feuille ACHAT uniquement: Filtrer les lignes "Non renseigné"
        if sheet_name == 'dB ACHAT':
            df = df[
                (df['Nom fournisseur'] != 'Non renseigné') & 
                (df['EXPORTATEUR SIMPLE'] != 'Non renseigné')
            ].copy()
        
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

# Configuration des couleurs BON PLEIN pour les graphiques
BON_PLEIN_COLORS = {
    'primary': '#1e3a5f',
    'secondary': '#2c5282', 
    'accent': '#bee3f8',
    'text': '#2c3e50',
    'text_secondary': '#666',
    'palette': ['#1e3a5f', '#2c5282', '#bee3f8', '#4a5568', '#2d3748', '#1a202c', '#718096', '#4299e1', '#63b3ed', '#90cdf4']
}

def format_number(num):
    """Formate un nombre selon les standards BON PLEIN : Arial, pas de virgule, séparateur milliers"""
    if isinstance(num, (int, float)):
        # Toujours convertir en entier et ajouter séparateur de milliers
        return f"{int(num):,}".replace(",", " ")
    return str(num)

def format_tonnage(kg_value):
    """Formate un tonnage : XXX XXX tonnes"""
    tonnes = kg_value / 1000
    return f"{format_number(tonnes)} tonnes"

def apply_bon_plein_theme(fig):
    """Applique le thème BON PLEIN à un graphique Plotly"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color=BON_PLEIN_COLORS['text']
        ),
        title=dict(
            font=dict(size=16, color=BON_PLEIN_COLORS['primary'], weight='normal'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(190, 227, 248, 0.3)',
            linecolor=BON_PLEIN_COLORS['accent'],
            tickcolor=BON_PLEIN_COLORS['secondary']
        ),
        yaxis=dict(
            gridcolor='rgba(190, 227, 248, 0.3)', 
            linecolor=BON_PLEIN_COLORS['accent'],
            tickcolor=BON_PLEIN_COLORS['secondary']
        ),
        colorway=BON_PLEIN_COLORS['palette']
    )
    return fig

def main():
    # Vérifier l'authentification
    if not check_password():
        st.stop()
    
    # Header BON PLEIN avec composants Streamlit natifs
    header_container = st.container()
    
    with header_container:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%); 
                    padding: 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 16px;">
        </div>
        """, unsafe_allow_html=True)
        
        # Utiliser les colonnes Streamlit pour la mise en page
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            # Container blanc pour le logo
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.2); text-align: center; 
                        position: relative; top: -100px; z-index: 10;">
                <img src="https://raw.githubusercontent.com/plakoplister/caca-dashboard-ci/main/assets/logo.png" 
                     alt="BON PLEIN" style="height: 80px; width: auto;">
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="position: relative; top: -120px; z-index: 10;">
                <h1 style="color: white; font-size: 2.5rem; font-weight: bold; 
                           margin: 0; text-align: center;">
                    Achats de cacao en Côte d'Ivoire
                </h1>
                <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem; 
                          text-align: center; margin: 0.5rem 0 0 0;">
                    Dashboard des Achats Cacaoyers (2013-2025)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: right; color: rgba(255,255,255,0.7); 
                        font-size: 1.1rem; position: relative; top: -100px; z-index: 10;">
                <div>Bon Plein</div>
                <div>Capital</div>
                <div>Analytics</div>
                <div>Solution</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chargement direct du fichier local
    df = None
    
    default_file = Path("Master_Data/DB - Achat Cacao - 2022021.xlsx")
    if default_file.exists():
        df = load_data(default_file, sheet_name='dB ACHAT')
        df_export = load_data(default_file, sheet_name='dB EXPORT')
        st.success(f"Données chargées: {format_number(len(df))} lignes (Achats) et {format_number(len(df_export) if df_export is not None else 0)} lignes (Exports)")
    else:
        st.error("Fichier de données non trouvé: Master_Data/DB - Achat Cacao - 2022021.xlsx")
        df_export = None
    
    if df is not None:
        # Sidebar pour les filtres
        st.sidebar.header("Filtres")
        
        # Affichage des informations sur les données
        with st.expander("Aperçu des données"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dimensions:**", df.shape)
                st.write("**Nombre d'exportateurs:**", df['EXPORTATEUR SIMPLE'].nunique())
                st.write("**Nombre de fournisseurs:**", df['Nom fournisseur'].nunique())
            
            with col2:
                st.write("**Volume total:**", f"{format_number(df['Volume livré (kg)'].sum())} kg")
                st.write("**Moyenne par ligne:**", f"{format_number(df['Volume livré (kg)'].mean())} kg")
            
            with st.expander("Détails techniques"):
                st.write("**Colonnes:**", df.columns.tolist())
                st.write("**Types de données:**", df.dtypes.to_dict())
                st.write("**Premières lignes:**")
                st.dataframe(df.head(3), use_container_width=True)
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Vue Achats",
            "Fournisseurs", 
            "Écarts Achats/Exports",
            "ABJ vs SP",
            "Données Brutes"
        ])
        
        with tab1:
            st.header("Vue d'Ensemble des Achats")
            analyse_achats_exports(df)
        
        with tab2:
            st.header("Plus Grands Fournisseurs par Exportateur")
            analyse_fournisseurs(df)
        
        with tab3:
            st.header("Différences de Poids Achat/Export")
            if df_export is not None:
                analyse_differences_poids(df, df_export)
            else:
                st.error("Données d'export non disponibles")
        
        with tab4:
            st.header("Comparaison Tendances ABJ vs SP")
            if df_export is not None:
                analyse_abj_vs_sp(df_export)
            else:
                st.error("Données d'export non disponibles")
        
        with tab5:
            st.header("Données Brutes")
            st.dataframe(df, use_container_width=True)
    
    else:
        st.info("Veuillez charger un fichier de données pour commencer l'analyse")
    
    # Footer BON PLEIN
    st.markdown("""
    <div class="footer">
        <p><strong>BON PLEIN Capital Analytics Solution</strong> | 
        Dashboard Achats Cacao - Côte d'Ivoire | 
        v2.2.3 - Décembre 2024 | 
        Données confidentielles - Usage interne uniquement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher les logs d'accès pour l'admin
    show_access_logs()

def analyse_achats_exports(df):
    """Vue d'ensemble des ACHATS uniquement (les exports viennent d'une autre base)"""
    
    st.info("**Focus ACHATS :** Cette base contient les achats aux fournisseurs. Les données d'export viennent d'une autre base (voir onglet Écarts pour comparaison).")
    
    # Calculs ACHATS uniquement
    total_achete_global = df['Volume livré (kg)'].sum()
    
    # Métriques principales - ACHATS SEULEMENT
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Acheté aux Fournisseurs", 
            f"{format_tonnage(total_achete_global)}",
            f"{format_number(total_achete_global)} kg"
        )
    
    with col2:
        nb_fournisseurs = df['Nom fournisseur'].nunique()
        st.metric(
            "Nombre de Fournisseurs",
            f"{format_number(nb_fournisseurs)}",
            "fournisseurs uniques"
        )
    
    with col3:
        nb_exportateurs = df['EXPORTATEUR SIMPLE'].nunique()
        st.metric(
            "Nombre d'Exportateurs",
            f"{format_number(nb_exportateurs)}",
            "exportateurs actifs"
        )
    
    # Consolidation ACHATS par EXPORTATEUR
    st.subheader("Achats par Exportateur")
    
    consolidation_achats = df.groupby('EXPORTATEUR SIMPLE').agg({
        'Volume livré (kg)': 'sum',        # Ce qu'ils ont acheté aux fournisseurs
        'Nom fournisseur': 'nunique'       # Nombre de fournisseurs différents
    }).round(0)
    
    # Renommer colonnes
    consolidation_achats.rename(columns={
        'Nom fournisseur': 'Nb Fournisseurs'
    }, inplace=True)
    
    # Calculer pourcentages
    consolidation_achats['% du Total'] = (consolidation_achats['Volume livré (kg)'] / total_achete_global * 100).round(1)
    
    # Trier par volume acheté
    consolidation_achats = consolidation_achats.sort_values('Volume livré (kg)', ascending=False)
    
    # Graphiques des achats
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 exportateurs par achats
        top_10_achats = consolidation_achats.head(10)
        
        fig = px.bar(
            x=top_10_achats.index,
            y=top_10_achats['Volume livré (kg)'],
            title="Top 10 Exportateurs par Achats",
            labels={'x': 'Exportateur', 'y': 'Volume Acheté (kg)'},
            color_discrete_sequence=[BON_PLEIN_COLORS['primary']]
        )
        fig.update_xaxes(tickangle=45)
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Diversification des fournisseurs
        fig = px.scatter(
            consolidation_achats,
            x='Nb Fournisseurs',
            y='Volume livré (kg)',
            size='% du Total',
            hover_name=consolidation_achats.index,
            title="Volume vs Nombre de Fournisseurs",
            labels={'x': 'Nombre de Fournisseurs', 'y': 'Volume Acheté (kg)'},
            color_discrete_sequence=[BON_PLEIN_COLORS['secondary']]
        )
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistiques sur la concentration
    st.subheader("Analyse de Concentration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_5_pct = consolidation_achats.head(5)['% du Total'].sum()
        st.metric("Top 5 Exportateurs", f"{top_5_pct:.1f}%", "du marché")
    
    with col2:
        volume_moyen = consolidation_achats['Volume livré (kg)'].mean()
        st.metric("Volume moyen", f"{format_number(volume_moyen/1000)} tonnes", "par exportateur")
    
    with col3:
        fournisseurs_moyen = consolidation_achats['Nb Fournisseurs'].mean()
        st.metric("Fournisseurs moyen", f"{format_number(fournisseurs_moyen)}", "par exportateur")
    
    # Tableau de consolidation ACHATS
    st.subheader("Tableau des Achats par Exportateur")
    
    # Formatage pour affichage
    consolidation_display = consolidation_achats.copy()
    consolidation_display['Volume livré (kg)'] = consolidation_display['Volume livré (kg)'].apply(lambda x: format_number(x))
    consolidation_display['% du Total'] = consolidation_display['% du Total'].apply(lambda x: f"{x}%")
    
    st.dataframe(consolidation_display, use_container_width=True)

def analyse_fournisseurs(df):
    """1. Plus grands fournisseurs par EXPORTATEUR + 2. Plus grands fournisseurs du pays"""
    
    st.info("**Objectif :** 1) Identifier les principaux fournisseurs de chaque exportateur et leurs ports, 2) Voir les plus grands fournisseurs du pays et leur diversification")
    
    # PARTIE 1: Fournisseurs par EXPORTATEUR
    st.subheader("1. Plus Grands Fournisseurs par Exportateur")
    
    # Sélecteur d'exportateur
    unique_exportateurs = df['EXPORTATEUR SIMPLE'].dropna().unique()
    exportateurs = sorted([str(x) for x in unique_exportateurs if str(x) != 'nan' and str(x) != 'Non renseigné'])
    selected_exportateur = st.selectbox("Sélectionner un exportateur:", exportateurs)
    
    if selected_exportateur:
        # Filtrer pour l'exportateur sélectionné
        df_exp = df[df['EXPORTATEUR SIMPLE'] == selected_exportateur]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"### Fournisseurs de **{selected_exportateur}**")
            
            # Top fournisseurs pour cet exportateur
            fournisseurs_exp = df_exp.groupby('Nom fournisseur').agg({
                'Volume livré (kg)': 'sum',
                'Region activité': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Non spécifié'
            }).sort_values('Volume livré (kg)', ascending=False)
            
            # Volume total de l'exportateur
            total_exp = int(fournisseurs_exp['Volume livré (kg)'].sum())
            fournisseurs_exp['% du total'] = (fournisseurs_exp['Volume livré (kg)'] / total_exp * 100).round(1)
            
            # Affichage des métriques avec séparateurs de milliers
            total_exp_str = f"{total_exp:,}".replace(",", " ")
            total_tonnes_str = f"{int(total_exp/1000):,}".replace(",", " ")
            st.metric("Total acheté", f"{total_exp_str} kg", f"{total_tonnes_str} tonnes")
            st.metric("Nombre de fournisseurs", format_number(len(fournisseurs_exp)))
            
            # Top 10
            top_10_exp = fournisseurs_exp.head(10)
            for i, (fournisseur, data) in enumerate(top_10_exp.iterrows(), 1):
                st.write(f"**{i}. {fournisseur}** - {format_number(data['Volume livré (kg)'])} kg ({data['% du total']}%) - {data['Region activité']}")
        
        with col2:
            st.write(f"### Répartition par Port - **{selected_exportateur}**")
            
            # Volumes exportés par port pour cet exportateur
            ports_exp = df_exp.groupby('EXPORTATEUR SIMPLE').agg({
                'ABIDJAN': 'sum',
                'INTERIEUR': 'sum', 
                'SAN PEDRO': 'sum'
            }).iloc[0]
            
            total_exp_export = ports_exp.sum()
            
            if total_exp_export > 0:
                # Graphique en secteurs
                fig = px.pie(
                    values=[ports_exp['ABIDJAN'], ports_exp['INTERIEUR'], ports_exp['SAN PEDRO']],
                    names=['ABIDJAN', 'INTÉRIEUR', 'SAN PEDRO'],
                    title=f"Exports de {selected_exportateur} par Port",
                    color_discrete_sequence=BON_PLEIN_COLORS['palette']
                )
                fig = apply_bon_plein_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
                
                # Métriques par port
                st.write("**Détail par port:**")
                st.write(f"- ABIDJAN: {format_number(ports_exp['ABIDJAN'])} kg ({ports_exp['ABIDJAN']/total_exp_export*100:.1f}%)")
                st.write(f"- INTÉRIEUR: {format_number(ports_exp['INTERIEUR'])} kg ({ports_exp['INTERIEUR']/total_exp_export*100:.1f}%)")
                st.write(f"- SAN PEDRO: {format_number(ports_exp['SAN PEDRO'])} kg ({ports_exp['SAN PEDRO']/total_exp_export*100:.1f}%)")
            else:
                st.warning("Aucun volume d'export trouvé pour cet exportateur")
    
    # PARTIE 2: Plus grands fournisseurs du pays
    st.subheader("2. Plus Grands Fournisseurs du Pays")
    
    # Analyse globale des fournisseurs
    fournisseurs_pays = df.groupby('Nom fournisseur').agg({
        'Volume livré (kg)': 'sum',
        'EXPORTATEUR SIMPLE': 'nunique',  # Nombre d'exportateurs différents
        'Region activité': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Non spécifié'
    }).sort_values('Volume livré (kg)', ascending=False)
    
    fournisseurs_pays.rename(columns={'EXPORTATEUR SIMPLE': 'Nb Exportateurs'}, inplace=True)
    
    # Volume total pays
    total_pays = fournisseurs_pays['Volume livré (kg)'].sum()
    fournisseurs_pays['% du total pays'] = (fournisseurs_pays['Volume livré (kg)'] / total_pays * 100).round(1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 15 fournisseurs
        top_15_pays = fournisseurs_pays.head(15)
        
        fig = px.bar(
            x=top_15_pays['Volume livré (kg)'],
            y=top_15_pays.index,
            orientation='h',
            title="Top 15 Fournisseurs du Pays",
            labels={'x': 'Volume (kg)', 'y': 'Fournisseur'},
            color_discrete_sequence=[BON_PLEIN_COLORS['primary']]
        )
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Statistiques de diversification
        st.write("### Analyse de Diversification")
        
        # Fournisseurs par nombre d'exportateurs
        diversification = fournisseurs_pays['Nb Exportateurs'].value_counts().sort_index()
        
        fig = px.bar(
            x=diversification.index,
            y=diversification.values,
            title="Fournisseurs par Nb d'Exportateurs",
            labels={'x': 'Nombre d\'Exportateurs', 'y': 'Nombre de Fournisseurs'},
            color_discrete_sequence=[BON_PLEIN_COLORS['secondary']]
        )
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
        
        # Métriques de diversification
        mono_exportateur = len(fournisseurs_pays[fournisseurs_pays['Nb Exportateurs'] == 1])
        multi_exportateurs = len(fournisseurs_pays[fournisseurs_pays['Nb Exportateurs'] > 1])
        
        st.metric("Fournisseurs exclusifs (1 exportateur)", mono_exportateur)
        st.metric("Fournisseurs diversifiés (2+ exportateurs)", multi_exportateurs)
    
    # Tableau détaillé des top fournisseurs
    st.subheader("Top 20 Fournisseurs du Pays - Détail")
    
    top_20_display = fournisseurs_pays.head(20).copy()
    top_20_display['Volume livré (kg)'] = top_20_display['Volume livré (kg)'].apply(lambda x: format_number(x))
    top_20_display['% du total pays'] = top_20_display['% du total pays'].apply(lambda x: f"{x}%")
    
    st.dataframe(top_20_display, use_container_width=True)

def analyse_differences_poids(df_achats, df_exports):
    """Comparaison Achats (dB ACHAT) vs Exports (dB EXPORT) par EXPORTATEUR"""
    
    st.info("**Comparaison des bases :** Volumes achetés (dB ACHAT) vs Volumes exportés (dB EXPORT) pour identifier les écarts par exportateur et par port.")
    
    # Consolidation ACHATS par exportateur (depuis dB ACHAT)
    achats_data = df_achats.groupby('EXPORTATEUR SIMPLE').agg({
        'Volume livré (kg)': 'sum'  # Ce qui a été acheté aux fournisseurs
    }).round(0)
    
    # Consolidation EXPORTS par exportateur (depuis dB EXPORT)
    # Utiliser les colonnes ABIDJAN, INTERIEUR, SAN PEDRO ou Total Exporté
    export_cols = []
    if 'Total Exporté' in df_exports.columns:
        export_cols.append('Total Exporté')
    if all(col in df_exports.columns for col in ['ABIDJAN', 'INTERIEUR', 'SAN PEDRO']):
        export_cols.extend(['ABIDJAN', 'INTERIEUR', 'SAN PEDRO'])
    
    if export_cols:
        exports_data = df_exports.groupby('EXPORTATEUR SIMPLE').agg({
            col: 'sum' for col in export_cols if col in df_exports.columns
        }).round(0)
    else:
        st.error("Colonnes d'export non trouvées dans la feuille dB EXPORT")
        return
    
    # Fusionner achats et exports
    ecarts_data = achats_data.join(exports_data, how='outer').fillna(0)
    
    # Calculs des totaux et écarts
    if 'Total Exporté' not in ecarts_data.columns:
        if all(col in ecarts_data.columns for col in ['ABIDJAN', 'INTERIEUR', 'SAN PEDRO']):
            ecarts_data['Total Exporté'] = ecarts_data['ABIDJAN'] + ecarts_data['INTERIEUR'] + ecarts_data['SAN PEDRO']
        else:
            st.error("Impossible de calculer le total exporté")
            return
    
    ecarts_data['Écart (Acheté - Exporté)'] = ecarts_data['Volume livré (kg)'] - ecarts_data['Total Exporté']
    
    # Éviter division par zéro
    ecarts_data['% Écart'] = ecarts_data.apply(
        lambda row: (row['Écart (Acheté - Exporté)'] / row['Volume livré (kg)'] * 100) if row['Volume livré (kg)'] > 0 else 0, 
        axis=1
    ).round(1)
    
    # Filtrer les exportateurs avec activité significative
    ecarts_data = ecarts_data[
        (ecarts_data['Volume livré (kg)'] > 1000) | (ecarts_data['Total Exporté'] > 1000)
    ].sort_values('Écart (Acheté - Exporté)', key=abs, ascending=False)
    
    # Vue d'ensemble des écarts
    st.subheader("Vue d'Ensemble des Écarts")
    
    col1, col2, col3 = st.columns(3)
    
    # Statistiques globales
    total_achete_global = ecarts_data['Volume livré (kg)'].sum()
    total_exporte_global = ecarts_data['Total Exporté'].sum()
    ecart_global_total = total_achete_global - total_exporte_global
    
    with col1:
        st.metric("Total Acheté", f"{format_number(total_achete_global/1000)} tonnes", f"{format_number(total_achete_global)} kg")
    
    with col2:
        st.metric("Total Exporté", f"{format_number(total_exporte_global/1000)} tonnes", f"{format_number(total_exporte_global)} kg")
    
    with col3:
        pourcentage_global = (ecart_global_total / total_achete_global * 100) if total_achete_global > 0 else 0
        st.metric("Écart Global", f"{format_number(ecart_global_total/1000)} tonnes", f"{pourcentage_global:.1f}%")
        
        if pourcentage_global > 5:
            st.warning("Écart significatif")
        elif pourcentage_global > 0:
            st.success("Excédent (stock)")
        else:
            st.error("Déficit")
    
    # Écarts par EXPORTATEUR
    st.subheader("Écarts par Exportateur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique des écarts par exportateur
        top_15_ecarts = ecarts_data.head(15)
        
        fig = px.bar(
            x=top_15_ecarts.index,
            y=top_15_ecarts['% Écart'],
            title="Top 15 Exportateurs par % Écart",
            labels={'x': 'Exportateur', 'y': 'Écart (%)'},
            color=top_15_ecarts['% Écart'],
            color_continuous_scale=[[0, BON_PLEIN_COLORS['accent']], [0.5, 'white'], [1, BON_PLEIN_COLORS['primary']]]
        )
        fig.update_xaxes(tickangle=45)
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution des écarts
        fig = px.histogram(
            ecarts_data,
            x='% Écart',
            nbins=20,
            title="Distribution des Écarts par Exportateur",
            labels={'% Écart': 'Écart (%)', 'count': 'Nombre d\'Exportateurs'},
            color_discrete_sequence=[BON_PLEIN_COLORS['primary']]
        )
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analyse détaillée par port (si les colonnes existent)
    if all(col in ecarts_data.columns for col in ['ABIDJAN', 'INTERIEUR', 'SAN PEDRO']):
        st.subheader("Écarts par Port")
        
        st.write("**Analyse des volumes exportés par port vs achats globaux:**")
        
        # Totaux par port
        total_abj = ecarts_data['ABIDJAN'].sum()
        total_int = ecarts_data['INTERIEUR'].sum()
        total_sp = ecarts_data['SAN PEDRO'].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ABIDJAN", f"{format_number(total_abj/1000)} tonnes", f"{total_abj/total_exporte_global*100:.1f}% des exports" if total_exporte_global > 0 else "0%")
            
        with col2:
            st.metric("INTÉRIEUR", f"{format_number(total_int/1000)} tonnes", f"{total_int/total_exporte_global*100:.1f}% des exports" if total_exporte_global > 0 else "0%")
            
        with col3:
            st.metric("SAN PEDRO", f"{format_number(total_sp/1000)} tonnes", f"{total_sp/total_exporte_global*100:.1f}% des exports" if total_exporte_global > 0 else "0%")
        
        # Graphique répartition par port
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique en secteurs des exports
            fig = px.pie(
                values=[total_abj, total_int, total_sp],
                names=['ABIDJAN', 'INTÉRIEUR', 'SAN PEDRO'],
                title="Répartition des Exports par Port",
                color_discrete_sequence=BON_PLEIN_COLORS['palette']
            )
            fig = apply_bon_plein_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top exportateurs par port préféré
            port_preferences = []
            for idx, row in ecarts_data.iterrows():
                if pd.notna(row['ABIDJAN']) and pd.notna(row['INTERIEUR']) and pd.notna(row['SAN PEDRO']):
                    max_port = row[['ABIDJAN', 'INTERIEUR', 'SAN PEDRO']].idxmax()
                    port_preferences.append({'Exportateur': idx, 'Port Principal': max_port, 'Volume': row[max_port]})
            
            if port_preferences:
                port_pref_df = pd.DataFrame(port_preferences)
                port_counts = port_pref_df['Port Principal'].value_counts()
                
                fig = px.bar(
                    x=port_counts.index,
                    y=port_counts.values,
                    title="Nombre d'Exportateurs par Port Principal",
                    labels={'x': 'Port Principal', 'y': 'Nombre d\'Exportateurs'},
                    color_discrete_sequence=[BON_PLEIN_COLORS['secondary']]
                )
                fig = apply_bon_plein_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    # Analyses détaillées des plus gros écarts
    st.subheader("Top Écarts par Exportateur")
    
    # Séparer excédents et déficits
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Top 10 Excédents (Stock)")
        excedents = ecarts_data[ecarts_data['Écart (Acheté - Exporté)'] > 0].nlargest(10, 'Écart (Acheté - Exporté)')
        
        if len(excedents) > 0:
            fig = px.bar(
                x=excedents.index,
                y=excedents['Écart (Acheté - Exporté)'],
                title="Exportateurs avec le Plus de Stock",
                labels={'x': 'Exportateur', 'y': 'Excédent (kg)'},
                color_discrete_sequence=[BON_PLEIN_COLORS['primary']]
            )
            fig.update_xaxes(tickangle=45)
            fig = apply_bon_plein_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucun excédent détecté")
    
    with col2:
        st.write("### Top 10 Déficits") 
        deficits = ecarts_data[ecarts_data['Écart (Acheté - Exporté)'] < 0].nsmallest(10, 'Écart (Acheté - Exporté)')
        
        if len(deficits) > 0:
            fig = px.bar(
                x=deficits.index,
                y=abs(deficits['Écart (Acheté - Exporté)']),  # Valeur absolue pour affichage
                title="Exportateurs en Déficit",
                labels={'x': 'Exportateur', 'y': 'Déficit (kg)'},
                color_discrete_sequence=['#ff4444']
            )
            fig.update_xaxes(tickangle=45)
            fig = apply_bon_plein_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucun déficit détecté")
    
    # Tableau récapitulatif complet
    st.subheader("Tableau Complet des Écarts par Exportateur")
    
    # Formatage pour affichage
    ecart_display = ecarts_data.copy()
    cols_to_format = ['Volume livré (kg)', 'Total Exporté', 'Écart (Acheté - Exporté)']
    if 'ABIDJAN' in ecart_display.columns:
        cols_to_format.extend(['ABIDJAN', 'INTERIEUR', 'SAN PEDRO'])
    for col in cols_to_format:
        if col in ecart_display.columns:
            ecart_display[col] = ecart_display[col].apply(lambda x: format_number(x))
    ecart_display['% Écart'] = ecart_display['% Écart'].apply(lambda x: f"{x}%")
    
    # Ajouter une colonne de couleur pour le statut
    def get_status(row):
        pct = float(row['% Écart'].replace('%', ''))
        if pct > 5:
            return "Excédent Important"
        elif pct > 0:
            return "Excédent Normal"
        elif pct > -5:
            return "Déficit Modéré"
        else:
            return "Déficit Important"
    
    ecart_display['Statut'] = ecart_display.apply(get_status, axis=1)
    
    st.dataframe(ecart_display, use_container_width=True)

def analyse_abj_vs_sp(df):
    """Comparaison des tendances entre ABJ et SP"""
    
    st.subheader("Comparaison Abidjan vs San Pedro")
    
    # Vérifier si les colonnes existent
    if not all(col in df.columns for col in ['ABIDJAN', 'SAN PEDRO', 'INTERIEUR']):
        st.error("Les colonnes ABIDJAN, SAN PEDRO et INTERIEUR ne sont pas présentes dans les données d'export")
        return
    
    # Métriques de base
    col1, col2, col3 = st.columns(3)
    
    total_abj = df['ABIDJAN'].sum()
    total_sp = df['SAN PEDRO'].sum() 
    total_interieur = df['INTERIEUR'].sum()
    
    with col1:
        st.metric("ABIDJAN", f"{format_number(total_abj)} kg", f"{format_number(total_abj/1000)} tonnes")
        
    with col2:
        st.metric("SAN PEDRO", f"{format_number(total_sp)} kg", f"{format_number(total_sp/1000)} tonnes")
        
    with col3:
        st.metric("INTÉRIEUR", f"{format_number(total_interieur)} kg", f"{format_number(total_interieur/1000)} tonnes")
    
    # Comparaison visuelle
    st.subheader("Comparaison Visuelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en barres
        ports_comparison = {
            'Port': ['ABIDJAN', 'SAN PEDRO', 'INTÉRIEUR'],
            'Volume (kg)': [total_abj, total_sp, total_interieur]
        }
        
        fig = px.bar(
            ports_comparison, 
            x='Port', 
            y='Volume (kg)',
            title="Volume par Port",
            color='Port',
            color_discrete_sequence=BON_PLEIN_COLORS['palette']
        )
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Graphique en secteurs
        fig = px.pie(
            values=[total_abj, total_sp, total_interieur],
            names=['ABIDJAN', 'SAN PEDRO', 'INTÉRIEUR'],
            title="Répartition par Port (%)",
            color_discrete_sequence=BON_PLEIN_COLORS['palette']
        )
        fig = apply_bon_plein_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analyse par exportateur  
    st.subheader("Préférences par Exportateur")
    
    # Créer un ratio ABJ/SP pour chaque exportateur
    export_ports = df.groupby('EXPORTATEUR SIMPLE').agg({
        'ABIDJAN': 'sum',
        'SAN PEDRO': 'sum',
        'INTERIEUR': 'sum'
    }).copy()
    
    # Ajouter le total exporté comme référence
    export_ports['Total Exporté'] = export_ports['ABIDJAN'] + export_ports['SAN PEDRO'] + export_ports['INTERIEUR']
    
    # Calculer les ratios et préférences
    export_ports['Total Ports'] = export_ports['ABIDJAN'] + export_ports['SAN PEDRO']
    export_ports['% ABJ'] = (export_ports['ABIDJAN'] / export_ports['Total Ports'] * 100).fillna(0)
    export_ports['% SP'] = (export_ports['SAN PEDRO'] / export_ports['Total Ports'] * 100).fillna(0)
    export_ports['% INT'] = (export_ports['INTERIEUR'] / export_ports['Total Exporté'] * 100).fillna(0)
    
    # Identifier la préférence principale
    def get_preference(row):
        if row['ABIDJAN'] > row['SAN PEDRO'] and row['ABIDJAN'] > row['INTERIEUR']:
            return 'ABIDJAN'
        elif row['SAN PEDRO'] > row['ABIDJAN'] and row['SAN PEDRO'] > row['INTERIEUR']:
            return 'SAN PEDRO'
        elif row['INTERIEUR'] > row['ABIDJAN'] and row['INTERIEUR'] > row['SAN PEDRO']:
            return 'INTÉRIEUR'
        else:
            return 'MIXTE'
    
    export_ports['Préférence'] = export_ports.apply(get_preference, axis=1)
    
    # Graphique scatter ABJ vs SP
    fig = px.scatter(
        export_ports, 
        x='% ABJ', 
        y='% SP',
        size='Total Exporté',
        color='Préférence',
        hover_name=export_ports.index,
        title="Position des Exportateurs: % Abidjan vs % San Pedro",
        labels={'% ABJ': '% Volume via Abidjan', '% SP': '% Volume via San Pedro'},
        color_discrete_sequence=BON_PLEIN_COLORS['palette']
    )
    
    # Ajouter des lignes de référence
    fig.add_hline(y=50, line_dash="dash", line_color=BON_PLEIN_COLORS['text_secondary'], annotation_text="50% San Pedro")
    fig.add_vline(x=50, line_dash="dash", line_color=BON_PLEIN_COLORS['text_secondary'], annotation_text="50% Abidjan")
    
    fig = apply_bon_plein_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    # Graphique en barres empilées
    st.subheader("Répartition Détaillée par Exportateur")
    
    # Prendre les top exportateurs pour la lisibilité
    top_exportateurs = export_ports.nlargest(15, 'Total Exporté')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='ABIDJAN',
        x=top_exportateurs.index,
        y=top_exportateurs['ABIDJAN'],
        marker_color=BON_PLEIN_COLORS['primary']
    ))
    
    fig.add_trace(go.Bar(
        name='SAN PEDRO', 
        x=top_exportateurs.index,
        y=top_exportateurs['SAN PEDRO'],
        marker_color=BON_PLEIN_COLORS['secondary']
    ))
    
    fig.add_trace(go.Bar(
        name='INTÉRIEUR',
        x=top_exportateurs.index,
        y=top_exportateurs['INTERIEUR'],
        marker_color=BON_PLEIN_COLORS['accent']
    ))
    
    fig.update_layout(
        barmode='stack',
        title='Répartition des Volumes par Port - Top 15 Exportateurs',
        xaxis_title='Exportateur',
        yaxis_title='Volume (kg)',
        xaxis_tickangle=45
    )
    
    fig = apply_bon_plein_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistiques détaillées
    st.subheader("Statistiques par Port")
    
    preference_counts = export_ports['Préférence'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Répartition des préférences:**")
        for pref, count in preference_counts.items():
            percentage = (count / len(export_ports)) * 100
            st.write(f"- {pref}: {count} exportateurs ({percentage:.1f}%)")
    
    with col2:
        st.write("**Moyennes par port:**")
        avg_abj = export_ports['% ABJ'].mean() if not export_ports['% ABJ'].empty else 0
        avg_sp = export_ports['% SP'].mean() if not export_ports['% SP'].empty else 0
        avg_int = export_ports['% INT'].mean() if not export_ports['% INT'].empty else 0
        st.write(f"- Moyenne ABIDJAN: {avg_abj:.1f}%")
        st.write(f"- Moyenne SAN PEDRO: {avg_sp:.1f}%")
        st.write(f"- Moyenne INTÉRIEUR: {avg_int:.1f}%")
    
    # Tableau détaillé
    st.subheader("Détail par Exportateur")
    ports_display = export_ports[['ABIDJAN', 'SAN PEDRO', 'INTERIEUR', '% ABJ', '% SP', '% INT', 'Préférence']].copy()
    
    for col in ['ABIDJAN', 'SAN PEDRO', 'INTERIEUR']:
        ports_display[col] = ports_display[col].apply(lambda x: format_number(x))
    
    for col in ['% ABJ', '% SP', '% INT']:
        ports_display[col] = ports_display[col].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(ports_display, use_container_width=True)

if __name__ == "__main__":
    main()