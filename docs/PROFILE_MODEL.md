# Profile Model Documentation

> **Version:** 1.0
> **Date:** 2026-09-03
> **Scope:** Explains the design rationale behind `profile.json` and how it should evolve.

---

## 1. Why Dynamic, Not Static

A static profile ("Elin likes AI, design, and psychology") is useless for a Personal Intelligence Radar.

Here's why:

**Static profiles answer:** "What topics does this person generally like?"
**Dynamic profiles answer:** "What should enter this person's intellectual world *right now*?"

These are fundamentally different questions.

A static profile would recommend the same things in September 2026 as it would in March 2027. But Elin in September 2026 (Y1 S1 starting, just moved to Venice, post-EUTOPIA submission) is a different intellectual organism than Elin in March 2027 (mid-Y1, 5 months of DS coursework complete, possibly starting research).

The profile must capture **velocity**, not just position.

### What Changes

| Layer | Change Rate | Example |
|-------|------------|---------|
| Stable Identity | Very slow (months–years) | Core intellectual territory |
| Current Context | Medium (weeks–months) | Courses, projects, skill levels |
| Active Curiosity | Fast (days–weeks) | What's catching attention right now |
| Growth Edges | Medium (months) | Transitions being actively pursued |

---

## 2. Stable Identity vs Current Context

These two layers are often conflated but serve different purposes:

