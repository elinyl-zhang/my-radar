# AI-Radar Intelligence Protocol

> **Version:** 1.0-draft
> **Status:** Protocol definition — no implementation
> **Date:** 2026-09-03
> **Scope:** Defines the intelligence architecture for AI-Radar v2, a Personal Intelligence Radar.

---

## 1. PRODUCT PURPOSE

AI-Radar is a **Personal Intelligence Radar**, not a news reader.

Its purpose is to:
1. **Detect** meaningful signals from the world across multiple domains.
2. **Interpret** those signals according to the user's evolving academic and intellectual trajectory.
3. **Connect** signals across disciplines to reveal emerging intellectual themes.
4. **Act** — translate signals into learning, building, and research opportunities.

It answers four questions every day:
- **What changed?** — What's new in the world that matters?
- **Why does it matter to me?** — Personal relevance interpretation.
- **What should I learn?** — Knowledge gaps surfaced by current signals.
- **What could I do with it?** — Actionable output opportunities.

It is **not**:
- An RSS reader
- A news aggregator
- A chatbot
- A productivity dashboard

---

## 2. SIGNAL TYPES

### 2.1 NOW — What's happening
Meaningful developments worth knowing about today.

Sub-types:
| Sub-type | Description | Examples |
|----------|-------------|----------|
| `research` | New papers, studies, findings | arXiv preprint, Nature publication |
| `release` | New tools, models, platforms | Model release, API update, open-source project |
| `policy` | Regulations, standards, industry shifts | EU AI Act enforcement, new standard |
| `event` | Conferences, competitions, deadlines | NeurIPS CFP, hackathon, grant deadline |
| `shift` | Structural changes in a field | Market trend, paradigm shift, community movement |

### 2.2 LEARN — What you should understand
Concepts or foundational knowledge worth investing time in.

Sub-types:
| Sub-type | Description | Examples |
|----------|-------------|----------|
| `concept` | A term, framework, or mental model | "Agentic workflow", "Bayesian thinking" |
| `theory` | A body of knowledge with depth | Information theory, cognitive load theory |
| `method` | A technique or approach | A/B testing, affinity mapping, design research |
| `context` | Historical or cultural background needed | History of the internet, Venetian printing press |
| `foundation` | Core prerequisite knowledge | Linear algebra for ML, typography fundamentals |

Key distinction from NOW: LEARN signals are **not time-sensitive**. They are surfaced because current activity or signals indicate a knowledge gap.

### 2.3 SEE — What you should study visually
Visual, design, or data visualization works worth studying.

Sub-types:
| Sub-type | Description | Examples |
|----------|-------------|----------|
| `website` | A well-designed web experience | linear.app, bluecorridors.org |
| `dataviz` | Data visualization project or study | Information is Beautiful, Pudding.cool |
| `editorial` | Print or digital editorial design | Magazine spread, book design, poster |
| `exhibition` | Physical or digital exhibition | Museum installation, digital archive interface |
| `interface` | Notable interaction design | New design pattern, micro-interaction study |

Each SEE signal includes a **Steal This** section: what specific technique to extract and apply.

### 2.4 BUILD — What can become output
Opportunities that could become projects, experiments, or portfolio pieces.

Sub-types:
| Sub-type | Description | Examples |
|----------|-------------|----------|
| `project` | A concrete project idea | "Interactive Venice archive map" |
| `experiment` | A small, time-boxed exploration | "Recreate this chart in D3" |
| `contribution` | An open-source or community opportunity | "Contribute to Programming Historian" |
| `portfolio` | Something that directly builds portfolio | "Data viz for your Cultural Heritage course" |
| `research` | A potential research direction | "AI + historical document restoration" |

Each BUILD signal includes:
- **Inputs needed**: what resources/data/skills are required
- **Possible outputs**: what it could produce
- **Difficulty**: 1–5 scale
- **Time estimate**: rough duration
- **Connection to profile**: why this fits the user's trajectory

---

## 3. PERSONAL RELEVANCE MODEL

Every signal is scored on five dimensions, each 0–10.

### 3.1 Personal Relevance (PR)
**Definition:** How directly connected is this signal to the user's current academic direction, active interests, and long-term goals?

