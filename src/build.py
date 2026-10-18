"""Builds the Toppform app for GitHub Pages.

The source is app.html (the page body, the same file that can be published as an artifact in Claude).
This script wraps it in a full HTML document with a manifest and service worker, and draws the icons.

Run from the repo root: python3 src/build.py   (writes index.html, sw.js, the manifest and icons to the root, which GitHub Pages serves)
"""
import json, re, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
DIST = ROOT.parent
VERSION = "4.0.2"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#f2f3f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#07081a" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Toppform">
<meta name="description" content="Training log with Claude as your coach">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<title>Toppform</title>
</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"

SW = """// Toppform service worker: the app opens offline. The GitHub API always goes straight to the network.
const CACHE = 'toppform-__VERSION__';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put('./index.html', c)); return r; }).catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
"""

MANIFEST = {
    "name": "Toppform",
    "short_name": "Toppform",
    "description": "Training log with Claude as your coach",
    "lang": "en",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#07081a",
    "theme_color": "#07081a",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}


def icon(size, inset=0.0):
    """Dark background with the same coloured lights as the app, and a white dumbbell in the middle."""
    S = 1024
    img = Image.new("RGB", (S, S), "#07081a")
    grad = Image.new("RGB", (S, S), "#07081a")
    gd = ImageDraw.Draw(grad)
    for r in range(S, 0, -8):
        t = r / S
        c = tuple(int(a * (1 - t) + b * t) for a, b in zip((0x1b, 0x14, 0x46), (0x07, 0x08, 0x1a)))
        gd.ellipse([S / 2 - r, -r * 0.6, S / 2 + r, r * 1.0], fill=c)
    img.paste(grad)
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse([-150, -150, 520, 520], fill=(107, 107, 255, 200))
    g.ellipse([560, 300, 1180, 920], fill=(0, 201, 173, 170))
    g.ellipse([180, 700, 760, 1220], fill=(255, 95, 168, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    # glass plate
    pad = int(S * (0.2 + inset))
    glass = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gl = ImageDraw.Draw(glass)
    gl.rounded_rectangle([pad, pad, S - pad, S - pad], radius=int((S - 2 * pad) * 0.28), fill=(255, 255, 255, 38), outline=(255, 255, 255, 120), width=6)
    img = Image.alpha_composite(img, glass)
    # dumbbell
    d = ImageDraw.Draw(img)
    cx, cy = S / 2, S / 2
    k = (S - 2 * pad) / 620
    w = (255, 255, 255, 255)
    d.rounded_rectangle([cx - 200 * k, cy - 22 * k, cx + 200 * k, cy + 22 * k], radius=22 * k, fill=w)
    for sgn in (-1, 1):
        x = cx + sgn * 150 * k
        d.rounded_rectangle([x - 34 * k, cy - 140 * k, x + 34 * k, cy + 140 * k], radius=30 * k, fill=w)
        x2 = cx + sgn * 222 * k
        d.rounded_rectangle([x2 - 26 * k, cy - 92 * k, x2 + 26 * k, cy + 92 * k], radius=24 * k, fill=w)
    return img.convert("RGB").resize((size, size), Image.LANCZOS)


def build():
    (DIST / "icons").mkdir(parents=True, exist_ok=True)
    body = (ROOT / "app.html").read_text(encoding="utf-8")
    body = re.sub(r"^<title>.*?</title>\s*", "", body, flags=re.S)
    body = re.sub(r'^<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", body)
    (DIST / "index.html").write_text(HEAD + body + TAIL, encoding="utf-8")
    (DIST / "sw.js").write_text(SW.replace("__VERSION__", VERSION), encoding="utf-8")
    (DIST / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    icon(192).save(DIST / "icons" / "icon-192.png")
    icon(512).save(DIST / "icons" / "icon-512.png")
    icon(512, inset=0.08).save(DIST / "icons" / "icon-maskable-512.png")
    icon(180).save(DIST / "icons" / "apple-touch-icon.png")
    print("Built", VERSION, "to", DIST)


if __name__ == "__main__":
    build()
