"""Turn hourly rows into model features."""
import numpy as np
import pandas as pd

import config as C

FEATURES = C.WEATHER_VARS + [
    "hour_sin", "hour_cos", "doy_sin", "doy_cos", "dow",
    "wind_u", "wind_v", "pm25_lag24",
]


def build(df: pd.DataFrame, pm_col: str = "pm2_5") -> pd.DataFrame:
    df = df.sort_values("time").copy()
    t = df["time"]
    df["hour_sin"] = np.sin(2 * np.pi * t.dt.hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * t.dt.hour / 24)
    df["doy_sin"] = np.sin(2 * np.pi * t.dt.dayofyear / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * t.dt.dayofyear / 365.25)
    df["dow"] = t.dt.dayofweek
    rad = np.deg2rad(df["wind_direction_10m"])
    df["wind_u"] = df["wind_speed_10m"] * np.sin(rad)
    df["wind_v"] = df["wind_speed_10m"] * np.cos(rad)
    # Same hour yesterday: the strongest single clue about today's air.
    lag = df[["time", pm_col]].copy()
    lag["time"] = lag["time"] + pd.Timedelta(hours=24)
    df = df.merge(lag.rename(columns={pm_col: "pm25_lag24"}), on="time", how="left")
    return df
