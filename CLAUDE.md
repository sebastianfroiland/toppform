# Plates (the app, formerly Toppform)

Installable web app on GitHub Pages: https://sebastianfroiland.github.io/toppform/

- Edit only `src/app.html`. Then run `python3 src/build.py` from the repo root, which writes `index.html`, `sw.js`, `manifest.webmanifest` and `icons/`. Commit both the source and the built output.
- Bump `VERSION` in `src/build.py` on every change so the service worker picks up the new version.
- The design is built on Sebastian's liquid glass kit (tokens, `.glass`, spring physics tab bar, sheets), but the app always shows the calm Claude look (the Paper tokens: warm surfaces, serif headings, clay accent). Sebastian asked to drop the liquid glass options, so do not bring them back. Stick to the tokens at the top of the stylesheet.
- No dependencies and no build tools beyond Python with Pillow (for the icons).
- The data lives in the private repo `sebastianfroiland/toppform-data`. The data model is in the README there. If you change the format, update it too.
- App text is English, short, with no dashes in sentences. Avoid explanatory blurbs under headings; the UI should speak for itself.
- iPhone details that matter: inputs are at least 16 px (no focus zoom), pinch zoom is off (`touch-action: pan-x pan-y` and the viewport meta), `--gap` covers the strip iOS sometimes leaves under a home screen app, and the page scroll is reset after the keyboard closes.
- Test locally only on a fresh origin (its own port) seeded with fake data, and never on a page Sebastian has connected to GitHub: a connected page uploads everything stored in it, and test data once overwrote his real workouts, plan and settings this way.
- Workout, Log, Body, Records and every flashcard must fit the screen exactly with no scrolling. `syncFit` and `fitBox` handle it: a box that is too tall hides tips (`snug`), then gets compact spacing (`tight`), then scales down to at least 80 percent. Put new content inside that system (a `.grow` part that can shrink, tips as `.hint`) instead of fixed heights. Sebastian uses an iPhone 14, so test at 390x763 first.
- Before pushing, run the app as several kinds of users (random trainer, structured user with history, cardio only, new user on a small phone with large text, offline) and check for overflow and console errors.
