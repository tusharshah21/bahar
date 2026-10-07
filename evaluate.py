"""How good is the forecast? Compares TabPFN against two baselines on the last
N days of history the model never saw. Produces the chart for your DEV post.

Run:  python evaluate.py          (after fetch_data.py)
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config as C
import features
import model

TEST_DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 21


def metrics(y, p):
    err = np.asarray(p) - np.asarray(y)
    return {"MAE": round(float(np.mean(np.abs(err))), 2),
            "RMSE": round(float(np.sqrt(np.mean(err ** 2))), 2)}


def backtest(df, seeds=3):
    """Rolling-origin backtest: 21-day windows across the seasons, each model trained
    only on hours before its window. TabPFN is averaged over a few context samples."""
    F, rows = features.FEATURES, []
    first = df["time"].min() + pd.Timedelta(days=90)
    last = df["time"].max() - pd.Timedelta(days=TEST_DAYS)
    for start in pd.date_range(first.normalize(), last, freq="45D"):
        train = df[df["time"] < start]
        test = df[(df["time"] >= start) & (df["time"] < start + pd.Timedelta(days=TEST_DAYS))]
        tab = []
        for s in range(seeds):
            ctx = model.context(train, seed=s)
            tab.append(metrics(test["pm2_5"], model.make_tabpfn().fit(ctx[F], ctx["pm2_5"]).predict(test[F]))["MAE"])
        gbm = model.make_gbm().fit(train[F], train["pm2_5"]).predict(test[F])
        rows.append({"start": str(start.date()), "train_hours": len(train),
                     "TabPFN": round(float(np.mean(tab)), 2),
                     "Gradient boosting": metrics(test["pm2_5"], gbm)["MAE"],
                     "Same as yesterday": metrics(test["pm2_5"], test["pm25_lag24"])["MAE"]})
        print("  ", rows[-1])
    wins = sum(r["TabPFN"] < r["Gradient boosting"] for r in rows)
    avg = {k: round(float(np.mean([r[k] for r in rows])), 2)
           for k in ("TabPFN", "Gradient boosting", "Same as yesterday")}
    print(f"TabPFN beats gradient boosting in {wins} of {len(rows)} windows; average MAE {avg}")
    return rows


def plot_backtest(rows):
    fig, ax = plt.subplots(figsize=(10, 4.5))
    x = pd.to_datetime([r["start"] for r in rows])
    for key, color, ls, lw in [("TabPFN", "#2a9d8f", "-", 2), ("Gradient boosting", "#7b4fbf", "-", 2),
                               ("Same as yesterday", "#e76f51", "--", 1)]:
        y = [r[key] for r in rows]
        ax.plot(x, y, color=color, ls=ls, lw=lw, marker="o", ms=7 if lw == 2 else 0, label=key)
    ax.set_ylabel("Mean abs. error, PM2.5 (µg/m³)")
    ax.set_xlabel("Start of each 3-week test window (trained only on earlier data)")
    ax.set_title(f"{C.CITY}: forecast error through the seasons (lower is better)")
    ax.grid(axis="y", color="#ddd", lw=0.6)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = os.path.join(C.DATA_DIR, "backtest.png")
    fig.savefig(out, dpi=150)
    print(f"Chart saved to {out}")


def main():
    df = features.build(pd.read_csv(C.HISTORY_CSV, parse_dates=["time"]))
    df = df.dropna(subset=features.FEATURES + ["pm2_5"])
    cutoff = df["time"].max() - pd.Timedelta(days=TEST_DAYS)
    train, test = df[df["time"] <= cutoff], df[df["time"] > cutoff]
    print(f"Train {len(train):,} rows, test {len(test):,} rows ({TEST_DAYS} days)")

    pred, name = model.fit_predict(train, test)
    gbm = model.make_gbm().fit(train[features.FEATURES], train["pm2_5"]).predict(test[features.FEATURES])

    results = {
        name: metrics(test["pm2_5"], pred),
        "Gradient boosting (all history)": metrics(test["pm2_5"], gbm),
        "Same as yesterday": metrics(test["pm2_5"], test["pm25_lag24"]),
    }
    print(json.dumps(results, indent=2))
    if name == "TabPFN":
        print("Backtest across the seasons:")
        results["backtest"] = backtest(df)
        plot_backtest(results["backtest"])
    with open(os.path.join(C.DATA_DIR, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    last = test.tail(24 * 7)
    p = pd.Series(pred, index=test.index).loc[last.index]
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(last["time"], last["pm2_5"], label="Actual", color="#222", lw=1.6)
    ax.plot(last["time"], p, label=name, color="#2a9d8f", lw=1.6)
    ax.plot(last["time"], last["pm25_lag24"], label="Same as yesterday", color="#e76f51", lw=1, ls="--")
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_title(f"{C.CITY}: hourly PM2.5, last 7 test days")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = os.path.join(C.DATA_DIR, "accuracy.png")
    fig.savefig(out, dpi=150)
    print(f"Chart saved to {out}")


if __name__ == "__main__":
    main()
