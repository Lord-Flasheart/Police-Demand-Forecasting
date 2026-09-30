# v2 metrics: after fixing the roll3 leak

- Run date: 2026-09-30
- Source: notebooks/Police_Demand_Forecasting_Monthly.ipynb, sections 4.5–4.6
- Features from `src/features.py` via `model_df_v2` (see section 3.6)

## Linear Regression (section 4.5, v2 of 4.2)
MAE 563.8340574048698 | RMSE 667.5584522178598 | R² 0.16268804097144618

## Random Forest (section 4.6, v2 of 4.3)
MAE 352.9283333333333 | RMSE 431.47064901034395 | R² 0.6502069212449074

Feature importance (v2):

| Feature | Importance |
|---|---|
| Crime_Count_lag1 | 0.470518 |
| Month_num | 0.278691 |
| Crime_Count_lag3 | 0.108174 |
| Crime_Count_roll3 | 0.068780 |
| Crime_Count_lag2 | 0.049572 |
| Year | 0.014922 |
| Quarter | 0.009343 |

## Comparison with v1

| Metric | v1 (leaked) | v2 (corrected) | Change |
|---|---|---|---|
| LR MAE | ~0 | 563.83 | Now realistic — v1 was never actually predicting anything |
| LR R² | 1.0 | 0.163 | A perfect score was entirely the leak |
| RF MAE | 305.85 | 352.93 | Slightly worse |
| RF RMSE | 437.26 | 431.47 | Slightly better |
| RF R² | 0.641 | 0.650 | Slightly better |

## Interpretation

Fixing the leak collapsed Linear Regression's score from perfect to weak but
genuine (R² 0.16). Random Forest was almost unaffected overall, and actually
improved slightly on RMSE and R², though MAE rose. This suggests the forest
was not heavily dependent on the leaked feature, and correctly shifted its
reliance to `Crime_Count_lag1` and `Month_num` once `roll3` no longer
contained the answer. Whether either model beats a simple seasonal-naive
forecast is still to be tested properly in Step 3.