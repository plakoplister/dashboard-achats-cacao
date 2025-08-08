# Dashboard Achats Cacao - Côte d'Ivoire

## 📊 Vue d'ensemble

Tableau de bord professionnel développé par **Bon Plein Capital Analytics Solution** pour l'analyse des achats et exportations de cacao en Côte d'Ivoire (saison 2020-2021).

## ✨ Fonctionnalités

### 📈 Vue Achats
- Consolidation des achats par exportateur
- Métriques clés : volumes, fournisseurs, concentration
- Analyse de la diversification des sources

### 🏭 Analyse Fournisseurs
- Top fournisseurs par exportateur
- Cartographie des fournisseurs par région
- Analyse de la diversification client

### ⚖️ Écarts Achats/Exports
- Comparaison volumes achetés vs exportés
- Identification des stocks et déficits
- Analyse par exportateur et par port

### 🚢 Comparaison Ports (ABJ vs SP)
- Répartition Abidjan vs San Pedro vs Intérieur
- Préférences par exportateur
- Tendances portuaires

## 🛠 Technologies

- **Frontend** : Streamlit
- **Visualisations** : Plotly
- **Data Processing** : Pandas, NumPy
- **Fichiers** : Excel (openpyxl)

## 🚀 Installation & Usage

### Prérequis
```bash
pip install streamlit pandas plotly openpyxl numpy
```

### Lancement local
```bash
streamlit run analyse_cacao.py
```

### Déploiement Streamlit Cloud
1. Fork ce repository
2. Connecter à [share.streamlit.io](https://share.streamlit.io)
3. Déployer depuis votre fork

## 📁 Structure des données

### Fichier principal
`Master_Data/DB - Achat Cacao - 2022021.xlsx`

**Feuille "dB ACHAT"** :
- Volume livré (kg)
- Code/Nom fournisseur
- EXPORTATEUR SIMPLE
- Région activité

**Feuille "dB EXPORT"** :
- EXPORTATEUR SIMPLE
- ABJ (Abidjan)
- SP (San Pedro) 
- Total général

### Mappings
`Master_Data/Coops_Entity_Mappings.xlsx` - Correspondances coopératives

## 📊 Métriques clés

- **Total Acheté** : 2 349 118 tonnes
- **Total Exporté** : 2 163 574 tonnes
- **Écart Global** : 185 544 tonnes (7,9%)

## 🎨 Design System

### Charte graphique BON PLEIN
- **Couleur principale** : #1e3a5f (Bleu foncé)
- **Couleur secondaire** : #2c5282 (Bleu moyen)
- **Couleur accent** : #bee3f8 (Bleu clair)
- **Police** : Arial
- **Style** : Moderne, professionnel, coins légèrement arrondis

## 🔒 Sécurité & Confidentialité

- Données confidentielles - Usage interne uniquement
- Accès restreint aux parties prenantes autorisées
- Respect des réglementations sur les données commerciales

## 👨‍💼 Contact

**Bon Plein Capital Analytics Solution**
- Développé pour l'optimisation des achats et exportations
- Analyse professionnelle des chaînes d'approvisionnement cacao

---

*© 2024 Bon Plein Capital. Tous droits réservés.*