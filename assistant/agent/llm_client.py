"""
Optional LLM-backed fallback for open-ended chat.

If settings.LLM_API_KEY is empty (the default), the agent never calls
this module — it uses the offline rule-based responder in core_agent.py
instead. Set LLM_API_KEY (and optionally LLM_BASE_URL / LLM_MODEL) in your
.env to enable this for any OpenAI-compatible chat completions endpoint
(OpenAI itself, Azure OpenAI, or a local server like Ollama/LM Studio).
"""

import requests
from django.conf import settings

SYSTEM_PROMPT = (
    "You are MindMesh, a concise, friendly personal AI assistant embedded in a "
    "live dashboard. Keep replies to 2-4 sentences unless asked for more detail."
)


def is_configured():
    return bool(settings.LLM_API_KEY)


def chat_completion(user_message, history=None):
    """
    history: list of {"role": "user"|"assistant", "content": str}, oldest first.
    Returns the assistant's reply text, or None on failure.
    """
    if not is_configured():
        return None

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in (history or [])[-8:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    try:
        resp = requests.post(
            f"{settings.LLM_BASE_URL.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "messages": messages,
                "temperature": 0.6,
                "max_tokens": 300,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except (requests.RequestException, KeyError, IndexError):
        return None
