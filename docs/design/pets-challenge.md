# Algebra Monster Battle — Challenge Pet Deck Design

**Date:** 2026-09-05
**Status:** Draft for review
**Depends on:** [`core-rules.md`](core-rules.md) §5 (damage model), §11 (differentiation — already flags "pets with negative constants" as an extension); [`pets.md`](pets.md) (the roster this deck re-skins)
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

- `a ∈ {2, 3}` — **1 is excluded**: multiplying by 1 isn't real distribution practice, so it wouldn't earn its place as a "harder" attack.
- `b ∈ {1, 2}`.
- Printed exactly as authored (unexpanded). Expands to `ax ± ab`.

### 2.2 Negative coefficient

```
−a·x + b
```

- `a ∈ {1, 2, 3}`.
- `b` is chosen per template (§4) so the attack's range stays proportionate to what a Core pet of the same archetype would deal — not fixed to Core's `b ∈ {−3..3}` band, since these attacks need a bigger constant to have any bite at a roll of 1.
- Printed as authored — no expansion needed, but combining it with a modifier requires care (see §3).

Internally, once parsed, **every attack — plain, bracket, or negative — reduces to a canonical `(a, b)` pair** (`a` may now be negative). All derived card content (affinity, the printed damage range, the `(min 1)` check) is computed from that canonical pair, regardless of which form was authored. The card only ever displays the authored form.

## 3. Two things worth teaching explicitly

**The floor rule generalizes, it doesn't change.** Core already floors a base attack at 1 wherever it would hit 0 or below, printing `(min 1)`. That always happened at the low-roll end (`x = 1`) before, because every base attack had a positive coefficient. Now:

- Positive coefficient (plain or bracket): worst roll is still `x = 1`.
- Negative coefficient: worst roll is `x = 6` — **your best possible die roll**. A steep negative attack can legitimately floor at 1 on a 6. This is intentional: some attacks become a "hope for a low roll" gamble, big at 1–2, floored at 5–6. Because the forms are linear (monotonic), checking the one relevant endpoint is always sufficient — no need to scan every roll.

**A positive modifier softens a negative attack; it doesn't strengthen it.** Modifiers are always a plain `+x` or `−x` added to whatever the base attack already is. For a positive-coefficient attack, a character's `+x` buff steepens the slope (bigger numbers, bigger swings). For a negative-coefficient attack, that same `+x` buff **partially cancels the negative coefficient** — flattening the curve toward a constant, not steepening it further negative. Example: `−3x + 10` with a High-Magic `+x` and a boosting environment `+x` becomes `−x + 10`, not `−5x + 10`. This is a genuine, teachable consequence of "modifiers are terms you add," not a special case to implement — call it out in the Challenge rulebook addendum so it reads as a feature, not a bug.

## 4. Template pool

Seven templates cover every archetype, mirroring Core's own efficiency (pets.md §5: only 10 distinct base equations across all 22 pets). Range shown is the *base attack alone*, before any modifier, floored per §3.

| # | Form | Expands to | Range (x=1..6) | Power tier |
|---|---|---|---|---|
| B1 | `2(x + 1)` | `2x + 2` | 4, 6, 8, 10, 12, 14 | baseline/tank affinity |
| B2 | `2(x − 1)` | `2x − 2` (min 1) | 1, 2, 4, 6, 8, 10 | off-affinity, any archetype |
| B3 | `3(x + 1)` | `3x + 3` | 6, 9, 12, 15, 18, 21 | glass-cannon affinity |
| B4 | `3(x − 1)` | `3x − 3` (min 1) | 1, 3, 6, 9, 12, 15 | off-affinity, swingy |
| N1 | `−x + 5` | — | 4, 3, 2, 1, 1, 1 | weak/off-affinity |
| N2 | `−2x + 8` | — | 6, 4, 2, 1, 1, 1 | baseline/tank affinity |
| N3 | `−3x + 10` | — | 7, 4, 1, 1, 1, 1 | glass-cannon affinity |

Authoring guidance for the 22 × 3 grid (done as part of implementation, enforced by the generator, not hand-fixed here):

- **Glass cannon** (HP 26–32): one attack from {B3, N3} (its affinity — highest `|a|`), the other two from {B1, B2, N1, N2}.
- **Baseline** (HP 44–54): one attack from {B1, B3, N2} as affinity, the other two from {B2, B4, N1}.
- **Tank** (HP 76–84): affinity from {B2, N2} — tanks win on HP, not damage, same as Core; the other two from {N1, B2}.
- Every pet still gets **all three attack types** (magic/strike/agility). **Every individual pet's three attacks must include at least one bracket form and at least one negative-coefficient form** — no card gets three of the same form. Vary which attack type carries which template pet-to-pet, same as Core does with its own templates.
- Affinity is now "the attack type with the largest `|a|`" (was: largest `a`) — the generalization needed once `a` can be negative.

## 5. Balance check

Same success criteria as Core §5.6: no configuration one-shots a 50 HP pet; a fully favourable stack can burst a 26–32 HP glass cannon.

| Scenario | Combine | Roll | Result |
|---|---|---|---|
| B3 affinity, full favourable stack (character High `+x`, environment boost `+x`) | `3x+3 +x +x` = `5x+3` | 6 | **33** — bursts a glass cannon (≥26), needs 2 hits on a 50 HP pet |
| B3, everything against it (environment hinder `−x`, enemy High Strength `−x`) | `3x+3 −x −x` = `x+3` | 1 | 4 — never dead weight |
| N3 affinity, full favourable stack | `−3x+10 +x +x` = `−x+10` | 1 | 9 |
| N3, same stack, worst roll for this attack | `−x+10` | 6 | 4 |
| N3, hostile stack (hinder `−x`, enemy High Strength `−x`) | `−3x+10 −x −x` = `−5x+10` | 6 | `−20` → floors to **0** (post-modifier floor, §5.4 — the base attack's own `(min 1)` floor doesn't apply once modifiers are in play) |

