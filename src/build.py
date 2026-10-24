"""Builds the Plates app (formerly Toppform) for GitHub Pages.

The source is app.html (the page body). The images live in art/ at the repo root, where the page loads them from.
This script wraps the page in a full HTML document with a manifest and service worker, and draws the icons.

Run from the repo root: python3 src/build.py   (writes index.html, sw.js, the manifest and icons to the root, which GitHub Pages serves)
The icons need Pillow. Without it the build keeps the committed icons, which only change when icon() does.
"""
import json, random, re
from pathlib import Path
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None

ROOT = Path(__file__).parent
DIST = ROOT.parent
VERSION = "4.37.0"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#f5f4ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#262624" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Plates">
<meta name="description" content="Training log with a coach who reads it every evening">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<title>Plates</title>
</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"

SW = """// Plates service worker: the app opens offline. The GitHub API always goes straight to the network.
const CACHE = 'toppform-__VERSION__';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png', __ART__];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request.url, {cache: 'no-cache', credentials: 'same-origin'}).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put('./index.html', c)); return r; }).catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
// Tapping the rest alert or the lock screen card brings the app back to the front
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(clients.matchAll({type: 'window', includeUncontrolled: true}).then(cs => cs.length ? cs[0].focus() : clients.openWindow('./#workout')));
});
"""

MANIFEST = {
    "name": "Plates",
    "short_name": "Plates",
    "description": "Training log with a coach who reads it every evening",
    "lang": "en",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#262624",
    "theme_color": "#262624",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}


def icon(size, inset=0.0):
    """Plates: three weight plates screen printed on terracotta. Flat colour, an ink layer printed a little off
    register under the cream layer, and nothing glossy, so it looks made by hand rather than generated."""
    S = 1024
    terracotta, ink, cream = (198, 91, 59), (31, 27, 22), (243, 233, 214)
    img = Image.new("RGB", (S, S), terracotta)
    d = ImageDraw.Draw(img)
    k = S / 120 * (1 - inset * 1.6)
    ox = oy = S / 2 - 60 * k
    P = lambda x, y: (ox + x * k, oy + y * k)
    plates = [(45, 62, 23), (66, 55, 23), (80, 69, 17)]
    w = round(5 * k)
    def ring(cx, cy, r, colour):
        x, y = P(cx, cy)
        d.ellipse([x - r * k, y - r * k, x + r * k, y + r * k], outline=colour, width=w)
    def disc(cx, cy, r, colour):
        x, y = P(cx, cy)
        d.ellipse([x - r * k, y - r * k, x + r * k, y + r * k], fill=colour)
    # back to front, each plate covering the one behind it
    for cx, cy, r in plates:
        disc(cx, cy, r + 2.5, terracotta)
        ring(cx + 1.2, cy + 1.6, r, ink)
        ring(cx, cy, r, cream)
        disc(cx + .8, cy + 1, 5.2, ink)
        disc(cx, cy, 4.6, cream)
    # a light print grain, so the flat colour is not perfectly flat
    rnd = random.Random(7)
    grain = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g = ImageDraw.Draw(grain)
    for _ in range(9000):
        x, y = rnd.randrange(S), rnd.randrange(S)
        g.point((x, y), fill=(255, 255, 255, rnd.randrange(10, 26)) if rnd.random() < .5 else (0, 0, 0, rnd.randrange(10, 22)))
    img = Image.alpha_composite(img.convert("RGBA"), grain)
    return img.convert("RGB").resize((size, size), Image.LANCZOS)


def build():
    (DIST / "icons").mkdir(parents=True, exist_ok=True)
    art = sorted((DIST / "art").glob("*.webp"))   # the coach portraits and Purple's parts, cached for offline use
    body = (ROOT / "app.html").read_text(encoding="utf-8")
    body = re.sub(r"^<title>.*?</title>\s*", "", body, flags=re.S)
    (DIST / "index.html").write_text(HEAD + body + TAIL, encoding="utf-8")
    (DIST / "sw.js").write_text(SW.replace("__VERSION__", VERSION).replace("__ART__", ", ".join("'./art/" + f.name + "'" for f in art)), encoding="utf-8")
    (DIST / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    if Image:
        icon(192).save(DIST / "icons" / "icon-192.png")
        icon(512).save(DIST / "icons" / "icon-512.png")
        icon(512, inset=0.08).save(DIST / "icons" / "icon-maskable-512.png")
        icon(180).save(DIST / "icons" / "apple-touch-icon.png")
    else:
        print("Pillow is missing, so the icons were left as they are (pip3 install pillow to draw them)")
    print("Built", VERSION, "to", DIST)


if __name__ == "__main__":
    build()
