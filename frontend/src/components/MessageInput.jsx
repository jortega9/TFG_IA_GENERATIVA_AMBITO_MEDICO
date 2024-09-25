import React, { useState } from 'react'
import { Send, User } from 'lucide-react'


// Componente que tiene el input del usuario, se le pasa el handleSendMessage del
// componente Tobichat para manejar los mensajes al llegarle el input
function MessageInput({ onSendMessage }) {
  // Estado que actualiza el input a enviar
  const [input, setInput] = useState('')

  /*
    Se hace trim del input, si no esta vacio se llama a la funcion onSendMessage
    que es la que en el componente TobiChat actualizara la lista de mensajes y llamara
    a la API y vacia el input
  */
  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  /*
    Renderizado: Se define la barra inferior del chat como message-input, la cual tiene
    tres partes. La primera es un icono de usuario el cual es de la libreria de lucide-react
    luego el input que es donde se recibe el mensaje del usuario y se actualiza el estado
    del input y por ultimo el boton de enviar que tambien tiene un icono de la libreria 
    lucide-react.
  */
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