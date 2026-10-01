"""RAG-chatbot: FastAPI-palvelin. Käynnistys: uvicorn app:app"""
import chromadb
import requests
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from config import DB_DIR, COLLECTION, TOP_K
from rag import embed, chat

app = FastAPI(title="Maatila-RAG-chatbot")

try:
    col = chromadb.PersistentClient(path=DB_DIR).get_collection(COLLECTION)
except Exception:
    raise SystemExit("Indeksiä ei löydy. Aja ensin: python ingest.py")

SYSTEM = """Olet avustaja maatilayrittäjille. Vastaa suomeksi (tai käyttäjän kielellä).
Käytä vastauksessa vain annettua kontekstia.
Jos vastausta ei löydy kontekstista, sano selvästi, ettet löydä tietoa annetuista dokumenteista.
Älä keksi lukuja, päivämääriä tai määräyksiä. Vastaa ytimekkäästi."""


class Ask(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.post("/api/chat")
def ask(body: Ask):
    try:
        qvec = embed([body.question])[0]
        res = col.query(query_embeddings=[qvec], n_results=TOP_K)
        docs, metas = res["documents"][0], res["metadatas"][0]
        context = "\n\n".join(f"[{m['source']}]\n{d}" for d, m in zip(docs, metas))
        answer = chat([
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Konteksti:\n{context}\n\nKysymys: {body.question}"},
        ])
    except requests.RequestException:
        raise HTTPException(502, "Mallipalvelin (Ollama) ei vastaa")
    return {"answer": answer, "sources": sorted({m["source"] for m in metas})}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
