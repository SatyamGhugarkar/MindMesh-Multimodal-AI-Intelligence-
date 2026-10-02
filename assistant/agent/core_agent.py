"""
The MindMesh agent.

This is the "agent" the user asked for: given a line of user text (typed
or transcribed from speech), it
  1. classifies intent,
  2. calls the right tool (weather / system stats / Wikipedia knowledge /
     clock), or falls back to a conversational responder (LLM if
     configured, otherwise a small offline responder), and
  3. returns a structured result: the reply text to show/speak, plus an
     optional "visual" payload telling the frontend what to render in the
     centre knowledge panel (mirrors the anatomy-model swap in the
     reference UI, generalised to any Wikipedia topic).
"""

import random

from django.conf import settings

from . import intents, tools
from . import llm_client
from .models_3d import find_3d_model


GREETING_REPLIES = [
    "Hey there. How can I help you today?",
    "Hello! What would you like to know?",
    "Hi — I'm listening. What's on your mind?",
]

CHAT_FALLBACKS = [
    "I'm not entirely sure about that one yet, but I'm always learning — "
    "try asking me about the weather, system stats, or \"tell me about\" any topic.",
    "I don't have a specific answer for that right now. Ask me to explain "
    "a topic, check the weather, or read out your system stats.",
]


class AgentResponse:
    def __init__(self, text, intent="chat", visual=None, topic=None):
        self.text = text
        self.intent = intent
        self.visual = visual  # dict or None
        self.topic = topic  # set on knowledge intents so the view can remember it

    def as_dict(self):
        return {"reply": self.text, "intent": self.intent, "visual": self.visual}


class MindMeshAgent:
    """Stateless per-call; conversation history is passed in by the view."""

    def handle(self, user_text, history=None, last_topic=""):
        intent, entity = intents.classify(user_text)

        handler = getattr(self, f"_handle_{intent}", None)
        if handler is None:
            handler = self._handle_chat
        return handler(user_text, entity, history or [], last_topic)

    # ------------------------------------------------------------------
    # Intent handlers
    # ------------------------------------------------------------------

    def _handle_empty(self, text, entity, history, last_topic):
        return AgentResponse("I didn't catch that — could you say it again?", "empty")

    def _handle_greeting(self, text, entity, history, last_topic):
        return AgentResponse(random.choice(GREETING_REPLIES), "greeting")

    def _handle_identity(self, text, entity, history, last_topic):
        name = settings.ASSISTANT_NAME
        reply = (
            f"I'm {name}, your personal AI dashboard assistant. I can check the "
            "weather, read out live system stats, look up almost any topic and "
            "show it on screen, and chat with you — by voice or text."
        )
        return AgentResponse(reply, "identity")

    def _handle_time(self, text, entity, history, last_topic):
        data = tools.get_current_datetime()
        reply = f"It's {data['time_label']} on {data['date_label']}."
        return AgentResponse(reply, "time", visual=None)

    def _handle_weather(self, text, entity, history, last_topic):
        data = tools.get_weather(city=self._normalise_city(entity))
        note = " (simulated — add OPENWEATHER_API_KEY for live data)" if data["simulated"] else ""
        reply = (
            f"It's currently {data['temp_c']}°C and {data['description']} in "
            f"{data['city']}, feels like {data['feels_like_c']}°C, humidity "
            f"{data['humidity']}%.{note}"
        )
        visual = {"type": "weather", "data": data}
        return AgentResponse(reply, "weather", visual=visual)

    def _handle_system_stats(self, text, entity, history, last_topic):
        data = tools.get_system_stats()
        reply = (
            f"CPU is at {data['cpu_percent']}%, RAM at {data['ram_percent']}% "
            f"({data['ram_used_gb']} / {data['ram_total_gb']} GB), and disk usage "
            f"is {data['disk_percent']}%."
        )
        visual = {"type": "stats", "data": data}
        return AgentResponse(reply, "system_stats", visual=visual)

    def _handle_knowledge(self, text, entity, history, last_topic):
        topic = entity or text
        return self._answer_knowledge(topic)

    def _handle_knowledge_followup(self, text, entity, history, last_topic):
        """
        Handles "tell me more", "what about that?", "and that?" — anything
        that only makes sense in light of the previous topic asked about.
        """
        if not last_topic:
            reply = (
                "About what, exactly? We haven't talked about a specific "
                "topic yet in this conversation — try \"tell me about X\" first."
            )
            return AgentResponse(reply, "knowledge_followup")
        return self._answer_knowledge(last_topic)

    def _answer_knowledge(self, topic):
        # Prefer a real, interactive 3D model when we have one for this
        # topic (mirrors the anatomy-model viewer from the reference UI).
        model3d = find_3d_model(topic)

        data = tools.wiki_lookup(topic)
        if not data and not model3d:
            reply = (
                f"I couldn't find a clear entry for \"{topic}\". Try rephrasing, "
                "or ask about something more specific."
            )
            return AgentResponse(reply, "knowledge_miss")

        if data:
            summary = data["summary"]
            reply = summary if len(summary) < 500 else summary[:497].rstrip() + "..."
        else:
            reply = f"Here's the {model3d['title']} — drag to rotate, scroll to zoom."

        if model3d:
            if data:
                reply += " I've pulled up an interactive 3D model too — drag to rotate it."
            visual = {
                "type": "model3d",
                "data": {
                    "title": model3d["title"],
                    "embed_url": model3d["embed_url"],
                },
            }
        else:
            visual = {
                "type": "knowledge",
                "data": {
                    "title": data["title"],
                    "image": data["image"],
                    "url": data["url"],
                },
            }

        return AgentResponse(reply, "knowledge", visual=visual, topic=topic)

    def _handle_chat(self, text, entity, history, last_topic):
        llm_reply = llm_client.chat_completion(text, history=history)
        if llm_reply:
            return AgentResponse(llm_reply, "chat")
        return AgentResponse(random.choice(CHAT_FALLBACKS), "chat")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalise_city(entity):
        if not entity:
            return None
        return entity.strip()
