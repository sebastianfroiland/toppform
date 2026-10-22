# Plates app (repo `toppform`, public)

Installable web app on GitHub Pages: https://sebastianfroiland.github.io/toppform/. The whole app is one file, `src/app.html` (HTML, CSS and JS, about 6,000 lines, no dependencies). The workspace around this repo (data repo, evening review, tests, art, planning) is described in `../CLAUDE.md`.

## Build and ship

- Edit only `src/app.html`, and the images in `art/` (made in `../art-source/`). Then run `python3 src/build.py` from the repo root, which writes `index.html`, `sw.js` (its offline cache lists every `art/*.webp`), `manifest.webmanifest`, `.nojekyll` and `icons/`. Never edit those outputs by hand.
- Bump `VERSION` in `src/build.py` on every change so the service worker picks up the new version.
- Commit both the source and the built output, as two commits: `Plates X.Y.Z (source): what changed` and `Plates X.Y.Z (build)`.
- Push only when Sebastian says so: a push to `main` is live on his phone.
- No dependencies and no build tools beyond Python with Pillow (for the icons). This Mac's Python 3.9 has no Pillow; the build then keeps the committed icons, which is fine unless `icon()` changed.
- `haptics.html` in the repo root is a test page with six kinds of slider, to find out on the phone whether any of them can tick during a drag.
- The data lives in the private repo `sebastianfroiland/toppform-data`. The data model is in the README there. If you change the format, update it too (and `../new-user-setup/data-README.md`).

## Map of `src/app.html`

Line numbers are from 4.34.0 and drift. Jump with `grep -n '^/\* ---------- ' src/app.html` (the section banners) or by function name.

| Line | Section | What is there |
|---|---|---|
| 1 | head | `<title>`, and a script that puts the saved look (`tl.look`) on the page before it paints |
| 11 | CSS | Tokens in `:root` at the top (the Paper look), then base, background lights, glass, swipeable pages, Progress switch, tab bar, sidebar, settings, buttons, sheets, toast, page parts |
| 1476 | markup | sidebar `#side`, pager `#pager` with the five pages, workout deck `#deck`/`#cards`, rest pill `#rest`, tab bar `#dock`, sheet `#sheet`, settings `#setModal` |
| 1596 | Liquid Glass | `window.LiquidGlass`: springs, tab bar, sheet, toast, haptic (changed copy of `../liquid-glass/liquid-glass.js`) |
| 1722 | app start | one IIFE to the end of the file. `LIB` (exercise library: name, muscle slot, compound or isolation), `SLOTS`, labels |
| 1765 | helpers | `esc`, `num`, dates (`todayISO`, `dLong`, `fShort`), `toast`, `haptic`, `setHTML` |
| 1832 | state | `S` (all state), `D` (the data collections), `normDoc`, `derive`, `recFor`, `activeSession`, `suggested` |
| 1980 | appearance | `applyLook`, `fixGap` |
| 2019 | storage | the save queue (`queue`, `flush`, `savePending`), GitHub GraphQL (`gql`, `ghLoad`, `ghFlush`, `ghStart`, `ghConnect`), phone-only mode |
| 2243 | start-up and pages | `routeHash`, `setView`, `selectTab`, `init` |
| 2317 | rendering | `PAGES`, error boundary (`guard`, `paintPage`), fit (`fitBox`, `syncFit`, `fitCards`), `refresh`, Connect screen, `renderToday` |
| 2526 | workout | `renderWorkout`, exercise cards (`buildCard`, `fillCard`, `REST_BOX`), `logSet`, skips, warm-ups (`buildWarm`, `paceVs`), cardio timer and plans (`isCardioS`) |
| 3021 | cards view | the flashcard deck (`renderDeck`, `deckGo`), `finish`, past workouts |
| 3153 | log | `renderLog` (calendar) |
| 3194 | records, charts | PRs (`strengthPRs`, `cardioPRs`), curves (`curveHtml`, `scrubCurve`) |
| 3348 | progress | the longest section. Body (`renderBody`, `periodWeeks`, muscle figure `figureSvg`), goals (`renderGoals`, `openGoal`), coaches (`TRAINERS`, `coach`, `coachPick`, `GN`, `PALS`, `gnTick`), onboarding (`renderOb`), Food (`renderFood`, `foodRing`, `openFoodHelp`, camera `openCam`, hand calibration), lift card and pins (`renderLiftCard`, `lcPins`), `renderProgress`, `renderRecords` |
| 4450 | coach messages | threads (`threadHtml`, `sendMsg`), the coach card on Today (`renderCoach`), earlier reviews (`openReviews`) |
| 4624 | rest timer | `startRest`, `paintRestBoxes`, rest alert, lock screen card |
| 4736 | sheets | `openSheet`, exercise library (`openLib`), workouts and folders, check-in, cardio log, history |
| 4968 | sidebar, Social | `renderSide`, `soSamples`, `SO_GROUPS`, `TIERS` |
| 5198 | settings | `renderSettings`, feedback, exercise preferences (`renderXP`), `UPDATES` (the changelog in Settings, Updates), CSV export |
| 5424 | sliders | `paintRange`, `rangeNudge`, drag |
| 5523 | exercise notes | `openNotes`, `notesHtml`, `openSetEdit` |
| 5608 | 1RM test | `renderRmCard`, `startRm` |
| 5664 | events | one click handler for the whole app: every button has `data-a="name"` and a `case 'name'` here. Then `saveSettings` and the keyboard (`typingField`, `body.kb`) |

