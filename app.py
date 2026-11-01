from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag import answer

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()[:500]
    reply, sources = answer(question)
    return {"answer": reply, "sources": sources}