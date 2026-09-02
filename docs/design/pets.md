# Algebra Monster Battle — Pet Collection Design

**Date:** 2026-09-02
**Status:** Implemented — 12 pets, generator, and print sheet in the repo; core-rules §7/§13/§14, teacher guide §2, answer key updated.
**Depends on:** [`core-rules.md`](core-rules.md) §7, §5.4, §5.6
**Changes applied:** [`core-rules.md`](core-rules.md) §7 (→ pointer), §13, §14; teacher guide §2; answer key §2
**Scope:** The 12-pet starter collection — HP, the three attack equations per pet, names, flavour, and print layout.

---

## 1. Purpose

Core-rules §7 fixes the pet model: each pet has an **HP / archetype** and **three attack equations** (magic / strike / agility), each `ax + b` with a printed floor where it could otherwise drop below 1. Affinity is carried **in the equations**, never as a modifier. This spec picks the actual numbers and names for a starter set of 12.

No rules change. The damage model, the `±x` modifier system, and the §5.4 minimums are untouched.

## 2. What goes on a pet card

1. **Name** and an art box (empty in v1).
2. **HP** (the pet's health pool) and its **archetype** (Glass cannon / Baseline / Tank).
3. **Affinity** — the attack type with the highest `x`-coefficient (or *Balanced* on a tie). Derived by the generator, not authored; it is a reading aid for the trading phase.
4. **Three attack rows**, always in magic / strike / agility order, each showing:
   - the attack's **name**,
   - its **equation** `ax + b`, with `(min 1)` printed when `a + b < 1`,
   - its **damage range** — the value at a roll of 1 (floored at 1) to the value at a roll of 6, *before* any modifier. A quick "is this worth using" cue.
5. A **flavour line**.
6. A **card number**.

## 3. Number model

| Archetype | HP band | Affinity attack | Off-affinity attacks |
|---|---|---|---|
| **Glass cannon** | 26–32 | `3x + 1` or `3x + 2` (max 19–20) | `x`, `x + 1`, or `x − 1 (min 1)` |
| **Baseline** | 44–54 | `3x` or `2x + 2` (max 14–18) | `2x`, `2x − 1`, `x + 1` |
| **Tank** | 76–84 | `2x + 1` (max 13) | `x`, `x + 1`, `x − 1 (min 1)` |

Constraints the generator enforces:

- Coefficient `a ∈ {1, 2, 3}`; constant `b ∈ {−3 … 3}`. Every attack has an `x` term (no bare-constant attacks).
- `(min N)` is printed **exactly when** `a + b < 1` (i.e. a roll of 1 would give 0 or less), and then `N` must be **1** — the universal §5.4 base-attack floor.
- HP must sit inside its archetype's band.
- All three attack types present.

### Why these ceilings

From core-rules §5.6, the balance target is: no configuration one-shots a 50 HP pet; a fully favourable stack can burst a 30 HP glass cannon.

- A `3x + 2` affinity attack + character `+x` + environment `Boosts` `+x` → `5x + 2`, roll 6 → **32**. One-shots a 28 HP glass cannon (intended); leaves a 50 HP pet at 18 (two hits).
- A tank's best, `2x + 1`, tops out at 13 — a tank wins by outlasting, not by hitting hard.
- The lowest attacks (`x − 1 (min 1)`) still deal 1–5. No attack is dead weight.

## 4. The 12 pets

Authored content is the source of truth in [`../cards/pets.md`](../cards/pets.md); reproduced here for review.

| # | Name | HP | Archetype | Magic | Strike | Agility | Affinity |
|---|---|---|---|---|---|---|---|
| 1 | Emberwisp | 28 | Glass cannon | Cinderburst `3x + 2` | Singe `x − 1 (min 1)` | Flit `x + 1` | Magic |
| 2 | Gorehoof | 30 | Glass cannon | Snort `x − 1 (min 1)` | Goring Charge `3x + 2` | Trample `x + 1` | Strike |
| 3 | Dartclaw | 26 | Glass cannon | Static Lick `x` | Tail Whip `x + 1` | Blink Slash `3x + 1` | Agility |
| 4 | Sootmane | 50 | Baseline | Warding Roar `x + 1` | Pounce `3x` | Prowl `2x` | Strike |
| 5 | Tidecaller | 48 | Baseline | Tidal Pulse `3x` | Tail Slap `x + 1` | Slip Away `2x` | Magic |
| 6 | Gustling | 46 | Baseline | Whisper Gale `2x` | Buffet `x + 1` | Cyclone Kick `3x` | Agility |
| 7 | Patchwork Golem | 54 | Baseline | Spark Seam `2x` | Hammer Fist `2x + 1` | Lumber `2x − 1` | Balanced |
| 8 | Riftmoth | 44 | Baseline | Dust of Ages `x` | Wing Slam `x + 1` | Phase Flurry `3x − 2` | Agility |
| 9 | Grave Hound | 46 | Baseline | Baying Howl `x − 1 (min 1)` | Bone Crush `3x` | Lunge `2x − 1` | Strike |
| 10 | Boulderhide | 82 | Tank | Dust Cloud `x − 1 (min 1)` | Shell Bash `2x + 1` | Withdraw `x` | Strike |
| 11 | Old Cairn | 78 | Tank | Root Surge `2x + 1` | Deadfall `x + 1` | Slow Creak `x − 1 (min 1)` | Magic |
| 12 | Moss Troll | 84 | Tank | Spore Cloud `2x` | Heavy Club `2x` | Shamble `x + 1` | Balanced |

Spread: 3 glass cannons, 6 baselines, 3 tanks. Affinity — Magic ×3, Strike ×4, Agility ×3, Balanced ×2. Every archetype covers each affinity at least once except tanks (no dedicated agility tank — a slow pet that dodges well is a contradiction; the balanced Moss Troll fills the gap).

Two pets (Riftmoth `3x − 2`, and the `2x − 1` attacks on Patchwork/Grave Hound) carry **negative constants without a printed floor** — legal because `a + b ≥ 1` — giving a gentler on-ramp to the core-rules §11 "pets with negative constants" extension.

## 5. Fast-marking table

Every pet attack's value at `x = 1..6`, floored at 1, **before any modifier** — the pet answer key. Once a student has *added* modifiers and collected like terms, use the main `nx + c` lookup table in [`../rulebook/answer-key.md`](../rulebook/answer-key.md) §2 instead. Regenerate this with `python tools/gen_pet_cards.py --table`.

| Pet · attack | eqn | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Emberwisp · Cinderburst | `3x + 2` | 5 | 8 | 11 | 14 | 17 | 20 |
| Emberwisp · Singe | `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 |
| Emberwisp · Flit | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Gorehoof · Snort | `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 |
| Gorehoof · Goring Charge | `3x + 2` | 5 | 8 | 11 | 14 | 17 | 20 |
| Gorehoof · Trample | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Dartclaw · Static Lick | `x` | 1 | 2 | 3 | 4 | 5 | 6 |
| Dartclaw · Tail Whip | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Dartclaw · Blink Slash | `3x + 1` | 4 | 7 | 10 | 13 | 16 | 19 |
| Sootmane · Warding Roar | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Sootmane · Pounce | `3x` | 3 | 6 | 9 | 12 | 15 | 18 |
| Sootmane · Prowl | `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| Tidecaller · Tidal Pulse | `3x` | 3 | 6 | 9 | 12 | 15 | 18 |
| Tidecaller · Tail Slap | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Tidecaller · Slip Away | `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| Gustling · Whisper Gale | `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| Gustling · Buffet | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Gustling · Cyclone Kick | `3x` | 3 | 6 | 9 | 12 | 15 | 18 |
| Patchwork Golem · Spark Seam | `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| Patchwork Golem · Hammer Fist | `2x + 1` | 3 | 5 | 7 | 9 | 11 | 13 |
| Patchwork Golem · Lumber | `2x − 1` | 1 | 3 | 5 | 7 | 9 | 11 |
| Riftmoth · Dust of Ages | `x` | 1 | 2 | 3 | 4 | 5 | 6 |
| Riftmoth · Wing Slam | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Riftmoth · Phase Flurry | `3x − 2` | 1 | 4 | 7 | 10 | 13 | 16 |
| Grave Hound · Baying Howl | `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 |
| Grave Hound · Bone Crush | `3x` | 3 | 6 | 9 | 12 | 15 | 18 |
| Grave Hound · Lunge | `2x − 1` | 1 | 3 | 5 | 7 | 9 | 11 |
| Boulderhide · Dust Cloud | `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 |
| Boulderhide · Shell Bash | `2x + 1` | 3 | 5 | 7 | 9 | 11 | 13 |
| Boulderhide · Withdraw | `x` | 1 | 2 | 3 | 4 | 5 | 6 |
| Old Cairn · Root Surge | `2x + 1` | 3 | 5 | 7 | 9 | 11 | 13 |
| Old Cairn · Deadfall | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| Old Cairn · Slow Creak | `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 |
| Moss Troll · Spore Cloud | `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| Moss Troll · Heavy Club | `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| Moss Troll · Shamble | `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |

## 6. Deck size for a class

12 designs × **5 copies each = 60 cards** → every student in a class of 30 draws 2, with duplicates expected and fine. Print more copies, not more designs, for a bigger class. The set can grow later; 12 keeps every number checkable for v1.

## 7. Print layout

**Files:** [`../cards/pets.md`](../cards/pets.md) → `tools/gen_pet_cards.py` → `../cards/pets.html`.

- Same 63 mm × 88 mm card and A4 sheet as the other decks (shared `tools/cardsheet.py`). 12 cards → **2 pages** (9 + 3).
- HP shown large in the header; archetype + affinity as a sub-line.
- Each attack row: type label · name · equation (equation in the serif face used for maths elsewhere) · `(min 1)` badge where present · the 1→6 range in grey.
- Black on white; no red needed (pets carry no defensive / enemy-Strength content).
- Self-contained HTML; "Print to PDF" gives the deck.
- The generator derives affinity, the min-badge, and the range; it validates every constraint in §3 and exits non-zero on a violation.

## 8. Changes to existing documents

- **`core-rules.md` §7** — replace the scope summary with a pointer here and the archetype/number model.
- **`core-rules.md` §13** — mark the pet open questions resolved (12 pets; HP/coefficients per §3; capture still moot since loss = elimination).
- **`core-rules.md` §14** — mark the pet collection done.
- **`rulebook/teacher-guide.md` §2** — pet deck prep: "12 designs, 5 copies each".
- **`rulebook/answer-key.md`** — one line noting pet base attacks are all within the §2 table, pointing here for the per-attack listing.
- **`README.md`** — components + build status.

No change to the student rulebook (it already describes how pets are used) or the worksheet.

## 9. Verification checklist

- [x] Every attack: `a ∈ {1,2,3}`, `b ∈ {−3..3}`, has an `x` term. Enforced by the generator.
- [x] `(min 1)` printed exactly when `a + b < 1`; never otherwise (and never `(min N≠1)`). Enforced.
- [x] Every HP inside its archetype band (§3). Enforced.
- [x] Affinity on the card = attack type with the strictly highest `a`, else *Balanced*. Derived.
- [x] §5 fast-marking table generated by `--table`, matches the equations.
- [x] Worst single-attack stack `3x + 2` + character `+x` + environment `+x` = `5x + 2` → 32 at roll 6: does not drop a 50 HP pet, does one-shot the 26–30 HP glass cannons.
- [x] `python tools/gen_pet_cards.py` runs clean, is idempotent (`--check` after two runs), rejects out-of-band HP / missing / spurious min / bad coefficient / nameless attack.
- [x] Print preview: 12 cards, page 1 holds 9, cards 10–12 flow onto page 2, nothing clipped.

## 10. Out of scope

- Extreme pets (Hill Giant, 200 HP, no heal) — core-rules §12 marks these V2.
- Pet art, card backs.
- Any per-pet special rule, keyword, typing, or ability beyond the three equations.
- Captured-pet card handling — still moot while a loss is an elimination (core-rules §13).
