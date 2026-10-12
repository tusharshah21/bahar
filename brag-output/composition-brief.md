# Hyperframes Composition Brief: Bahar

## Objective
Create a short demo video of Bahar to attach to the DEV challenge post.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape, 1920x1080, 30fps
- Duration: 21.5 seconds

## Source Material
- Project root: `C:\open\bahar`
- Primary files read: `app.py` (layout and CSS), `README.md`, `narrator.py`, `planner.py`, `data/metrics.json`, `data/plans_log.jsonl`, `POST.md`
- Product name: Bahar
- Tagline / strongest claim: "The best hour today to go outside"; TabPFN's forecast errors are 16% lower than gradient boosting's in smog season
- Key UI to recreate: the Streamlit app screen from `app.py` (kicker, big window time, two teal pills, plan paragraph) and the hourly forecast chart from its "Why this window?" expander
- Copy that must appear verbatim:
  - BAHAR · HYDERABAD · BEST WINDOW TOMORROW
  - 5:00 AM to 8:00 AM
  - Air: Satisfactory / Feels 28.4°C
  - Wake up for your outdoor session between 5:00 AM and 8:00 AM when the air quality is Satisfactory. Go for a run, cycle, or play cricket before the worst stretch around 11:00 AM. Put your phone away and enjoy the Hyderabad morning.
  - Now put the phone down and head out.

## Creative Direction
- Tone preset: default
- Creative direction: calm, warm Hyderabad-morning product demo; clean and honest, a little playful
- Interpretation: 3 to 5 second scenes, real numbers, soft slides and crossfades, no hype words
- Angle: three apps to check becomes one time range and one friendly nudge; then one honest proof point
- Hook: three app tiles, then "So... when do you go outside?"
- Outro / punchline: "Bahar" + "Now put the phone down and head out."
- Avoid: generic SaaS language, abstract filler visuals, redesigning the app's look, em dashes in any on-screen text

## Visual Identity
- Background: #FFFFFF; title cards #FBFAF7
- Text: #31333F
- Accent: #2A9D8F (pill fill rgba(42,157,143,.15)); secondary series #7B4FBF
- Display and body font: Source Sans 3 (variable), shipped locally from Streamlit's static assets
- Visual references: app.py `.big`, `.kicker`, `.pill`, `.plan` styles; `data/backtest.png`; `data/cover.png`

## Storyboard
Use `brag-output/brag-plan.md` as the creative contract.

1. Too many numbers (0.0 to 3.0s): three app tiles, then "So... when do you go outside?"
2. The answer (3.0 to 7.5s): recreated app screen, plan text, "written by Gemma 4, locally"
3. Why this window (7.5 to 11.5s): real hourly forecast line with the 5 to 8 AM band; "TabPFN forecasts every hour."
4. The proof (11.5 to 15.8s): "16%" count-up, sparkline from the real backtest
5. Built with (15.8 to 18.5s): three chips
6. Outro (18.5 to 21.5s): Bahar wordmark and closing line

Backtest data for the sparkline (start, TabPFN, gradient boosting): 2025-07-08 5.51 5.80; 2025-08-22 3.19 3.11; 2025-10-06 12.14 11.98; 2025-11-20 10.27 11.58; 2026-01-04 7.90 11.30; 2026-02-18 8.69 9.19; 2026-04-04 7.76 7.61; 2026-05-19 8.77 7.49; 2026-07-03 3.56 3.31; 2026-08-17 3.47 3.65. Shade Nov to Feb.

## Audio
- Audio role: warm bed with sparse motion-matched accents
- Audio arc: bed fades in, light clicks on the hook tiles and pills, soft impact on the answer, bell on the wordmark, bed fades under the closing line
- Music: `assets/music/happy-beats-business-moves-vol-10-by-ende-dot-app.mp3`
- Music treatment: low bed around 0.35, 0.5s fade in, 1.5s fade out at the end
- Music cue guidance: preset `happy-beats-business-moves-vol-10-by-ende-dot-app.music-cues.json`; strong cues 15.82s and 18.55s; beat grid 0.27, 0.82, 1.37 for the hook tiles
- Audio-reactive treatment: subtle, optional; skip if extraction is unavailable
- SFX selection guidance: low high-frequency-risk picks from `~/.claude/skills/brag/assets/sfx/sfx-analysis.md` (impactSoft_medium for the reveal, interface/click_003 for tiles, pills and chips, impactBell_heavy_000 for the logo)
- Exact SFX choice: chosen after the animation exists
- Audio files: copied into `brag-output/composition/assets/`

## Hyperframes Instructions
Follow hyperframes-core: one paused GSAP timeline at `window.__timelines["main"]`, `data-*` timing, local `@font-face`, every `<audio>` has an id, no CSS transform plus GSAP transform conflicts. Show real UI and copy, keep text readable, stay within 15 to 25 seconds, and run `npx hyperframes check` before render.
