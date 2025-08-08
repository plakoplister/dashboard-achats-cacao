import pandas as pd

df = pd.read_excel('Master_Data/DB - Achat Cacao - 2022021.xlsx')
new_columns = df.iloc[0].astype(str).tolist()
df.columns = new_columns
df = df.iloc[1:].reset_index(drop=True)

for col in ['Volume livré (kg)', 'ABIDJAN', 'INTERIEUR', 'SAN PEDRO']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

text_cols = ['Nom fournisseur', 'EXPORTATEUR SIMPLE']
for col in text_cols:
    df[col] = df[col].astype(str).replace('nan', 'Non renseigné').fillna('Non renseigné')

print('AVANT FILTRAGE:')
print(f'Total lignes: {len(df)}')
print(f'Total volume: {df["Volume livré (kg)"].sum()/1000:,.0f} tonnes')

# Filtrer les lignes "Non renseigné"
df_filtered = df[
    (df['Nom fournisseur'] != 'Non renseigné') & 
    (df['EXPORTATEUR SIMPLE'] != 'Non renseigné')
].copy()

print('\nAPRÈS FILTRAGE:')
print(f'Total lignes: {len(df_filtered)}')
print(f'Total volume ACHATS: {df_filtered["Volume livré (kg)"].sum()/1000:,.0f} tonnes')

print('\nEST-CE QU\'ON OBTIENT 2,349 TONNES ?', df_filtered['Volume livré (kg)'].sum()/1000000 < 2.5)