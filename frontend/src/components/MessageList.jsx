import React, { useEffect, useRef } from 'react'
import { User, Bot } from 'lucide-react'
import TobiCon from '../../public/TobiCon.png'

function MessageList({ messages }) {
  const messagesEndRef = useRef(null)

  // Desplazamos al final de la lista de mensaje el ultimo mensaje
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  /*
    Renderizado: El componente principal es la lista de mensajes, que tiene una funcion map que 
    itera sobre el array de mensajes, para cada mensaje se ve si es de User o de bot para crear 
    un className y en el css que tenga una disposicion distinta en el chat. Tambien se le asigna
    el icono del mensaje que si es Usuario se usa el de la libreria de lucide-react sino, se usa
    el del bot. Tenemos tambien el contenedor del mensaje, que primero se verifica si es un 
    mensaje de error para mostrarlo distinto en pantalla, luego se verifica si es usuario o bot
    para crear el classname para el css.
  */
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div key={index} className={`message-container ${message.isUser ? 'user' : 'bot'}`}>
          <div className="message-icon">
            {message.isUser ? (
              <User size={24}/>
            ) : (
              <img src={TobiCon} alt="Bot avatar" className="avatar-image-small" />
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