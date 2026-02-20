import pandas as pd

file_path = 'calenviroscreen40resultsdatadictionary_F_2021.xlsx'

# Read Demographic Profile with header on row 1 (0-indexed)
demographic_df = pd.read_excel(file_path, sheet_name='Demographic Profile', header=1, nrows=10)
print("=== Demographic Profile (with correct header) ===")
print("Columns:", list(demographic_df.columns))
print("\nFirst 10 rows:")
print(demographic_df)
