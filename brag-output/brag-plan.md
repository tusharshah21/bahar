# Brag Plan: Bahar

## What is this app?
Bahar forecasts hourly PM2.5 for Hyderabad with TabPFN, scores every hour for air, heat and rain, picks the best window to go outside, and has Gemma 4 (running locally) tell you the plan in two sentences.

## The angle
Checking whether it's safe to go outside means juggling three apps: air quality, weather and rain. Bahar collapses all of it into one time range and one friendly nudge, then tells you to put the phone down. The video is a demo for a DEV challenge post, so it shows the working app first and then the one hard proof point: in smog season TabPFN's forecast errors are 16% lower than gradient boosting's.

## Hook (first 2-3 seconds)
Three app tiles pop in like a cluttered home screen: "AQI app", "Weather app", "Rain radar". Then the line: "So... when do you go outside?"

## Key moments (the middle)
- The app answer slams in: "5:00 AM to 8:00 AM", the two pills pop ("Air: Satisfactory", "Feels 28.4°C"), and Gemma's real plan types out.
- The real hourly forecast line draws across the day, with the 5 to 8 AM window shading in. Label: "TabPFN forecasts every hour".
- The proof: "16%" counts up. "Lower forecast error in smog season vs gradient boosting."

## Outro / punchline
Stack chips "TabPFN · Gemma 4 · runs on a CPU laptop", then "Bahar" with the app's own sign-off: "Now put the phone down and head out."

## User flow worth showing
Open the app → it reads the forecast and scores every hour → it shows the best window with Gemma's plan. The centerpiece (scenes 2 and 3) recreates the real Streamlit screen from `app.py`: kicker line, big window time, teal pills, plan paragraph, and the hourly chart from the "Why this window?" expander.

## Tone
- Preset: default
- Creative direction: calm, warm Hyderabad-morning product demo; clean and honest, a little playful
- Interpretation: comfortable 3 to 5 second scenes, real numbers on screen, soft slides and crossfades, no hype words. The playful bit is the "put the phone down" ending.

## Format: landscape, 1920x1080
## Duration: 21.5s

