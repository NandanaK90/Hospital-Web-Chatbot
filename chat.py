from rag import answer

print("Chatbot ready. Ask a question (type 'quit' to exit).\n")

while True:
    question = input("You: ").strip()
    if question.lower() in {"quit", "exit"}:
        break
    if not question:
        continue

    reply, sources = answer(question)
    print(f"\nBot: {reply}")
    if sources:
        print(f"(Sources: {', '.join(sources)})")
    print()