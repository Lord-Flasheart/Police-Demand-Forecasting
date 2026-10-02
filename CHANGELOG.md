# Changelog

## v2.0 (2026-09-30)

### Fixed
- **Data leak in `Crime_Count_roll3`.** The 3-month rolling average
  included the current month, allowing the model to reconstruct the
  target it was meant to predict. Proven by manual reconstruction,
  model coefficients, and an automated test (`tests/test_no_leakage.py`).
  Fixed in `src/features.py` by shifting the series before the rolling
  average. See `docs/learning_log.md` for the full investigation.

### Changed
- Retrained Linear Regression and Random Forest on corrected features.
  LR's R² dropped from 1.0 (artefact of the leak) to 0.16 (a genuine, if
  weak, result). RF's MAE rose slightly (305.9 → 352.9) but RMSE and R²
  improved marginally.
- Added a seasonal-naive baseline and a walk-forward backtest
  (`results/v2_metrics.md`), which found seasonal-naive outperforms all
  other methods tested, including a purpose-built Holt-Winters model.
- Replaced the final Jul–Dec 2026 forecast with one built from
  seasonal-naive, including an honest error range per month.
- Rewrote the README: honest results, added Limitations and Data Ethics
  sections, fixed folder/filename inconsistencies, added run
  instructions.

### Added
- `src/features.py`, `tests/test_no_leakage.py` — reusable, tested
  feature-building logic (DRY: one function for both training and
  forecasting).
- `docs/learning_log.md` — investigation record.
- `results/v1_baseline.md`, `results/v2_metrics.md` — before/after
  metrics.
- `.gitignore` for `venv/` and related folders.

## v1.0-original (2026-08-19, approximate)
Initial version, as originally announced on LinkedIn. Tagged as
[`v1.0-original`](../../tree/v1.0-original) for reference. Contains the
data leak described above.