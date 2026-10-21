import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://localhost:5000/api/chat";

function App() {
  const [sessionId] = useState(
    () => {
      let id = sessionStorage.getItem("chatSessionId");

      if (!id) {
        id = `sess_${crypto.randomUUID()}`;
        sessionStorage.setItem("chatSessionId", id);
      }

      return id;
    }
  );

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! 👋 I'm your Customer Support AI. How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(event) {
    event.preventDefault();

    const message = input.trim();

    if (!message || loading) return;

    setMessages((previous) => [
      ...previous,
      { sender: "user", text: message },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sessionId,
          message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || "Request failed");
      }

      setMessages((previous) => [
        ...previous,
        {
          sender: "bot",
          text: data.reply,
          intent: data.intent,
          confidence: data.confidence,
          escalated: data.escalated,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          sender: "bot",
          text: `Sorry, I couldn't process your message. ${error.message}. Please check that the backend, AI service, and database are running.`,
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <section className="chat-card">
        <header className="chat-header">
          <div className="avatar">🤖</div>
          <div>
            <h1>Customer Support AI</h1>
            <p><span className="status-dot" /> AI Assistant Online</p>
          </div>
        </header>

        <div className="chat-window">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.sender}`}
            >
              <div className="message">
                <p>{message.text}</p>

                {message.sender === "bot" && message.intent && (
                  <div className="message-meta">
                    <span>Intent: {message.intent}</span>
                    {typeof message.confidence === "number" && (
                      <span>
                        Confidence: {Math.round(message.confidence * 100)}%
                      </span>
                    )}
                  </div>
                )}

                {message.escalated && (
                  <div className="escalation">
                    🧑‍💼 Human support escalation requested
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row bot">
              <div className="message typing">AI is thinking...</div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        <form className="chat-form" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Type your message..."
            disabled={loading}
            aria-label="Type your message"
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "..." : "Send ➤"}
          </button>
        </form>

        <footer>AI-powered customer support · Your messages are processed by the chatbot backend</footer>
      </section>
    </main>
  );
}

export default App;