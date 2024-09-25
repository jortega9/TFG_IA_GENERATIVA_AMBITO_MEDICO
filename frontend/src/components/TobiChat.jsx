import React, { useState, useEffect } from 'react'
import ThemeToggle from './ThemeToggle'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import TobiCon from '../../public/TobiCon.png'

/*
	TobiChat.jsx
	
	Componente del chat principal, aqui se produce la llamada a la API de Hugging Face y se 
	le envia a los componentes de los mensajes la informacion de la llamada a la API para 
	mostrarlos en pantalla

*/

function TobiChat() {
  // Constante que indica el status OK de la API
  const OK_API = 200
  // Clave que da la autorización a la API
  const API_KEY = "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"
  // Mensaje de error
  const ERROR_MSG = "Error, please refresh!"
  // El array de mensajes que sera actualizado mendiante un estado 
  const [messages, setMessages] = useState([])

  useEffect(() => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      requestNotificationPermission();
    }
  }, []);

  const requestNotificationPermission = async () => {
    try {
      const permission = await Notification.requestPermission();
      if (permission !== 'granted') {
        console.log('Notification permission denied');
      }
    } catch (error) {
      console.error('Error requesting notification permission:', error);
    }
  };

  const sendNotification = (message) => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      navigator.serviceWorker.ready.then((registration) => {
        registration.showNotification('TobiChat', {
          body: message,
          icon: TobiCon,
        }).catch((error) => {console.log(error)});
      });
    }
  };

  /*
    Metodo que actualiza la lista de los mensajes, primero el input del usuario, que se manda el nuevo mensaje
    con isUser a true y luego se hace la llamada a sendMessageToAPI que como su nombre indica envia el input
    a la api, esta respuesta se añade a el array de mensajes.
  */
  const handleSendMessage = async (message) => {
    setMessages(prev => [...prev, { text: message, isUser: true, error: false}])
    
    const response = await sendMessageToAPI(message)
    setMessages(prev => [...prev, { text: response, isUser: false, error: (response == ERROR_MSG ? true : false)}])

    sendNotification(response);
  }

  /*
    query: llamada a la API, hacemos fetch a la API de Hugging Face con nuestra API_KEY autorizada 
    generada por la web de Hugging Face, verificamos que la respose de la API haya sido correcta
    y si lo es, hacemos que la response sea un json que nos dará un array con un json, en ese json
    tiene como unica clave "generated_text" que es la que contiene la respuesta al input que recibe
    la API
  */
	const query = async (data) => {
		const response = await fetch(
			"https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
			{
			headers: {
				Authorization: `Bearer ${API_KEY}`,
				"Content-Type": "application/json",
			},
			method: "POST",
			body: JSON.stringify(data),
			}
		);
    // Si la query no tiene de codigo de salida 200, significa que ha habido un error.
    console.log(response)
		if  (response.status != OK_API) {
        return `${ERROR_MSG}`
    } 
		const result = await response.json()
		return (result[0].generated_text)
	};

  /*
	sendMessageToAPI: metodo que recibe el input del usuario y llama a la API con el mismo para 
  generar una respuesta.
  */
	const sendMessageToAPI = async (message) => {
		return query(message)
	}

  /*
    Tenemos aqui el app container que se divide en el header y en el contenido principal,
    el header solo tiene el titulo de la aplicación y el contenido principal se divide en dos
    secciones, la seccion del avatar que es donde está el icono de la aplicación y luego el chat 
    container que tiene el header del chat donde esta el boton de cambio de modo claro a oscuro,
    luego la lista de los mensajes y la barra inferior con el input.
  */
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>TobiChat</h1>
      </header>
      <div className="main-content">
        <div className="avatar-container">
          <div className="avatar">
            <img src={TobiCon} alt="Bot avatar" className="avatar-image" />
          </div>
        </div>
        <div className="chat-container">
          <div className="chat-header">
            <h2>Chat with me!</h2>
            <ThemeToggle />
          </div>
          <MessageList messages={messages} />
          <MessageInput onSendMessage={handleSendMessage} />
        </div>
      </div>
    </div>
  )
}

export default TobiChat