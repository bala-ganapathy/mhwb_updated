// API calls to backend
export const sendMessage = async (userId, message) => {
  const res = await fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  });
  return res.json();
};

export const fetchHistory = async (userId) => {
  const res = await fetch(`http://127.0.0.1:5000/history/${userId}`);
  return res.json();
};
