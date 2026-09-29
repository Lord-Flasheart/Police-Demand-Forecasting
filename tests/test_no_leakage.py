import numpy as np
import pandas as pd
from src.features import make_features


def test_features_up_to_t_ignore_target_at_t():
    idx = pd.date_range("2023-07-01", periods=36, freq="MS")
    s = pd.Series(np.random.default_rng(0).normal(10000, 500, 36), index=idx)

    for t in (5, 15, 30):
        s2 = s.copy()
        s2.iloc[t] += 1000  # change only month t

        feats_original = make_features(s)
        feats_changed = make_features(s2)

        pd.testing.assert_frame_equal(
            feats_original.iloc[: t + 1],
            feats_changed.iloc[: t + 1],
        )