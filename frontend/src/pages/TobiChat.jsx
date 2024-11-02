import React, { useState, useEffect } from 'react';
import ThemeToggle from '../components/ThemeToggle';
import MessageList from '../components/MessageList';
import MessageInput from '../components/MessageInput';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import AppHeader from '../components/AppHeader';
import ChatList from '../components/ChatList';
import ChatWelcome from '../components/ChatWelcome';
import '../styles/TobiChat.css';

function TobiChat() {
  const OK_API = 200;
  const API_KEY = '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';
  const ERROR_MSG = 'Error, please refresh!';
  
  // Estado que guarda la lista de chats
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(0);

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
          icon: AsistenteIcon,
        }).catch((error) => { console.log(error); });
      });
    }
  };

  const handleSendMessage = async (message) => {
    setChats((prevChats) =>
      prevChats.map((chat) => 
        chat.id === activeChatId 
          ? { ...chat, messages: [...chat.messages, { text: message, isUser: true, error: false }] } 
          : chat
      )
    );

    const response = await sendMessageToAPI(message);

    setChats((prevChats) =>
      prevChats.map((chat) => 
        chat.id === activeChatId 
          ? { ...chat, messages: [...chat.messages, { text: response, isUser: false, error: response === ERROR_MSG }] }
          : chat
      )
    );

    sendNotification(response);
  };

  const query = async (data) => {
    const response = await fetch(
      'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill',
      {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify(data),
      }
    );

    if (response.status !== OK_API) {
      return `${ERROR_MSG}`;
    }
    const result = await response.json();
    return result[0].generated_text;
  };

  const sendMessageToAPI = async (message) => {
    return query(message);
  };

  const handleSelectChat = (chatId) => {
    setActiveChatId(chatId);
  };

  return (
    <div className="app-container">
      <AppHeader />
      <div className="main-content">
        <div className="menu-container">
          <ChatList chats={chats} setChats={setChats} onSelectChat={handleSelectChat} />
        </div>
        {activeChatId !== 0 ? (
          <div className="chat-container">
            <div className="chat-header">
              <h2>Chat with me!</h2>
              <ThemeToggle />
            </div>
            <MessageList messages={chats.find(chat => chat.id === activeChatId)?.messages || []} />
            <MessageInput onSendMessage={handleSendMessage} />
          </div>
        ) : <ChatWelcome/> }
      </div>
    </div>
  );
}

export default TobiChat;
