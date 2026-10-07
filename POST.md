---
title: Bahar: the best hour today to go outside, forecast by TabPFN and told by Gemma
published: false
tags: devchallenge, opensource, ai, python
---

*This is a submission for the DEV Hacktoberfest Open-Source AI Challenge, Week 1: Touch Grass.*

## What I Built

Bahar ("outside" in Hindi and Urdu) answers one question every morning: **when is the best hour today to get out of the house?**

In Hyderabad that question isn't trivial. Air quality changes a lot over a single day, summer afternoons can feel hotter than 40°C, and the monsoon brings sudden rain. Weather apps show you all of that as six separate charts. Bahar turns it into one sentence and then tells you to put your phone down.

How it works:

1. It pulls about 18 months of hourly weather and PM2.5 history for the city from Open-Meteo (free, no key).
2. **TabPFN** forecasts PM2.5 for every remaining hour today from the weather forecast.
3. Each hour gets a score: air quality using India's National AQI bands (55%), heat using the "feels like" temperature (30%), and rain (15%). Bahar picks the best 1 to 3 hour window between 5 AM and 7 PM.
4. **Gemma 4**, running locally in Ollama, writes the plan in two or three sentences, and the app can read it aloud offline.

Everything runs on my laptop: a Windows machine with an i7, 16 GB of RAM and no GPU. There's no paid API. The only network calls are the weather requests and TabPFN's license check.

## Demo

[Add a screenshot or short screen recording of the Streamlit app here]

Here's today's plan, word for word as Gemma wrote it:

> Hey friend, let's hit the park between 5:00 and 6:00 PM when the air quality is good. A run or a cycle sounds perfect for that evening cool. Put your phone away and enjoy the fresh air.

## Code

[Link to the GitHub repo]

```bash
python fetch_data.py        # once, about a minute
python evaluate.py          # accuracy charts
python bahar.py             # today's plan, printed and spoken
streamlit run app.py        # the one-screen app
```

## How I Used TabPFN

TabPFN is a foundation model for tables. Instead of training, you hand it example rows at prediction time and it learns from them in context. For Bahar, each row is one hour: temperature, humidity, wind (split into east and north components), rain, cloud cover, boundary layer height, time of day and season encoded as sine and cosine, and PM2.5 at the same hour yesterday. TabPFN sees 2,000 example hours, half from the most recent weeks and half sampled from the whole history, so it remembers what last winter looked like.

Adding **boundary layer height** helped the most. It's the height of the air layer that pollution mixes into. On calm winter nights that layer drops to a couple of hundred metres and PM2.5 has nowhere to go.

### Does it actually beat a normal model?

I wanted an honest answer, so I compared TabPFN against two baselines:

- **Gradient boosting** (scikit-learn's HistGradientBoostingRegressor) trained on the **full** history, not just 2,000 rows.
- **Same as yesterday**: predict that each hour will match the same hour yesterday.

A single test period turned out to be misleading. On the last three weeks alone, gradient boosting edged out TabPFN (6.76 vs 6.90 mean absolute error, in µg/m³). Depending on which random sample of history TabPFN saw, it could win or lose that comparison. So I built a rolling backtest instead: ten 3-week windows spread across the year. Each model is trained only on the hours before its window, so nothing peeks into the future. The short version: **through the winter smog season, TabPFN's forecast errors were 16% lower than gradient boosting's.**

![Forecast error through the seasons](UPLOAD data/backtest.png)

| Window starts | Hours of history | TabPFN | Gradient boosting | Same as yesterday |
|---|---|---|---|---|
| Jul 2025 | 2,160 | **5.51** | 5.80 | 6.30 |
| Aug 2025 | 3,240 | 3.19 | **3.11** | 4.32 |
| Oct 2025 | 4,320 | 12.14 | 11.98 | **9.76** |
| Nov 2025 | 5,400 | **10.27** | 11.58 | 10.64 |
| Jan 2026 | 6,480 | **7.90** | 11.30 | 10.06 |
| Feb 2026 | 7,560 | **8.69** | 9.19 | 9.04 |
| Apr 2026 | 8,640 | 7.76 | **7.61** | 8.72 |
| May 2026 | 9,720 | 8.77 | **7.49** | 8.45 |
| Jul 2026 | 10,800 | 3.56 | **3.31** | 4.33 |
| Aug 2026 | 11,880 | **3.47** | 3.65 | 4.40 |
| **Average** | | **7.13** | 7.50 | 7.60 |

Mean absolute error in µg/m³, lower is better. TabPFN's scores are averaged over three different samples of history.

What I take from it:

- **In smog season, TabPFN's error is 16% lower than gradient boosting's.** That's the average across the November to February windows, the weeks when picking the right hour to go outside matters most for your lungs.
- **TabPFN also has the lowest average error across the whole year**, about 5% better than gradient boosting, even though it only ever sees 2,000 rows.
- **The overall win count is a tie** (5 windows each). Gradient boosting's wins are small and come later in the year, once it has more than 8,500 hours to learn from.
- **Both models had a bad October.** In the first weeks after the monsoon, "same as yesterday" beat them both. The air changes in ways that last year's pattern doesn't capture well yet.

A practical note on running TabPFN on a CPU laptop: the default settings took about 20 minutes per evaluation. Setting `n_estimators=1` scored within noise of the default and runs about 20 times faster, so a full plan now takes about a minute.

## How I Used Gemma

Gemma 4 (`gemma4:e4b-it-qat`, the quantization-aware 4B-effective model) runs locally through Ollama. On my CPU it writes a plan in about 20 seconds.

The prompt gives Gemma a short list of facts (the window, the air quality band and PM2.5, the "feels like" temperature, a suggested activity, the worst stretch of the day) and tells it not to invent anything else. It writes 2 or 3 sentences, warm and direct, and ends by telling you to put the phone away. I wanted the numbers to stay with the forecasting model and the voice to come from the language model, and keeping those jobs separate stops Gemma from making up an air quality reading.

One thing that tripped me up: Gemma 4 can think before it answers. With a 120-token budget it sometimes spent every token thinking and returned an empty reply. Passing `"think": false` to Ollama fixed it. For a two-sentence nudge, thinking adds latency without adding much.

If Ollama isn't running, Bahar falls back to a template sentence. If TabPFN isn't available, it falls back to gradient boosting. Either way it still gives you a plan.

## Honest caveats

- The PM2.5 history comes from the CAMS atmospheric model via Open-Meteo, not ground sensors. It's free and has full hourly history, which makes it great for patterns. For ground truth, compare a few days against CPCB station readings for your area.
- The size of the winter win depends on where the test windows fall. The single January window in the table shows 30%, but in an earlier run with windows a few days apart it was 10%. That's why I quote the 16% winter average rather than any one window.
- With one winter in the data, I can't fully separate "TabPFN is better in winter" from "TabPFN is better when there's less history". Next winter will tell.
- Recent TabPFN versions download their weights only after you accept a license with a free Prior Labs account.

Every run appends to `data/plans_log.jsonl`, so I can check over time whether the hour Bahar picked actually felt good outside.

Now close this tab and go outside.
