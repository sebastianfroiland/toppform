# Toppform (the app)

Installable web app on GitHub Pages: https://sebastianfroiland.github.io/toppform/

- Edit only `src/app.html`. Then run `python3 src/build.py` from the repo root, which writes `index.html`, `sw.js`, `manifest.webmanifest` and `icons/`. Commit both the source and the built output.
- Bump `VERSION` in `src/build.py` on every change so the service worker picks up the new version.
- The design is Sebastian's liquid glass kit (tokens, `.glass`, spring physics tab bar, sheets). Stick to the tokens at the top of the stylesheet.
- No dependencies and no build tools beyond Python with Pillow (for the icons).
- The data lives in the private repo `sebastianfroiland/toppform-data`. The data model is in the README there. If you change the format, update it too.
- App text is English, short, with no dashes in sentences. Avoid explanatory blurbs under headings; the UI should speak for itself.
- iPhone details that matter: inputs are at least 16 px (no focus zoom), pinch zoom is off (`touch-action: pan-x pan-y` and the viewport meta), `--gap` covers the strip iOS sometimes leaves under a home screen app, and the page scroll is reset after the keyboard closes.
- Before pushing, run the app as several kinds of users (random trainer, structured user with history, cardio only, new user on a small phone with large text, offline) and check for overflow and console errors.
