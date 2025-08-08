# 🚀 Guide de Démarrage - BON PLEIN Analyse Cacao

## 🍫 Application Créée

Votre webapp d'analyse des achats de cacao a été créée avec succès ! Elle comprend toutes les fonctionnalités demandées avec la charte graphique BON PLEIN.

## ⚡ Démarrage Rapide

### 1. Lancer l'application
```bash
streamlit run analyse_cacao.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse: `http://localhost:8501`

### 2. Charger vos données
- **Option 1**: L'app charge automatiquement le fichier `Master_Data/DB - Achat Cacao - 2022021.xlsx`
- **Option 2**: Utilisez "Upload nouveau fichier" pour charger de nouvelles données

## 📊 Fonctionnalités Disponibles

### onglet 1: 📈 Achats vs Exports
- Volume total livré et répartition par port (Abidjan, San Pedro, Intérieur)
- Top 10 des exportateurs par volume
- Graphiques circulaires et en barres
- Tableau récapitulatif détaillé

### onglet 2: 🏭 Fournisseurs  
- **Analyse par exportateur** avec sélecteur dropdown
- Top 10 des fournisseurs (graphique horizontal)
- **Matrice interactive** fournisseurs × exportateurs
- Statistiques: nombre, volume moyen/médian

### onglet 3: ⚖️ Différences Poids
- **Écarts** entre volumes livrés et exportés
- Distribution des écarts (histogramme)
- **Analyse par exportateur** avec code couleur
- **Top 20 des plus gros écarts** pour investigation

### onglet 4: 🌍 ABJ vs SP
- **Comparaison** Abidjan vs San Pedro vs Intérieur
- **Préférences par exportateur** (scatter plot interactif)
- **Graphique empilé** des top 15 exportateurs
- Statistiques de répartition portuaire

### onglet 5: 📋 Données Brutes
- Vue complète du dataset
- Filtrage et tri interactifs

## 🎨 Design BON PLEIN

L'application utilise la charte graphique BON PLEIN:
- **Header** avec gradient bleu signature (#1e3a5f → #2c5282)
- **Couleurs** harmonisées sur tous les graphiques
- **Interface** cohérente avec le branding corporat
- **Footer** avec mentions légales

## 📁 Structure des Fichiers

```
ACHAT-Db/
├── analyse_cacao.py          # ✅ Application Streamlit principale
├── explore_data.py           # 🔍 Script d'exploration des données  
├── requirements.txt          # 📦 Dépendances Python
├── GUIDE_DEMARRAGE.md       # 📖 Ce guide
└── Master_Data/             # 📊 Dossier des données
    └── DB - Achat Cacao - 2022021.xlsx
```

## 🔄 Mise à Jour Annuelle

### Pour ajouter de nouvelles données:

1. **Préparer** le fichier Excel avec la même structure:
   - Colonne A: Code fournisseur
   - Colonne B: Nom fournisseur
   - Colonne C: Exportateurs
   - Colonne D: Exportateur Simple
   - Colonne E: Région activité
   - Colonne F: Volume livré (kg)
   - Colonne G: ABIDJAN
   - Colonne H: INTÉRIEUR  
   - Colonne I: SAN PEDRO

2. **Option 1**: Remplacer le fichier dans `Master_Data/`
3. **Option 2**: Utiliser l'upload dans l'interface web

## 🔧 Dépendances

Si besoin d'installer les dépendances:
```bash
pip install -r requirements.txt
```

Dépendances requises:
- `streamlit` (interface web)
- `pandas` (manipulation données)
- `plotly` (graphiques interactifs)
- `openpyxl` (lecture Excel)
- `numpy` (calculs numériques)

## 💡 Conseils d'Usage

### Pour l'analyse des écarts:
- Regardez d'abord la **distribution globale** (onglet 3)
- Identifiez les **exportateurs problématiques** (barres rouges)
- Explorez le **top 20 des écarts** pour les anomalies

### Pour l'analyse des ports:
- Utilisez le **scatter plot ABJ vs SP** pour voir les préférences
- Le **graphique empilé** montre la répartition détaillée
- Les **pourcentages** aident à identifier les spécialisations

### Pour les fournisseurs:
- Sélectionnez un **exportateur spécifique** pour l'analyse fine
- La **matrice** révèle les relations exclusives
- Comparez les **volumes moyens** pour évaluer la concentration

## 🎯 Indicateurs Clés Calculés

- **Volumes totaux** par port et exportateur
- **Parts de marché** des fournisseurs  
- **Écarts de poids** (livré vs exporté)
- **Préférences portuaires** des exportateurs
- **Concentration** des approvisionnements
- **Statistiques descriptives** complètes

## ✅ Application Prête !

Votre dashboard BON PLEIN est maintenant opérationnel pour l'analyse des achats de cacao 2020-2021 et peut être facilement mis à jour chaque année avec de nouvelles données.

---
**BON PLEIN** - Développé pour l'optimisation des achats et exportations de cacao