# 8. DRY & YAGNI

**Part 2 — Design Principles & Patterns** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
DRY and YAGNI are the two principles most often cited to justify opposite mistakes —
over-abstracting duplication that wasn't really the same thing, and building
flexibility nobody asked for — so the real skill is judgment about *when* each applies.

## Learning objectives
- Can state Don't Repeat Yourself precisely: "every piece of knowledge must have a
  single, unambiguous, authoritative representation" — not merely "no duplicate code."
- Can distinguish duplicated *code* that represents the same underlying knowledge
  (should be unified) from duplicated code that coincidentally looks similar but
  represents different concepts that will diverge (should stay separate).
- Can state You Aren't Gonna Need It and identify speculative generality — config
  options, plugin hooks, or abstraction layers built for a requirement that doesn't
  exist yet.
- Can strip an over-engineered abstraction down to the simplest implementation that
  satisfies today's actual requirement, while documenting the trigger condition that
  would justify re-adding the abstraction later.
- Can articulate the tension between DRY and YAGNI in a code review comment, not just
  in the abstract.

## Session outline (~45 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the wrong abstraction | 5 min | A "DRY" fix that made things worse |
| DRY, precisely | 10 min | Knowledge vs. code; the rule of three |
| The premature abstraction trap | 8 min | When looks-the-same isn't is-the-same |
| YAGNI, precisely | 10 min | Cost of unused flexibility; speculative generality |
| The under-engineering trap | 7 min | YAGNI isn't an excuse to skip design |
| Wrap-up: the shared judgment call | 5 min | Where the two principles actually meet |

**Hook: the wrong abstraction (5 min).** Present Sandi Metz's well-known observation
(paraphrase, don't quote at length): duplicated code is far cheaper than the wrong
abstraction, because duplication is easy to see and easy to later unify, while a bad
shared abstraction accretes conditionals and parameters until nobody can safely change
it. Ask the class: have you ever added an `if isSpecialCase` flag to a "shared"
function? That's the smell this session is about.

**DRY, precisely (10 min).** State the actual definition from *The Pragmatic
Programmer*: DRY is about a single authoritative representation of a piece of
*knowledge* — a business rule, a constant, a validation rule — not simply "no two
blocks of code look alike." Two functions can have identical-looking code today and
still represent different knowledge (a US phone validator and a US ZIP validator both
happen to be five digits right now — that's coincidence, not shared knowledge).
Introduce the "rule of three" heuristic: don't abstract on the first duplication,
consider it on the second, usually extract on the third — by then the *actual* shared
shape is clearer.

**The premature abstraction trap (8 min).** Show a concrete case: two "similar"
functions that compute a discount, one for "loyalty discount" and one for "bulk
discount," sharing a percentage-off calculation today. A junior extracts a shared
`applyDiscount(rule)` function. Next sprint, loyalty discounts need to stack, bulk
discounts don't — now the shared function needs a `stackable` flag, and the code that
looked unified is really two things wearing one coat. Discuss: the fix isn't "never
abstract," it's noticing when duplication is conceptual coincidence.

**YAGNI, precisely (10 min).** State the rule: don't build capability for a
requirement you don't have yet, even if you're confident it's coming. Walk through the
real cost: every unused config option, plugin hook, or "just in case" parameter is
code that must be maintained, tested, and understood by every future reader, for a
scenario that may never occur or may occur differently than guessed. Contrast "make it
easy to change later" (good — keep coupling low) with "build the general mechanism
now" (usually premature).

**The under-engineering trap (7 min).** YAGNI is not a license to skip basic design
— it applies to *speculative* generality, not to reasonable structure for present
requirements. Show a config-driven "export framework" with a plugin registry, when the
product only ever exports CSV. Contrast with a case where a second real format is
already a stated near-term requirement — in that case building *some* seam is
reasonable, not speculative.

**Wrap-up (5 min).** Both principles are really the same instinct pointed in two
directions: don't pay for structure the current requirements don't need — whether
that's redundant knowledge (DRY) or unused flexibility (YAGNI). The judgment call is
always "what do today's actual requirements need," not "what looks reusable" or "what
might be useful."

## Homework notes

### 1. Extract a shared abstraction from near-duplicate functions — and justify the line

**Goal:** Practice telling apart duplication that represents genuinely shared
knowledge from duplication that merely looks similar, and defend the boundary you drew
in writing.

**Approach / hints:**
- Start from (or write) 3–4 functions that look similar on the surface — e.g., several
  "validate and format" functions for different input types, or several report
  generators that each filter, sort, and render a dataset slightly differently.
- For each pair, ask: if a requirement changed for one, would it plausibly need to
  change for the others too? If yes, that's the same knowledge — extract it. If the
  answer is "maybe not," keep them separate even if the code currently matches.
- Extract only the piece that represents genuinely shared knowledge (e.g., the sorting
  algorithm) and leave the parts that differ conceptually (e.g., what counts as
  "filtered out") as separate, explicit code — pass it as a parameter or keep it as a
  distinct function rather than forcing it through a shared flag.
- Write 3–5 sentences justifying where you drew the line, specifically naming one case
  you *didn't* unify and why.

**Definition of done:** A shared abstraction exists for the pieces that represent one
piece of knowledge; conceptually distinct logic that happened to look similar remains
separate; a short written justification names at least one deliberate non-unification.

### 2. Strip an over-engineered mini-framework down to YAGNI

**Goal:** Practice recognizing and removing speculative generality, and practice
stating — concretely — what future signal would justify re-adding it.

**Approach / hints:**
- Start from (or build) a small "framework": a config file, a plugin registry, and an
  interface with one real implementation, solving a problem that in practice only ever
  needs that one implementation (e.g., a notification "framework" that only ever sends
  email, but has a config-driven channel registry, a `NotificationStrategy` interface,
  and a factory).
- Delete the registry, the interface, and the config-driven selection. Replace with the
  simplest direct implementation that satisfies the actual current requirement (a
  function or single class that sends email).
- Write down 2–3 concrete signals that would justify re-introducing the abstraction —
  not "if we need more flexibility" but something testable, like "when a second
  notification channel is an actual, scheduled requirement" or "when the same
  selection logic is needed in a second place in the codebase."

**Definition of done:** The simplified version has no unused interface, config option,
or plugin seam; behavior for the one real use case is unchanged; a short note lists
concrete trigger conditions for re-adding the abstraction later.

## Further resources
- Free companion: [DeviQ — DRY](https://deviq.com/principles/dont-repeat-yourself) / [YAGNI](https://deviq.com/principles/yagni/) · Martin Fowler, [Yagni](https://martinfowler.com/bliki/Yagni.html)