| Score | Meaning |
|-------|--------|
| 9–10 | Directly addresses a core interest or active project. Cannot be ignored. |
| 7–8 | Strongly connected to 1–2 profile dimensions. Worth immediate attention. |
| 5–6 | Relevant but indirect. Interesting connection exists but not urgent. |
| 3–4 | Tangentially related. Might become relevant with context. |
| 1–2 | Minimal connection. Only included if exceptional in other dimensions. |

**Evaluation criteria:**
- Does it touch `academic_direction` fields?
- Does it relate to `active_interests`?
- Does it connect to `long_term_goal.theme`?
- Is it timely for the user's current `stage` (e.g., first-year undergrad)?

### 3.2 Novelty (NV)
**Definition:** How new or surprising is this information relative to what the user likely already knows?

| Score | Meaning |
|-------|--------|
| 9–10 | Breakthrough or entirely unexpected. Changes understanding of a domain. |
| 7–8 | Significant new development. Not yet widely discussed. |
| 5–6 | Notable but already circulating in the user's likely information diet. |
| 3–4 | Incremental update on known topic. |
| 1–2 | Already well-known to anyone following the field. |

**Evaluation criteria:**
- How recently was this published/announced?
- Is it a first-of-kind, or an iteration?
- Would the user likely have encountered this through their existing channels?

### 3.3 Learning Value (LV)
**Definition:** How much would engaging with this signal deepen the user's understanding or capabilities?

| Score | Meaning |
|-------|--------|
| 9–10 | Foundational — understanding this unlocks multiple other areas. |
| 7–8 | High — directly fills a gap in `learning_priorities` or connects two areas of knowledge. |
| 5–6 | Moderate — useful but peripheral to current trajectory. |
| 3–4 | Low — interesting but doesn't build transferable understanding. |
| 1–2 | Negligible — no clear learning path. |

**Evaluation criteria:**
- Does it address a `learning_priorities` gap?
- Does it connect two or more of the user's interest domains?
- Is the depth appropriate for the user's current level?
- Does understanding this signal enable understanding future signals?

### 3.4 Actionability (AC)
**Definition:** Can the user do something concrete with this information today, this week, or this semester?

| Score | Meaning |
|-------|--------|
| 9–10 | Immediate, concrete action possible (build something, apply to something, attend something). |
| 7–8 | Action possible within the week with moderate effort. |
| 5–6 | Action possible but requires planning or resources not immediately available. |
| 3–4 | Long-term relevance — shapes thinking but no near-term action. |
| 1–2 | Purely informational. No clear action path. |

**Evaluation criteria:**
- Can this become a project, experiment, or portfolio piece?
- Does it suggest a specific next step?
- Is the required effort proportional to the user's current bandwidth?
- Does it align with upcoming deadlines or academic milestones?

### 3.5 Cross-disciplinary Connection Potential (CC)
**Definition:** How strongly does this signal bridge two or more of the user's interest domains?

| Score | Meaning |
|-------|--------|
| 9–10 | Bridges 3+ domains and reveals a non-obvious connection. |
| 7–8 | Bridges 2 domains in a meaningful, specific way. |
| 5–6 | Touches 2 domains but the connection is straightforward. |
| 3–4 | Primarily single-domain with minor adjacent relevance. |
| 1–2 | Single-domain only. |

**Evaluation criteria:**
- How many of the user's interest/academic domains does it touch?
- Is the connection non-obvious (surprising) or predictable?
- Does the connection suggest a new intellectual direction or research area?
- Would the connection be invisible to someone who only follows one domain?

### 3.6 Composite Radar Score

```
RADAR_SCORE = PR × 0.30 + NV × 0.15 + LV × 0.25 + AC × 0.15 + CC × 0.15
```

Weighted toward **Personal Relevance** and **Learning Value** — because the system serves a person, not a newsroom.

---

## 4. SIGNAL SELECTION

### 4.1 Anti-Quota Principle
The system does **not** force equal representation across disciplines.

If today's strongest signals are all in AI × Cultural Heritage, then today's radar reflects that. If next week the strongest signals are in Psychology × Design, so be it.

