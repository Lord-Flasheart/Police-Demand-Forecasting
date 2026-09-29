import pandas as pd


def make_features(s: pd.Series) -> pd.DataFrame:
    """
    Build model features from a monthly crime-count Series.
    s: a pandas Series of counts, indexed by month-start dates.

    Each feature for month t uses only data from before month t,
    so it can be used safely for both training and forecasting.
    """
    return pd.DataFrame({
        "lag1": s.shift(1),
        "lag2": s.shift(2),
        "lag3": s.shift(3),
        "roll3": s.shift(1).rolling(3).mean(),   # fixed: excludes month t
        "month": s.index.month,
    })