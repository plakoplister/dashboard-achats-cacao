import pandas as pd
import numpy as np

def explore_excel_file(file_path):
    """Explore la structure d'un fichier Excel"""
    print(f"Analyse du fichier: {file_path}")
    print("=" * 50)
    
    try:
        # Lire le fichier Excel
        df = pd.read_excel(file_path)
        
        print(f"Dimensions: {df.shape}")
        print(f"Nombre de lignes: {len(df)}")
        print(f"Nombre de colonnes: {len(df.columns)}")
        print()
        
        print("Colonnes disponibles:")
        for i, col in enumerate(df.columns):
            print(f"{i+1}. {col}")
        print()
        
        print("Types de données:")
        print(df.dtypes)
        print()
        
        print("Valeurs manquantes:")
        missing = df.isnull().sum()
        print(missing[missing > 0])
        print()
        
        print("Aperçu des premières lignes:")
        print(df.head())
        print()
        
        # Analyser la première ligne pour comprendre les en-têtes
        print("Première ligne (potentiels en-têtes):")
        print(df.iloc[0].values)
        print()
        
        # Recherche de colonnes clés dans la première ligne
        print("Détection automatique de colonnes importantes:")
        first_row = df.iloc[0].astype(str)
        
        # Achats/Purchases
        achat_cols = [i for i, val in enumerate(first_row) if any(keyword in val.lower() for keyword in ['achat', 'purchase', 'buy', 'qty', 'quantit', 'volume'])]
        if achat_cols:
            print(f"Colonnes d'achat potentielles (indices): {achat_cols} - {[first_row.iloc[i] for i in achat_cols]}")
        
        # Exports
        export_cols = [i for i, val in enumerate(first_row) if any(keyword in val.lower() for keyword in ['export', 'ship', 'sold', 'livr'])]
        if export_cols:
            print(f"Colonnes d'export potentielles (indices): {export_cols} - {[first_row.iloc[i] for i in export_cols]}")
        
        # Poids
        poids_cols = [i for i, val in enumerate(first_row) if any(keyword in val.lower() for keyword in ['poids', 'weight', 'kg', 'tonne', 'masse'])]
        if poids_cols:
            print(f"Colonnes de poids potentielles (indices): {poids_cols} - {[first_row.iloc[i] for i in poids_cols]}")
        
        # Fournisseurs
        fournisseur_cols = [i for i, val in enumerate(first_row) if any(keyword in val.lower() for keyword in ['fournisseur', 'supplier', 'vendor', 'coop', 'producteur'])]
        if fournisseur_cols:
            print(f"Colonnes de fournisseur potentielles (indices): {fournisseur_cols} - {[first_row.iloc[i] for i in fournisseur_cols]}")
        
        # Exportateurs
        exportateur_cols = [i for i, val in enumerate(first_row) if any(keyword in val.lower() for keyword in ['exportateur', 'exporter', 'client', 'acheteur'])]
        if exportateur_cols:
            print(f"Colonnes d'exportateur potentielles (indices): {exportateur_cols} - {[first_row.iloc[i] for i in exportateur_cols]}")
        
        # Locations (ABJ/SP)
        location_cols = [i for i, val in enumerate(first_row) if any(keyword in val.lower() for keyword in ['port', 'ville', 'city', 'location', 'abj', 'sp', 'abidjan', 'san pedro', 'destination', 'interieur'])]
        if location_cols:
            print(f"Colonnes de localisation potentielles (indices): {location_cols} - {[first_row.iloc[i] for i in location_cols]}")
        
        print()
        
        # Analyse des valeurs uniques pour certaines colonnes
        print("Échantillon de valeurs pour les colonnes importantes:")
        for col in df.columns[:10]:  # Première 10 colonnes
            if df[col].dtype == 'object':
                unique_vals = df[col].dropna().unique()[:5]
                print(f"{col}: {unique_vals}")
        
        return df
        
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None

if __name__ == "__main__":
    file_path = "Master_Data/DB - Achat Cacao - 2022021.xlsx"
    df = explore_excel_file(file_path)