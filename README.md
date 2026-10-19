# Plates

A training app for your phone with Claude as your coach. Log a set with one tap, build your own workouts and keep them in folders or just train freely, do a quick morning check-in, and see your records from 1RM to your longest run. Every evening Claude reads the log, writes a short review and sets a recommended weight and rep target for your next workout.

**The app:** https://sebastianfroiland.github.io/toppform/

## Getting started

1. Open the link above in Safari on iPhone (or Chrome on Android), tap Share and choose Add to Home Screen.
2. Open the app from your home screen.
3. Create a **private** repo on GitHub for your data, for example `toppform-data`, with a README so it isn't empty.
4. Create an access token at github.com/settings/personal-access-tokens/new: select only that private repo and give Contents Read and write access.
5. Enter your username, repo and token in the app. The token is stored only on your phone.

The code in this repo is public but holds no data. Everything you log ends up in your own private repo.

## How it's built

All the code is in `src/app.html`: the liquid glass design, five pages you can swipe between, sheets that slide up, and a save queue that copes with bad reception. `src/build.py` wraps it as an installable app (manifest, service worker and icons) and writes the result to the root, which GitHub Pages serves.

```
python3 src/build.py
```

The app talks directly to GitHub's GraphQL API. Every change becomes a commit in the data repo. If something else has written to the repo in the meantime (for example Claude's evening review), the app fetches the latest version and tries again.

The data model is described in the README of the data repo.
