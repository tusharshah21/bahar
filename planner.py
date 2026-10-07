"""Score every hour of today and find the best window to be outside."""
from dataclasses import dataclass

import pandas as pd

import config as C

# India's National AQI bands for PM2.5 (µg/m³).
AQI_BANDS = [(30, "Good", 1.0), (60, "Satisfactory", 0.8), (90, "Moderate", 0.5),
             (120, "Poor", 0.2), (250, "Very poor", 0.05), (float("inf"), "Severe", 0.0)]


def air_band(pm):
    for limit, label, score in AQI_BANDS:
        if pm <= limit:
            return label, score
    return "Severe", 0.0


def heat_score(feels_like):
    if feels_like <= 30:
        return 1.0
    if feels_like >= 40:
        return 0.1
    return 1.0 - 0.09 * (feels_like - 30)


def rain_score(mm):
    return 1.0 if mm < 0.2 else 0.6 if mm < 1 else 0.2


@dataclass
class Window:
    start: pd.Timestamp
    end: pd.Timestamp
    score: float
    pm25: float
    feels_like: float
    air_label: str


def score_hours(day: pd.DataFrame) -> pd.DataFrame:
    d = day.copy()
    d["air_label"] = d["pm25_pred"].apply(lambda v: air_band(v)[0])
    d["air_score"] = d["pm25_pred"].apply(lambda v: air_band(v)[1])
    d["heat_score"] = d["apparent_temperature"].apply(heat_score)
    d["rain_score"] = d["precipitation"].apply(rain_score)
    d["score"] = d["air_score"] * 0.55 + d["heat_score"] * 0.3 + d["rain_score"] * 0.15
    hrs = d["time"].dt.hour
    d.loc[(hrs < C.EARLIEST_HOUR) | (hrs > C.LATEST_HOUR), "score"] = 0
    return d


def best_window(scored: pd.DataFrame, min_hours=1, max_hours=3) -> Window:
    s = scored.reset_index(drop=True)
    best = None
    for length in range(min_hours, max_hours + 1):
        for i in range(len(s) - length + 1):
            chunk = s.iloc[i:i + length]
            if (chunk["score"] == 0).any():
                continue
            # Small bonus for longer windows, so a 2-hour good stretch beats 1 great hour.
            val = chunk["score"].mean() + 0.02 * (length - 1)
            if best is None or val > best[0]:
                best = (val, chunk)
    if best is None:
        return None
    _, c = best
    return Window(c["time"].iloc[0], c["time"].iloc[-1] + pd.Timedelta(hours=1),
                  round(float(c["score"].mean()), 2), round(float(c["pm25_pred"].mean()), 1),
                  round(float(c["apparent_temperature"].mean()), 1),
                  air_band(c["pm25_pred"].mean())[0])


def suggest_activity(w: Window) -> str:
    if w is None or w.score < 0.35:
        return "an indoor day; maybe a short walk only if you must"
    if w.score >= 0.8:
        return "a run, a cycle, or a game of cricket in the park"
    if w.score >= 0.6:
        return "a brisk walk or easy jog"
    return "a gentle walk, no hard exercise"
