import json                                              # NEW
from pathlib import Path

import numpy as np                                       # NEW
from sentence_transformers import SentenceTransformer   # NEW

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "all-MiniLM-L6-v2"                     # NEW


def read_file(path):
    return path.read_text(encoding="utf-8")


def split_into_chunks(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


# ---- Everything below is NEW ----

text = read_file(Path("data/docs/sample.txt"))
pieces = split_into_chunks(text)

# Keep the file name with every piece, so we can show the source later
chunks = [{"text": piece, "source": "sample.txt"} for piece in pieces]
print("Chunks:", len(chunks))

print("Loading model (the first time it downloads, please wait)...")
model = SentenceTransformer(EMBEDDING_MODEL)

vectors = model.encode([c["text"] for c in chunks], normalize_embeddings=True)
print("Shape of vectors:", vectors.shape)
print("First 5 numbers of chunk 1:", vectors[0][:5])

Path("index").mkdir(exist_ok=True)
np.save("index/vectors.npy", vectors)
Path("index/chunks.json").write_text(
    json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("Saved to the index folder.")