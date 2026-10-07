# Bahar 🌿

**The best hour today to go outside, then off your screen.**

Bahar ("outside" in Hindi/Urdu) forecasts hourly PM2.5 for your city with **TabPFN**, combines it with heat and rain into a "go outside" score, finds the best window, and has **Gemma** (running locally) tell you the plan in two sentences. Everything core runs on a laptop with no paid API.

Built for the DEV Hacktoberfest Open-Source AI Challenge, Week 1: *Touch Grass*.

## How it works

1. `fetch_data.py` pulls ~18 months of hourly weather + PM2.5 for your city from Open-Meteo (free, no key).
2. `model.py` hands TabPFN a few thousand example hours (in-context learning, no training loop) and asks it to predict today's PM2.5 from the weather forecast.
3. `planner.py` scores each hour: air quality (India's AQI bands) 55%, heat 30%, rain 15%, then picks the best 1 to 3 hour window.
4. `narrator.py` asks Gemma via Ollama to write the plan, and can read it aloud offline.

If TabPFN or Ollama isn't available, Bahar falls back to gradient boosting and a template sentence, so it never breaks.

## Setup (Windows / Mac / Linux, CPU is fine)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

**Gemma:** install Ollama from ollama.com, then:

```bash
ollama pull gemma4:e4b-it-qat
```

On a slower laptop, `gemma4:e2b-it-qat` is smaller and faster; set `BAHAR_MODEL` to its tag.

**TabPFN:** the first run downloads the open weights. Newer TabPFN versions may ask you to accept the license and log in to Hugging Face once; follow the message it prints.

## Run

```bash
python fetch_data.py        # once, ~1 min
python evaluate.py          # accuracy vs baselines + data/accuracy.png and data/backtest.png
python bahar.py             # today's plan, printed and spoken
streamlit run app.py        # the one-screen app
```

Change the city in `config.py`. If TabPFN is slow on your laptop, lower `BAHAR_CONTEXT_ROWS` (e.g. `set BAHAR_CONTEXT_ROWS=1000`).

Each run appends to `data/plans_log.jsonl` so you can compare what Bahar predicted with how the air actually felt outside.

## Honest caveat

Open-Meteo's air quality data is from the CAMS atmospheric model, not ground sensors. It's great for patterns and free history; for ground truth, compare a few days against CPCB station readings for your area.