## Visual identity (from the project)
- Background: #FFFFFF (Streamlit light theme) with a warm off-white #FBFAF7 for title cards (matches the DEV cover image)
- Accent: #2A9D8F (teal: pills use rgba(42,157,143,.15), TabPFN line in charts)
- Secondary series: #7B4FBF (gradient boosting in the backtest chart)
- Text: #31333F (Streamlit body text); kicker at 65% opacity
- Display font: Source Sans 3 (Streamlit's bundled font), weight 700 for the big window time
- Body font: Source Sans 3
- Strongest visual element: the big "5:00 AM to 8:00 AM" with the two teal pills, exactly as `app.py` styles it (.big 2.6rem bold, .kicker uppercase letter-spaced, .pill rounded teal tint)

## Share copy (draft)
Bahar picks the best hour today to go outside in Hyderabad: TabPFN forecasts the air, Gemma 4 writes the plan, all on a CPU laptop.

## Audio direction
- Role: warm bed with sparse, motion-matched UI accents
- Music: happy-beats-business-moves-vol-10 (109.96 BPM)
- Music treatment: start at 0, low bed (around 0.35), fade in over 0.5s, fade out over the last 1.5s
- Music cue guidance: preset read (`assets/music/cues/happy-beats-business-moves-vol-10-by-ende-dot-app.music-cues.md`). Strong cues to target: 15.82s (proof scene to chips handoff), 18.55s (Bahar wordmark lands). Beat grid around the hook: 0.27, 0.82, 1.37 for the three readings.
- Audio-reactive treatment: subtle; the teal glow behind the wordmark and the shaded window may breathe with RMS. No waveforms.
- SFX posture: sparse; soft impact on the window reveal, light clicks on pills and chips, a gentle bell on the final wordmark.
- Audio-coupled moments: three hook readings arrive one by one; plan text types with very quiet key ticks (or none if busy); 16% count-up; chips arrive one by one.
- Restraint rule: no SFX on every word, nothing sharp or bright repeated, music never louder than the reveals.

## Storyboard

### Scene 1: Too many numbers (0.0 to 3.0s)
Three small app tiles pop in on white, slightly scattered: "AQI app", "Weather app", "Rain radar". At about 1.5s they dim and slide down and the line "So... when do you go outside?" lands centered (hold at least 1.3s).
Sequential/interaction: yes, 3 cards arrive one by one on beats 0.27, 0.82, 1.37
Audio intent: light, curious
Audio-coupled idea: soft click per card
Music: warm upbeat bed starts
Transition mood: clean slide up → Scene 2

### Scene 2: The answer (3.0 to 7.5s)
Recreated Bahar screen on white. Kicker "BAHAR · HYDERABAD · BEST WINDOW TOMORROW" fades in, "5:00 AM to 8:00 AM" slams in, pills "Air: Satisfactory" and "Feels 28.4°C" pop, then Gemma's plan types out (verbatim): "Wake up for your outdoor session between 5:00 AM and 8:00 AM when the air quality is Satisfactory. Go for a run, cycle, or play cricket before the worst stretch around 11:00 AM. Put your phone away and enjoy the Hyderabad morning." A small caption "written by Gemma 4, locally" appears under it.
Sequential/interaction: yes, pills arrive one by one; plan types out quickly then holds about 1.5s
Audio intent: payoff, the "aha"
Audio-coupled idea: soft impact on the big time; click per pill
Transition mood: soft slide → Scene 3

### Scene 3: Why this window (7.5 to 11.5s)
The hourly chart from the app: the "Bahar forecast (PM2.5)" line draws left to right over 00:00 to 23:00 using the real run's values (48.9, 44.7, 43.5, 42.0, 42.1, 45.5, 46.0, 39.3, 33.3, 32.2, 31.5, 31.0, 29.2, 29.5, 29.3, 29.8, 29.2, 31.3, 36.4, 39.5, 43.0, 44.5, 45.0, 44.5). The 05:00 to 08:00 band shades teal. Headline: "TabPFN forecasts every hour." Sub: "Air 55% · heat 30% · rain 15%."
Sequential/interaction: line draw, then band shade
Audio intent: steady, informative
Audio-coupled idea: none beyond the bed
Transition mood: clean crossfade → Scene 4

### Scene 4: The proof (11.5 to 15.8s)
Big "16%" counts up from 0. Line under it: "lower forecast error than gradient boosting in smog season". Small footnote: "10 seasonal backtest windows, Hyderabad, 2025 to 2026". A small two-line sparkline (TabPFN teal vs gradient boosting purple) with Nov to Feb shaded, using the real backtest values.
Sequential/interaction: count-up, then sparkline draws
Audio intent: confident
Audio-coupled idea: subtle tick on count-up finish
Transition mood: clean slide → Scene 5 (lands on strong cue 15.82s)

### Scene 5: Built with (15.8 to 18.5s)
Three chips arrive one by one: "TabPFN forecasts the air", "Gemma 4 writes the plan", "Runs on a CPU laptop. No paid API."
Sequential/interaction: yes, 3 chips on every other beat (about 0.9s apart), then hold together
Audio intent: tidy, building
Audio-coupled idea: click per chip
Transition mood: soft → Scene 6

### Scene 6: Outro (18.5 to 21.5s)
"Bahar" wordmark lands on the 18.55s strong cue on warm off-white with a soft teal glow, tagline "The best hour today to go outside", then "Now put the phone down and head out." Hold to end.
Sequential/interaction: none
Audio intent: warm landing
Audio-coupled idea: gentle bell on the wordmark
Transition mood: end

**Music mood for this video:** upbeat, warm
**Audio summary:** a light upbeat bed with a few soft clicks and one bell, fading out under the closing line.
