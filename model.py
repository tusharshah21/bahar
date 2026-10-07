"""TabPFN regressor for hourly PM2.5, with a fallback so the app never dies."""
import warnings

import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

import config as C
from features import FEATURES

warnings.filterwarnings("ignore")


def make_tabpfn():
    from tabpfn import TabPFNRegressor  # first run downloads open weights
    # One estimator scores within noise of 'auto' here and is ~20x faster on CPU.
    return TabPFNRegressor(device="cpu", ignore_pretraining_limits=True, n_estimators=1)


def make_gbm():
    return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0)


def context(train: pd.DataFrame, rows: int = C.TABPFN_CONTEXT_ROWS, seed: int = 0) -> pd.DataFrame:
    """Pick the examples TabPFN sees: half the most recent rows, half a random spread
    from the whole history (so it also remembers last year's October)."""
    train = train.dropna(subset=FEATURES + ["pm2_5"])
    if len(train) <= rows:
        return train
    recent = train.tail(rows // 2)
    older = train.iloc[: -rows // 2].sample(rows - len(recent), random_state=seed)
    return pd.concat([older, recent])


def fit_predict(train: pd.DataFrame, target_rows: pd.DataFrame):
    """Returns (predictions, model_name)."""
    ctx = context(train)
    X, y = ctx[FEATURES], ctx["pm2_5"]
    Xt = target_rows[FEATURES].fillna(X.median())
    try:
        m = make_tabpfn()
        m.fit(X, y)
        return m.predict(Xt), "TabPFN"
    except Exception as e:  # missing package, weights not downloaded, etc.
        print(f"[bahar] TabPFN unavailable ({type(e).__name__}: {e}); using gradient boosting.")
        m = make_gbm().fit(train.dropna(subset=FEATURES + ['pm2_5'])[FEATURES],
                           train.dropna(subset=FEATURES + ['pm2_5'])["pm2_5"])
        return m.predict(Xt), "GradientBoosting (fallback)"
