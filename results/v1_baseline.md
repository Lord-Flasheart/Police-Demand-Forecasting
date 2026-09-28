# v1 baseline results (before any changes)

- Source: notebooks/Police_Demand_Forecasting_Monthly.ipynb
- Code state: tag v1.0-original (commit 2413050)
- Run date: 2026-09-28, kernel restarted, Run All

## Linear Regression (section 4.2)
MAE 5.4569682106375694e-12 | RMSE 6.8865827364792174e-12 | R² 1.0

## Random Forest (section 4.3)
MAE 305.8455555555559 | RMSE 437.25507966047576 | R² 0.6407651820766519

Feature importance:

| Feature | Importance |
|---|---|
| Crime_Count_roll3 | 0.657216 |
| Crime_Count_lag3 | 0.115102 |
| Month_num | 0.103847 |
| Crime_Count_lag1 | 0.072668 |
| Crime_Count_lag2 | 0.036203 |
| Quarter | 0.009172 |
| Year | 0.005791 |

## Recursive forecast Jul-Dec 2026 (section 5.2)

| Year | Month_num | Predicted_Crime_Count |
|---|---|---|
| 2026 | 7 | 10298.410000 |
| 2026 | 8 | 10335.263333 |
| 2026 | 9 | 10280.453333 |
| 2026 | 10 | 10196.476667 |
| 2026 | 11 | 10018.006667 |
| 2026 | 12 | 9909.136667 |

## Observations

Test set: Jan to Jun 2026. Error = Actual − Predicted (negative means the model over-predicted).

| Month (2026) | Actual | RF predicted | Error | Abs error |
|---|---|---|---|---|
| Jan | 8,945 | 9,028.8 | −83.9 | 83.9 |
| Feb | 8,515 | 9,496.1 | −981.1 | 981.1 |
| Mar | 9,943 | 9,737.9 | +205.1 | 205.1 |
| Apr | 9,637 | 9,587.3 | +49.7 | 49.7 |
| May | 10,289 | 10,041.0 | +248.0 | 248.0 |
| Jun | 10,606 | 10,338.8 | +267.2 | 267.2 |

Mean absolute error: 305.85 (average of the six absolute errors, checked in the notebook).

- February has the largest error (981.1), about 53% of the total absolute error of 1,835.0. Without February the MAE of the other five months is about 171.
- The model over-predicts in the two winter months (Jan, Feb) and under-predicts every month from March.
- Hypothesis: the model follows recent levels and lags behind the seasonal swing instead of capturing it. To be tested in the v2 backtest.