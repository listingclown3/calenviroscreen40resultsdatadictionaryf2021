# CalEnviroScreen 4.0 Analysis

Environmental justice analysis of Los Angeles County using CalEnviroScreen 4.0 data to examine relationships between traffic exposure, air pollution, poverty, and asthma rates.

## Overview

This project analyzes census tract-level data to investigate the "double burden" hypothesis—whether communities near freeways experience both higher pollution exposure and worse health outcomes.

## Key Findings

- **Poverty** is the dominant predictor of asthma rates (r=0.601, p<0.001)
- **PM2.5** shows weak correlation with asthma (r=0.033)
- **Traffic exposure** has negative correlation with asthma (r=-0.049)
- High-traffic areas show significant demographic disparities
- The "double burden" appears primarily socioeconomic rather than environmental

## Data Source

CalEnviroScreen 4.0 Results Data Dictionary (F_2021)
- Environmental indicators (PM2.5, traffic density, pollution burden)
- Health outcomes (asthma rates)
- Demographic profiles (race/ethnicity, poverty)
- Census tract level for California

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas numpy statsmodels matplotlib seaborn openpyxl
```

## Usage

```bash
# Basic analysis
python main.py

# Enhanced analysis with stratification
python enhanced_analysis.py
```

## Scripts

- **main.py** - Core analysis with disparity tables, correlations, and regression
- **enhanced_analysis.py** - Stratified analysis and comprehensive visualizations
- **inspect_data.py** - Data exploration utilities
- **inspect_demo.py** - Demographic data inspection

## Output

- `analysis_results.png` - Bar charts and correlation heatmap
- `enhanced_analysis.png` - Multi-panel visualization with demographic breakdowns
- `output.log` - Detailed analysis logs

## Methodology

1. Merge environmental and demographic data by census tract
2. Filter for Los Angeles County
3. Define high-risk (traffic >90th percentile) vs low-risk (<10th percentile) populations
4. Calculate disparity metrics
5. Multivariate regression controlling for poverty
6. Stratified analysis by poverty level

## License

Data provided by California Office of Environmental Health Hazard Assessment (OEHHA)
