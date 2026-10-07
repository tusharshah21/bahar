"""Central settings for Bahar. Change the city here."""
import os

CITY = "Hyderabad"
LAT = 17.385
LON = 78.4867
TIMEZONE = "Asia/Kolkata"

# How much history to learn from (days). Open-Meteo air quality history starts mid-2022.
HISTORY_DAYS = 540

# Weather features shared by the historical archive and the forecast API.
WEATHER_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "precipitation",
    "cloud_cover",
    "boundary_layer_height",  # low mixing height traps PM2.5 near the ground
]

# TabPFN is an in-context learner: "training" means handing it example rows.
# On a CPU laptop, a few thousand rows keeps prediction under a minute or two.
TABPFN_CONTEXT_ROWS = int(os.getenv("BAHAR_CONTEXT_ROWS", "2000"))

# Local Gemma via Ollama. Override with BAHAR_MODEL if you pull a different tag.
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
GEMMA_MODEL = os.getenv("BAHAR_MODEL", "gemma4:e4b-it-qat")

# Only plan windows in daylight-ish hours.
EARLIEST_HOUR = 5
LATEST_HOUR = 19

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
HISTORY_CSV = os.path.join(DATA_DIR, "history.csv")