**Selection is driven by signal strength, not category balance.**

### 4.2 Daily Output Target

| Category | Count | Requirement |
|----------|-------|-------------|
| NOW signals | 3–5 | Must include at least 1 with CC ≥ 7 |
| LEARN | 1 | Mandatory — the single most valuable concept to understand this week |
| SEE | 1 | Mandatory — one visual/design case study |
| BUILD | 0–1 | Optional — only if a genuinely actionable opportunity exists |

**Total daily output: 5–8 signals.**

### 4.3 Filtering Pipeline

```
Raw collection (100+ items)
  → Deduplication
  → Spam/hype filter (remove: generic AI news, low-depth summaries, promotional content)
  → Personal relevance pre-screen (PR ≥ 4)
  → Full 5-dimension scoring
  → Rank by RADAR_SCORE
  → Select top signals within category targets
  → Cross-reference with profile preferences (avoid list, prioritize list)
  → Final output
```

### 4.4 Anti-Slop Rules

The following are **automatically filtered out** unless they pass exceptional manual review:
- "X company raises $Y billion" — market signals, not knowledge signals
- "Top 10 AI tools you must try" — listicles without depth
- Content that is primarily promotional or sponsored
- Repackaged press releases without analysis
- Content that only exists in one language and lacks primary source
- Anything matching `radar_preferences.avoid` in profile.json

---

## 5. CROSS-DISCIPLINARY CONNECTION ENGINE

### 5.1 Purpose
Identify **emerging intellectual themes** across domains, not just categorize information.

The user's intellectual position is inherently cross-disciplinary:

```
                    AI
                     │
          Data ──────┼───── HCI
                     │
    Psychology ─── YOU ─── Culture
                     │
          Design ───┼──── Digital Humanities
                     │
                 Knowledge
```

The connection engine makes this web visible.

### 5.2 Connection Types

| Type | Definition | Example |
|------|-----------|--------|
| `bridge` | A signal that directly links two domains | AI OCR breakthrough → Cultural Heritage archives |
| `theme` | Multiple signals across days point to an emerging pattern | Agent architecture + Knowledge systems + Cognitive offloading → "AI-Augmented Cognition" |
| `gap` | A domain connection where the user has no signal (blind spot) | No recent signals in Statistics despite it being a learning priority |
| `convergence` | Two independent signals point to the same conclusion | A psychology paper and an HCI paper both suggest the same interaction pattern |
| `tension` | Two signals or domains contain contradictory implications | AI automation narrative vs. manual craft preservation in Cultural Heritage |

### 5.3 Connection Detection Algorithm

**Per-signal connections** (daily):
1. For each scored signal, identify which domains from the user's profile it touches.
2. If it touches ≥2 domains, flag as a `bridge` connection.
3. Look up recent archive (last 7 days) for signals in the same domain intersection.
4. If a pattern of 3+ related signals emerges across the intersection, note a potential `theme`.

**Weekly synthesis connections**:
1. Aggregate all signals from the past 7 days.
2. Build a domain co-occurrence graph.
3. Identify the highest-weight edges (domain pairs that appeared together most often).
4. Name the emerging theme from the intersection.
5. Check for `gap` connections — domains in profile with zero signals this week.
6. Check for `tension` — signals that contradict each other.

### 5.4 Domain Taxonomy

Primary domains (from profile):
- AI
- Data Science
- Psychology
- Cognitive Science
- HCI
- Design
- Data Visualization
- Culture
- Cultural Heritage
- Digital Humanities
- Knowledge Systems

These are not rigid categories. A signal can touch any combination. The engine tracks **observed domain intersections** over time to detect recurring themes.

---

## 6. DAILY OUTPUT SCHEMA

### 6.1 File: `daily-feed.json`

