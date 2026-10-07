"""One-screen Bahar. Run:  streamlit run app.py"""
import os
import tempfile

import pandas as pd
import streamlit as st

import config as C
import narrator
from bahar import log_plan, plan_today

st.set_page_config(page_title="Bahar", page_icon="🌿", layout="centered")
st.markdown("""
<style>
.block-container {max-width: 640px; padding-top: 2.5rem;}
.big {font-size: 2.6rem; font-weight: 700; line-height: 1.1; margin: .2rem 0 .6rem;}
.kicker {letter-spacing: .12em; text-transform: uppercase; font-size: .8rem; opacity: .65;}
.plan {font-size: 1.15rem; line-height: 1.55;}
.pill {display:inline-block; padding:.2rem .7rem; border-radius:999px; margin-right:.4rem;
       background: rgba(42,157,143,.15); font-size:.9rem;}
</style>""", unsafe_allow_html=True)

if not os.path.exists(C.HISTORY_CSV):
    st.error("No history yet. Run `python fetch_data.py` first.")
    st.stop()


@st.cache_data(ttl=3600, show_spinner="Reading the sky...")
def get_plan():
    r = plan_today()
    log_plan(r)
    return r


r = get_plan()
f, w = r["facts"], r["window"]

st.markdown(f"<div class='kicker'>Bahar · {C.CITY} · best window {f['when']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='big'>{f['start']} to {f['end']}</div>" if w else
            "<div class='big'>Stay in today</div>", unsafe_allow_html=True)
if w:
    st.markdown(f"<span class='pill'>Air: {w.air_label}</span>"
                f"<span class='pill'>Feels {w.feels_like}°C</span>", unsafe_allow_html=True)
st.markdown(f"<p class='plan'>{r['text']}</p>", unsafe_allow_html=True)

if st.button("🔊 Read it to me"):
    wav = os.path.join(tempfile.gettempdir(), "bahar_plan.wav")
    if narrator.speak(r["text"], out_wav=wav) and os.path.exists(wav):
        st.audio(wav, autoplay=True)

with st.expander("Why this window? (hourly details)"):
    h = r["hourly"].copy()
    h["hour"] = h["time"].dt.strftime("%H:%M")
    chart = h.set_index("hour")[["pm25_pred", "pm2_5_cams"]].rename(
        columns={"pm25_pred": "Bahar forecast (PM2.5)", "pm2_5_cams": "CAMS model (PM2.5)"})
    st.line_chart(chart)
    st.dataframe(h[["hour", "pm25_pred", "apparent_temperature", "air_label", "score"]]
                 .round(1), hide_index=True, width="stretch")
    st.caption(f"Forecast: {r['model']} · Words: {r['writer']} · Runs on this laptop")
