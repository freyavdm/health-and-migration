# Influence of Community Health on U.S. Migration

**SIADS 593 – Milestone I · University of Michigan Master of Applied Data Science (MADS)**
Freya Van de Motter, Ransom MacLeith, and Shay Gooding

This project was originally built and run on [Deepnote](https://deepnote.com) in January–February 2026. It is being uploaded here as-is, just to share. The notebooks assume the Deepnote environment (working directory at repo root, `data/` alongside the notebooks); to re-run, replicate the setup on Deepnote or install `requirements.txt` locally and run the notebooks in numbered order. Notebook 2 pulls ACS migration data from the Census API (requires your own API key) but falls back to the cached `data/raw_migration_data.csv`.

## Final output

📄 **[Milestone I – Team 04 (slidedoc, PDF)](<Milestone I - Team 04.pdf>)**

## Contents

```
.
├── 1. Setup_ Importing Dependencies.ipynb   # checks/installs pinned dependencies
├── 2. Ingesting and Cleaning Data.ipynb     # ETL: ACS migration (API), CHR 2025 rankings, CHR 2022 metrics → cleaned CSVs
├── 3. Analysis_ Choropleths.ipynb           # univariate & bivariate (concordance) county maps
├── 4. Overall Relationship.ipynb            # z-score distributions, Pearson/Spearman (county & state), deciles/ANOVA, box plots by population
├── 5. Sankeys, Histograms, OLS.ipynb        # Sankeys, correlation heatmaps, VIF pruning, LassoCV → OLS (net / in / out)
├── functions.py                             # shared data-loading and merge helpers
├── requirements.txt                         # pinned Python dependencies
├── Milestone I - Team 04.pdf                # final report (slidedoc)
└── data/
    ├── raw_migration_data.csv               # cached ACS 5-Year Migration Flows 2016–2020 API pull (raw)
    ├── health_rankings_2025.xlsx            # County Health Rankings 2025 (raw)
    ├── chd_metrics_config_OLS1.csv          # column-rename config for CHR 2022 metrics
    ├── county_to_county_US_2020.csv         # cleaned county-to-county flows (output of nb 2)
    ├── cleaned_health_rankings_2025.csv     # cleaned CHR z-scores (output of nb 2)
    └── cleaned_chd_metrics_2022.csv         # cleaned CHR 2022 analytic metrics (output of nb 2)
```

Files are left in their original relative locations; moving them may break notebook paths.

**Data:** U.S. Census Bureau, American Community Survey 5-Year Migration Flows (2016–2020), and [County Health Rankings & Roadmaps](https://www.countyhealthrankings.org/) (2022 Analytic Data, 2025 National Data), University of Wisconsin Population Health Institute. Data files are included for reproducibility and remain subject to their sources' respective terms of use.

---

*This README was generated with the assistance of Generative AI. Generative AI may have been used during coding as an assistant – humans lead the ETL, EDA, and modeling, and created the presentation.*
