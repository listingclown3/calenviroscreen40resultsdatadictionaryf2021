import pandas as pd

file_path = 'calenviroscreen40resultsdatadictionary_F_2021.xlsx'

# Get sheet names
xl_file = pd.ExcelFile(file_path)
print("Sheet names:", xl_file.sheet_names)

# Inspect CES4.0FINAL_results
print("\n=== CES4.0FINAL_results ===")
results_df = pd.read_excel(file_path, sheet_name='CES4.0FINAL_results', nrows=5)
print("Columns:", list(results_df.columns))
print("\nFirst 5 rows:")
print(results_df.head())

# Inspect Demographic Profile
print("\n=== Demographic Profile ===")
demographic_df = pd.read_excel(file_path, sheet_name='Demographic Profile', nrows=5)
print("Columns:", list(demographic_df.columns))
print("\nFirst 5 rows:")
print(demographic_df.head())
