import pandas as pd
import numpy as np

file_path = 'calenviroscreen40resultsdatadictionary_F_2021.xlsx'
results_df = pd.read_excel(file_path, sheet_name='CES4.0FINAL_results')
demographic_df = pd.read_excel(file_path, sheet_name='Demographic Profile', header=1)

def slugify(col):
    return col.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'pct').replace('.', '').replace('<', 'lt').replace('>', 'gt').replace('-', '_')

df = pd.merge(results_df, demographic_df, on='Census Tract', how='inner', suffixes=('', '_drop'))
df = df.loc[:, ~df.columns.str.contains('_drop')]
df.columns = [slugify(c) for c in df.columns]

la_df = df[df['california_county'] == 'Los Angeles'].copy()
print(f"Total LA tracts: {len(la_df)}")

critical_cols = ['asthma', 'traffic_pctl', 'pm25', 'poverty_pctl']
print(f"\nChecking critical columns:")
for col in critical_cols:
    if col in la_df.columns:
        print(f"  {col}: exists, NaN count = {la_df[col].isna().sum()}")
    else:
        print(f"  {col}: MISSING")

la_df.dropna(subset=critical_cols, inplace=True)
print(f"\nAfter dropping NaNs: {len(la_df)} tracts")

print(f"\nTraffic percentile stats:")
print(la_df['traffic_pctl'].describe())

pop_a = la_df[la_df['traffic_pctl'] > 90]
pop_b = la_df[la_df['traffic_pctl'] < 10]

print(f"\nPopulation A (>90th percentile): {len(pop_a)} tracts")
print(f"Population B (<10th percentile): {len(pop_b)} tracts")

print(f"\nAsthma column name: 'asthma'")
print(f"Asthma values in Pop A: {pop_a['asthma'].describe()}")
print(f"Asthma values in Pop B: {pop_b['asthma'].describe()}")

print(f"\nMean Asthma Pop A: {pop_a['asthma'].mean()}")
print(f"Mean Asthma Pop B: {pop_b['asthma'].mean()}")
