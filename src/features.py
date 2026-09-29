import pandas as pd


def make_features(s: pd.Series) -> pd.DataFrame:
    """
    Build model features from a monthly crime-count Series.
    s: a pandas Series of counts, indexed by month-start dates.

    NOTE: this currently reproduces the v1 notebook logic,
    including the roll3 leakage. It will be corrected in Step 2.
    """
    return pd.DataFrame({
        "lag1": s.shift(1),
        "lag2": s.shift(2),
        "lag3": s.shift(3),
        "roll3": s.rolling(3).mean(),   # v1 logic: includes the current month
        "month": s.index.month,
    })