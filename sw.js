const CACHE_NAME = 'worldcup-cache-v1';
const FILES_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './worldcup_icon.png',
  './worldcup_opengraph.png',
  // 필요하면 CSS/JS 경로도 추가
];

self.addEventListener('install', evt => {
  evt.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(FILES_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', evt => {
  evt.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', evt => {
  if (evt.request.mode !== 'navigate') {
    evt.respondWith(
      fetch(evt.request)
        .then(resp => {
          caches.open(CACHE_NAME).then(cache => cache.put(evt.request, resp.clone()));
          return resp;
        })
        .catch(() => caches.match(evt.request))
    );
    return;
  }
  evt.respondWith(
    caches.match(evt.request).then(resp => resp || fetch(evt.request))
  );
});
