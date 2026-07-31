# Travel Planning Site — Project Context

Consolidated reference for this repo. Read this first in any new conversation instead of
re-explaining the project from scratch. Paste new context from one-off chats into the
**Context Log** section at the bottom rather than losing it.

## What this is

A personal travel-prep site for tracking species (birds + non-birds) expected on a trip,
studying bird ID before the trip, and marking where things were seen on a map. Static
HTML/JS/CSS, no build step, no framework. Data lives in two CSV files that each page
loads client-side via XHR.

Live pages:
- `index.html` — bird species tiles (targets + observed), filterable
- `nonbirds.html` — non-bird species tiles (mammals, reptiles, butterflies, flowers, etc.)
- `flashcards.html` — bird ID flashcard game using photos in `photos/`
- `map.html` — Leaflet map plotting sightings/locations from both CSVs

## File map

| File | Purpose |
|---|---|
| `index.html` | Bird tile browser. Fetches `location.csv`. |
| `nonbirds.html` | Non-bird tile browser. Fetches `nonbirds.csv`. |
| `flashcards.html` | ID quiz game. Fetches `location.csv`, reads `PHOTO_VARIANTS` map for multi-photo species. |
| `map.html` | Leaflet map. Fetches both CSVs, combines into one `SPECIES` array. |
| `location.csv` | Bird data: name, order/family, location, date, rarity, category, etc. (661 lines) |
| `nonbirds.csv` | Non-bird data: `Category, Subcategory, Name, Scientific name, Observed, Site, Obs Count` (816 lines) |
| `add_photos.py` | Utility: moves new photos from `photo_inbox/` into `photos/`, auto-numbers duplicates, rewrites `PHOTO_VARIANTS` in `flashcards.html`. Run locally, not from here (hardcoded `~/Desktop/github/travel-planning` path). |
| `photos/` | ~830 bird photos, named by species slug (`lowercase_with_underscores.jpg`, `_2.jpg`/`_3.jpg` for variants). |
| `photo_inbox/` | Drop zone for new photos before running `add_photos.py`. |
| `travelfav_3.png` | Favicon used by all pages. |

## Data model notes

- `location.csv` header: `Malaysia & Singapore, New, Order, Family, Full Location, Date, ID, Location, Rarity, Fam, Freq, Features, Where, Key, Category 1, Category 2, Category 3, Photo, SGroup, Merlin`
  - `New` = "Yes" means not yet observed (a target); index.html's convention is `New == "no" → observed`.
- `nonbirds.csv` categories currently in use: Lizards, Mammals, Butterflies, Damselflies, Dragonflies, Frogs & Toads, Snakes, Flowers.
- No database, no backend — editing the CSVs directly (or via a script) is how data changes.

## Design system

Shared CSS custom properties across pages (ochre/tan/cream palette, `--ink`, `--header-bg: #4a6e68`, etc.) — keep new pages visually consistent by reusing these tokens rather than inventing new colors. Category tiles use per-category `--c1/--c2/--c3/--cd` color sets (see `nonbirds.html`).

## Workflow

**Adding photos:** drop files in `photo_inbox/` → run `python3 add_photos.py` locally → commit `photos/` + `flashcards.html`.

**Publishing:** this repo's `origin` remote already has push credentials embedded (a GitHub PAT), so commits made from a connected Claude session can be pushed directly with `git push` — no extra auth setup needed. (Worth knowing: that token is currently sitting in plaintext in `.git/config` — fine for a personal project, but don't share this repo's git config, and rotate the token if that ever changes.)

**Typical loop:** update CSV/HTML → `git add -A && git commit -m "..."` → `git push`.

## Open items / TODOs

_(nothing tracked yet — add as they come up)_

## Context Log

_Paste key decisions, preferences, or background from past one-off chats here so future
sessions don't lose them. Newest at top._

- 2026-07-31: Doc created by scanning the repo directly (no prior chat notes were available to pull in yet).
