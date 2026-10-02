# MindMesh — Django Edition

A JARVIS-style personal AI assistant dashboard, rebuilt on **Django**: a
live conversation panel, an animated central "knowledge graph" visual that
swaps in Wikipedia imagery when you ask about a topic, real-time system
stats (CPU / RAM / Disk), a weather widget, and voice input/output — all
driven by a backend **agent** that classifies your intent and calls the
right tool.

This is a from-scratch Django rebuild of the "MindMesh" UI shown in the
reference recording (React + Python prototype), not a copy of its source.

## What the agent does

`assistant/agent/core_agent.py` is the agent. For every message it:

1. **Classifies intent** (`agent/intents.py`) — regex/keyword rules for
   weather, system stats, the time, greetings, "who are you", and
   "tell me about X" knowledge lookups. Anything else is free chat.
2. **Calls a tool** (`agent/tools.py`):
   - `get_system_stats()` — real host metrics via `psutil`.
   - `get_weather(city)` — live data via OpenWeatherMap if you set
     `OPENWEATHER_API_KEY`, otherwise a believable simulated reading so
     the widget is never empty.
   - `wiki_lookup(topic)` — pulls a summary + thumbnail from Wikipedia's
     public REST API. This is what drives the centre panel image swap
     (the Django equivalent of the reference UI's anatomy-model viewer).
   - `get_current_datetime()`.
3. **Falls back to chat** — if nothing matches, and you've set
   `LLM_API_KEY` (any OpenAI-compatible endpoint — OpenAI, Azure OpenAI,
   or a local server like Ollama/LM Studio), the agent hands off to
   `agent/llm_client.py`. Without a key it uses a small offline responder
   so the whole app works with zero paid services.

Every turn (yours and the agent's) is persisted to the database
(`ConversationSession` / `Message` models) against your browser session,
so history survives a page refresh. The session also tracks
**`last_topic`** — the most recent "tell me about X" subject — so
follow-ups like *"what about the brain?"* or *"tell me more"* resolve
against it instead of being treated as a brand-new, context-free
question.

## Project layout

```
mindmesh_django/
├── manage.py
├── requirements.txt
├── .env.example
├── mindmesh_project/        # Django project (settings, urls, wsgi/asgi)
└── assistant/                # the one app
    ├── models.py             # ConversationSession, Message
    ├── views.py               # dashboard + JSON API endpoints
    ├── urls.py
    ├── admin.py
    ├── agent/
    │   ├── core_agent.py      # the agent itself
    │   ├── intents.py         # rule-based intent classifier
    │   ├── tools.py            # weather / system-stats / wiki tools
    │   └── llm_client.py       # optional LLM fallback
    ├── templates/assistant/dashboard.html
    └── static/assistant/
        ├── css/style.css       # dark/cyan sci-fi dashboard theme
        └── js/
            ├── app.js           # wiring: chat, stats/weather polling, mic
            ├── knowledge_graph.js  # idle-state canvas radar animation
            └── speech.js          # Web Speech API (STT + TTS) wrapper
```

## API endpoints

| Endpoint            | Method | Purpose                                   |
|----------------------|--------|--------------------------------------------|
| `/`                  | GET    | Dashboard page                            |
| `/api/chat/`         | POST   | `{"message": "..."}` → agent reply + visual |
| `/api/stats/`        | GET    | Live CPU/RAM/disk stats                   |
| `/api/weather/`      | GET    | Weather for `?city=` (defaults to config) |
| `/api/clock/`        | GET    | Server date/time                          |
| `/api/history/`      | GET    | Full conversation history for the session |

## Setup

```bash
cd mindmesh_django
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows

pip install -r requirements.txt

cp .env.example .env            # then edit as you like (all optional)

python manage.py migrate
python manage.py createsuperuser  # optional, for /admin/
python manage.py runserver
```

Open **http://127.0.0.1:8000/** — click the mic (or the small mic next to
the text box) and talk, or just type. Try:

- "What's the weather?"
- "How's the system doing?" / "Check CPU usage"
- "Tell me about the heart" / "What is quantum computing"
- "Who are you?"
- Anything else → free chat (offline canned response unless you set
  `LLM_API_KEY`)

## Notes on parity with the reference recording

- **Wake word**: true always-on wake-word detection needs a native
  library (e.g. Porcupine) and a downloaded model — out of scope for a
  browser-based demo. The mic button gives you the same push-to-talk
  experience; `WAKE_WORD` in settings is wired through to the UI copy so
  you can rebrand it, and the state label already reads "LISTENING FOR
  WAKE WORD" like the original.
- **3D anatomy model**: for topics with a curated match (heart, brain,
  skull, skeleton, stomach, lungs, digestive system, DNA, Earth, solar
  system — see `assistant/agent/models_3d.py`), the centre panel embeds
  a **real, interactive Sketchfab 3D model** (drag to rotate, scroll to
  zoom), just like the anatomy viewer in the reference recording. Ask
  "tell me about the heart", "show me the stomach", or "what is DNA" to
  see it — the agent understands "tell me about X", "what is X", "show
  me X", and "picture/image of X" phrasings. Any topic *not* in that
  table falls back to a Wikipedia image instead, so the panel is never
  empty. Add more topics by dropping a new entry into
  `MODEL_3D_LIBRARY` — pick a "Download Free 3D model" page on
  sketchfab.com and copy the id out of its URL.
- **System stats / weather**: real, live data (`psutil`, OpenWeatherMap),
  not mocked — same as the original.

## Extending the agent

Add a new tool by:

1. Writing a function in `agent/tools.py`.
2. Adding a pattern list + branch in `agent/intents.py::classify`.
3. Adding a `_handle_<intent>` method to `MindMeshAgent` in
   `agent/core_agent.py` that calls your tool and returns an
   `AgentResponse(text, intent, visual=...)`.

No other wiring needed — `views.chat_api` and the frontend already handle
any intent generically.
