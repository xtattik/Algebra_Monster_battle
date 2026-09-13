# Algebra Monster Battle — Challenge Pet Deck Design

**Date:** 2026-09-05 · **v2 rebalance:** 2026-09-14
**Status:** Implemented and rebalanced for v2 — `cards/pets-challenge.md`/`.html`, `--variant challenge`, and the extended answer key are in the repo; core-rules-v2 §9, teacher guide §10, student rulebook §10, and answer-key §2a/§2b updated. HP now copies Core's v2 bands exactly (§4), and the glass-cannon-affinity templates were bumped from `3x`- to `4x`-tier to match Core's own v2 bump (§4, §5).
**Depends on:** [`core-rules-v2.md`](core-rules-v2.md) §3 (damage model); [`pets.md`](pets.md) (the v2 roster this deck re-skins — same names, HP, archetype, flavour, art)
**Scope:** A second, harder printing of the same 22 pets — same names, HP, archetype, flavour, and art. Only the three attack equations change.

---

## 1. Purpose

Core's pet attacks are always `ax + b` — the same shape as every modifier — so "collect like terms" is a single trivial merge. This deck raises the algebra one notch **without touching anything else**: characters, environments, the trading phase, the battle loop, the `±x` modifier system, and the after-modifiers floor-at-0 rule are all untouched. A Challenge pet card is a **drop-in swap** for its Core counterpart — same HP tracker, same art, same name — so a class can mix Core and Challenge decks freely, or a teacher can hand a stronger pair the Challenge card for the same monster.

Two new base-attack forms are added, and — per the design conversation — **every pet's three attacks use one of them** (not a mix of easy/hard on one card):

1. **Bracket** — printed unexpanded, e.g. `3(x − 1)`. The student must expand it to `3x − 3` before doing anything else.
2. **Negative coefficient** — e.g. `−3x + 10`. Damage now *shrinks* as the roll grows.

Both forms **expand to the same `ax + b` family** the rest of the game already knows how to handle. That is deliberate: it means the damage model, the answer-key *shape*, and the battle sheet need no redesign — only the pet-card content and the tools that generate it change.

## 2. The two new forms

### 2.1 Bracket

```
a(x + b)   or   a(x − b)
```

- `a ∈ {2, 3, 4}` — **1 is excluded**: multiplying by 1 isn't real distribution practice, so it wouldn't earn its place as a "harder" attack. (4 added in the v2 pass for the glass-cannon-affinity template, §4.)
- `b ∈ {1, 2}`.
- Printed exactly as authored (unexpanded). Expands to `ax ± ab`.

### 2.2 Negative coefficient

```
−a·x + b
```

- `a ∈ {1, 2, 3, 4}` (4 added in v2, for the glass-cannon-affinity template N4, §4).
- `b` is chosen per template (§4) so the attack's range stays proportionate to what a Core pet of the same archetype would deal — not fixed to Core's `b ∈ {−3..3}` band, since these attacks need a bigger constant to have any bite at a roll of 1.
- Printed as authored — no expansion needed, but combining it with a modifier requires care (see §3).

Internally, once parsed, **every attack — plain, bracket, or negative — reduces to a canonical `(a, b)` pair** (`a` may now be negative). All derived card content (affinity, the printed damage range, the `(min 1)` check) is computed from that canonical pair, regardless of which form was authored. The card only ever displays the authored form.

## 3. Two things worth teaching explicitly

**The floor rule generalizes, it doesn't change.** Core already floors a base attack at 1 wherever it would hit 0 or below, printing `(min 1)`. That always happened at the low-roll end (`x = 1`) before, because every base attack had a positive coefficient. Now:

- Positive coefficient (plain or bracket): worst roll is still `x = 1`.
- Negative coefficient: worst roll is `x = 6` — **your best possible die roll**. A steep negative attack can legitimately floor at 1 on a 6. This is intentional: some attacks become a "hope for a low roll" gamble, big at 1–2, floored at 5–6. Because the forms are linear (monotonic), checking the one relevant endpoint is always sufficient — no need to scan every roll.

