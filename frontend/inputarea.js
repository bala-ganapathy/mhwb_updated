import React from "react";

export default function InputArea({ input, setInput, handleSubmit }) {
  return (
    <form onSubmit={handleSubmit} className="flex gap-4 p-4 border-t bg-white">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        className="flex-1 border rounded-full px-4 py-2 text-sm"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white rounded-full px-6 py-2 font-semibold hover:bg-blue-700"
      >
        Send
      </button>
    </form>
  );
}
