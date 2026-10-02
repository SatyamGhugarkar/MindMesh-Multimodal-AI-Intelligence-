[Uploading README (1).md…]()
# 🧠 MindMesh — AI Conversational Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-092E20.svg)](https://www.djangoproject.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Web%20Speech%20API-F7DF1E.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
[![Wikipedia](https://img.shields.io/badge/Wikipedia-REST%20API-636466.svg)](https://www.wikipedia.org/)
[![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-API-orange.svg)](https://openweathermap.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#-license)

**MindMesh** is a Django-based, JARVIS-style conversational AI dashboard that combines **natural-language interaction, voice input/output, system monitoring, weather information, knowledge lookup, interactive 3D visualizations, and optional LLM-powered conversation** in a single web application.

The system uses a lightweight rule-based intent classifier to determine what the user is asking and then routes the request to the appropriate backend tool.

It supports both **text and voice interaction**, while maintaining conversation history using Django models and browser sessions.

> **Note:** MindMesh is an educational and portfolio project. Its responses and external API results should not be treated as authoritative information for high-impact decisions.

---

# 📸 Application Preview

MindMesh provides a futuristic dashboard interface designed around a conversational AI experience.

Suggested repository screenshots:

```text
screenshots/
├── dashboard.png
├── chat.png
├── weather.png
├── system-stats.png
└── 3d-model.png
```

Add screenshots to your repository and reference them like:

```md
![MindMesh Dashboard](screenshots/dashboard.png)

![MindMesh Chat](screenshots/chat.png)

![MindMesh 3D Visualization](screenshots/3d-model.png)
```

---

# 🎯 Project Overview

Traditional chat applications mainly return text responses.

MindMesh extends the conversational interface by connecting user requests to different tools and visual outputs.

For example:

```text
"What's the weather?"
        ↓
Weather Intent
        ↓
OpenWeatherMap
        ↓
Weather Data
        ↓
Dashboard Visualization
```

Similarly:

```text
"Check CPU usage"
        ↓
System Stats Intent
        ↓
psutil
        ↓
CPU / RAM / Disk Data
        ↓
Dashboard Widget
```

And:

```text
"Tell me about the heart"
        ↓
Knowledge Intent
        ↓
Wikipedia Lookup
        +
3D Model Matching
        ↓
Knowledge Summary
        +
Interactive 3D Visualization
```

The application can also use an optional OpenAI-compatible LLM endpoint for open-ended conversations.

---

# ✨ Key Features

## 🤖 Conversational AI

MindMesh supports natural-language interaction through a lightweight intent-based agent.

Supported intents include:

* Greetings
* Assistant identity
* Current time/date
* Weather
* System statistics
* Knowledge lookup
* Knowledge follow-up questions
* General conversation

Example:

```text
User:
Tell me about the brain

MindMesh:
Provides a Wikipedia-based summary and displays an
interactive 3D brain model.
```

---

## 🧠 Rule-Based Intent Classification

The project uses a lightweight regex/keyword-based intent classifier rather than requiring a hosted NLU service.

The classifier identifies requests such as:

```text
Weather:
"What's the weather?"
"Temperature in Pune"

System:
"Check CPU usage"
"How is my system?"

Time:
"What is the time?"
"What's today's date?"

Knowledge:
"Tell me about AI"
"What is quantum computing?"
"Show me the heart"
```

This approach allows the application to work without an external AI service for the core commands.

---

# 🗣️ Voice Interaction

MindMesh supports browser-based voice interaction using the **Web Speech API**.

The frontend includes:

```text
Speech Recognition
        ↓
User Voice
        ↓
Text
        ↓
MindMesh Agent
        ↓
Response
        ↓
Speech Synthesis
```

The application can therefore support both:

```text
🎤 Voice Input
        +
⌨️ Text Input
```

with spoken responses through browser text-to-speech.

---

# 🌐 Knowledge Search

MindMesh integrates with the public **Wikipedia REST API** to retrieve information about user-requested topics.

For example:

```text
User:
What is artificial intelligence?
```

The backend:

```text
User Question
      ↓
Intent Classification
      ↓
Knowledge Intent
      ↓
Wikipedia REST API
      ↓
Article Summary
      ↓
MindMesh Response
```

The system can retrieve:

* Article title
* Summary
* Thumbnail image
* Wikipedia article URL

If an exact Wikipedia title is not found, the system uses Wikipedia search suggestions to find a relevant article.

---

# 🧊 Interactive 3D Knowledge Visualization

One of the main visual features of MindMesh is its interactive 3D knowledge panel.

For selected topics, the application displays a real interactive **Sketchfab 3D model** instead of only a static image.

Supported curated topics include:

```text
❤️ Heart
🧠 Brain
💀 Skull
🦴 Skeleton
🧬 DNA
🌍 Earth
☀️ Solar System
🫃 Stomach
🫁 Lungs
Digestive System
```

Example:

```text
"Tell me about the heart"
```

produces:

```text
Wikipedia Summary
        +
Interactive 3D Heart Model
```

The 3D model can be:

```text
Drag → Rotate
Scroll → Zoom
```

Topics without a curated 3D model automatically fall back to a Wikipedia visual.

---

# 💻 Live System Monitoring

MindMesh can monitor the host system using `psutil`.

The dashboard can retrieve:

* CPU usage
* RAM usage
* RAM used/total
* Disk usage
* Disk used/total
* System boot time

Example:

```text
CPU       35%
RAM       62%
Disk      71%
```

The data comes from the actual host system rather than being hard-coded.

---

# 🌦️ Weather Information

MindMesh supports weather information through **OpenWeatherMap**.

If an API key is configured:

```text
User
 ↓
Weather Request
 ↓
OpenWeatherMap API
 ↓
Live Weather Data
 ↓
Dashboard
```

The application can return:

* Temperature
* Feels-like temperature
* Humidity
* Wind speed
* Weather description
* City
* Country

If no API key is configured, MindMesh uses a simulated weather response so the dashboard can still function during development.

---

# 💬 Conversation Memory

Conversation history is persisted using Django models.

The application contains two primary models:

```text
ConversationSession
        │
        └── Message
              ├── User message
              ├── Assistant response
              ├── Intent
              ├── Visual type
              └── Visual payload
```

Each browser session gets its own `ConversationSession`.

The system also stores:

```text
last_topic
```

This allows contextual follow-up requests.

Example:

```text
User:
Tell me about the heart.

MindMesh:
[Heart information]

User:
Tell me more.

MindMesh:
[More information about the heart]
```

The previous topic is retained instead of treating the follow-up as an unrelated question.

---

# 🧩 Optional LLM Integration

MindMesh includes an optional LLM fallback.

If `LLM_API_KEY` is configured, free-form conversations can be sent to an **OpenAI-compatible chat-completions endpoint**.

Supported architecture:

```text
User Message
      ↓
Intent Classifier
      ↓
Known Intent?
   ↙       ↘
 YES        NO
  ↓          ↓
Tool       LLM Fallback
  ↓          ↓
Response ←──┘
```

The endpoint can be configured through:

```env
LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

The project is designed so that an OpenAI-compatible endpoint can also be replaced with another compatible service or a local server.

Without an API key, MindMesh falls back to its built-in offline responses.

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────────────────┐
│                         USER                             │
│                                                          │
│       🎤 Voice Input       ⌨️ Text Input                │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│                    DJANGO WEB APP                        │
│                                                          │
│              Dashboard / Frontend                        │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│                     CHAT API                             │
│                                                          │
│                 POST /api/chat/                          │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│                  MINDMESH AGENT                          │
│                                                          │
│                Intent Classification                     │
└──────────────┬────────────┬────────────┬────────────────┘
               │            │            │
               ▼            ▼            ▼
          Weather       System Stats   Knowledge
               │            │            │
               ▼            ▼            ▼
       OpenWeatherMap     psutil      Wikipedia
                                           │
                                           ▼
                                      Sketchfab
                                           │
               ┌───────────────────────────┘
               │
               ▼
        Optional LLM Fallback
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│                    AGENT RESPONSE                        │
│                                                          │
│        Text + Intent + Visual Payload                    │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│                     DASHBOARD                            │
│                                                          │
│  💬 Chat    📊 Stats    🌦️ Weather    🧠 Knowledge      │
│                                                          │
│                    🧊 3D Visual                          │
└──────────────────────────────────────────────────────────┘
```

---

# 🔄 Agent Workflow

The central agent is implemented in:

```text
assistant/agent/core_agent.py
```

For every user message, MindMesh performs the following workflow:

```text
User Message
     ↓
Intent Classification
     ↓
Entity Extraction
     ↓
Select Handler
     ↓
Call Tool
     ↓
Generate Response
     ↓
Create Visual Payload
     ↓
Save Conversation
     ↓
Return JSON
     ↓
Frontend Rendering
```

The main agent response contains:

```python
{
    "reply": "...",
    "intent": "...",
    "visual": {...}
}
```

---

# 🧠 Intent Types

The current classifier supports the following major intent categories:

| Intent               | Example               |
| -------------------- | --------------------- |
| `greeting`           | "Hello"               |
| `identity`           | "Who are you?"        |
| `time`               | "What is the time?"   |
| `weather`            | "What's the weather?" |
| `system_stats`       | "Check CPU usage"     |
| `knowledge`          | "Tell me about AI"    |
| `knowledge_followup` | "Tell me more"        |
| `chat`               | General conversation  |
| `empty`              | Empty input           |

The classifier is implemented in:

```text
assistant/agent/intents.py
```

---

# 🛠️ Technology Stack

## Backend

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Python        | Core programming language    |
| Django        | Web framework                |
| Django ORM    | Conversation persistence     |
| SQLite        | Default development database |
| Requests      | External API communication   |
| python-dotenv | Environment configuration    |

## AI / Agent

| Technology                   | Purpose                 |
| ---------------------------- | ----------------------- |
| Rule-based Intent Classifier | Request classification  |
| Optional LLM                 | Open-ended conversation |
| OpenAI-compatible API        | LLM integration         |
| Wikipedia REST API           | Knowledge retrieval     |

## System Monitoring

| Technology      | Purpose               |
| --------------- | --------------------- |
| psutil          | CPU monitoring        |
| psutil          | RAM monitoring        |
| psutil          | Disk monitoring       |
| Python datetime | Time/date information |

## Frontend

| Technology              | Purpose                      |
| ----------------------- | ---------------------------- |
| HTML5                   | UI structure                 |
| CSS3                    | Dashboard styling            |
| JavaScript              | Frontend logic               |
| Web Speech API          | Speech recognition/synthesis |
| Canvas/JS visualization | Knowledge graph animation    |

## 3D Visualization

| Technology | Purpose               |
| ---------- | --------------------- |
| Sketchfab  | Interactive 3D models |

## Development

| Technology                | Purpose            |
| ------------------------- | ------------------ |
| Git                       | Version control    |
| GitHub                    | Repository hosting |
| Django Development Server | Local development  |

---

# 📁 Project Structure

```text
mindmesh_django/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── mindmesh_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── assistant/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    │
    ├── migrations/
    │   ├── __init__.py
    │   ├── 0001_initial.py
    │   └── 0002_conversationsession_last_topic.py
    │
    ├── agent/
    │   ├── __init__.py
    │   ├── core_agent.py
    │   ├── intents.py
    │   ├── tools.py
    │   ├── llm_client.py
    │   └── models_3d.py
    │
    ├── templates/
    │   └── assistant/
    │       └── dashboard.html
    │
    └── static/
        └── assistant/
            ├── css/
            │   └── style.css
            │
            └── js/
                ├── app.js
                ├── speech.js
                └── knowledge_graph.js
```

---

# 🔌 API Endpoints

MindMesh exposes lightweight JSON endpoints through Django.

| Endpoint        | Method | Purpose                          |
| --------------- | ------ | -------------------------------- |
| `/`             | GET    | Main dashboard                   |
| `/api/chat/`    | POST   | Send message to MindMesh         |
| `/api/stats/`   | GET    | Get CPU/RAM/Disk statistics      |
| `/api/weather/` | GET    | Get weather information          |
| `/api/clock/`   | GET    | Get current date/time            |
| `/api/history/` | GET    | Get current conversation history |

---

# 💬 Chat API

### Request

```http
POST /api/chat/
```

Example:

```json
{
    "message": "Tell me about the brain"
}
```

### Response

```json
{
    "reply": "The brain is...",
    "intent": "knowledge",
    "visual": {
        "type": "model3d",
        "data": {
            "title": "Human Brain Anatomy",
            "embed_url": "..."
        }
    },
    "timestamp": "..."
}
```

The visual payload allows the frontend to decide what should appear in the central knowledge panel.

---

# 📊 System Statistics API

```http
GET /api/stats/
```

Example response:

```json
{
    "cpu_percent": 35.4,
    "ram_percent": 61.8,
    "ram_used_gb": 9.87,
    "ram_total_gb": 15.85,
    "disk_used_gb": 240.5,
    "disk_total_gb": 475.8,
    "disk_percent": 50.5,
    "boot_time": "..."
}
```

The values are obtained using `psutil`.

---

# 🌦️ Weather API

```http
GET /api/weather/?city=Pune
```

When an OpenWeatherMap API key is configured, the application requests live weather data.

The returned data includes:

```text
City
Country
Temperature
Feels Like
Humidity
Wind Speed
Weather Description
```

---

# 🕒 Clock API

```http
GET /api/clock/
```

Returns the current server-local date and time.

---

# 🗂️ Conversation History API

```http
GET /api/history/
```

Returns the stored messages for the current browser session.

Each message can contain:

```text
Role
Content
Intent
Visual Type
Visual Payload
Created At
```

---

# 🚀 Installation

## Prerequisites

Install:

* Python 3.10+
* pip
* Git
* Web browser

Optional:

* OpenWeatherMap API key
* LLM API key
* Docker

---

# 1. Clone the Repository

```bash
git clone https://github.com/SatyamGhugarkar/MindMesh-AI-in-the-Making-of-Next-Generation-Conversational-System.git
```

Then:

```bash
cd MindMesh-AI-in-the-Making-of-Next-Generation-Conversational-System
```

---

# 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The current project dependencies include:

```text
Django
psutil
requests
python-dotenv
```

---

# 4. Configure Environment Variables

Copy:

```text
.env.example
```

to:

```text
.env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Configure the values as required.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ASSISTANT_NAME=MindMesh
WAKE_WORD=hey mindmesh

OPENWEATHER_API_KEY=
DEFAULT_CITY=Aurangabad,IN

LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

All external API configuration is optional for the core application.

---

# 5. Run Database Migrations

```bash
python manage.py migrate
```

This creates the Django database tables used by the application.

---

# 6. Create Admin User

Optional:

```bash
python manage.py createsuperuser
```

Then access:

```text
http://127.0.0.1:8000/admin/
```

---

# 7. Start the Application

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🖥️ How to Use

## Step 1 — Open MindMesh

Navigate to:

```text
http://127.0.0.1:8000/
```

---

## Step 2 — Type or Speak

You can type a message or use the microphone.

Example:

```text
Hello
```

```text
Who are you?
```

```text
What is the weather?
```

```text
Check CPU usage
```

```text
Tell me about artificial intelligence
```

```text
Tell me about the heart
```

---

# Step 3 — View the Response

Depending on the request, MindMesh can return:

```text
💬 Text Response
```

or:

```text
🌦️ Weather Visualization
```

or:

```text
📊 System Statistics
```

or:

```text
🧠 Knowledge Information
```

or:

```text
🧊 Interactive 3D Model
```

---

# 🔬 Example Interactions

### Weather

```text
User:
What's the weather in Pune?

MindMesh:
Returns temperature, humidity, wind speed and
weather description.
```

### System Monitoring

```text
User:
How is my system doing?

MindMesh:
CPU is at XX%, RAM at XX%, and disk usage is XX%.
```

### Knowledge

```text
User:
What is quantum computing?

MindMesh:
Retrieves a Wikipedia summary and displays
the relevant knowledge visual when available.
```

### 3D Visualization

```text
User:
Tell me about the heart.

MindMesh:
Provides a knowledge summary and loads an
interactive 3D heart model.
```

### Contextual Follow-up

```text
User:
Tell me about DNA.

MindMesh:
[DNA information]

User:
Tell me more.

MindMesh:
[Additional information about DNA]
```

---

# 🧠 3D Model Library

The curated 3D model library is maintained in:

```text
assistant/agent/models_3d.py
```

Current model categories include:

```text
Heart
Coronary Arteries
Brain
Skull
Skeleton
DNA
Earth
Solar System
Stomach
Digestive System
Lungs
```

To add another model:

```python
MODEL_3D_LIBRARY = {
    "example": {
        "title": "Example Model",
        "sketchfab_uid": "YOUR_MODEL_UID",
        "keywords": ["example", "demo"],
    }
}
```

The application automatically creates the Sketchfab embed URL from the model UID.

---

# 🔧 Extending MindMesh

The architecture is designed so additional capabilities can be added without rewriting the entire application.

## Add a New Tool

Create a function inside:

```text
assistant/agent/tools.py
```

Example:

```python
def get_example_data():
    return {
        "value": "Example"
    }
```

---

## Add an Intent

Add a pattern inside:

```text
assistant/agent/intents.py
```

Then route the new intent through the classifier.

---

## Add an Agent Handler

Add a corresponding handler inside:

```text
assistant/agent/core_agent.py
```

For example:

```python
def _handle_example(self, text, entity, history, last_topic):
    data = tools.get_example_data()

    return AgentResponse(
        "Here is the example data.",
        "example",
        visual={
            "type": "example",
            "data": data
        }
    )
```

The existing API and frontend architecture can then process the response.

---

# 🔐 Security Considerations

The current project is primarily designed for development and portfolio demonstration.

Before production deployment, consider the following.

## 1. Secret Key

Do not expose a production Django secret key.

Use:

```env
SECRET_KEY=your-production-secret
```

and store it outside source control.

---

## 2. Debug Mode

Development:

```env
DEBUG=True
```

Production:

```env
DEBUG=False
```

---

## 3. API Keys

Never commit:

```text
.env
```

to GitHub.

The repository should contain:

```text
.env.example
```

instead.

---

## 4. Allowed Hosts

Configure production hosts appropriately:

```python
ALLOWED_HOSTS = [
    "your-domain.com",
]
```

---

## 5. HTTPS

Production deployment should use HTTPS for secure communication.

---

# ⚠️ Current Limitations

## Rule-Based Intent Classification

The primary intent classifier is based on regex and keyword patterns.

It does not provide full semantic NLU understanding.

For example, highly unusual phrasing may not match an existing intent.

---

## LLM Is Optional

Without:

```env
LLM_API_KEY=
```

open-ended chat uses the built-in fallback responses.

The core tool-based features do not require an LLM.

---

## Weather Requires API Configuration for Live Data

Without:

```env
OPENWEATHER_API_KEY=
```

the application uses simulated weather data.

---

## Browser Speech Support

Voice functionality depends on browser support for the Web Speech API.

Speech recognition behavior can vary between browsers and operating systems.

---

## Knowledge Depends on External APIs

Wikipedia lookups require network access.

If Wikipedia is unavailable, the application may not be able to retrieve knowledge information.

---

## 3D Models Depend on External Embeds

The 3D visualization uses Sketchfab embeds, so availability depends on the external service and the selected model.

---

# 🧪 Testing

The current project contains the Django application structure, but detector-style comprehensive automated tests are not currently implemented.

Recommended future tests include:

### Agent Tests

```text
Greeting classification
Weather classification
System statistics classification
Knowledge classification
Follow-up classification
Unknown request fallback
```

### API Tests

```text
GET /
POST /api/chat/
GET /api/stats/
GET /api/weather/
GET /api/clock/
GET /api/history/
```

### Conversation Tests

```text
Session creation
Message persistence
Last-topic persistence
Knowledge follow-up
```

---

# 🔧 Troubleshooting

## `ModuleNotFoundError: No module named 'django'`

Activate your virtual environment:

```powershell
venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

---

## Server Does Not Start

Run:

```bash
python manage.py check
```

Then:

```bash
python manage.py migrate
python manage.py runserver
```

---

## Weather Is Simulated

Check your `.env`:

```env
OPENWEATHER_API_KEY=your_api_key
```

Restart Django after changing environment variables.

---

## LLM Is Not Responding

Check:

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

If no API key is configured, MindMesh intentionally uses its offline fallback.

---

## Voice Input Is Not Working

Check:

* Browser microphone permission
* Browser support for Web Speech API
* HTTPS requirements where applicable
* Microphone availability

---

# 📈 Future Improvements

## AI / Agent Improvements

* Replace rule-based classification with an LLM-based router.
* Add structured tool calling.
* Add multi-step agent workflows.
* Add better conversational memory.
* Add semantic retrieval.
* Add RAG using a vector database.
* Add conversation summarization.
* Add long-term user memory.

---

## Knowledge Improvements

* Add RAG pipeline.
* Add document upload.
* Add PDF question answering.
* Add embeddings.
* Add vector database integration.
* Add source citations.
* Add multi-source knowledge retrieval.

---

## Voice Improvements

* True wake-word detection.
* Streaming speech recognition.
* Better speech synthesis.
* Voice activity detection.
* Continuous conversation mode.

---

## Visualization Improvements

* Expand the 3D model library.
* Add more interactive knowledge graphs.
* Add real-time animated visualizations.
* Add data-driven charts.
* Add topic relationships.
* Add WebGL-based custom 3D scenes.

---

## Application Improvements

* User authentication.
* Multi-user conversations.
* Conversation search.
* Conversation deletion.
* Conversation export.
* User-specific preferences.
* REST API.
* WebSocket-based real-time responses.
* Mobile responsive improvements.

---

## Production Improvements

* PostgreSQL.
* Redis.
* Celery background tasks.
* Production ASGI server.
* HTTPS.
* Docker deployment.
* CI/CD.
* Logging and monitoring.
* Rate limiting.
* API authentication.
* Cloud deployment.

---

# 🧭 Roadmap

```text
[x] Django web application
[x] Conversational dashboard
[x] Rule-based intent classification
[x] Weather tool
[x] System monitoring
[x] Wikipedia knowledge lookup
[x] Conversation persistence
[x] Contextual follow-up questions
[x] Voice input/output integration
[x] Interactive knowledge visualization
[x] Sketchfab 3D model integration
[x] Optional LLM fallback
[x] JSON API endpoints

[ ] Advanced LLM agent
[ ] RAG pipeline
[ ] Vector database
[ ] Long-term memory
[ ] True wake-word detection
[ ] Streaming responses
[ ] User authentication
[ ] REST API expansion
[ ] WebSocket support
[ ] PostgreSQL
[ ] Production deployment
[ ] CI/CD
```

---

# 🧩 Potential RAG Architecture

A future MindMesh version can extend the knowledge system into a Retrieval-Augmented Generation architecture:

```text
User Question
      ↓
Embedding Model
      ↓
Vector Database
      ↓
Relevant Documents
      ↓
Context Construction
      ↓
LLM
      ↓
Grounded Response
```

Potential technologies include:

```text
Embeddings
   +
ChromaDB / Pinecone
   +
RAG
   +
LLM
```

This would allow MindMesh to answer questions from private documents and user-provided knowledge sources instead of relying only on Wikipedia or an LLM.

---

# 🧑‍💻 Development Workflow

The project follows a modular architecture:

```text
Frontend
   ↓
Django Views
   ↓
MindMesh Agent
   ↓
Intent Classifier
   ↓
Tools / LLM
   ↓
Structured Response
   ↓
Database
   ↓
Frontend Visualization
```

This separation makes it easier to add new tools and capabilities without tightly coupling the frontend to the underlying implementation.

---

# 📦 Dependencies

The current `requirements.txt` contains:

```text
Django>=4.2,<5.1
psutil>=5.9
requests>=2.31
python-dotenv>=1.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

# ⚖️ License

This project is released under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Satyam Ghugarkar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Third-party services, APIs, libraries, and external 3D models remain subject to their respective licenses and terms.

---

# 👨‍💻 Author

## Satyam Ghugarkar

**AI / Data Science | Generative AI | Python | Django**

* GitHub: https://github.com/SatyamGhugarkar
* LinkedIn: https://www.linkedin.com/in/satyamghugarkar/
* Email: [ghugarkarsatyam1@gmail.com](mailto:ghugarkarsatyam1@gmail.com)

---

# 🌟 Why This Project?

MindMesh demonstrates an end-to-end AI application rather than only an isolated machine-learning model.

It combines:

```text
Python
   +
Django
   +
AI Agent Architecture
   +
Intent Classification
   +
LLM Integration
   +
API Integration
   +
Computer/System Monitoring
   +
Wikipedia Knowledge Retrieval
   +
Voice Interaction
   +
3D Visualization
   +
JavaScript
   +
Database Persistence
   +
GitHub
```

The overall workflow is:

```text
User
 ↓
Voice / Text
 ↓
Django
 ↓
MindMesh Agent
 ↓
Intent Classification
 ↓
Tool Selection
 ↓
┌───────────────┬───────────────┬───────────────┐
│               │               │               │
Weather       System          Knowledge       Chat
              Stats
│               │               │               │
OpenWeather   psutil        Wikipedia        LLM
                              +
                           Sketchfab
└───────────────┴───────────────┴───────────────┘
                       ↓
              Structured Response
                       ↓
                 Django Dashboard
```

The project demonstrates how multiple AI and software components can be combined into a single conversational application.

---

# ⚠️ Disclaimer

MindMesh is an educational and experimental AI assistant.

Information retrieved from external APIs or generated by optional LLM services may contain errors.

The application should not be treated as a replacement for professional advice or authoritative information.

---

# ⭐ Support

If you find the project useful, consider starring the repository and sharing feedback.

**Built by Satyam Ghugarkar.**