**A positive modifier softens a negative attack; it doesn't strengthen it.** Modifiers are always a plain `+x` or `−x` added to whatever the base attack already is. For a positive-coefficient attack, a character's `+x` buff steepens the slope (bigger numbers, bigger swings). For a negative-coefficient attack, that same `+x` buff **partially cancels the negative coefficient** — flattening the curve toward a constant, not steepening it further negative. Example: `−4x + 13` with a High-Magic `+x` and a Boosting environment `+2x` becomes `−x + 13`, not `−7x + 13`. This is a genuine, teachable consequence of "modifiers are terms you add," not a special case to implement — call it out in the Challenge rulebook addendum so it reads as a feature, not a bug.

## 4. Template pool  *(v2)*

Eight templates cover every archetype, mirroring Core's own efficiency (pets.md §5: only 12 distinct base equations across all 22 pets). Range shown is the *base attack alone*, before any modifier, floored per §3.

| # | Form | Expands to | Range (x=1..6) | Power tier |
|---|---|---|---|---|
| B1 | `2(x + 1)` | `2x + 2` | 4, 6, 8, 10, 12, 14 | tank affinity / secondary |
| B2 | `2(x − 1)` | `2x − 2` (min 1) | 1, 2, 4, 6, 8, 10 | off-affinity, any archetype |
| B3 | `3(x + 1)` | `3x + 3` | 6, 9, 12, 15, 18, 21 | baseline affinity |
| B4 | `3(x − 1)` | `3x − 3` (min 1) | 1, 3, 6, 9, 12, 15 | off-affinity, swingy |
| **B5** | `4(x + 1)` | `4x + 4` | 8, 12, 16, 20, 24, 28 | **glass-cannon affinity (v2)** |
| N1 | `−x + 5` | — | 4, 3, 2, 1, 1, 1 | weak/off-affinity |
| N2 | `−2x + 8` | — | 6, 4, 2, 1, 1, 1 | baseline/tank affinity |
| **N4** | `−4x + 13` | — | 9, 5, 1, 1, 1, 1 | **glass-cannon affinity, v2 (was N3 `−3x + 10`)** |

**v2 change:** Core's own glass-cannon affinity moved from `3x`-tier to `4x`-tier (docs/design/pets.md §3), so the Challenge glass-cannon affinity slot moves with it — B3/N3 (both `|a|=3`) are replaced by B5/N4 (`|a|=4`) wherever a Glass cannon card uses them. B3 stays exactly as it was for Baseline pets (their affinity is still `3x`-tier in Core too), and B1/B2/B4/N1/N2 are unchanged — those tiers didn't move. Only 6 of the 66 authored attacks actually changed (the one glass-cannon-affinity slot on each of the 6 Glass cannon pets); HP changed on all 22 (see below).

**HP (v2 change):** Challenge HP now copies Core's v2 bands and per-pet values exactly — Glass cannon 36–44, Baseline 68–82, Tank 95–110 (was a separate, lower v1-era band). This is what makes a Challenge card a genuine drop-in swap for its Core counterpart again, since Core's own HP moved up in its v2 pass and Challenge hadn't followed until now.

Authoring guidance for the 22 × 3 grid (done as part of implementation, enforced by the generator, not hand-fixed here):

