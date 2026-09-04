# My Radar

A personal intelligence system that curates the world around not just who you are, but who you are becoming.

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

A conventional recommender might show more of what you already like. My Radar looks for signals that can:

- strengthen an emerging capability
- connect previously separate fields
- introduce unfamiliar perspectives
- deepen an active curiosity
- support a meaningful intellectual transition

The goal is not simply personal relevance. It is personal evolution.

**My Radar is personalized not around who I am, but around the distance between who I am and who I am becoming.**

## Six Editorial Windows

| # | Section | Purpose |
|---|---------|---------|
| 01 | **World** | Intelligence briefing — what happened |
| 02 | **Think** | Conceptual questions — what idea is worth carrying |
| 03 | **Look** | Aesthetic training — what should train your eye |
| 04 | **Discover** | People to know — who should enter your world |
| 05 | **Explore** | Rabbit holes — where could curiosity take you |
| 06 | **Make** | Situated tools — what could help you create |

## Design Language

- Typography: Fraunces (serif headings) × Inter (body) × SF Mono (metadata)
- Colors: Paper `#F5F2ED`, Burgundy `#993556`, Dark `#1A1A1C`
- Section accents: World `#993556`, Think `#3B5998`, Look `#4A6741`, Discover `#6B4C7A`, Explore `#B07333`, Make `#1A1A1C`
- Principle: Typography IS structure, whitespace IS hierarchy, images ARE visual interruption

## Navigation

Five rails — **Today / Signals / Ideas / Vision / Make** — each scrolls to a content region. Vision covers Look + Discover + Explore.

## Architecture

```
index.html    ← standalone page (inline JSON, works with file://)
feed.json     ← six-section content model
schema.json   ← JSON Schema for feed validation
layout.css    ← editorial CSS system
```

The UI reads JSON only — no AI API calls at runtime. Personalization happens at generation time.

## Running

Open `index.html` directly in a browser. No server required.

## License

MIT
