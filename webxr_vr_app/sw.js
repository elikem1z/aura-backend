// Simple service worker to prevent 404 errors
// This is a placeholder service worker for the WebXR app

self.addEventListener('install', function(event) {
    console.log('Service Worker installed');
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker activated');
});

self.addEventListener('fetch', function(event) {
    // Simple pass-through for now
    event.respondWith(fetch(event.request));
}); 