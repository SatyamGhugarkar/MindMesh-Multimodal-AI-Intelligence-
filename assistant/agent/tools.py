"""
Tools available to the MindMesh agent.

Each tool is a plain Python function that takes simple arguments and
returns a JSON-serialisable dict. The agent (core_agent.py) decides which
tool to call based on the detected intent, then formats the result into a
spoken/typed reply plus an optional "visual" payload that the frontend
renders in the centre knowledge panel.
"""

import datetime
import random

import psutil
import requests
from django.conf import settings
from django.utils import timezone


# --------------------------------------------------------------------------
# System stats — mirrors the CPU / RAM / Disk widget in the reference UI
# --------------------------------------------------------------------------

def get_system_stats():
    """Live host system stats using psutil (real data, not simulated)."""
    cpu_percent = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": cpu_percent,
        "ram_percent": mem.percent,
        "ram_used_gb": round(mem.used / (1024 ** 3), 2),
        "ram_total_gb": round(mem.total / (1024 ** 3), 2),
        "disk_used_gb": round(disk.used / (1024 ** 3), 1),
        "disk_total_gb": round(disk.total / (1024 ** 3), 1),
        "disk_percent": disk.percent,
        "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat(),
    }


# --------------------------------------------------------------------------
# Weather — real data via OpenWeatherMap if a key is configured, otherwise
# a believable simulated reading so the dashboard works out of the box.
# --------------------------------------------------------------------------

def get_weather(city=None):
    city = city or settings.DEFAULT_CITY
    api_key = settings.OPENWEATHER_API_KEY

    if api_key:
        try:
            resp = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": api_key, "units": "metric"},
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "city": data.get("name", city),
                "country": data.get("sys", {}).get("country", ""),
                "temp_c": round(data["main"]["temp"], 1),
                "feels_like_c": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "wind_ms": data["wind"]["speed"],
                "description": data["weather"][0]["description"],
                "simulated": False,
            }
        except (requests.RequestException, KeyError, IndexError):
            pass  # fall through to simulated data below

    return _simulated_weather(city)


def _simulated_weather(city):
    """Deterministic-ish placeholder weather so the UI is never empty."""
    rng = random.Random(datetime.date.today().toordinal() + hash(city) % 1000)
    conditions = ["clear sky", "few clouds", "scattered clouds", "overcast clouds", "light rain"]
    temp = round(rng.uniform(18, 34), 1)
    return {
        "city": city.split(",")[0],
        "country": city.split(",")[1] if "," in city else "",
        "temp_c": temp,
        "feels_like_c": round(temp + rng.uniform(-1, 2), 1),
        "humidity": rng.randint(40, 95),
        "wind_ms": round(rng.uniform(1, 7), 1),
        "description": rng.choice(conditions),
        "simulated": True,
    }


# --------------------------------------------------------------------------
# Knowledge lookups — drives the centre "knowledge graph" visual panel,
# analogous to the anatomy-model viewer in the reference UI. Uses the
# public Wikipedia REST summary endpoint (no key required).
# --------------------------------------------------------------------------

def wiki_lookup(topic):
    topic = topic.strip().strip("?.!").title()

    result = _wiki_summary(topic)
    if result:
        return result

    # Exact-title lookup failed (404) or landed on a disambiguation page —
    # fall back to Wikipedia's search suggestions and retry with the best
    # real match instead of giving up outright.
    suggestion = _wiki_search_suggestion(topic)
    if suggestion and suggestion.lower() != topic.lower():
        return _wiki_summary(suggestion)

    return None


def _wiki_summary(title):
    try:
        resp = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}",
            timeout=6,
            headers={"User-Agent": "MindMesh-Assistant/1.0"},
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()
        if data.get("type") == "disambiguation":
            return None
        return {
            "title": data.get("title", title),
            "summary": data.get("extract", "No summary available."),
            "image": (data.get("thumbnail") or {}).get("source"),
            "url": (data.get("content_urls") or {}).get("desktop", {}).get("page"),
        }
    except requests.RequestException:
        return None


def _wiki_search_suggestion(topic):
    """Best-guess real article title for a topic that didn't resolve directly."""
    try:
        resp = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "opensearch",
                "search": topic,
                "limit": 1,
                "namespace": 0,
                "format": "json",
            },
            timeout=6,
            headers={"User-Agent": "MindMesh-Assistant/1.0"},
        )
        resp.raise_for_status()
        data = resp.json()
        titles = data[1] if len(data) > 1 else []
        return titles[0] if titles else None
    except (requests.RequestException, IndexError, ValueError):
        return None


# --------------------------------------------------------------------------
# Time / date
# --------------------------------------------------------------------------

def get_current_datetime():
    now = timezone.localtime()
    return {
        "iso": now.isoformat(),
        "date_label": now.strftime("%B %d, %Y"),
        "time_label": now.strftime("%I:%M:%S %p"),
    }
