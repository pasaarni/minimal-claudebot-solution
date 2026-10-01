import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen2.5:7b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")

DATA_DIR = os.getenv("DATA_DIR", "data")
DB_DIR = os.getenv("DB_DIR", "db")
COLLECTION = "farm_docs"

CHUNK_SIZE = 800      # merkkiä per pala
CHUNK_OVERLAP = 150   # palojen päällekkäisyys
TOP_K = 4             # montako palaa haetaan kontekstiksi
