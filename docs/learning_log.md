# ==============================
# Learning log
# ==============================

## Step 1: Leakage investigation (2026-09-28)

### Hypothesis: why was R² exactly 1.0?

**My first answer (before review):**
R² was 1.0 because the calculation was rolling up using the current month. A perfect R² jumps out as something to check for leakage.

**Corrected after review** (wording refined with AI coaching, Claude):
R² was 1.0 because my 3 month rolling average included the current month, which is the value I was predicting. The model could rebuild the target from the features, so the score was too good to be true. A perfect R² on real-world data is a signal to check for leakage.

- **Which features could contain the target?** Only `Crime_Count_roll3`. The lags come from `shift()`, which looks backwards, so they are fine.
- **How would I confirm it?** Print the first rows, work out which numbers roll3 averages, and test whether the target can be rebuilt from the other columns.

**Note on my first answer:** I mixed up the fix with the seasonal-naive benchmark (same month last year). That is a comparison model used later for evaluation. The fix for the leak is building the rolling mean from earlier months only.

### What I found

(Add after running the proof cells.)

- <one or two lines in your own words>