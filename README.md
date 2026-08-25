📘 Police Demand Forecasting (Norfolk & Suffolk)

## 🧭 Project Summary

This project analyses crime demand between **July 2023 and June 2026**, exploring crime types, outcomes, geographic hotspots, seasonal patterns, and long‑term trends.
A Random Forest model is used to generate a **6‑month forward forecast (Jul–Dec 2026)** based on engineered temporal features.


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

The final model produces a 6‑month forecast (Jul–Dec 2026) using engineered temporal features and a Random Forest regressor.

## 📈 Key Visuals

### Crime Type Distribution
![Crime Type Distribution](Crime%20Type%20Distribution%201_4.png)

### Outcome Category Distribution
![Outcome Category Distribution](Outcome%20Category%20Distribution%201_5.png)

### Crime Type × Outcome Heatmap
![Crime Type x Outcome Heatmap](Crime%20Type%20x%20Outcome%20Heatmap%201_7.png)

### Top 10 LSOAs
![Top 10 LSOA](Top%2010%20LSOA%201_6.png)

### Top 5 Crime Types with No Suspect Identified
![Top 5 Crime Types](Top%205%20Crime%20Types%20with%20No%20Suspect%20Identified%201_7.png)

### Monthly Crime Demand
![Monthly Crime Demand](Monthly%20Crime%20Demand%202_1.png)

### Monthly Crime Demand with Trend Line
![Monthly Crime Demand Trend](Monthly%20Crime%20Demand%20with%20Trend%20Line%202_2.png)

### Seasonal Profile — Average Crime Demand by Month
![Seasonal Profile](Seasonal%20Profile%20Average%20Crime%20Demand%20by%20Month%202_3.png)

### Combined Forecasted Crime Counts (Jul–Dec 2026)
![Combined Forecast](Combined%20Forecasted%20Crime%20Counts%20(Jul_Dec26)%205_3.png)

### Forecasted Crime Counts (Jul–Dec 2026)
![Forecasted Crime](Forecasted%20Crime%20Counts%20(Jul_Dec26)%205_3.png)

### Actual vs Predicted — Linear Regression
![LR Actual vs Predicted](Actual%20vs%20Predicted%20(Linear%20Regression)%204_2.png)

### Actual vs Predicted — Random Forest
![RF Actual vs Predicted](Actual%20vs%20Predicted%20(Random%20Forest)%204_3.png)

### LR vs RF Comparison
![LR vs RF](LR%20vs%20RF%204_4.png)

### Time Analysis by Month
![Time Analysis Month](6%20time%20analysis%20month.png)


🎯 Objectives
Understand crime demand behaviour across 36 months

Identify seasonal patterns and long‑term trends

Analyse geographic hotspots and outcome structures

Engineer modelling‑ready temporal features

Train and evaluate forecasting models

Produce a forward‑looking demand forecast

📂 Repository Structure
├── data/                     # Raw monthly CSV files
├── notebooks/
│   └── Police_Demand_Forecasting_Monthly.ipynb   # Full analysis + forecasting notebook
├── visuals/                  # Plots and charts
├── README.md                 # Project documentation
└── report/
    └── Police_Demand_Forecasting_Report.pdf

## 🛠️ How to Run This Project

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/police-demand-forecasting.git
cd police-demand-forecasting
```

🧪 Exploratory Data Analysis (EDA)
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

📈 Time Analysis
Monthly Demand
Highest month: July 2023 (11,418 incidents)

Lowest month: February 2025 (8,412 incidents)

Seasonal Pattern
Summer peaks (Jun–Aug)

Winter troughs (Dec–Feb)

Stable, repeating annual cycle

Trend
Slight long‑term decline

Seasonal variation dominates

🏗️ Feature Engineering
Features created for modelling:

Year

Month_num

Quarter

Season

Crime_Count (monthly aggregated target)

Lag features (t‑1, t‑2, t‑3)

Rolling mean (3‑month)

These features capture short‑term momentum and seasonal structure.

🤖 Models
Linear Regression
Perfect reconstruction due to lag features

Useful baseline

Not ideal for realistic forecasting

Random Forest Regressor
Captures non-linear seasonal behaviour

Produces smooth, realistic predictions

Strong feature importance alignment

Selected as the primary forecasting model

🔮 Forecasting (Jul–Dec 2026)
A recursive forecasting loop generates predictions month‑by‑month using:

Last 3 actual values

Updated lag features

Rolling mean

Forecast Summary
July–August: seasonal peak

September–November: gradual decline

December: winter trough

Forecast aligns with historical seasonal behaviour.

📊 Example Visuals
(Add your saved PNGs from the visuals folder)

Monthly crime demand

Seasonal profile

Crime type distribution

Outcome distribution

LSOA hotspots

LR vs RF comparison

Forecast plot

📝 Full Notebook
The full analysis and forecasting pipeline is available in:
notebooks/Police_Demand_Forecasting.ipynb
This includes:

EDA

Time analysis

Feature engineering

Model training

Forecasting

Final summary

🚀 Next Steps
Potential enhancements:

Add external predictors (weather, events, socio-economic data)

Forecast individual crime types

Build a dashboard (Power BI / Streamlit)

Deploy as an automated monthly pipeline

Add geographic forecasting (LSOA-level models)

👤 Author
Simon Gillies  