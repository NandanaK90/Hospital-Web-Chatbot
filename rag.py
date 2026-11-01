import json
import os
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "gemini-embedding-001"
EMBED_URL = "https://generativelanguage.googleapis.com/v1beta/models/{}:embedContent"
DIMS = 768
GEMINI_MODEL = "gemini-3.1-flash-lite"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
TOP_K = 3
MIN_SCORE = 0.6   # we will tune this after testing

# Load the index once, when the program starts
vectors = np.load("index/vectors.npy")
chunks = json.loads(Path("index/chunks.json").read_text(encoding="utf-8"))


def embed_query(question):
    api_key = os.environ.get("GEMINI_API_KEY")
    response = requests.post(
        EMBED_URL.format(EMBED_MODEL),
        headers={"x-goog-api-key": api_key},
        json={
            "model": "models/" + EMBED_MODEL,
            "content": {"parts": [{"text": question}]},
            "taskType": "RETRIEVAL_QUERY",
            "outputDimensionality": DIMS,
        },
        timeout=30,
    )
    response.raise_for_status()
    vector = np.array(response.json()["embedding"]["values"], dtype="float32")
    return vector / np.linalg.norm(vector)


def retrieve(question, k=TOP_K):
    q_vector = embed_query(question)
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

    system_text = messages[0]["content"]
    question = messages[-1]["content"]

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
    try:
        found = retrieve(question)
    except requests.exceptions.RequestException as error:
        return f"Search error: {error}", []

    if found[0][1] < MIN_SCORE:
        return "Sorry, I don't have that information.", []

    messages = build_prompt(question, found)
    reply = ask_llm(messages)
    sources = sorted({chunk["source"] for chunk, _ in found})
    return reply, sources