N3's favourable-stack ceiling (9) doesn't reach the glass-cannon-burst threshold the way B3's does (33) — negative-coefficient attacks trade that burst potential for their own risk profile (reliable-ish at a low roll, never dead at zero because of the base floor, never a game-swinging burst). That asymmetry is intentional, not a gap: it's a different reason to pick a pet, not a worse one.

## 6. What doesn't change

- Character cards, environment cards, HP bands, archetypes, names, flavour, art — identical to Core.
- The trading phase, battle loop, ladder, and capture rule.
- The `±x` modifier system and the post-modifier floor-at-0 rule (§5.4 of core-rules.md).
- The battle sheet — a Challenge attack still resolves through the same five steps (build → collect like terms → substitute → floor → subtract), with one new zeroth step: *if the base attack isn't already in `ax+b` form, expand or simplify it first.*

## 7. Tooling

- **New source:** `cards/pets-challenge.md` — same 22 rows as `cards/pets.md` (Name, HP, Archetype, Flavour copied verbatim), new Magic/Strike/Agility equations in the forms from §2.
- **`tools/gen_pet_cards.py --variant challenge`** (mirrors the existing `gen_cards.py --variant female` pattern): reads `cards/pets-challenge.md`, reuses the *same* art directory (`cards/art/pets/` — identical monsters, identical pictures), writes `cards/pets-challenge.html`.
- **Parser**: extend the equation grammar to accept all three forms (plain `ax+b` stays legal, for the rare case an author wants it) and reduce each to a canonical `(a, b)` pair, `a` possibly negative.
- **Derived fields**, generalized to work off the canonical pair: affinity (by `|a|`), the printed 1→6 damage range, and the `(min 1)` check (evaluated at `x=1` if `a>0`, `x=6` if `a<0`).
- **Validation** (generator exits non-zero on violation, same as Core): every attack matches one of the two new forms (or plain); `a`/`b` within the ranges in §2; HP inside its archetype band (unchanged bands); `(min 1)` printed exactly when required, never otherwise; every pet has all three attack types; both forms appear at least once per pet.

## 8. Answer key

Once modifiers are applied, a Challenge attack is still a single `nx + c` — modifiers only ever add `±x` terms, never touch the constant, so `c` is always exactly the base attack's own constant (or `a·b` for a bracket). The existing lookup table (`rulebook/answer-key.md` §2, generated by `tools/gen_lookup.py`) only covers `n = 1..6`. Extend it with negative-coefficient rows for `n = −6..−1` (the base range `−1..−3` shifted by up to `±3` from the three `±x` modifier sources), using the same small constant set the §4 templates produce (`c ∈ {5, 8, 10}` for the templates above, plus whatever the full 22-pet authoring settles on — keep it to a similarly small, curated set rather than every integer, the same discipline Core used to keep its own table at 42 rows).

## 9. Documentation changes

- **`core-rules.md` §11** — the "pets with negative constants" extension line already anticipated this; update it to point here and mention brackets too.
- **`core-rules.md` §14** — add a phase 5 (Challenge pet deck).
- **Rulebook — new short "Challenge Mode" addendum** (student-facing): explains the zeroth step (expand/simplify first), shows one bracket worked example and one negative-coefficient worked example end to end (including a modifier interacting with each), and states plainly that a Challenge card swaps in for its Core counterpart — everything else about the game is unchanged.
- **`rulebook/teacher-guide.md`** — one paragraph: what Challenge is, that it's optional per pair/table, and the same two worked examples for the answer key.
- **`rulebook/answer-key.md`** — the extended table from §8.
- **`README.md`** — components + build status.

No change to the student rulebook's core rules, the battle sheet template, or any character/environment content.

## 10. Verification checklist

- [ ] Every Challenge attack parses to one of: plain `ax+b`, bracket `a(x±b)` with `a∈{2,3}, b∈{1,2}`, or negative `−ax+b` with `a∈{1,2,3}`.
- [ ] `(min 1)` printed exactly when the canonical `(a,b)` pair evaluates to ≤0 at its worst roll (`x=1` for `a>0`, `x=6` for `a<0`), never otherwise.
- [ ] Every pet: all three attack types present, HP inside its archetype band (same bands as Core), both new forms appear at least once on the card.
- [ ] Affinity = attack type with the largest `|a|` (or *Balanced* on a tie).
- [ ] §5's worked ceiling numbers reproduced independently and matched.
- [ ] `python tools/gen_pet_cards.py --variant challenge` runs clean and is idempotent (`--check` after two runs).
- [ ] `python tools/gen_pet_cards.py` (no variant) still produces byte-identical output to before this change — Core is untouched.
- [ ] Print preview: 22 cards, same 3-page layout as Core, same art, nothing clipped.
- [ ] Extended answer-key table: every `(n, c)` pair that the 22-pet Challenge roster can actually produce (base × up to `±3` from modifiers) has a row.

## 11. Out of scope

- Indices (`x²`, `x³`) — a separate, larger project (its own damage-scale rebalance, and paired with the "environments can neutralise a whole attack type" idea raised alongside it). Not part of this deck.
- A Challenge variant of characters or environments — only pets change in this pass.
- Re-authoring pet names, flavour, HP, or archetype — all copied verbatim from Core.
- New art — the Challenge deck reuses `cards/art/pets/` exactly as-is.
