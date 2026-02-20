import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# 1. Load Data
file_path = 'calenviroscreen40resultsdatadictionary_F_2021.xlsx'
results_df = pd.read_excel(file_path, sheet_name='CES4.0FINAL_results')
demographic_df = pd.read_excel(file_path, sheet_name='Demographic Profile', header=1)

# 2. Merge Data on Census Tract
df = pd.merge(results_df, demographic_df, on='Census Tract', how='inner', suffixes=('', '_drop'))
df = df.loc[:, ~df.columns.str.contains('_drop')]

# 3. Slugify Headers (Cleaning)
def slugify(col):
    return col.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'pct').replace('.', '').replace('<', 'lt').replace('>', 'gt').replace('-', '_')

df.columns = [slugify(c) for c in df.columns]

# 4. Filter for Los Angeles County & Handle NaNs
la_df = df[df['california_county'] == 'Los Angeles'].copy()
print(f"Total LA County tracts: {len(la_df)}")

critical_cols = ['asthma_pctl', 'traffic_pctl', 'pm25', 'poverty_pctl']
la_df.dropna(subset=critical_cols, inplace=True)
print(f"After removing NaNs: {len(la_df)} tracts")

# 5. Define Groups (Proxies for Freeway Proximity)
pop_a = la_df[la_df['traffic_pctl'] > 90] # High Risk
pop_b = la_df[la_df['traffic_pctl'] < 10] # Low Risk
print(f"\nPopulation A (High Traffic >90th): {len(pop_a)} tracts")
print(f"Population B (Low Traffic <10th): {len(pop_b)} tracts")

# 6. Calculate Disparity Means
metrics = ['asthma_pctl', 'pm25', 'poverty_pctl', 'hispanic_pct', 'african_american_pct', 'white_pct']
available_metrics = [m for m in metrics if m in la_df.columns]
print(f"\nAvailable metrics: {available_metrics}")

disparity_table = pd.DataFrame({
    'Population A (High Traffic)': pop_a[available_metrics].mean(),
    'Population B (Low Traffic)': pop_b[available_metrics].mean()
})
disparity_table['Delta (A - B)'] = disparity_table['Population A (High Traffic)'] - disparity_table['Population B (Low Traffic)']
print("\n--- Mean Disparity Table ---")
print(disparity_table)

# 7. Pearson Correlation
correlation = la_df[['pm25', 'poverty_pctl', 'asthma_pctl']].corr()
print("\n--- Pearson Correlation Matrix ---")
print(correlation)

# 8. Multivariate Regression (The "Smoking Gun")
# Controlling for Poverty to see the independent impact of PM2.5 on Asthma
X = la_df[['pm25', 'poverty_pctl']]
X = sm.add_constant(X)
y = la_df['asthma_pctl']
model = sm.OLS(y, X).fit()
print("\n--- Regression Results ---")
print(model.summary())
print(f"\nKey Finding: PM2.5 coefficient = {model.params['pm25']:.4f}, p-value = {model.pvalues['pm25']:.4e}")

# 9. Visualization: Side-by-Side Bar Chart
try:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar chart
    labels = ['Population A\n(High Traffic)', 'Population B\n(Low Traffic)']
    asthma_means = [pop_a['asthma_pctl'].mean(), pop_b['asthma_pctl'].mean()]
    sns.barplot(x=labels, y=asthma_means, palette='viridis', ax=axes[0])
    axes[0].set_title('Asthma Percentile: High Traffic vs. Low Traffic Census Tracts (LA County)', fontsize=11)
    axes[0].set_ylabel('Mean Asthma Percentile')
    axes[0].set_ylim(0, 100)
    
    # Add value labels on bars
    for i, v in enumerate(asthma_means):
        axes[0].text(i, v + 2, f'{v:.1f}', ha='center', fontweight='bold')

    # Correlation heatmap
    corr_vars = ['traffic_pctl', 'pm25', 'poverty_pctl', 'asthma_pctl']
    corr_matrix = la_df[corr_vars].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0, ax=axes[1], vmin=-1, vmax=1)
    axes[1].set_title('Correlation Heatmap: Traffic, PM2.5, Poverty, and Asthma', fontsize=11)

    plt.tight_layout()
    plt.savefig('analysis_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualizations saved to 'analysis_results.png'")
    plt.close()
except Exception as e:
    print(f"\nError creating visualizations: {e}")
    import traceback
    traceback.print_exc()

print("\n=== ANALYSIS COMPLETE ===")