# Toppform (appen)

Installerbar nettapp på GitHub Pages: https://sebastianfroiland.github.io/toppform/

- Rediger bare `src/app.html`. Kjør så `python3 src/build.py` fra repoets rot, som skriver `index.html`, `sw.js`, `manifest.webmanifest` og `icons/`. Commit både kilden og det bygde resultatet.
- Øk `VERSION` i `src/build.py` ved hver endring, så service workeren henter den nye versjonen.
- Designet er Sebastians liquid glass-pakke (tokens, `.glass`, fanelinje med fjærfysikk, ark). Hold deg til tokenene øverst i stilarket.
- Ingen avhengigheter, ingen byggverktøy utover Python med Pillow (for ikonene).
- Dataene ligger i det private repoet `sebastianfroiland/toppform-data`. Datamodellen står i README-en der. Endrer du formatet, oppdater den også.
- Tekst i appen skrives på norsk bokmål, uten tankestreker.
