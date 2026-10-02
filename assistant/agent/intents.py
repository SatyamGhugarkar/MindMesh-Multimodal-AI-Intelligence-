"""
Lightweight, dependency-free intent classification for the MindMesh agent.

This is intentionally rule-based (regex + keyword matching) rather than a
hosted NLU service, so the assistant works fully offline out of the box.
If an LLM key is configured, free-chat fallback can hand off to it — see
agent/llm_client.py and core_agent.py.
"""

import re

_WEATHER_PATTERNS = [
    r"\bweather\b", r"\btemperature\b", r"\bforecast\b", r"\braining\b",
    r"\bhow (?:hot|cold|warm) is it\b", r"\bhumidity\b",
]

_STATS_PATTERNS = [
    r"\bcpu\b", r"\bram\b", r"\bmemory usage\b", r"\bdisk (?:space|usage)\b",
    r"\bsystem stat", r"\bsystem status\b", r"\bhow('?s| is) (?:the )?system\b",
    r"\bperformance\b",
]

_TIME_PATTERNS = [
    r"\bwhat(?:'s| is) the time\b", r"\bcurrent time\b", r"\btoday'?s date\b",
    r"\bwhat(?:'s| is) the date\b", r"\bwhat day is it\b",
]

_GREETING_PATTERNS = [
    r"^\s*(hi|hello|hey|yo|sup)\b", r"\bgood (morning|afternoon|evening)\b",
]

_KNOWLEDGE_PATTERNS = [
    r"^(?:tell me about|what is|what'?s|who is|who was|explain|define)\s+(.+)$",
    r"^show me\s+(?:a |an |the )?(.+)$",
    r"^(?:picture|image|photo|pic|model|3d model)\s+of\s+(.+)$",
    r"^(?:i want to (?:see|know about))\s+(.+)$",
]

# Trailing filler words to strip off a captured topic, e.g. "stomach
# image" -> "stomach", "heart model please" -> "heart".
_TOPIC_TRAILING_NOISE = re.compile(
    r"\s+(?:image|images|picture|pictures|photo|photos|pic|pics|"
    r"model|3d model|animation|please|now)$",
    flags=re.IGNORECASE,
)
_TOPIC_LEADING_ARTICLE = re.compile(r"^(?:the|a|an)\s+", flags=re.IGNORECASE)


def _clean_topic(topic):
    topic = topic.strip().rstrip("?.! ")
    # Strip repeatedly in case of "heart image please" (two trailing words).
    while True:
        new_topic = _TOPIC_TRAILING_NOISE.sub("", topic).strip()
        if new_topic == topic:
            break
        topic = new_topic
    # "tell me about the heart" -> "heart" (better Wikipedia + 3D-model match)
    topic = _TOPIC_LEADING_ARTICLE.sub("", topic).strip()
    return topic

_IDENTITY_PATTERNS = [
    r"\bwho are you\b", r"\bwhat can you do\b", r"\bwhat is mindmesh\b",
    r"\byour name\b",
]

# Follow-up phrasing that only makes sense with a previous topic in hand,
# e.g. after "tell me about the heart": "what about the brain?" (new
# topic, same style of question) or "tell me more" / "and that?" (same
# topic, wants elaboration). See core_agent.py for how last_topic is
# threaded through.
_FOLLOWUP_NEW_TOPIC_PATTERNS = [
    r"^(?:and|what about|how about)\s+(?:the |a |an )?(.+)$",
]
_FOLLOWUP_SAME_TOPIC_PATTERNS = [
    r"^(?:tell me more|more info|more details|more|go on|continue)\.?$",
    r"^(?:and|what about|how about)\s+(?:that|this|it)\??$",
]


def _matches_any(text, patterns):
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def classify(text):
    """
    Returns (intent, entity) where entity is the extra bit of text the
    tool needs (a city, a topic to look up, ...) or None.
    """
    cleaned = text.strip()
    lowered = cleaned.lower()

    if not cleaned:
        return "empty", None

    if _matches_any(lowered, _IDENTITY_PATTERNS):
        return "identity", None

    if _matches_any(lowered, _GREETING_PATTERNS) and len(cleaned.split()) <= 4:
        return "greeting", None

    if _matches_any(lowered, _TIME_PATTERNS):
        return "time", None

    if _matches_any(lowered, _WEATHER_PATTERNS):
        city_match = re.search(r"\bin\s+([a-zA-Z\s]+)$", cleaned, flags=re.IGNORECASE)
        return "weather", (city_match.group(1).strip() if city_match else None)

    if _matches_any(lowered, _STATS_PATTERNS):
        return "system_stats", None

    for pattern in _KNOWLEDGE_PATTERNS:
        match = re.search(pattern, cleaned, flags=re.IGNORECASE)
        if match:
            topic = _clean_topic(match.group(1))
            if topic:
                return "knowledge", topic

    # Check pronoun follow-ups ("and that?", "tell me more") BEFORE the
    # new-topic pattern below, so "and that?" isn't captured literally as
    # a topic named "that".
    if _matches_any(cleaned, _FOLLOWUP_SAME_TOPIC_PATTERNS):
        return "knowledge_followup", None

    for pattern in _FOLLOWUP_NEW_TOPIC_PATTERNS:
        match = re.search(pattern, cleaned, flags=re.IGNORECASE)
        if match:
            topic = _clean_topic(match.group(1))
            if topic:
                return "knowledge", topic

    return "chat", cleaned