```json
{
  "$schema": "radar-daily-feed-v1",
  "date": "2026-09-03",
  "generated_at": "2026-09-03T07:00:00+02:00",
  "signal_count": 6,

  "signals": [
    {
      "id": "20260903-01",
      "title": "AI model restores damaged historical manuscripts",
      "source": {
        "name": "Nature",
        "url": "https://nature.com/articles/...",
        "type": "research"
      },
      "date": "2026-09-02",
      "category": "NOW",
      "sub_type": "research",
      "domains": ["AI", "Cultural Heritage", "Digital Humanities"],
      "summary": "New multimodal model achieves 94% accuracy in restoring text from damaged historical manuscripts, outperforming previous methods by 23 percentage points.",
      "why_it_matters": "Pushes the boundary of what AI can do for cultural preservation — moves beyond transcription into restoration.",
      "why_you_should_care": "Directly connects your Data Science skills with Cultural Heritage interests. Potential application for Venice archive digitization projects at Ca' Foscari.",
      "radar_score": 9.2,
      "score_breakdown": {
        "personal_relevance": 9.5,
        "novelty": 8.7,
        "learning_value": 9.0,
        "actionability": 8.2,
        "cross_disciplinary": 10.0
      },
      "connections": [
        {
          "type": "bridge",
          "domains": ["AI", "Cultural Heritage"],
          "note": "AI applied to cultural preservation — your exact intersection."
        },
        {
          "type": "bridge",
          "domains": ["AI", "Digital Humanities"],
          "note": "Digital restoration of historical documents is a core DH research area."
        }
      ],
      "suggested_action": {
        "type": "explore",
        "label": "Explore connection",
        "detail": "Read the paper. Note the methodology — could inform how you approach Venice Cultural Layers."
      }
    }
  ],

  "daily_learn": {
    "id": "20260903-learn",
    "title": "Agentic Workflow",
    "sub_type": "concept",
    "level": "intermediate",
    "domains": ["AI", "HCI"],
    "summary": "The architecture of AI systems that plan, use tools, and execute multi-step tasks. Covers planning, tool use, and agent orchestration patterns.",
    "why_now": "You've encountered MCP, OpenClaw, and AI agents repeatedly across projects. Building structured understanding will let you design agent-based systems rather than just use them.",
    "suggested_action": {
      "type": "learn",
      "label": "Learn the architecture",
      "detail": "Start with Anthropic's agent patterns doc, then map it to your experience with WorkBuddy and OpenClaw."
    },
    "radar_score": 8.4,
    "score_breakdown": {
      "personal_relevance": 9.0,
      "novelty": 6.0,
      "learning_value": 10.0,
      "actionability": 8.0,
      "cross_disciplinary": 9.0
    }
  },

  "daily_see": {
    "id": "20260903-see",
    "title": "Blue Corridors — Whale Migration Data Visualization",
    "source": {
      "name": "bluecorridors.org",
      "url": "https://bluecorridors.org",
      "type": "dataviz"
    },
    "domains": ["Data Visualization", "Design"],
    "observation": "Full-bleed map as the interface. No sidebar, no dashboard clutter. Migration tracks are brightest; threats secondary; conservation tertiary.",
    "analysis": "Three-layer visual hierarchy (data > threat > solution) with a scrubable timeline as the primary interaction. Clean sans-serif typography that serves the map.",
    "steal_this": "The scrubable timeline pattern: a horizontal slider that animates data across a spatial view. Recreate this concept for your Venice Cultural Layers project — same pattern, different data.",
    "radar_score": 7.8,
    "score_breakdown": {
      "personal_relevance": 7.0,
      "novelty": 7.5,
      "learning_value": 9.0,
      "actionability": 8.5,
      "cross_disciplinary": 7.0
    }
  },

  "daily_build": null,

  "connections_today": [
    {
      "type": "bridge",
      "signal_ids": ["20260903-01"],
      "domains": ["AI", "Cultural Heritage", "Digital Humanities"],
      "summary": "AI restoration of historical manuscripts bridges your three core areas."
    }
  ]
}
```

### 6.2 Schema Notes

- `daily_build` is `null` when no actionable build opportunity exists. It should **not** be force-populated.
- `suggested_action.type` values: `explore` | `read` | `learn` | `analyze` | `build` | `attend` | `bookmark`
- `domains` array uses the Domain Taxonomy from §5.4. A signal may touch 1–N domains.
- `connections` within each signal are **per-signal** connections (bridges discovered at scoring time).
- `connections_today` at the root level are **cross-signal** connections discovered after all signals are scored.