## Rules

- Test locally only on a fresh origin (its own port) seeded with fake data, and never on a page Sebastian has connected to GitHub: a connected page uploads everything stored in it, and test data once overwrote his real workouts, plan and settings this way. `../testing/` does this for you.
- The design is built on Sebastian's liquid glass kit (tokens, `.glass`, spring physics tab bar, sheets), but the app always shows the calm Paper look (warm surfaces, serif headings, clay accent). Sebastian asked to drop the liquid glass options, so do not bring them back. Stick to the tokens at the top of the stylesheet.
- App text is English, short, with no dashes in sentences. Avoid explanatory blurbs under headings; the UI should speak for itself.
- The app never says Claude to the user: Today, messages, food and toasts use the picked coach (`coach()`); the app feedback thread answers as Plates.
- No supersets, ever: Sebastian does not like them. The coaching rules in the data repo forbid them, and `hintOf` hides any hint that asks for one.
- Food is photo only: no typed foods or calories. Meals are saved as `status: "pending"` and the evening review analyses them, using `meta.hand` as the ruler. Keep the analysis behind the pending status so a model on the phone can replace the review later without changing the page.
- Workout, Log, Body, Records and every flashcard must fit the screen exactly with no scrolling (see Fit below).

## Testing

- Sebastian uses an iPhone 14, so test at 390x763 first, then a small phone at 375x627.
- Before pushing, run the app as several kinds of users (random trainer, structured user with history, cardio only, new user on a small phone with large text, offline) and check for overflow and console errors. The personas in `../testing/` match these.
- iPhone details that matter: inputs are at least 16 px (no focus zoom), pinch zoom is off (`touch-action: pan-x pan-y` and the viewport meta), `--gap` covers the strip iOS sometimes leaves under a home screen app, and the page scroll is reset after the keyboard closes.

## Fit and speed

- `syncFit` and `fitBox` make pages fit: a box that is too tall hides tips (`snug`), then gets compact spacing (`tight`), then scales down to at least 80 percent. Put new content inside that system (a `.grow` part that can shrink, tips as `.hint`) instead of fixed heights.
- Fitting is the slow part of a render. `fitCards` only fits the card you look at and its neighbours, and only when the card's content or the space changed (`el._fit`), so keep that check when you add to a card. Motion that runs while the fit check measures must be opacity only, since a moving box measures taller than it is.
- The tab bar hides only while you type (`body.kb`). `typingField` must match real text fields only: the hidden switches that make the iPhone tick are checkboxes, and counting them once hid the tab bar at random. The bars also sit in their own layers (`will-change`, `backface-visibility`).

## How the pages work

### Today and the coaches

