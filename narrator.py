"""Gemma (running locally in Ollama) turns the numbers into a short, human plan.
Optional offline voice via pyttsx3 (uses your OS's built-in speech engine)."""
import requests

import config as C

PROMPT = """You are Bahar, a friendly outdoor coach for {city}. Write the plan for {when}.
Facts (do not invent others):
- Best window: {start} to {end}
- Air quality in that window: {air} (PM2.5 about {pm} µg/m³)
- Feels like: {feels} °C
- Suggested activity: {activity}
- Worst stretch of the day: {worst}

Rules: 2 to 3 short sentences, under 60 words. Start with the window. Be warm and direct,
like a friend nudging you out the door. End by telling them to put the phone away.
No lists, no emojis, no markdown."""


def fallback(f):
    return (f"Your best window {f['when']} is {f['start']} to {f['end']}: air is {f['air'].lower()} "
            f"and it feels like {f['feels']}°C. Go for {f['activity']}. "
            f"Avoid {f['worst']}. Now put the phone down and head out.")


def write_plan(facts: dict) -> tuple[str, str]:
    """Returns (text, source)."""
    try:
        r = requests.post(f"{C.OLLAMA_URL}/api/generate", timeout=120, json={
            "model": C.GEMMA_MODEL,
            "prompt": PROMPT.format(city=C.CITY, **facts),
            "stream": False,
            "think": False,  # Gemma 4 otherwise spends the whole token budget thinking
            "options": {"temperature": 0.6, "num_predict": 120},
        })
        r.raise_for_status()
        text = r.json()["response"].strip()
        if text:
            return text, C.GEMMA_MODEL
        print("[bahar] Gemma returned an empty reply; using template text.")
    except Exception as e:
        print(f"[bahar] Gemma not reachable ({type(e).__name__}); using template text.")
    return fallback(facts), "template"


def speak(text: str, out_wav: str | None = None) -> bool:
    try:
        import pyttsx3
        eng = pyttsx3.init()
        eng.setProperty("rate", 175)
        if out_wav:
            eng.save_to_file(text, out_wav)
        else:
            eng.say(text)
        eng.runAndWait()
        return True
    except Exception as e:
        print(f"[bahar] Voice unavailable ({type(e).__name__}).")
        return False
