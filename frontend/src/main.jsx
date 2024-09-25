import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/Tobichat/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registered succesfully', registration.scope)
      }, (err) => {
        console.log('Service Worker registration failed:', err)
      });
  });
}


