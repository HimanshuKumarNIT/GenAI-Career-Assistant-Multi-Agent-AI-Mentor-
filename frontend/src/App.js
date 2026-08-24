import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMessage = {
      role: "user",
      content: query
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: query
        })
      });

      const data = await res.json();

      const botMessage = {
        role: "assistant",
        category: data.category || "Unknown",
        content: data.success
          ? data.response
          : data.error
      };

      setMessages((prev) => [...prev, botMessage]);

    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          category: "System",
          content: "Backend connection failed"
        }
      ]);
    }

    setQuery("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendQuery();
    }
  };

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "1000px",
        margin: "auto"
      }}
    >
      <h1>GenAI Career Assistant</h1>

      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "15px",
          height: "550px",
          overflowY: "auto",
          backgroundColor: "#f8f9fa",
          marginBottom: "20px"
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              marginBottom: "15px",
              textAlign:
                msg.role === "user"
                  ? "right"
                  : "left"
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "12px",
                borderRadius: "10px",
                maxWidth: "80%",
                backgroundColor:
                  msg.role === "user"
                    ? "#d1e7dd"
                    : "#ffffff",
                border: "1px solid #ddd"
              }}
            >
              <div
                style={{
                  fontWeight: "bold",
                  marginBottom: "5px"
                }}
              >
                {msg.role === "user"
                  ? "You"
                  : "Assistant"}
              </div>

              {msg.role === "assistant" && (
                <div
                  style={{
                    color: "green",
                    fontSize: "12px",
                    fontWeight: "bold",
                    marginBottom: "8px"
                  }}
                >
                  Agent Used: {msg.category}
                </div>
              )}

              <div
                style={{
                  whiteSpace: "pre-wrap"
                }}
              >
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Ask something..."
        style={{
          width: "75%",
          padding: "12px",
          borderRadius: "8px",
          border: "1px solid #ccc"
        }}
      />

      <button
        onClick={sendQuery}
        style={{
          marginLeft: "10px",
          padding: "12px 20px",
          borderRadius: "8px",
          cursor: "pointer"
        }}
      >
        Send
      </button>
    </div>
  );
}

export default App;