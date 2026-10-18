# Toppform

En treningsapp for mobilen med Claude som trener. Logg sett med ett trykk, lag dine egne økter eller tren fritt, ta en kort morgensjekk, og se rekordene dine fra 1RM til lengste løpetur. Hver kveld leser Claude loggen, skriver en kort tilbakemelding og legger inn anbefalt vekt og reps til neste økt.

**Appen:** https://sebastianfroiland.github.io/toppform/

## Slik tar du den i bruk

1. Åpne lenken over i Safari på iPhone (eller Chrome på Android), trykk Del og velg «Legg til på Hjem-skjerm».
2. Åpne appen fra hjemskjermen.
3. Lag et **privat** repo på GitHub til dataene dine, for eksempel `toppform-data`, med en README så det ikke er tomt.
4. Lag en tilgangsnøkkel på github.com/settings/personal-access-tokens/new: velg bare det private repoet og gi Contents tilgangen Read and write.
5. Fyll inn brukernavn, repo og nøkkel i appen. Nøkkelen lagres bare på telefonen din.

Koden i dette repoet er offentlig, men inneholder ingen data. Alt du logger havner i ditt eget private repo.

## Hvordan den er bygget

All kode ligger i `src/app.html`: liquid glass-design, fem faner du kan sveipe mellom, ark som glir opp, og en lagringskø som tåler dårlig dekning. `src/build.py` pakker den inn som en installerbar app (manifest, service worker og ikoner) og skriver resultatet til rota, som GitHub Pages publiserer.

```
python3 src/build.py
```

Appen snakker direkte med GitHub sitt GraphQL-API. Hver endring blir en commit i datarepoet. Hvis noen andre har skrevet i repoet i mellomtiden (for eksempel Claude sin kveldsgjennomgang), henter appen siste versjon og prøver igjen.

Datamodellen er beskrevet i README-en i datarepoet.
