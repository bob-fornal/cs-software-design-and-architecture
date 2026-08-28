# 30. Architect Responsibilities & Soft Skills

**Part 8 — The Software Architect Role** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Technical depth gets you invited to the room; the ability to elicit real requirements, communicate a decision so it sticks, and coach a team through a tradeoff is what makes people actually follow the architecture once you leave it.

## Learning objectives
- Can run a requirements-elicitation conversation that surfaces both functional and non-functional requirements and explicitly flags open questions rather than guessing.
- Can distinguish enforcing a standard (non-negotiable) from coaching a preference (negotiable), and can explain why conflating the two erodes trust.
- Can write a decision memo that presents competing proposals fairly, states explicit evaluation criteria, and makes a clear recommendation with reasoning a reader can audit.
- Can estimate a body of work at a level of confidence appropriate to how much is still unknown, and communicate that uncertainty instead of hiding it.
- Can explain at least three concrete techniques for simplifying a design that's grown too complex.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the architect who never talks to anyone | 5 min | Short scenario: an architect designs a "perfect" system in isolation, ships the diagram, and it's wrong because nobody asked the support team about their actual pain points. Land on: architecture is a communication practice as much as a technical one. |
| Requirements elicitation | 10 min | Functional vs. non-functional requirements (what it does vs. how well it does it — latency, availability, security, compliance). Techniques: ask "why" behind every requested feature, distinguish stated wants from underlying needs, actively hunt for non-functional requirements because stakeholders rarely volunteer them. Practice framing: "what happens if this is slow/down/wrong?" surfaces NFRs fast. |
| Documentation & enforcing standards | 8 min | Documentation as a communication artifact for a specific audience (not documentation for its own sake). Standards: the difference between a hard constraint (security policy, a compliance requirement) and a preference (a coding style) — architects must enforce the former and coach on the latter, and be honest with themselves about which is which. |
| Collaboration & coaching developers | 8 min | The architect as multiplier: unblocking a stuck team is often higher-leverage than writing more code personally. Coaching means asking questions that lead a developer to the answer rather than just handing down a decision — builds team capability, not dependency. |
| Decision-making, estimating & tradeoffs | 10 min | A decision-making framework: name the criteria *before* comparing options (avoids rationalizing a favorite after the fact). Estimating: communicate a range and the confidence behind it, not a false-precision single number; re-estimate as unknowns resolve. Tradeoffs: there is no free lunch — every quality attribute traded for another (consistency vs. availability, speed of delivery vs. long-term flexibility) should be named explicitly, not left implicit. |
| Simplifying & communication wrap-up | 10 min | Techniques for simplifying: remove a requirement instead of engineering around it, merge near-duplicate components, defer a speculative capability (YAGNI at the architecture level), and re-explain the problem to a non-expert to see what's actually essential. Close with: all of the above is worthless if it isn't communicated — tie back into the homework. |

## Homework notes

### 1. Mock requirements-elicitation session
> Run a mock requirements-elicitation session (with a classmate or written scenario) for an ambiguous feature request, and produce a requirements document distinguishing functional vs. non-functional requirements and open questions.

- **Goal:** Tests whether students can turn a vague ask ("make it faster," "add reporting") into a requirements document that separates what the system must *do* from how well it must do it, and is honest about what's still unknown.
- **Approach / hints:** Pick a deliberately underspecified request (e.g., "we need a notifications feature"). If working solo, role-play both sides by writing the stakeholder's answers as you go, resisting the urge to fill gaps with assumptions before asking. Push past the first answer — "notify users" isn't done until you know which events, which channels, how fast, what happens on failure, and who can opt out. Every requirement you couldn't pin down goes in an explicit "open questions" section rather than being silently assumed.
- **Starter example:**
```markdown
## Functional Requirements
- FR1: System sends a notification when an order ships.
- FR2: Users can choose email or push per notification type.

## Non-Functional Requirements
- NFR1: Notification must be sent within 60s of the triggering event.
- NFR2: Failed sends must retry at least 3 times before giving up.

## Open Questions
- Q1: Should SMS be supported at launch, or is that a future channel?
- Q2: What happens to notifications queued while a user is opted out
      mid-flight — drop, or deliver on re-opt-in?
```
- **Definition of done:** A requirements document with clearly separated functional and non-functional sections and a non-empty, genuinely unresolved open-questions list — not a document that pretends everything was nailed down.

### 2. Decision memo for competing proposals
> Given two competing technical proposals for the same problem (provided or written by classmates), write a decision memo that fairly evaluates trade-offs and makes a recommendation with clear reasoning — practicing decision-making and communication together.

- **Goal:** Tests whether students can evaluate options against explicit criteria rather than gut feel, and communicate that reasoning so a reader who disagrees can pinpoint exactly where.
- **Approach / hints:** If you don't have two ready-made proposals, write both yourself for a problem from an earlier module (e.g., two ways to add caching, two ways to split a monolith). State your evaluation criteria (cost, time-to-ship, team familiarity, long-term maintainability, risk) *before* scoring either option — this is what keeps the memo fair instead of a post-hoc justification of whichever you liked first. Score both against every criterion, even the ones that favor the option you're not recommending.
- **Starter example:**
```markdown
## Decision Memo: Search Implementation

### Criteria
1. Time to ship (weight: high)
2. Operational cost at current scale (weight: medium)
3. Team familiarity (weight: medium)
4. Room to grow (weight: low, revisit in 12mo)

### Option A: Postgres full-text search
Ships fastest, no new infra, weaker relevance ranking, ceiling around
~1M rows before latency degrades.

### Option B: Dedicated search engine (e.g., Elasticsearch)
Better relevance and scale ceiling, new operational surface, team has
no prior ops experience with it.

### Recommendation
Option A. Time-to-ship and team familiarity dominate at current scale;
revisit Option B if row count or relevance requirements outgrow it.
```
- **Definition of done:** A memo with explicit, weighted criteria applied evenly to both options, and a recommendation whose reasoning a disinterested reader could reconstruct without asking the author follow-up questions.

## Further resources
- Free companion: MIT [21W.780 Communicating in Technical Organizations](https://ocw.mit.edu/courses/21w-780-communicating-in-technical-organizations-fall-2001/)
