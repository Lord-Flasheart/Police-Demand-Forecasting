# Learning log

Investigation record for the Police Demand Forecasting project: what was
wrong with the original model, how I found it, and how I fixed it.

## 1.4–1.5: Leakage investigation (2026-09-28)

### Hypothesis: why was R² exactly 1.0?

**My first answer (before review):**
R² was 1.0 because the calculation was rolling up using the current
month. A perfect R² jumps out as something to check for leakage.

**Corrected after review** (wording refined with AI coaching, Claude):
R² was 1.0 because my 3-month rolling average included the current
month, which is the value I was predicting. The model could rebuild the
target from the features, so the score was too good to be true. A
perfect R² on real-world data is a signal to check for leakage.

- **Which features could contain the target?** Only `Crime_Count_roll3`.
  The lags come from `shift()`, which looks backwards, so they are fine.
- **How would I confirm it?** Print the first rows, work out which
  numbers roll3 averages, and test whether the target can be rebuilt
  from the other columns.

**Note on my first answer:** I mixed up the fix with the seasonal-naive
benchmark (same month last year). That is a comparison model used later
for evaluation. The fix for the leak is building the rolling mean from
earlier months only.

### What I found

- **Worked example:** for October 2023, (10,766 [Aug] + 10,587 [Sep] +
  10,289 [Oct]) / 3 = 10,547.33, which equals `Crime_Count_roll3`. The
  October target (10,289) is inside its own feature.
- **Rebuilding the target:** 3 × roll3 − lag1 − lag2 reproduces the
  actual crime count exactly, across all 33 rows. The maximum absolute
  difference was 0.0.
- **Coefficients:** the linear model learned roll3 = +3, lag1 = −1,
  lag2 = −1, and 0 for everything else — the same formula, so the model
  was recovering the target rather than forecasting it.
- **Random Forest without roll3:** MAE 364.51 and RMSE 446.13, both
  worse than the v1 baseline (305.85, 437.26), showing the forest was
  also benefiting from the leak, though with only 27 training rows the
  exact size of this gap should be treated cautiously.

## 1.6: Automated test (2026-09-28)

Wrote `src/features.py` (reproducing the v1 logic) and
`tests/test_no_leakage.py`, which checks that changing one month's value
doesn't change features for that month or earlier. Running it against v1
fails exactly as expected: the `roll3` column changes, confirming the
leak mechanically rather than just by hand calculation. Saved the
failure output to `docs/evidence/leakage_test_v1_fail.txt`.

Step 1 is complete: the leak is proven by hand, by algebra, by the
model's own coefficients, and by an automated test.

## 2: The fix (2026-09-29)

Corrected `src/features.py` so `roll3` is built as
`s.shift(1).rolling(3).mean()`, excluding the current month. Re-ran
`tests/test_no_leakage.py` — the same test that failed on v1 now passes.
Saved to `docs/evidence/leakage_test_v2_pass.txt`.

Retrained LR and RF on the corrected features (`model_df_v2`, notebook
section 3.6):
- LR: R² dropped from 1.0 to 0.16 — a genuine, if weak, result.
- RF: MAE rose slightly (305.9 → 352.9), but RMSE and R² improved
  marginally (437.3 → 431.5, 0.641 → 0.650).
- Feature importance shifted from `roll3` (0.657, now meaningless) to
  `lag1` (0.471) and `Month_num` (0.279) — the model correctly moved its
  trust onto real signal once the leak was removed.

Full numbers recorded in `results/v2_metrics.md`.

## 3–4: Finding a fair benchmark (2026-09-30)

Added a seasonal-naive baseline (predict each month as equal to the same
month last year) and a walk-forward backtest across 3 origins. Result:
seasonal-naive (MAE 188.1) beat Holt-Winters (299.8), Random Forest
(361.5), and Linear Regression (526.9). With only 36 months of data,
none of the more complex methods had enough history to beat simply
reusing last year's figure.

Final Jul–Dec 2026 forecast built from seasonal-naive, refit on all
data, with an error range from the backtest. Sense-checked against
history: July 2026's forecast exactly matches July 2025's actual value,
and December's corrected forecast (8,966) sits much closer to past
Decembers than the original leaked forecast (9,909).

## Note: apparent duplicate count (2026-10-02)

Investigated and resolved as not a real data quality issue.
`duplicated()` compares row contents but ignores the DataFrame index
(Month), so different crimes sharing identical category values (common
for ASB records, which have no Crime ID) are flagged as duplicates.
Crime ID uniqueness (312,584 unique IDs across 312,584 non-null records)
confirms there is no genuine duplication.