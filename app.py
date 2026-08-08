import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel

KIWIX_URL = "http://localhost:8080"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

app = FastAPI()

class Q(BaseModel):
    question: str

def search_all(question, k=2):
    books = [
        "wikipedia_en_all",
        "archlinux_en_all",
        "openstreetmap-wiki_en_all",
        "ragajunglism.org_en_all",
    ]
    chunks = []
    for book in books:
        r = requests.get(f"{KIWIX_URL}/search", params={"pattern": question, "books.name": book, "pageLength": k})
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.select("a")[:k]:
            href = link.get("href")
            if not href:
                continue
            page = requests.get(f"{KIWIX_URL}{href}")
            text = BeautifulSoup(page.text, "html.parser").get_text(" ", strip=True)
            chunks.append(f"[{book}]\n{text[:1500]}")
    return "\n\n".join(chunks)

@app.post("/ask")
def ask(q: Q):
    context = search_all(q.question)
    prompt = f"Answer using only this context, cite the source in brackets.\n\n{context}\n\nQuestion: {q.question}"
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False})
    print("OLLAMA RAW:", r.status_code, r.text)
    if r.status_code != 200:
        return {"answer": f"Ollama error: {r.text}", "sources": context[:200]}
    return {"answer": r.json()["response"], "sources": context[:200]}
