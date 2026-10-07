"""Pull hourly weather + PM2.5 history (and today's forecast) from Open-Meteo.

Free, no API key. Run:  python fetch_data.py
"""
from datetime import date, timedelta

import pandas as pd
import requests

import config as C

ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
FORECAST = "https://api.open-meteo.com/v1/forecast"
AIR = "https://air-quality-api.open-meteo.com/v1/air-quality"


def _get(url, params):
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    h = r.json()["hourly"]
    df = pd.DataFrame(h)
    df["time"] = pd.to_datetime(df["time"])
    return df


def _base():
    return {"latitude": C.LAT, "longitude": C.LON, "timezone": C.TIMEZONE}


def _chunks(start, end, days=90):
    cur = start
    while cur <= end:
        stop = min(cur + timedelta(days=days - 1), end)
        yield cur, stop
        cur = stop + timedelta(days=1)


def fetch_history(days=C.HISTORY_DAYS):
    # The weather archive lags a few days behind real time.
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=days)
    weather, air = [], []
    for a, b in _chunks(start, end):
        p = {**_base(), "start_date": a.isoformat(), "end_date": b.isoformat()}
        weather.append(_get(ARCHIVE, {**p, "hourly": ",".join(C.WEATHER_VARS)}))
        air.append(_get(AIR, {**p, "hourly": "pm2_5"}))
        print(f"  fetched {a} to {b}")
    df = pd.concat(weather).merge(pd.concat(air), on="time", how="inner")
    df = df.dropna(subset=["pm2_5"]).drop_duplicates("time").sort_values("time")
    df.to_csv(C.HISTORY_CSV, index=False)
    print(f"Saved {len(df):,} hourly rows to {C.HISTORY_CSV}")
    return df


def fetch_today():
    """Weather forecast plus air-quality model output for yesterday, today and tomorrow."""
    p = {**_base(), "past_days": 1, "forecast_days": 2}
    w = _get(FORECAST, {**p, "hourly": ",".join(C.WEATHER_VARS + ["apparent_temperature", "is_day"])})
    a = _get(AIR, {**p, "hourly": "pm2_5"}).rename(columns={"pm2_5": "pm2_5_cams"})
    return w.merge(a, on="time", how="left")


if __name__ == "__main__":
    print(f"Fetching {C.HISTORY_DAYS} days of history for {C.CITY}...")
    fetch_history()
