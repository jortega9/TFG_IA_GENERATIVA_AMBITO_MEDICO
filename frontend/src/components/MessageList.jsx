import React, { useEffect, useRef } from 'react'
import { User, Bot } from 'lucide-react'
import AsistenteIcon from '../../public/assets/AsistenteIcon.png'

function MessageList({ messages }) {
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div key={index} className={`message-container ${message.isUser ? 'user' : 'bot'}`}>
          <div className="message-icon">
            {message.isUser ? (
              <User size={24}/>
            ) : (
              <img src={AsistenteIcon} alt="Bot avatar" className="avatar-image-small" />
            )}
          </div>
          <div className={`message ${message.error ? 'error' : (message.isUser ? 'user' : 'bot')}`}>
            {message.text}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default MessageList