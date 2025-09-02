// Service Worker for React Field Insights PWA
// Provides offline capability and performance optimization

const CACHE_NAME = 'field-insights-v1'
const STATIC_CACHE = 'field-insights-static-v1'
const RUNTIME_CACHE = 'field-insights-runtime-v1'

// Files to cache for offline functionality
const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/css/',
  '/static/js/',
  // Add specific assets as needed
]

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Service Worker')
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Caching static files')
        return cache.addAll(STATIC_FILES.filter(url => url !== '/static/css/' && url !== '/static/js/'))
      })
      .then(() => {
        console.log('[SW] Static files cached')
        return self.skipWaiting()
      })
      .catch((error) => {
        console.error('[SW] Failed to cache static files:', error)
      })
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker')
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => {
              return cacheName !== STATIC_CACHE && 
                     cacheName !== RUNTIME_CACHE &&
                     cacheName !== CACHE_NAME
            })
            .map((cacheName) => {
              console.log('[SW] Deleting old cache:', cacheName)
              return caches.delete(cacheName)
            })
        )
      })
      .then(() => {
        console.log('[SW] Service Worker activated')
        return self.clients.claim()
      })
  )
})

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return
  }

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return
  }

  // Handle API requests with network-first strategy
  if (url.pathname.startsWith('/v1/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful API responses for offline access
          if (response.ok && request.url.includes('/product-lines')) {
            const responseClone = response.clone()
            caches.open(RUNTIME_CACHE)
              .then((cache) => cache.put(request, responseClone))
          }
          return response
        })
        .catch(() => {
          // Return cached data if network fails
          return caches.match(request)
            .then((cachedResponse) => {
              if (cachedResponse) {
                return cachedResponse
              }
              // Return offline page for critical API endpoints
              if (request.url.includes('/product-lines')) {
                return new Response(
                  JSON.stringify([
                    { id: 'offline', name: 'Modalità Offline - Connettiti per aggiornare' }
                  ]),
                  { 
                    headers: { 'Content-Type': 'application/json' },
                    status: 200 
                  }
                )
              }
              throw new Error('Network error and no cache available')
            })
        })
    )
    return
  }

  // Handle static assets with cache-first strategy
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse
        }

        return fetch(request)
          .then((response) => {
            // Cache successful responses
            if (response.ok) {
              const responseClone = response.clone()
              caches.open(RUNTIME_CACHE)
                .then((cache) => cache.put(request, responseClone))
            }
            return response
          })
          .catch(() => {
            // Return offline fallback for navigation requests
            if (request.mode === 'navigate') {
              return caches.match('/index.html')
            }
            throw new Error('Network error and no cache available')
          })
      })
  )
})

// Background sync for failed uploads
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-insight-sync') {
    console.log('[SW] Background sync triggered for insights')
    event.waitUntil(
      // Retry failed insight uploads
      retryFailedUploads()
    )
  }
})

// Handle failed uploads
async function retryFailedUploads() {
  try {
    // Get failed uploads from IndexedDB if implemented
    console.log('[SW] Retrying failed uploads...')
    // Implementation would go here for offline queue
  } catch (error) {
    console.error('[SW] Failed to retry uploads:', error)
  }
}

// Push notifications (optional)
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json()
    
    const options = {
      body: data.body || 'Nuovo aggiornamento disponibile',
      icon: '/icon-192.png',
      badge: '/icon-192.png',
      vibrate: [200, 100, 200],
      data: data.data || {},
      actions: [
        {
          action: 'open',
          title: 'Apri App'
        },
        {
          action: 'close',
          title: 'Chiudi'
        }
      ]
    }

    event.waitUntil(
      self.registration.showNotification(data.title || 'Field Insights', options)
    )
  }
})

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close()

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.openWindow('/')
    )
  }
})

console.log('[SW] Service Worker loaded successfully')

