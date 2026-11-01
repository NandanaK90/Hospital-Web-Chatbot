import json
import os
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "gemini-embedding-001"
EMBED_URL = "https://generativelanguage.googleapis.com/v1beta/models/{}:batchEmbedContents"
DIMS = 768
CHUNK_SIZE = 800
OVERLAP = 150
DOCS_DIR = Path("data/docs")


def read_file(path):
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8")


def split_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    text = " ".join(text.split())
    pieces = []
    start = 0
    while start < len(text):
        pieces.append(text[start:start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return pieces


def embed_texts(texts, api_key):
    all_vectors = []
    for i in range(0, len(texts), 50):
        batch = texts[i:i + 50]
        body = {
            "requests": [
                {
                    "model": "models/" + EMBED_MODEL,
                    "content": {"parts": [{"text": t}]},
                    "taskType": "RETRIEVAL_DOCUMENT",
                    "outputDimensionality": DIMS,
                }
                for t in batch
            ]
        }
        response = requests.post(
            EMBED_URL.format(EMBED_MODEL),
            headers={"x-goog-api-key": api_key},
            json=body,
            timeout=120,
        )
        if not response.ok:
            raise SystemExit("Embedding error: " + response.text)
        for item in response.json()["embeddings"]:
            all_vectors.append(item["values"])
    vectors = np.array(all_vectors, dtype="float32")
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms


api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Set GEMINI_API_KEY first (in .env or the terminal).")

chunks = []
for path in sorted(DOCS_DIR.glob("*")):
    if path.suffix.lower() in (".txt", ".md", ".pdf"):
        for piece in split_text(read_file(path)):
            chunks.append({"source": path.name, "text": piece})

print("Chunks:", len(chunks))
vectors = embed_texts([c["text"] for c in chunks], api_key)
print("Shape of vectors:", vectors.shape)

Path("index").mkdir(exist_ok=True)
np.save("index/vectors.npy", vectors)
Path("index/chunks.json").write_text(
    json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("Saved to the index folder.")