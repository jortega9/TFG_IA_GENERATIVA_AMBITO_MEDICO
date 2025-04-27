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
  const API_KEY = "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";
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

  const sendMessageToAPI = async (message) => {
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: "gpt-4o",
          messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: message }
          ],
          temperature: 0.7,
          max_tokens: 1000
        })
      });

      if (response.status !== OK_API) {
        console.error("OpenAI API error", await response.text());
        return ERROR_MSG;
      }

      const result = await response.json();
      const reply = result.choices[0].message.content.trim();
      return reply;
    } catch (error) {
      console.error('Error sending message to API:', error);
      return ERROR_MSG;
    }
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
            <div>
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
