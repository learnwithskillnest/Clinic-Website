/* Smile & Glow service worker.
   Pages: network first, so visitors always get the latest version when online; cached copy only when offline.
   CSS and JS: network first too. Fonts and images: from cache, refreshed in the background. */
const VERSION = "sg-2026-10-27";
const CORE = ["/", "/hi/", "/dental-emergency/", "/hi/dental-emergency/", "/assets/site.css", "/assets/chat.js?v=4",
  "/assets/img/logo-sm.webp", "/assets/fonts/mukta-latin-400.woff2", "/assets/fonts/mukta-latin-600.woff2", "/assets/fonts/playfair-latin-600.woff2"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;      // maps, WhatsApp etc. go straight to the network
  if (req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html")) {
    e.respondWith(fetch(req).then(res => {
      const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); return res;
    }).catch(() => caches.match(req).then(r => r || caches.match(url.pathname.startsWith("/hi/") ? "/hi/" : "/"))));
    return;
  }
  if (!/\.(woff2|webp|png|jpg|ico|svg)$/.test(url.pathname)) {            // CSS / JS: latest when online
    e.respondWith(fetch(req).then(res => { if (res.ok) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); } return res; })
      .catch(() => caches.match(req)));
    return;
  }
  e.respondWith(caches.match(req).then(hit => {
    const net = fetch(req).then(res => { if (res.ok) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); } return res; });
    return hit || net;
  }));
});
