import React, { useState, useEffect } from 'react';
import ThemeToggle from '../components/ThemeToggle';
import MessageList from '../components/MessageList';
import MessageInput from '../components/MessageInput';
import AsistenteIcon from '../../public/assets/AsistenteIcon.png';
import AppHeader from '../components/AppHeader';
import Controls from '../components/Controls/Controls';
import ChatWelcome from '../components/ChatWelcome';
import Report from '../components/Report/Report';
import '../styles/Urolobot.css';
import { Grid } from '@mui/material';

function Urolobot() {
  const OK_API = 200;
  const API_KEY = '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';
  const ERROR_MSG = 'Error, please refresh!';

  const [messages, setMessages] = useState([]);
  const [isChatAccessible, setIsChatAccessible] = useState(false);
  const [isReportAccessible, setIsReportAccessible] = useState(false);

  const handleChatAccessChange = (isAccessible) => {
    setIsChatAccessible(isAccessible);
  };

  const handleReportAccessChange = (isAccessible) => {
    setIsReportAccessible(isAccessible);
  };

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
        registration.showNotification('Urolobot', {
          body: message,
          icon: AsistenteIcon,
        }).catch((error) => { console.log(error); });
      });
    }
  };

  const handleSendMessage = async (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, isUser: true, error: false },
    ]);

    const response = await sendMessageToAPI(message);

    setMessages((prevMessages) => [
      ...prevMessages,
      { text: response, isUser: false, error: response === ERROR_MSG },
    ]);

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
    return query({ inputs: message });
  };

  return (
    <div className="app-container">
        <AppHeader />
      <div className="main-content" style={{ display: 'flex', height: '100%' }}>
        <div className="controls-section" style={{ width: '15%' }}>
          <Controls onChatAccessChange={handleChatAccessChange} onReportAccessChange={handleReportAccessChange} />
        </div>
        <div className="content-section" style={{ width: '80%' }}>
          {isChatAccessible ? (
            <div className="chat-container">
              <div className="chat-header">
                <h2>Chat with me!</h2>
                <ThemeToggle />
              </div>
              <MessageList messages={messages} />
              <MessageInput onSendMessage={handleSendMessage} />
            </div>
          ) : isReportAccessible ? (
            <div >
              <Report />
            </div>
          ) : (
            <ChatWelcome />
          )}
        </div>
      </div>
    </div>
  );
}

export default Urolobot;
