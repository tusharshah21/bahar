---
title: Bahar: the best hour today to go outside, forecast by TabPFN and told by Gemma
published: false
tags: devchallenge, opensource, ai, python
---

*This is a submission for the DEV Hacktoberfest Open-Source AI Challenge, Week 1: Touch Grass.*

Quick question before you scroll: **when did you last step outside on purpose?** Not to get to the car. Not to grab a delivery. Just to be outside.

If you had to think about it, this one's for you.

## What I Built

Here's a morning you might recognise. You decide to go for a walk. You open the air quality app: PM2.5 is "Moderate", whatever that means for the next hour. You open the weather app: it'll feel like 38°C by noon. You open a third app to check for rain. Ten minutes later you're still on your phone, still inside.

That loop is worse in a city like Hyderabad, where air quality changes a lot over a single day, summer afternoons can feel hotter than 40°C, and the monsoon brings sudden rain. So I built **Bahar** ("outside" in Hindi and Urdu). It answers exactly one question:

> **When is the best hour today to get out of the house?**

No charts to read. One time range, two sentences, and then it tells you to put your phone down.

Under the hood, four steps:

1. 🌦️ **Look back.** Pull about 18 months of hourly weather and PM2.5 history for the city from Open-Meteo (free, no key).
2. 🔮 **Look ahead.** **TabPFN** forecasts PM2.5 for every hour today from the weather forecast.
3. ⚖️ **Weigh it up.** Score every hour: air quality by India's National AQI bands (55%), heat by the "feels like" temperature (30%), rain (15%). Pick the best 1 to 3 hour window between 5 AM and 7 PM.
4. 💬 **Say it like a friend.** **Gemma 4**, running locally in Ollama, writes the plan in two or three sentences, and the app can read it aloud offline.

All of it runs on my laptop: Windows, an i7, 16 GB of RAM, no GPU. No paid API. The only network calls are the weather requests and TabPFN's license check.

## Demo

[Attach the demo video here]

Let's play a quick game first. Tomorrow's PM2.5 forecast for Hyderabad looked like this: higher overnight, a small bump around 6 AM, cleanest in the early afternoon, then climbing again after 5 PM.

**Which window do you think Bahar picked?**

