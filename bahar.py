"""Bahar: the best hour today to go outside.

Run:  python bahar.py            (prints and speaks today's plan)
      python bahar.py --quiet    (no voice)
"""
import json
import os
import sys

import pandas as pd

import config as C
import features
import fetch_data
import model
import narrator
import planner


def _fmt(t: pd.Timestamp) -> str:
    return t.strftime("%I:%M %p").lstrip("0")


def plan_today(now: pd.Timestamp | None = None) -> dict:
    now = now or pd.Timestamp.now(tz=C.TIMEZONE).tz_localize(None)
    history = features.build(pd.read_csv(C.HISTORY_CSV, parse_dates=["time"]))

    fc = fetch_data.fetch_today()
    fc = features.build(fc, pm_col="pm2_5_cams")

    # Plan for the rest of today; after 7 PM, plan tomorrow.
    target_day = now.normalize() + (pd.Timedelta(days=1) if now.hour >= 19 else pd.Timedelta(0))
    when = "tomorrow" if target_day > now.normalize() else "today"
    day = fc[fc["time"].dt.normalize() == target_day].copy()
    if when == "today":
        day = day[day["time"] >= now.floor("h")]

    day["pm25_pred"], model_name = model.fit_predict(history, day)
    day["pm25_pred"] = day["pm25_pred"].clip(lower=0)
    scored = planner.score_hours(day)
    w = planner.best_window(scored)

    daylight = scored[scored["score"] > 0]
    worst = daylight.loc[daylight["score"].idxmin()] if len(daylight) else None
    worst_txt = f"the hours around {_fmt(worst['time'])}" if worst is not None else "the late evening"

    facts = {
        "when": when,
        "start": _fmt(w.start) if w else "none",
        "end": _fmt(w.end) if w else "none",
        "air": w.air_label if w else "Poor",
        "pm": w.pm25 if w else "-",
        "feels": w.feels_like if w else "-",
        "activity": planner.suggest_activity(w),
        "worst": worst_txt,
    }
    text, writer = narrator.write_plan(facts)
    hourly = scored[["time", "pm25_pred", "pm2_5_cams", "apparent_temperature",
                     "precipitation", "air_label", "score"]]
    return {"facts": facts, "text": text, "window": w, "hourly": hourly,
            "model": model_name, "writer": writer}


def log_plan(result: dict):
    """Keeps a record so you can compare predictions with what actually happened outside."""
    path = os.path.join(C.DATA_DIR, "plans_log.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps({"made_at": pd.Timestamp.now().isoformat(),
                            **result["facts"], "model": result["model"],
                            "writer": result["writer"], "text": result["text"]}) + "\n")


if __name__ == "__main__":
    if not os.path.exists(C.HISTORY_CSV):
        sys.exit("No history yet. Run:  python fetch_data.py")
    r = plan_today()
    log_plan(r)
    print("\n" + r["text"] + "\n")
    print(f"(forecast: {r['model']}, words: {r['writer']})")
    if "--quiet" not in sys.argv:
        narrator.speak(r["text"])
