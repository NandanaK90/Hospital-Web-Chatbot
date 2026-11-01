import { useState, useRef, useEffect } from "react";

// Empty on your computer (the Vite proxy handles /chat).
// Online, this holds the backend address from VITE_API_URL.
const API = import.meta.env.VITE_API_URL || "";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);        // is the chat window open?
  const [input, setInput] = useState("");         // what the user is typing
  const [loading, setLoading] = useState(false);  // waiting for an answer?
  const [messages, setMessages] = useState([
    { who: "bot", text: "Hello! Ask me about timings, doctors, departments or appointments." },
  ]);

  const bottomRef = useRef(null);

  // Every time the messages change, scroll to the newest one
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  async function sendMessage(event) {
    event.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setMessages((old) => [...old, { who: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(API + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();
      setMessages((old) => [
        ...old,
        { who: "bot", text: data.answer, sources: data.sources },
      ]);
    } catch (error) {
      setMessages((old) => [
        ...old,
        { who: "bot", text: "Sorry, something went wrong. Please call the hospital." },
      ]);
    }
    setLoading(false);
  }

  return (
    <>
      {!open && (
        <button className="chat-fab" onClick={() => setOpen(true)}>
          Chat with us
        </button>
      )}

      {open && (
        <div className="chat-box">
          <div className="chat-head">
            <span>Hospital Assistant</span>
            <button onClick={() => setOpen(false)} aria-label="Close chat">
              &times;
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((m, index) => (
              <div key={index} className={"msg " + m.who}>
                {m.text}
                {m.sources && m.sources.length > 0 && (
                  <div className="src">Source: {m.sources.join(", ")}</div>
                )}
              </div>
            ))}
            {loading && <div className="msg bot">Thinking...</div>}
            <div ref={bottomRef} />
          </div>

          <form className="chat-form" onSubmit={sendMessage}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
            />
            <button type="submit" disabled={loading}>Send</button>
          </form>
        </div>
      )}
    </>
  );
}