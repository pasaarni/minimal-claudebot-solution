"""Ohut asiakas Ollaman rajapintaan: embeddingit ja chat."""
import requests
from config import OLLAMA_URL, CHAT_MODEL, EMBED_MODEL


def embed(texts):
    r = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["embeddings"]


def chat(messages):
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": CHAT_MODEL, "messages": messages, "stream": False},
        timeout=300,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]
