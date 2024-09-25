const CACHE_NAME = 'tobichat-cache-v1';

const urlsToCache = [
    '/',
    '/Tobichat/index.html',
    '/Tobichat/TobiCon.png',        
    '/Tobichat/src/styles/chat.css', 
    '/Tobichat/src/main.jsx',        
    '/Tobichat/src/components/MessageInput.jsx',
    '/Tobichat/src/components/MessageList.jsx',
    '/Tobichat/src/components/ThemeContext.jsx',
    '/Tobichat/src/components/ThemeToggle.jsx',
    '/Tobichat/src/components/TobiChat.jsx',
    '/Tobichat/src/App.jsx'
];


self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response; 
                }
                return fetch(event.request); 
            })
    );
});


self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

/*
self.addEventListener('push', (event) => {
	const options = {
	  body: event.data.text(),
	  icon: '/TobiCon.png',
	  badge: '/TobiCon.png'
	};
  
	event.waitUntil(
	  self.registration.showNotification('TobiChat', options)
	);
});

self.addEventListener('notificationclick', (event) => {
	event.notification.close();
	
	event.waitUntil(
	  clients.openWindow('/')
	);
	
});
*/

self.addEventListener('push', function(event) {
	console.log('push');
	const options = {
	  body: event.data.text(),
	  icon: '/TobiCon.png',
	  badge: '/TobiCon.png',
	  data: { url: 'https://miguelamato.github.io/Tobichat/' } // The URL of the page that triggered the notification
	};
  
	event.waitUntil(
	  self.registration.showNotification('Tobichat', options)
	);
  });
  
  self.addEventListener('notificationclick', function(event) {
	event.notification.close(); // Close the notification
  
	event.waitUntil(
	  clients.matchAll({
		type: 'window',
		includeUncontrolled: true // Include uncontrolled clients if needed
	  }).then(function(clientList) {
		for (let i = 0; i < clientList.length; i++) {
		  const client = clientList[i];
		  // Check if the page is already open by matching the URL
		  if (client.url === event.notification.data.url && 'focus' in client) {
			return client.focus(); // Focus the existing page
		  }
		}
		// If the page is not open, open a new one
		if (clients.openWindow) {
		  return clients.openWindow(event.notification.data.url);
		}
	  })
	);
  });