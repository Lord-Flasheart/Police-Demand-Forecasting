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

## Comparison against seasonal-naive baseline (section 4.7) Step 3

| Model | MAE | RMSE |
|---|---|---|
| Seasonal-naive | 172.5 | 207.77 |
| LR v2 (corrected) | 563.83 | 667.56 |
| RF v2 (corrected) | 352.93 | 431.47 |

The seasonal-naive baseline — predicting each month equals the same month
last year, with no learning at all — beats both trained models by a wide
margin. With only 27-32 months of training data, there is not enough
history for either model to learn more than the direct seasonal
relationship already captures. This will be tested more rigorously with a
walk-forward backtest (section 4.8) across multiple time windows rather
than this single six-month test period.

## Walk-forward backtest (section 4.8)

4 origins, 6-month horizon each, 24 test points total.

| Model | Overall MAE |
|---|---|
| Seasonal-naive | 188.1 |
| LR v2 | 526.9 |
| RF v2 | 361.5 |

Confirms the single-split finding in section 4.7: seasonal-naive
outperforms both trained models. Given only 4 origins, per-horizon
breakdowns are noisy and not individually reliable, but the overall
comparison across 24 points is meaningfully more robust than one test
split.

## Holt-Winters comparison (section 4.9)

| Model | Overall MAE |
|---|---|
| Seasonal-naive | 188.1 |
| Holt-Winters | 299.8 |
| Random Forest (v2) | 361.5 |
| Linear Regression (v2) | 526.9 |

Holt-Winters, a statistical method purpose-built for trend + seasonality,
beats both trained ML models but still doesn't beat seasonal-naive. Its
error rises more smoothly with horizon (236.6 at 1 month ahead, 430.9 at
6 months) than naive's, which is a point in its favour even though its
overall MAE is higher.

## Final forecast (section 5.4)

Using seasonal-naive, refit on all available data:

| Month | Forecast | Typical error (MAE) | Low | High |
|---|---|---|---|---|
| Jul 2026 | 10,774 | 320 | 10,454 | 11,094 |
| Aug 2026 | 10,026 | 250 | 9,776 | 10,276 |
| Sep 2026 | 9,593 | 122 | 9,471 | 9,715 |
| Oct 2026 | 9,958 | 96 | 9,862 | 10,054 |
| Nov 2026 | 9,019 | 148 | 8,871 | 9,167 |
| Dec 2026 | 8,966 | 192 | 8,774 | 9,158 |

Sense-check: July 2026's forecast (10,774) exactly matches July 2025's
actual value, confirming the method is working correctly.

December's corrected forecast (8,966) is much closer to historical
Decembers (8,992, 8,787, 8,966) than the original leaked forecast (9,909,
about 11% above every prior December) — concrete evidence the leak
distorted the final forecast, not just the test metrics.

## Recommendation

Seasonal-naive is recommended for this dataset, based on both a single
split and a walk-forward backtest. This is not a permanent conclusion:
with only 36 months of data, more complex methods haven't had enough
history to show their potential advantage, and the comparison should be
re-run as more data accumulates.