- **Glass cannon** (HP 36–44): one attack from {B5, N4} (its affinity — highest `|a|`), the other two from {B1, B2, N1, N2}.
- **Baseline** (HP 68–82): one attack from {B1, B3, N2} as affinity, the other two from {B2, B4, N1}.
- **Tank** (HP 95–110): affinity from {B2, N2} — tanks win on HP, not damage, same as Core; the other two from {N1, B2}. In practice, satisfying "at least one bracket and one negative" with only {B2, N1, N2} available means every Tank ends up pairing two `|a| = 2` templates (B2 with N2), which ties for the affinity computation — **every Challenge Tank reads "Balanced."** This is intentional, not a bug: it's a stronger version of Core's own stance that Tanks win on HP rather than a signature hit, and it was chosen over the alternative (dropping to only two distinct templates per Tank, e.g. B2 + N1 twice) because that alternative would force at least two of the six Tanks into an identical Magic/Strike/Agility arrangement — variety of arrangement was judged more valuable than a differentiated affinity label for an archetype that isn't supposed to have one anyway.
- Every pet still gets **all three attack types** (magic/strength/agility). **Every individual pet's three attacks must include at least one bracket form and at least one negative-coefficient form** — no card gets three of the same form. Vary which attack type carries which template pet-to-pet, same as Core does with its own templates. Note the Baseline pool has the same tension in miniature: B4 (`|a|=3`) can outrank the intended B1/B3/N2 affinity pick when both land on one card, so a handful of Baseline pets' computed affinity isn't the template that was meant to be "the" affinity slot — harmless (the card's numbers are still correct and archetype-appropriate), just a label that doesn't always match authoring intent.
- Affinity is "the attack type with the largest `|a|`" (generalized from Core's own "largest `a`" once `a` can be negative). It always lines up with which attack type is Core's own affinity for that pet — that continuity was preserved through the v2 template swap.

## 5. Balance check  *(v2)*

Same success criteria as Core (pets.md §3 "Balance targets"): no un-boosted attack one-shots any pet; a fully-aligned stack — character High `+x` and environment Boost `+2x`, the same combination Core's own burst check uses — can burst a 36–44 HP glass cannon. "Everything against it" means character Low `−x` and environment Weaken `−2x` on your *own* attack — v2 has no defensive stat, so the opponent's stat never touches your damage roll.

| Scenario | Combine | Roll | Result |
|---|---|---|---|
| B5 affinity, un-boosted | `4x+4` | 6 | 28 — doesn't one-shot another 36–44 HP glass cannon |
| B5 affinity, full favourable stack | `4x+4 +x +2x` = `7x+4` | 6 | **46** — one-shots a glass cannon (bursts the whole 36–44 band), takes a 68–82 HP baseline to a bit over half in one hit |
| B5, everything against it | `4x+4 −x −2x` = `x+4` | 1 | 5 — never dead weight |
| N4 affinity, full favourable stack | `−4x+13 +x +2x` = `−x+13` | 1 (best roll for this attack) | 12 |
| N4, same stack, worst roll for this attack | `−x+13` | 6 | 7 — still a real hit, just smaller |
| N4, hostile stack | `−4x+13 −x −2x` = `−7x+13` | 1 (best roll) | 6 |
| N4, hostile stack, worst roll | `−7x+13` | 6 | `−29` → floors to **0** (post-modifier floor — the base attack's own `(min 1)` floor no longer applies once modifiers are in play) |

N4's favourable-stack ceiling (12) doesn't reach the glass-cannon-burst threshold the way B5's does (46) — negative-coefficient attacks trade that burst potential for their own risk profile (reliable-ish at a low roll, never dead at zero on its own thanks to the base floor, never a game-swinging burst). That asymmetry is intentional, not a gap: it's a different reason to pick a pet, not a worse one. This mirrors Core's own asymmetry between its `4x`-tier affinity (burst-capable) and its `2x` secondary (reliable, not a burst) — Challenge's bracket/negative split reproduces the same design idea one notch harder to compute.

## 6. What doesn't change

- Character cards, environment cards, HP bands, archetypes, names, flavour, art — identical to Core.
- The trading phase, battle loop, ladder, and capture rule.
- The `±x`/`±2x` modifier system and the post-modifier floor-at-0 rule (`core-rules-v2.md` §3.1).
- The battle sheet — a Challenge attack still resolves through the same five steps (build → collect like terms → substitute → floor → subtract), with one new zeroth step: *if the base attack isn't already in `ax+b` form, expand or simplify it first.*

## 7. Tooling

- **Source:** `cards/pets-challenge.md` — same 22 rows as `cards/pets.md` (Name, Archetype, Flavour copied verbatim; HP copies Core's v2 value per pet), Magic/Strength/Agility equations in the forms from §2.
- **`tools/gen_pet_cards.py --variant challenge`** (mirrors the existing `gen_cards.py --variant female` pattern): reads `cards/pets-challenge.md`, reuses the *same* art directory (`cards/art/pets/` — identical monsters, identical pictures), writes `cards/pets-challenge.html`.
- **Parser**: the equation grammar accepts all three forms (plain `ax+b` stays legal, for the rare case an author wants it) and reduces each to a canonical `(a, b)` pair, `a` possibly negative. Bracket's coefficient range is `a∈{2,3,4}` (widened from `{2,3}` in v2 for the B5 template).
- **Derived fields**, generalized to work off the canonical pair: affinity (by `|a|`), the printed 1→6 damage range, and the `(min 1)` check (evaluated at `x=1` if `a>0`, `x=6` if `a<0`).
- **Validation** (generator exits non-zero on violation, same as Core): every attack matches one of the two new forms (or plain); `a`/`b` within the ranges in §2; HP inside its archetype band (Core's v2 bands, shared); `(min 1)` printed exactly when required, never otherwise; every pet has all three attack types; both forms appear at least once per pet.

## 8. Answer key  *(v2)*

Once modifiers are applied, a Challenge attack is still a single `nx + c` — modifiers only ever add `±x` terms, never touch the constant, so `c` is always exactly the base attack's own constant (or `a·b` for a bracket). The lookup table (`rulebook/answer-key.md` §2a/§2b, generated by `tools/gen_lookup.py`) covers every `(n, c)` the deck's three negative-form templates (`c ∈ {5, 8, 13}`) can reach once shifted by the `±3` combined modifier range — including the case where a large enough favourable stack pushes a *weak* negative attack (N1/N2) to a small **positive** `n` (§2a), not just negative `n`. The `4(x+1) = 4x+4` bracket also needs one small extra table (§2b) since its constant (`4`) sits one above Core's own `c` range.

## 9. Documentation changes

- **`core-rules-v2.md` §9** — Challenge deck row marked done, pointing here.
- **Rulebook — "Challenge Mode" addendum** (student-facing, §10 of `student-rulebook.md`): explains the zeroth step (expand/simplify first), shows one bracket worked example and one negative-coefficient worked example end to end (including a modifier interacting with each), and states plainly that a Challenge card swaps in for its Core counterpart — everything else about the game is unchanged.
- **`rulebook/teacher-guide.md`** §10 — what Challenge is, that it's a drop-in swap for v2, and which answer-key sections mark it.
- **`rulebook/answer-key.md`** — the extended table from §8 (§2a, §2b).
- **`README.md`** — components + build status.

No change to the student rulebook's core rules, the battle sheet template, or any character/environment content.

## 10. Verification checklist

- [x] Every Challenge attack parses to one of: plain `ax+b`, bracket `a(x±b)` with `a∈{2,3,4}, b∈{1,2}`, or negative `−ax+b` with `a∈{1,2,3,4}`.
- [x] `(min 1)` printed exactly when the canonical `(a,b)` pair evaluates to ≤0 at its worst roll (`x=1` for `a>0`, `x=6` for `a<0`), never otherwise.
- [x] Every pet: all three attack types present, HP inside its archetype band (same v2 bands as Core, copied verbatim per pet), both new forms appear at least once on the card.
- [x] Affinity = attack type with the largest `|a|` (or *Balanced* on a tie); matches Core's own affinity type for every pet.
- [x] §5's worked ceiling numbers reproduced independently and matched.
- [x] `python tools/gen_pet_cards.py --variant challenge` runs clean and is idempotent (`--check` after two runs).
- [x] `python tools/gen_pet_cards.py` (no variant) still produces byte-identical output to before this change — Core is untouched.
- [x] Print preview: 22 cards, same 3-page layout as Core, same art, nothing clipped.
- [x] Extended answer-key table: every `(n, c)` pair that the 22-pet Challenge roster can actually produce (base × up to `±3` from modifiers) has a row (§2a + §2b).

## 11. Out of scope

- Indices (`x²`, `x³`) — a separate, larger project (its own damage-scale rebalance, and paired with the "environments can neutralise a whole attack type" idea raised alongside it). Not part of this deck.
- A Challenge variant of characters or environments — only pets change in this pass.
- Re-authoring pet names, flavour, HP, or archetype — all copied verbatim from Core.
- New art — the Challenge deck reuses `cards/art/pets/` exactly as-is.