- The coaches are Gentle Gunnar (`guide`, new to the gym), Iron Ingrid (`builder`, training for a while) and Bulky Bjørn (`elite`, the experts, a gym bro) in `TRAINERS`, from least to most direct. Their voices (personality, word limits and examples) are in the data README under Trainers, and the evening review writes as the picked coach, never as Claude. The app uses `coach()`, with `name`, `short` and `coachAv` for the round face cut from the portrait by `face`.
- `coachPick` shows them as three equal boxes in the welcome steps and in Settings, Coach; the one you tap grows and squeezes the other two. On an iPhone 14 the welcome step fits with no scroll; on a smaller screen the sheet scrolls rather than cutting the open box's text.
- A portrait is `art/coach-<name>.webp`, 840 px tall, cut from `../art-source/<name>.png` (how each was made: `../art-source/README.md`). `ar` is the portrait's size, and `fk` shrinks a wide one (Bjørn) so his shoulders fit the picture column. A coach without one shows a silhouette.
- Gunnar is alive in the picker (`GN`, `gnTick`): while his box is open he breathes with his eyes closed, three painted butterflies drift round him, and now and then one lands on his nose and he sniffs it. A tap makes him hop; the butterflies fly off and come back one by one. His eyes stay closed and there is no hand or arm motion: Sebastian tried open eyes and a wave and liked him best calm, as painted (`coach-gunnar.webp`). The sniff uses the separate `scale` property so it never fights the breathing and hop on `transform`, and his position is read a few times a second, not every frame. Butterfly wings are HTML layers that turn in 3D (CSS keyframes), with glides and slow folding while they sit. His picture comes from `../art-source/gunnar-wave/lag_oyne.py` (the wave and eye attempts are kept there and in `older/`). It runs only while his open box is on screen, and not with reduced motion.
- Ingrid and Bjørn are alive the same way, set in `PALS` (how many, where one sits, the orbit, springs and the coach's reaction): two dragonflies dart and hover round Ingrid and one lands on her bun so she leans (`rotate`), and two bumblebees bumble round Bjørn and one settles on his biceps so he puffs up (`scale`).
- Purple, the old mascot, was taken out of the app in 4.34.0 at Sebastian's request; his art is kept in `../art-source/` in case he comes back. Keep the painted style with dark green outlines for the coaches.

### Workout

- Exercise cards start on the recommended weight, reps and RIR (`recFor`: today's target from the coach, else the next step from last time) with no tips and no Target box. Reset appears by the RIR label once you change the numbers and puts them back, for that card's next set only.
- How was it, the note and earlier notes live behind the bubble in each card's header (`openNotes`), never on the card itself, so the whole card always fits; Settings, Notes lists every note and rating by exercise (`notesHtml`).
- The rest lives on each exercise card (`REST_BOX`, `paintRestBoxes`): it waits with the planned time and starts by itself on Log set, with the time, a bar, sound and stop. With flashcards the rest bar at the bottom stays hidden so the card gets the room; in the list view the bar shows as before (`body.resting`).
- A warm-up has no timer: you type the time and distance from the machine, it shows the pace and how it compares with the last time (`paceVs`), you rate it Easy, Good or Hard (`effort`), then Done or Not done. Time and distance follow the Weight and reps setting, so with Slide they get the same sliders as the exercises (a time slider is in seconds and shows m:ss). Cardio cards keep their timer.
- Sliders: the weight slider moves in half kilos. A tap beside the marker moves it one step (`rangeNudge`), and that tap is what makes the iPhone tick: since iOS 26.5 a web page cannot tick while a finger drags, so a drag only ticks once when you let go.
- A tap on a logged set (on its card, or in a past workout in Log) opens it to change the weight, reps and RIR or to delete it (`openSetEdit`); the later sets move up so the numbers stay 1, 2, 3.

### Food

- The Food page is a week strip (tap a day, arrows move a week), one card with a calorie ring split by protein, carbs and fat (`foodRing`) and the macros beside it, the Snap-a-meal button with a question mark for the guide (`openFoodHelp`, also shown before the very first photo), and the meals with their calories on the right. Keep it that calm: no extra cards or explanations on the page.

### Progress

- Progress has a Records and Body switch under its title. Records is the goals card (a ring per goal, a dashed slot for each kind not set; a tap opens the goal with Now, Goal and its curve) and the lift card (chips that scroll sideways, goal lifts first with a small ring mark, then the pinned or most used lifts; the curve fills the card and shows a dashed goal line when the goal is close enough).
- Body is a period switch, three numbers (workouts, sets, sleep), the muscle figure and body weight. Charts take one point a day, and a single point shows as a dot, so the page looks right from the first workout. Weekly rates count from the first workout, not the start of the period (`periodWeeks`).

### Social

- Social (the side panel) shows Sebastian's own workouts and posts plus sample athletes and groups built into the app (`soSamples`, `SO_GROUPS`), clearly marked Sample. There is no shared server yet. Social actions start with `so-` so they keep the panel open.

## Ideas

Whenever Sebastian mentions an idea for the app (even in passing), add it at the top of "Nye" in `../docs/IDEER.md` as `- [ ] YYYY-MM-DD · idea` in his words (Norwegian), without asking. Tick it and move it to "Gjort" when it is built or moved into `../docs/LAUNCH.md`.
