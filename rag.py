import json
import os
from pathlib import Path

import numpy as np
import requests
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-3.1-flash-lite"   # we will check this name in Step 2
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
TOP_K = 3
MIN_SCORE = 0.25

# Load everything once, when the program starts
embedder = SentenceTransformer(EMBEDDING_MODEL)
vectors = np.load("index/vectors.npy")
chunks = json.loads(Path("index/chunks.json").read_text(encoding="utf-8"))


def retrieve(question, k=TOP_K):
    q_vector = embedder.encode(question, normalize_embeddings=True)
    scores = vectors @ q_vector
    best = np.argsort(scores)[::-1][:k]
    return [(chunks[i], float(scores[i])) for i in best]


def build_prompt(question, found):
    context = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk, _ in found
    )
    system = (
        "You are a helpful assistant for a hospital website. "
        "Answer only from the CONTEXT below. "
        "If the answer is not in the CONTEXT, say you do not have that information. "
        "Never give medical advice, diagnosis or medicine suggestions. "
        "If the user describes a health problem, tell them to consult a doctor. "
        "For emergencies, tell them to call the emergency number given in the CONTEXT. "
        "Keep answers short and clear.\n\n"
        f"CONTEXT:\n{context}"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]
def ask_llm(messages):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "No API key found. Set GEMINI_API_KEY first."

    system_text = messages[0]["content"]   # the rules and the chunks
    question = messages[-1]["content"]     # the user's question

    try:
        response = requests.post(
            GEMINI_URL.format(GEMINI_MODEL),
            headers={"x-goog-api-key": api_key},
            json={
                "system_instruction": {"parts": [{"text": system_text}]},
                "contents": [{"role": "user", "parts": [{"text": question}]}],
            },
            timeout=60,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        return f"The model returned an error: {error}"

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def answer(question):
    found = retrieve(question)

    if found[0][1] < MIN_SCORE:
        return "Sorry, I don't have that information.", []

    messages = build_prompt(question, found)
    reply = ask_llm(messages)
    sources = sorted({chunk["source"] for chunk, _ in found})
    return reply, sources