---

## 7. WEEKLY INTELLIGENCE

### 7.1 File: `weekly-intelligence.json`

Generated once per week (Sunday). Synthesizes the past 7 days of daily feeds.

```json
{
  "$schema": "radar-weekly-intelligence-v1",
  "week": "2026-W36",
  "date_range": {
    "start": "2026-08-28",
    "end": "2026-09-03"
  },
  "generated_at": "2026-09-03T21:00:00+02:00",

  "summary": {
    "total_signals": 38,
    "by_category": {
      "NOW": 25,
      "LEARN": 7,
      "SEE": 7,
      "BUILD": 3
    },
    "avg_radar_score": 7.6,
    "top_score": 9.4
  },

  "strongest_themes": [
    {
      "name": "AI-Augmented Knowledge Systems",
      "description": "Multiple signals this week pointed to how AI is changing the way humans interact with, preserve, and build upon knowledge — from agent architectures to digital archive restoration.",
      "domains": ["AI", "Knowledge Systems", "Digital Humanities", "Cultural Heritage"],
      "signal_count": 8,
      "key_signals": ["20260901-01", "20260902-03", "20260903-01"]
    },
    {
      "name": "Cognitive Load in Complex Interfaces",
      "description": "Three separate signals (a psychology study, an HCI paper, and a design case study) all addressed how humans process information-dense environments.",
      "domains": ["Psychology", "HCI", "Design", "Data Visualization"],
      "signal_count": 5,
      "key_signals": ["20260830-02", "20260901-04", "20260902-05"]
    }
  ],

  "recurring_concepts": [
    {
      "concept": "Agent architecture",
      "occurrences": 5,
      "domains": ["AI", "HCI"],
      "note": "Appeared in NOW signals, LEARN recommendations, and BUILD suggestions. This is becoming a persistent theme — consider making it a formal learning priority."
    },
    {
      "concept": "Typography as information hierarchy",
      "occurrences": 3,
      "domains": ["Design", "Data Visualization"],
      "note": "Continues from last week. You're developing a coherent design eye."
    }
  ],

  "unexpected_connections": [
    {
      "connection": "Bayesian reasoning in AI × Cultural Heritage dating",
      "domains": ["Data Science", "AI", "Cultural Heritage"],
      "description": "A NOW signal about Bayesian methods in DS and a separate LEARN signal about historical document dating both use the same mathematical framework. This is a non-obvious bridge."
    }
  ],

  "research_directions": [
    {
      "direction": "AI-assisted cultural knowledge preservation",
      "rationale": "Three themes this week converged here: AI document restoration, digital archive interfaces, and knowledge system design.",
      "feasibility": "high",
      "next_step": "Review the 3 key signals and write a 1-page research concept note."
    }
  ],

  "gaps": [
    {
      "domain": "Psychology",
      "signal_count": 0,
      "note": "No psychology signals this week despite it being in your active interests. The connection engine found a bridge via HCI, but no dedicated psychology signal. Consider whether this is a blind spot or a quiet week."
    },
    {
      "domain": "Statistics",
      "signal_count": 0,
      "note": "Statistics is a learning priority but not in your active interests. No signals surfaced naturally. This is expected — foundation gaps need active study, not passive discovery."
    }
  ],

  "next_week_suggestions": [
    "Deepen the AI-Augmented Knowledge Systems theme — read at least one of the 8 key signals in full.",
    "Look for a dedicated Psychology signal — your HCI work would benefit from cognitive foundations.",
    "The Venice Cultural Layers BUILD idea from Tuesday is still pending. Allocate one focused session this week."
  ]
}
```

### 7.2 Weekly Intelligence Purpose

The weekly report serves a meta-function: **it makes your intellectual evolution visible**.

Over months, you can look back:
- September 2026: AI Agents × Knowledge
- October 2026: Data Visualization × Culture
- November 2026: Cognitive Science × HCI
- January 2027: Digital Heritage × AI

This becomes your **Intellectual Archive** — the basis for identifying your research identity and academic direction.

---

## 8. DESIGN PRINCIPLE: SEPARATION OF CONCERNS

