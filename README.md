# My Radar

A personal intelligence system that curates the world around not just who you are, but who you are becoming.

One issue per day. Six signals max. Six editorial windows. Built to be read in ten minutes.

---

## A Different Model of Personalization

Most personalized systems begin with a simple question:

> What are you interested in?

My Radar starts somewhere else:

> What are you trying to become?

Interests are relatively static. Intellectual development is not.

The system models personalization across four evolving layers:

```
STABLE IDENTITY
  Who are you intellectually?
        ↓
CURRENT CONTEXT
  What are you navigating right now?
        ↓
ACTIVE CURIOSITY
  What is currently pulling your attention?
        ↓
GROWTH EDGES
  What are you trying to become?
```

This changes what the system recommends.

A conventional recommender shows more of what you already like. My Radar looks for signals that can:

- strengthen an emerging capability
- connect previously separate fields
- introduce unfamiliar perspectives
- deepen an active curiosity
- support a meaningful intellectual transition

The goal is not personal relevance. It is personal evolution.

**My Radar is personalized not around who I am, but around the distance between who I am and who I am becoming.**

---

## How an Issue Is Built

The interesting part of this project is not the page. It is the split between what the model decides and what the code guarantees.

```
        ┌──────────────────────────────────────────┐
        │  PROBABILISTIC LAYER  (runs once a day)  │
        │                                          │
        │  read sources → judge relevance → write  │
        │  headlines, chains, why-you, patterns    │
        │                                          │
        │  output: one JSON file. nothing else.    │
        └────────────────────┬─────────────────────┘
                             │  feed.json
                             ▼
        ┌──────────────────────────────────────────┐
        │  DETERMINISTIC LAYER  (always runs)      │
        │                                          │
        │  validate against schema.json            │
        │  → back up previous feed                 │
        │  → check every image URL resolves        │
        │  → render template + feed → index.html   │
        │  → verify output (JS syntax, DOM anchors)│
        │  → roll back if anything fails           │
        └────────────────────┬─────────────────────┘
                             ▼
                      index.html (static)
```

Two reasons for this boundary:

**1. The model should only do what requires judgment.** Picking which paper matters, and writing *why it matters to this specific person*, is judgment. Validating JSON, resolving redirects, and assembling HTML is not. Anything deterministic is moved out of the model's hands, because it can be tested.

**2. A page that breaks is worse than a page that is stale.** Every run validates before it deploys and rolls back on failure. A bad generation leaves yesterday's issue in place instead of an error screen.

Once built, the page is completely static. **There is no AI call at runtime** — personalization happened at generation time, and what ships is a single self-contained HTML file with the feed inlined.

---

## What a Signal Must Contain

Not everything worth reading is worth putting on the radar. A signal is only published if it can answer all of these:

| Field | Question it has to answer |
|---|---|
| `headline` | What is this, in language written for this reader? |
| `chain` | Which two territories does it connect? |
| `why_you` | Why *this* person, *now*? |
| `why_it_matters` | Why should the field care? |
| `suggested_action` | What is one concrete next step? |

A signal that cannot produce a second territory in `chain` is usually just news. It gets dropped.

`signal_type` is one of three:

- **NOW** — it happened
- **LEARN** — it is worth understanding
- **OPPORTUNITY** — you could act on it

---

## Six Editorial Windows

| # | Section | Purpose |
|---|---------|---------|
| 01 | **World** | Intelligence briefing — what happened |
| 02 | **Think** | Conceptual questions — what idea is worth carrying |
| 03 | **Look** | Aesthetic training — what should train your eye |
| 04 | **Discover** | People to know — who should enter your world |
| 05 | **Explore** | Rabbit holes — where could curiosity take you |
| 06 | **Make** | Situated tools — what could help you create |

---

## Repository Layout

```
index.html                          rendered issue — standalone, open with file://
feed.json                           today's content model
schema.json                         JSON Schema the feed is validated against
templates/radar-v4.html             page template with placeholders
pipeline/
  radar-pipeline.py                 validate → back up → render → verify → roll back
  radar-deploy.sh                   thin wrapper: freshness check + logging
data/source-list.json               the sources the radar watches
docs/
  RADAR_INTELLIGENCE_PROTOCOL.md    the editorial rules a generation must follow
  PROFILE_MODEL.md                  how the four personalization layers are modelled
```

`docs/` is where the actual thinking lives. The code is short; the protocol is long.

---

## Design Language

- Typography: Fraunces (serif headings) × Inter (body) × SF Mono (metadata)
- Colors: Paper `#F5F2ED`, Burgundy `#993556`, Dark `#1A1A1C`
- Section accents: World `#993556`, Think `#3B5998`, Look `#4A6741`, Discover `#6B4C7A`, Explore `#B07333`, Make `#1A1A1C`
- Principle: typography IS structure, whitespace IS hierarchy, images ARE visual interruption

## Navigation

Five rails — **Today / Signals / Ideas / Vision / Make** — each scrolls to a content region:

| Rail | Target |
|---|---|
| Today | the greeting and day summary |
| Signals | World |
| Ideas | Think |
| Vision | Look |
| Make | Make |

## Running

Open `index.html` directly in a browser. No server, no build step, no API key.

## Privacy

`feed.json` is published as a record of what the radar surfaced. The personal profile layer that drives selection — identity, grades, gaps, growth edges — is **not** in this repository. `docs/PROFILE_MODEL.md` documents how it is modelled without the contents.

## License

MIT
