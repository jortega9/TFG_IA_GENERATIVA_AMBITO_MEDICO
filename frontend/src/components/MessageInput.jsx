import React, { useState } from 'react'
import { Send, User } from 'lucide-react'

function MessageInput({ onSendMessage }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="message-input">
      <div className="input-icon">
        <User size={24} />
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        aria-label="Type your message"
      />
      <button type="submit" aria-label="Send message">
        <Send size={24} />
      </button>
    </form>
  )
}

export default MessageInput