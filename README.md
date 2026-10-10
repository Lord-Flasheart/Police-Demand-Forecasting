# 📘 Police Demand Forecasting (Norfolk & Suffolk)

![Status](https://img.shields.io/badge/Project%20Status-In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-yellow)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-red)

## 🧭 Project Summary

This project analyses crime demand between **July 2023 and June 2026**, exploring crime types, outcomes, geographic hotspots, seasonal patterns and long‑term trends.
A comparison of four forecasting approaches (seasonal-naive, Holt-Winters, Random Forest and Linear Regression) is used to select the most accurate method, which generates a **6-month forward forecast (Jul–Dec 2026)**.

## 🔍 Project Overview
This project analyses crime demand across Norfolk and Suffolk between July 2023 and June 2026.
It explores:

Crime type distribution

Outcome patterns

Geographic hotspots (LSOA‑level)

Monthly demand trends

Seasonal behaviour

Investigative attrition

Time‑series forecasting

The final forecast (Jul–Dec 2026) uses the seasonal-naive method, selected after comparing four approaches via a walk-forward backtest. See the Models section below.

## 🎯 Objectives
Understand crime demand behaviour across 36 months

Identify seasonal patterns and long‑term trends

Analyse geographic hotspots and outcome structures

Engineer modelling‑ready temporal features

Train and evaluate forecasting models

Produce a forward‑looking demand forecast

📂 Repository Structure
```
├── data/                     # Raw monthly CSV files
├── docs/
│   ├── evidence/
│   │   ├── leakage_test_v1_fail.txt   # Test output before the fix (fails)
│   │   └── leakage_test_v2_pass.txt   # Test output after the fix (passes)
│   └── learning_log.md       # Investigation record (leak discovery and fix)
├── notebooks/
│   └── Police_Demand_Forecasting_Monthly.ipynb   # Full analysis + forecasting notebook
├── results/
│   ├── v1_baseline.md        # Original (leaked) model results
│   └── v2_metrics.md         # Corrected model results and comparison
├── src/
│   └── features.py           # Shared, tested feature-building logic
├── tests/
│   └── test_no_leakage.py    # Automated leak-detection test
├── visuals/                  # Plots and charts
├── CHANGELOG.md              # v1 → v2 change record
└── README.md                 # Project documentation
```

## 📂 Data Sources

The analysis uses recorded crime data for Norfolk and Suffolk between **July 2023 and June 2026**.

Key fields include:

- Crime type  
- Outcome category  
- LSOA location  
- Occurrence date  

Data was cleaned, aggregated and transformed into modelling‑ready monthly tables for forecasting.

## 🧪 Exploratory Data Analysis (EDA)
Key Findings
353,570 rows × 12 columns

36 months of crime data

14 crime types, 15 outcome categories, 2,606 LSOAs

Crime demand dominated by:

Violence & sexual offences

Anti‑social behaviour

Criminal damage & arson

Outcome distribution heavily weighted toward:

Unable to prosecute suspect

No suspect identified

Urban hotspots include:

Norwich

Ipswich

Great Yarmouth

## 📈 Time Analysis
Monthly Demand
Highest month: July 2023 (11,418 incidents)

Lowest month: February 2025 (8,412 incidents)

Seasonal Pattern
Summer peaks (June–August)

Winter troughs (December–February)

Stable, repeating annual cycle

Trend
Slight long‑term decline

Seasonal variation dominates

## 🏗️ Feature Engineering
Features created for modelling:

Year

Month_num

Quarter

Season

Crime_Count (monthly aggregated target)

Lag features (t‑1, t‑2, t‑3)

Rolling mean (3‑month)

**Note:** the original rolling-mean feature contained a data leak, corrected in v2. See the Models section below for detail.

These features capture short‑term momentum and seasonal structure.

## 🤖 Models

Four approaches were tested and compared via a walk-forward backtest (see `results/v2_metrics.md` for full detail):

| Model | Overall MAE (backtest) |
|---|---|
| **Seasonal-naive** (selected) | **188.1** |
| Holt-Winters | 299.8 |
| Random Forest | 361.5 |
| Linear Regression | 526.9 |

### v1 vs v2: Linear Regression and Random Forest, in detail

An earlier version of this project (tagged [`v1.0-original`](../../tree/v1.0-original)) reported a perfect R² for Linear Regression. This was later found to be caused by a data leak: the 3-month rolling-average feature included the value being predicted. The leak was proven three ways (manual reconstruction, model coefficients and an automated test, described in `docs/learning_log.md`), then fixed. See `CHANGELOG.md` for the full before/after comparison.

| Model | Version | MAE | RMSE | R² |
|---|---|---|---|---|
| Linear Regression | v1 (leaked) | ~0 | ~0 | 1.0 |
| Linear Regression | v2 (corrected) | 563.8 | 667.6 | 0.16 |
| Random Forest | v1 (leaked) | 305.9 | 437.3 | 0.641 |
| Random Forest | v2 (corrected) | 352.9 | 431.5 | 0.650 |

Fixing the leak changed the two models in different ways. Linear Regression's score dropped sharply, from a perfect but meaningless fit to a weak and honest one. That's what you'd expect once the shortcut was removed. Random Forest barely changed at all: its MAE got slightly worse but its RMSE and R² actually improved a little. That suggests it hadn't relied on the leaked feature much in the first place.

Even with the leak fixed, Random Forest did not outperform seasonal-naive on any metric. Naive's MAE was 172.5 on the single split and 188.1 on the backtest, and its RMSE was 207.77 on the single split, all lower than Random Forest's. Given the small dataset, this project takes the more accurate and simpler seasonal-naive approach as the recommended method, while noting this should be re-evaluated as more data accumulates.

## 🔮 Forecasting (Jul–Dec 2026)

Using the selected seasonal-naive method, refit on all available data:

| Month | Forecast | Range |
|---|---|---|
| Jul 2026 | 10,774 | 10,454–11,094 |
| Aug 2026 | 10,026 | 9,776–10,276 |
| Sep 2026 | 9,593 | 9,471–9,715 |
| Oct 2026 | 9,958 | 9,862–10,054 |
| Nov 2026 | 9,019 | 8,871–9,167 |
| Dec 2026 | 8,966 | 8,774–9,158 |

The range reflects the method's typical error at each forecast horizon, based on the walk-forward backtest. It is not a formal statistical confidence interval. With only 36 months of data, this simpler approach is more honest about the actual level of certainty available.

## ⚠️ Limitations

- **Recorded crime, not total crime.** This data reflects crimes reported to and recorded by police, not all crime that occurred. Under-reporting varies by crime type and area.
- **Small dataset.** 36 months of data gives limited ability to distinguish genuine long-term trend from noise, and limits how much a more complex model can learn versus a simple seasonal comparison.
- **Aggregate forecasting only.** This project forecasts total monthly crime counts. It does not predict individual crimes, target areas or identify individuals, and should not be used for that purpose.
- **Geographic anomalies unexplained.** A small number of records show locations outside Norfolk and Suffolk (e.g. Southwark, Peterborough). The cause was not investigated and should be checked before relying on geographic breakdowns.
- **ASB records carry no unique ID or outcome.** Roughly 11.6% of records (Anti-social behaviour) have no Crime ID and no outcome category. This appears to be a structural feature of how ASB is recorded, not a data quality defect, but it means these records can't be tracked individually through to an outcome.

## 🛡️ Data ethics

This project is a personal portfolio piece and technical demonstration, not an operational tool. If forecasts of this kind were used to inform real policing decisions, the following would need to be addressed:

- **Feedback loops.** Recorded crime reflects policing activity as well as underlying crime. Areas with historically higher patrol presence may show higher recorded crime, which could reinforce the same patrolling pattern if used uncritically as a demand signal.
- **Aggregate use only.** Forecasts here are at the force-wide monthly level. Any use at a finer geographic or individual level would need separate, careful assessment. This kind of forecast should never be used to profile individuals or communities.
- **Human oversight.** Any operational use of a model like this should sit alongside, not replace, human judgement and existing evidence-based practice, consistent with frameworks such as [ALGO-CARE](https://www.college.police.uk) developed for UK policing algorithmic accountability.
- **Data protection.** Any operational deployment would need to comply with UK GDPR and the Data Protection Act 2018, including its provisions for law enforcement processing (Part 3).

This section reflects my own understanding of good practice in this area, rather than a completed ethics review.

## 🤝 AI assistance

This project was originally built with GitHub Copilot as a coding and learning aid. The v2 correction (fixing a data leak discovered on review) was developed with Claude (Anthropic) as a coach, guiding the investigation and code changes. All code was written, run and understood by me; `docs/learning_log.md` records the investigation process, including my own reasoning before each correction.

## 📈 Key Visuals

### Exploratory analysis
![Crime Type Distribution](visuals/Crime%20Type%20Distribution%201_4.png)
![Outcome Category Distribution](visuals/Outcome%20Category%20Distribution%201_5.png)
![Crime Type x Outcome Heatmap](visuals/Crime%20Type%20x%20Outcome%20Heatmap%201_7.png)
![Top 10 LSOA](visuals/Top%2010%20LSOA%201_6.png)
![Top 5 Crime Types](visuals/Top%205%20Crime%20Types%20with%20No%20Suspect%20Identified%201_7.png)
![Monthly Crime Demand](visuals/Monthly%20Crime%20Demand%202_1.png)
![Monthly Crime Demand Trend](visuals/Monthly%20Crime%20Demand%20with%20Trend%20Line%202_2.png)
![Seasonal Profile](visuals/Seasonal%20Profile%20Average%20Crime%20Demand%20by%20Month%202_3.png)

### v1 modelling (superseded, kept for the before/after record)
![LR Actual vs Predicted (v1, leaked)](visuals/Actual%20vs%20Predicted%20(Linear%20Regression)%204_2.png)
![RF Actual vs Predicted (v1)](visuals/Actual%20vs%20Predicted%20(Random%20Forest)%204_3.png)
![LR vs RF Comparison (v1)](visuals/LR%20vs%20RF%204_4.png)
![Combined Forecast (v1, leaked)](visuals/Combined%20Forecasted%20Crime%20Counts%20(Jul_Dec26)%205_3.png)

### v2 modelling, corrected
![LR Actual vs Predicted (v2, corrected)](visuals/Actual%20vs%20Predicted%20(Linear%20Regression%20v2).png)
![RF Actual vs Predicted (v2, corrected)](visuals/Actual%20vs%20Predicted%20(Random%20Forest%20v2).png)
![Overall MAE by model](visuals/Overall%20MAE%20by%20Model.png)
![All models vs Actual](visuals/All%20Models%20vs%20Actual.png)
![Seasonal-naive Forecast with error range](visuals/Forecasted%20Crime%20Counts%20v2%20with%20Range.png)
![Combined Forecast (v2, corrected)](visuals/Combined%20Forecast%20v2.png)

## 🧰 Tech Stack

- Python  
- Pandas, NumPy  
- Scikit‑learn  
- Matplotlib, Seaborn  
- Jupyter Notebook  
- Git & GitHub  

## 🛠️ How to Run This Project

### 1. Clone the repository
```bash
git clone https://github.com/simon-gillies/Police-Demand-Forecasting.git
cd Police-Demand-Forecasting
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the tests
```bash
python -m pytest
```

### 4. Open the notebook
Open `notebooks/Police_Demand_Forecasting_Monthly.ipynb` in Jupyter or VS Code and run all cells.

## 📝 Full Notebook
The full analysis and forecasting pipeline is available in:
notebooks/Police_Demand_Forecasting_Monthly.ipynb
This includes:

EDA

Time analysis

Feature engineering

Model training

Forecasting

Final summary

## 🔭 Potential enhancements:

Several enhancements could be explored in a future iteration:

- Incorporate external predictors (weather, events, socio-economic indicators)
- Forecast individual crime types separately
- Build an interactive dashboard (Power BI or Streamlit)
- Deploy as an automated monthly pipeline
- Extend forecasting to geographic granularity (LSOA-level models)

👤 Author
Simon Gillies