# AI-Radar — Personal Intelligence Radar

A daily editorial interface that detects, interprets, and cross-connects meaningful signals across interdisciplinary interests. Not a dashboard. Not a feed. A personal intellectual magazine.

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

## Profile

Built for a Data Science undergraduate at Ca' Foscari Venice, with growth edges in computational thinking, AI systems understanding, interaction design, knowledge building, and interdisciplinary research.

## License

MIT
