import React, { useState, useEffect } from "react";
import { sendMessage, fetchHistory } from "./api";
import ChatBox from "./components/ChatBox";
import InputArea from "./components/InputArea";
import Login from "./components/Login";

function App() {
  const [userId, setUserId] = useState(localStorage.getItem("user_id") || "");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(!!userId);

  useEffect(() => {
    if (userId) {
      localStorage.setItem("user_id", userId);
      fetchHistory(userId).then((data) => setMessages(data.messages || []));
    }
  }, [userId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || !userId) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    const result = await sendMessage(userId, input);
    setMessages((prev) => [...prev, { sender: "assistant", text: result.reply }]);
  };

  const handleLogin = (id) => {
    setUserId(id);
    setIsLoggedIn(true);
  };

  if (!isLoggedIn) return <Login onLogin={handleLogin} />;

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="text-center py-4 text-blue-900 font-bold text-xl bg-blue-100">
        MindCare Assistant 💬
      </div>
      <ChatBox messages={messages} />
      <InputArea input={input} setInput={setInput} handleSubmit={handleSubmit} />
    </div>
  );
}

export default App;