**Stable Identity** answers: "Who is this person, fundamentally?" It changes slowly because it describes long-term characteristics:
- Intellectual territory (the space between domains where this person lives)
- Methodological preferences (how they think about problems)
- Design philosophy (what they find valuable vs. noisy)
- Long-term direction (where they're heading over years)

**Current Context** answers: "Where is this person *right now*?" It changes because life happens:
- Academic stage and grades
- Active projects and their status
- Skill gaps that are actually urgent
- Environmental factors (location, access to resources)
- Upcoming deadlines and milestones

The Radar uses **Stable Identity** for signal relevance scoring (does this match who you are?) and **Current Context** for actionability scoring (can you do something with this *now*?).

A signal might be highly relevant to your Stable Identity (AI × Cultural Heritage paper) but low actionability if your Current Context shows you're in exam week with no time for side projects. The Radar should still show it — but flag it differently than a signal you can act on today.

---

## 3. Why Active Curiosity Should Decay/Change

`active_curiosity` is not a permanent list of interests. It's a **snapshot of attention**.

Each curiosity entry has:
- `interest_level` (1–5): current intensity
- `why_now`: what triggered this interest
- `exploration_status`: not_started → awareness → planned → actively_exploring → actively_practicing → mastered

**Curiosity entries should:**
- Be added when something new catches attention (a paper, a conversation, a project need)
- Have their `interest_level` decay over time if not reinforced by signals or actions
- Transition through exploration statuses as engagement deepens
- Eventually either graduate into Stable Identity (if it becomes a core interest) or be archived (if it was a passing interest)

**This is not implemented as automatic decay in v1.** For now, curiosity maintenance is manual during weekly reviews. Future versions could track how many times a topic appears in daily feeds and auto-adjust interest_level.

### Anti-Pattern: The "Everything Is Interesting" Trap

A common failure mode of personalization systems is that users say "everything is interesting" and the system has no signal to distinguish priorities.

The 1–5 scale + exploration_status + explicit `why_now` field forces specificity. If you can't articulate why a topic matters *now*, it probably shouldn't be in active_curiosity.

---

## 4. Why Growth Edges Are the Most Important Recommendation Signal

Growth edges are the **engine** of the entire Radar system.

Here's the logic chain:

1. The Radar's purpose is not to inform — it's to **accelerate intellectual development**.
2. Intellectual development happens at transitions (from X to Y), not within stable states.
3. Therefore, the most valuable signals are those that support active transitions.
4. Growth edges define exactly which transitions are happening.

### How Growth Edges Drive Scoring

When a signal is scored:

- **Personal Relevance (PR)** checks: does this touch any domain in the growth edge's `supported_by_domains`?
- **Learning Value (LV)** checks: does this fill a gap identified in the growth edge's `current_state` → `desired_direction`?
- **Actionability (AC)** checks: can this become a concrete step toward the `desired_direction`?

A signal that scores high on all three relative to your #1 growth edge (DS Beginner → Computational Thinker) will get a very high RADAR_SCORE even if its novelty is moderate. **That's correct behavior.** You don't need novelty in foundations — you need coverage.

Conversely, a highly novel signal in a peripheral domain with no growth edge connection might score lower on PR/LV/AC despite high NV. **Also correct.** Interesting ≠ important.

### Growth Edge Lifecycle

```
Identified → Actively Supported by Radar → Evidence Accumulates → Transition Completes → New Edge Emerges
```

The Radar should explicitly track evidence of transition progress:
- Did a LEARN recommendation get followed? (signal marked as "learned")
- Did a BUILD suggestion turn into a project? (new entry in current_context.active_projects)
- Do skills in radar improve? (skill_radar values increase)

This feedback loop makes the Radar **adaptive**, not just personalized.

---

## 5. How the Intellectual Territory Map Supports Cross-Disciplinary Connections

The territory map (`intellectual_territory_map.domains`) is not a flat list of interests. Each domain has:

- **relationship_type**: core / supporting / exploratory / peripheral
- **current_depth**: beginner / developing / intermediate / advanced
- **desired_depth**: where it should be
- **connection_targets**: which other domains it connects to

This structure enables the Connection Engine (§5 of Intelligence Protocol) to work:

### Connection Detection Uses Territory Map Data

1. When a signal touches Domain A, look up A's `connection_targets`
2. Check if any recent signal touched those targets
3. If yes → potential bridge connection
4. If multiple bridges form between the same pair over time → emerging theme
5. If a domain in `connection_targets` has zero signals this week → gap detection

### relationship_type Matters

- **Core domains** (AI, DS, HCI, Culture, Cultural Heritage) generate more connections because more signals will touch them.
- **Supporting domains** (Psychology, Design, DH) often appear as the *second* leg of a connection — the bridge destination.
- **Peripheral domains** (Cross-cultural Communication) may surface as gaps rather than sources.

### depth Gap = Learning Opportunity

If `current_depth` < `desired_depth` for a domain, AND that domain appears in a signal's connections, the LEARN engine should prioritize surfacing foundational content for that domain.

Example: Digital Humanities is "beginner" but "developing" desired. A signal connects AI → DH. The LEARN recommendation for that day could be a Programming Historian lesson — building DH capacity so future DH-connected signals can be engaged more deeply.

---

## 6. How profile.json Should Evolve Without Daily Manual Rewriting

The goal is **low-friction evolution**. The user should not need to edit profile.json every day.

### Automatic Updates (Future)

| Trigger | What Updates | Frequency |
|---------|-------------|-----------|
| Daily feed generated | `evolution_log` appends entry | Daily |
| Weekly intelligence run | `growth_edges.evidence_of_current_stage` updated from signal actions | Weekly |
| Monthly review | `active_curiosity.interest_level` adjusted based on engagement | Monthly |
| Project status change | `current_context.active_projects` updated | As needed |

### Manual Updates (User)

| Trigger | What to Update | Frequency |
|---------|---------------|-----------|
| New semester starts | `current_context.academic_situation`, `learning_priorities`, `skill_gaps` | Per semester |
| Major project starts/ends | `active_projects` list | As needed |
| Direction change | `stable_identity.long_term_direction`, `growth_edges` | Rarely (quarterly+) |
| New strong interest emerges | `active_curiosity` add entry | As felt |
 Interest fades | `active_curiosity` archive or reduce level | Monthly review |

### Evolution Log Pattern

The `evolution_log` array at the bottom of profile.json serves two purposes:

1. **Audit trail**: What changed when and why.
2. **Input for future automated analysis**: Over time, the log reveals patterns in how the profile evolves — which interests persist, which were fleeting, how growth edges progress.

For v1, this is manual. For v2+, an agent could analyze the evolution log during weekly synthesis and suggest profile updates.

---

## 7. Assumptions Made About the User's Intellectual Profile

The following assumptions are encoded in profile.json and should be validated or corrected by the user:

1. **Intellectual territory framing**: "Technology × Knowledge × Culture × Human Cognition" is my interpretation of the user's scattered interests into a coherent territory. This may not match how she would describe herself.

2. **Growth edge priority ordering**: ge-01 (DS foundations) > ge-02 (AI systems) > ge-03 (Interaction design) > ge-04 (Knowledge builder) > ge-05 (Research direction). This reflects my assessment of urgency vs. importance, which may differ from the user's own prioritization.

3. **Domain classification**: Some domains are clearly defined (AI, Data Science). Others involve judgment calls:
   - "Knowledge Systems" as distinct from "Digital Humanities" — these overlap significantly; the separation exists because PKM tools (Anki) feel different from DH methods (Programming Historian).
   - "Cognitive Science" separate from "Psychology" — in practice these blur; the split exists because cogsci tends toward computational models while psych tends toward experimental.

4. **Skill level estimates**: Programming 1.0→1.4, AI 1.5→2.0, CS 1.0→1.5 come from the old AI-Radar Skill Radar data. These may have shifted since August 20.

5. **Design skill at "intermediate"**: This is based on shipped OPC UI, Design Language spec, and demonstrated aesthetic judgment. The user might rate herself lower (imposter syndrome is real).

6. **Time budget**: 10-15 min/day for radar consumption is assumed. This may be unrealistic during exam periods.

7. **Language preference for sources**: Prioritized English/French sources because those are the user's academic languages. Chinese sources excluded despite native fluency because the academic/research ecosystem she operates in is English-dominant. This is a deliberate choice that should be confirmed.

8. **European bias in source selection**: Since the user is now in Venice, European sources (Europeana, DHQ, Venice museums) are weighted higher. This is contextually appropriate but creates a geographic filter that may miss important non-European work.

---

## 8. What Should Be Updated Manually in the Future

| Item | When | Who |
|------|------|-----|
| `current_context.academic_situation` (grades, CFU, courses) | After each exam session / semester | User (or agent with access to university portal) |
| `active_projects` status changes | When projects start/end/ship | User |
| `growth_edges.evidence_of_current_stage` | Weekly, based on what was actually done | Agent (from daily feed actions) + User confirmation |
| `active_curiosity` additions/removals | When interests shift | User primarily; agent can suggest archiving |
| `stable_identity` fields | Only when fundamental direction changes | User (rarely) |
| `source-list.json` | Quarterly review — add useful new sources, remove stale ones | Joint (agent suggests, user approves) |
| `radar_preferences.avoid/prioritize` | When patterns emerge in what gets filtered incorrectly | User |
| `time_budget` | When schedule changes significantly (exam week, holidays) | User |

*End of Profile Model Documentation.*