The intelligence architecture must maintain a strict pipeline:

```
DATA COLLECTION
    ↓
FILTERING
    ↓
PERSONAL SCORING
    ↓
CONNECTION DETECTION
    ↓
CONTENT GENERATION
    ↓
UI RENDERING
```

### 8.1 Layer Definitions

| Layer | Input | Output | Owner |
|-------|-------|--------|-------|
| **Data Collection** | Source list, search queries | Raw signal candidates (100+) | Automated (cron + agent) |
| **Filtering** | Raw candidates | Deduplicated, de-spammed list (~20) | Automated (rules + profile.avoid) |
| **Personal Scoring** | Filtered list + profile.json | Scored signals with breakdowns | AI agent (needs profile context) |
| **Connection Detection** | Scored signals + 7-day archive | Connection graph + theme candidates | AI agent (needs historical context) |
| **Content Generation** | Top signals + connections | daily-feed.json with full content | AI agent (needs writing capability) |
| **UI Rendering** | daily-feed.json + archive/ | Rendered HTML page | Static HTML/JS (no AI needed) |

### 8.2 Key Implications

1. **UI never calls an AI API.** The page reads JSON. This means:
   - The page loads instantly.
   - No API key needed in the browser.
   - No proxy server needed.
   - The page works offline once JSON is generated.

2. **Profile is the brain.** All personalization comes from `profile.json`. Changing the profile changes the radar's behavior — no code changes needed.

3. **Archive enables connections.** The system needs access to recent daily feeds to detect patterns. A simple file-based archive (one JSON per day) is sufficient.

4. **Each layer is independently testable.** You can test scoring without collection, test UI without AI, test connections without rendering.

---

## 9. FILE STRUCTURE (Proposed)

```
AI-Radar/
│
├── AI-Radar.html          ← Existing v1 (UNTOUCHED)
├── radar-server.py        ← Existing v1 proxy (UNTOUCHED)
│
├── v2/
│   ├── index.html         ← New UI (Phase 3)
│   ├── style.css          ← New styles (Phase 3)
│   ├── app.js             ← New rendering logic (Phase 3)
│   │
│   ├── data/
│   │   ├── profile.json       ← User profile (Phase 1)
│   │   ├── source-list.json   ← Curated sources (Phase 1)
│   │   ├── daily-feed.json    ← Today's output (Phase 2)
│   │   └── archive/           ← Historical daily feeds
│   │       ├── 2026-09-03.json
│   │       ├── 2026-09-02.json
│   │       └── ...
│   │
│   └── docs/
│       ├── RADAR_INTELLIGENCE_PROTOCOL.md  ← This document
│       └── weekly-intelligence/             ← Weekly reports
│           ├── 2026-W36.json
│           └── ...
│
└── scripts/               ← Generation scripts (Phase 2)
    └── generate-radar.py
```

**Existing files (`AI-Radar.html` and `radar-server.py`) are never modified.**

---

## 10. IMPLEMENTATION PRIORITY

### Phase 1 — Foundation (Do first)
1. Create `profile.json` with the user's full intellectual profile.
2. Create `source-list.json` with curated primary sources per domain.
3. Finalize this protocol document.

**Deliverables:** 3 JSON/MD files. No code. No UI.

### Phase 2 — Daily Radar Engine
1. Build the generation pipeline (can start as a manual agent prompt, automate later via cron).
2. Run 3 test generations to validate signal quality.
3. Iterate on scoring rubric and source list based on results.

**Deliverables:** `generate-radar.py` or equivalent + 3 days of test `daily-feed.json`.

### Phase 3 — Interface
1. Migrate AI-Radar v1's visual language (paper texture, Fraunces, Inter, dark red accent) to v2.
2. Build signal-driven layout (Today's signals → Learn → See → Build → Connections).
3. Add domain filtering and archive browsing.

**Deliverables:** `v2/index.html` + `v2/style.css` + `v2/app.js`.

### Phase 4 — Weekly Intelligence
1. Build weekly synthesis generation.
2. Add weekly report to UI.
3. Begin building the Intellectual Archive.

**Deliverables:** Weekly generation + UI integration.

---

*End of Protocol.*