{% details 👉 Make your guess, then click to see Bahar's answer %}

**5:00 AM to 8:00 AM.** Not the cleanest air of the day, but the coolest hours: it feels like 28°C at 5 AM and already over 32°C by 9. Bahar weighs heat too. Here's the plan, word for word as Gemma wrote it:

> Wake up for your outdoor session between 5:00 AM and 8:00 AM when the air quality is Satisfactory. Go for a run, cycle, or play cricket before the worst stretch around 11:00 AM. Put your phone away and enjoy the Hyderabad morning.

{% enddetails %}

![The Bahar app](UPLOAD data/app_screenshot.png)

## Code

[Link to the GitHub repo]

```bash
python fetch_data.py        # once, about a minute
python evaluate.py          # accuracy charts
python bahar.py             # today's plan, printed and spoken
streamlit run app.py        # the one-screen app
```

🏙️ **Try it for your city.** Open `config.py`, change `CITY`, `LAT`, `LON` and `TIMEZONE`, and run the four commands above. I'd love to see what Bahar says about yours.

## How I Used TabPFN

TabPFN is a foundation model for tables, and it works differently from what I was used to. There's no training loop. You hand it example rows at prediction time and it learns from them in context, a bit like showing a friend a few hundred past days and asking "so what about tomorrow?"

For Bahar, each row is one hour: temperature, humidity, wind (split into east and north components), rain, cloud cover, boundary layer height, time of day and season encoded as sine and cosine, and PM2.5 at the same hour yesterday. TabPFN sees 2,000 example hours, half from the most recent weeks and half sampled from the whole history, so it still remembers what last winter looked like.

The feature that helped most is one most people have never heard of: **boundary layer height**. It's the height of the air layer that pollution mixes into. On calm winter nights it drops to a couple of hundred metres, and PM2.5 has nowhere to go. That's the smog you can taste.

### Plot twist: TabPFN lost. At first.

I'll be honest about how this went, because it surprised me.

My first test was the obvious one: train on everything up to three weeks ago, forecast the last three weeks. TabPFN lost to plain gradient boosting (6.90 vs 6.76 mean absolute error, in µg/m³). And it took **20 minutes** on my laptop to get there.

The 20 minutes turned out to be an easy fix. Setting `n_estimators=1` gave almost the same accuracy and ran about 20 times faster. A full plan now takes about a minute.

The loss was more interesting. When I re-ran the test with different random samples of history, TabPFN sometimes won and sometimes lost. Three weeks was simply too small a window to judge anything. So I asked a better question: **how does each model do across a whole year of seasons?**

I built a rolling backtest: ten 3-week windows spread from July 2025 to August 2026, each model trained only on the hours before its window, so nothing peeks into the future. Two opponents:

- 🌲 **Gradient boosting** (scikit-learn's HistGradientBoostingRegressor), trained on the **full** history, not just 2,000 rows.
- 🔁 **Same as yesterday**: predict that each hour will match the same hour yesterday.

![Forecast error through the seasons](UPLOAD data/backtest.png)

Look at the shaded winter months on the chart. That's where it gets good:

> **Through the November to February smog season, TabPFN's forecast errors were 16% lower than gradient boosting's.**

That's the stretch when choosing the right hour matters most for your lungs. Across the whole year TabPFN also had the lowest average error, about 5% better than gradient boosting, while only ever looking at 2,000 rows.

{% details 📊 See every window (for the numbers people) %}

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

{% enddetails %}

It isn't a clean sweep, and I don't want to pretend it is:

- **Count the wins and it's a tie**, 5 windows each. Gradient boosting's wins are small and come later in the year, once it has more than 8,500 hours to learn from.
- **October humbled everyone.** In the first weeks after the monsoon, "same as yesterday" beat both models. The air shifts in ways last year's pattern doesn't capture yet.

## How I Used Gemma

If TabPFN is Bahar's brain, Gemma is its voice.

Gemma 4 (`gemma4:e4b-it-qat`, the quantization-aware 4B-effective model) runs locally through Ollama and writes a plan in about 20 seconds on my CPU. I gave it a clear division of labour: the numbers come from the forecast, the words come from Gemma. The prompt hands it a short list of facts (the window, the air quality band and PM2.5, the "feels like" temperature, a suggested activity, the worst stretch of the day) and asks for two or three warm, direct sentences that end with "put the phone away".

Then Gemma taught me two things.

**Lesson one: Gemma can overthink.** Gemma 4 can reason before it answers. With a 120-token budget, it sometimes spent every single token thinking and handed back an empty reply. Passing `"think": false` to Ollama fixed it. A two-sentence nudge doesn't need deep thought.

**Lesson two: Gemma is too nice.** I'd written "do not invent other facts" in the prompt. Gemma still kept upgrading the air. Given "Satisfactory", it wrote "good", "perfect" or "best" in **5 of 6** test runs. That sounds harmless until you think about someone with asthma, who would plan their day very differently around "Satisfactory" and "perfect".

So I tightened the prompt: use the air quality label word for word, never upgrade it, and mention no times or numbers beyond the facts given. Same facts, 8 new runs: **0 of 8** broke the rules. The plans are a little less bubbly now, and a lot more trustworthy.

And if anything's missing, Bahar still shows up. No Ollama? A template sentence. No TabPFN? Gradient boosting. You always get a plan.

## Honest caveats

- The PM2.5 history comes from the CAMS atmospheric model via Open-Meteo, not ground sensors. It's free and has full hourly history, which makes it great for patterns. For ground truth, compare a few days against CPCB station readings for your area.
- The size of the winter win depends on where the test windows fall. The single January window in the table shows 30%, but in an earlier run with windows a few days apart it was 10%. That's why I quote the 16% winter average rather than any one window.
- With one winter in the data, I can't fully separate "TabPFN is better in winter" from "TabPFN is better when there's less history". Next winter will tell.
- Recent TabPFN versions download their weights only after you accept a license with a free Prior Labs account.

Every run appends to `data/plans_log.jsonl`, so over time I can check whether the hour Bahar picked actually felt good outside.

## Your turn 👇

I'd love to hear from you in the comments:

- **What's the worst hour for air in your city?** Is it the morning rush, or the evening climb you can see in Hyderabad's forecast above?
- **If you try Bahar for your city, what window did it pick?**

And now, the most important instruction in this post: close this tab and go outside. 🌿
