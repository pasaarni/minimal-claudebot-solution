"""Lukee data/-kansion dokumentit, pilkkoo ne ja tallentaa vektoritietokantaan.
Ajetaan aina, kun dokumentit muuttuvat: python ingest.py
"""
from pathlib import Path

import chromadb
from pypdf import PdfReader

from config import DATA_DIR, DB_DIR, COLLECTION, CHUNK_SIZE, CHUNK_OVERLAP
from rag import embed

SUPPORTED = {".md", ".txt", ".pdf"}


def read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def chunk(text: str):
    text = text.strip()
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c.strip()]


def main():
    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION)  # rakennetaan indeksi puhtaalta pöydältä
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    files = [p for p in Path(DATA_DIR).rglob("*") if p.suffix.lower() in SUPPORTED]
    if not files:
        print(f"Ei dokumentteja kansiossa {DATA_DIR}/")
        return

    total = 0
    for f in files:
        chunks = chunk(read_file(f))
        source = str(f.relative_to(DATA_DIR))
        for i in range(0, len(chunks), 32):
            batch = chunks[i:i + 32]
            col.add(
                ids=[f"{source}:{i + j}" for j in range(len(batch))],
                documents=batch,
                embeddings=embed(batch),
                metadatas=[{"source": source}] * len(batch),
            )
        total += len(chunks)
        print(f"{source}: {len(chunks)} palaa")
    print(f"Valmis, yhteensä {total} palaa.")


if __name__ == "__main__":
    main()
