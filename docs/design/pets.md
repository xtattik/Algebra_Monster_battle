# Algebra Monster Battle — Pet Collection Design

**Date:** 2026-09-02
**Status:** Implemented — 22 pets, generator, and print sheet in the repo; core-rules §7/§13/§14, teacher guide §2, answer key updated.
**Depends on:** [`core-rules.md`](core-rules.md) §7, §5.4, §5.6
**Changes applied:** [`core-rules.md`](core-rules.md) §7 (→ pointer), §13, §14; teacher guide §2; answer key §2
**Scope:** The 22-pet starter collection — HP, the three attack equations per pet, names, flavour, and print layout.

---

## 1. Purpose

Core-rules §7 fixes the pet model: each pet has an **HP / archetype** and **three attack equations** (magic / strike / agility), each `ax + b` with a printed floor where it could otherwise drop below 1. Affinity is carried **in the equations**, never as a modifier. This spec picks the actual numbers and names for a starter set of 22 (12 distinct templates, the rest re-skins for name variety).

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

## 4. The 22 pets

Authored content is the source of truth in [`../cards/pets.md`](../cards/pets.md); reproduced here for review. Pets 13–22 were added purely for **name variety** — students hunt for a particular creature — and deliberately reuse the same stat and equation templates as pets 1–12.

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
| 13 | Sparkhound | 29 | Glass cannon | Arc Bite `3x + 1` | Nip `x − 1 (min 1)` | Dash `x + 1` | Magic |
| 14 | Bristlecharge | 31 | Glass cannon | Huff `x − 1 (min 1)` | Spine Rush `3x + 2` | Sidestep `x + 1` | Strike |
| 15 | Quickfin | 27 | Glass cannon | Bubble `x` | Fin Slap `x + 1` | Riptide Dart `3x + 2` | Agility |
| 16 | Cindercat | 49 | Baseline | Ember Purr `3x` | Swipe `x + 1` | Slink `2x` | Magic |
| 17 | Ironhide Ram | 52 | Baseline | Bleat `x + 1` | Headbutt `3x` | Scramble `2x` | Strike |
| 18 | Zephyr Kite | 45 | Baseline | Updraft `2x` | Talon Rake `x + 1` | Divebomb `3x` | Agility |
| 19 | Clockwork Beetle | 53 | Baseline | Spark Coil `2x` | Pincer `2x + 1` | Scuttle `2x − 1` | Balanced |
| 20 | Barrow Wight | 79 | Tank | Chill Touch `x − 1 (min 1)` | Grave Reach `2x + 1` | Drift `x` | Strike |
| 21 | Deepstone Toad | 80 | Tank | Mud Bolt `2x + 1` | Bellyflop `x + 1` | Hunker `x − 1 (min 1)` | Magic |
| 22 | Rust Golem | 83 | Tank | Oxide Cloud `x − 1 (min 1)` | Iron Fist `2x + 1` | Grind Forward `x` | Strike |

Spread: 6 glass cannons, 10 baselines, 6 tanks. Affinity — Magic ×6, Strike ×8, Agility ×5, Balanced ×3. No dedicated agility tank (a slow pet that dodges well is a contradiction); the balanced tanks cover that slot.

Negative constants without a printed floor (`3x − 2`, `2x − 1`) appear on Riftmoth, Patchwork Golem, Clockwork Beetle and Grave Hound — legal because `a + b ≥ 1` — a gentle on-ramp to the core-rules §11 "pets with negative constants" extension.

## 5. Fast-marking table

Across all 22 pets there are only **10 distinct base equations**. Every pet attack, at `x = 1..6`, floored at 1, **before any modifier**:

| eqn | 1 | 2 | 3 | 4 | 5 | 6 | used by |
|---|---|---|---|---|---|---|---|
| `3x + 2` | 5 | 8 | 11 | 14 | 17 | 20 | Emberwisp, Gorehoof, Bristlecharge, Quickfin |
| `3x + 1` | 4 | 7 | 10 | 13 | 16 | 19 | Dartclaw, Sparkhound |
| `3x` | 3 | 6 | 9 | 12 | 15 | 18 | Sootmane, Tidecaller, Gustling, Grave Hound, Cindercat, Ironhide Ram, Zephyr Kite |
| `3x − 2` | 1 | 4 | 7 | 10 | 13 | 16 | Riftmoth |
| `2x + 1` | 3 | 5 | 7 | 9 | 11 | 13 | Patchwork Golem, Boulderhide, Old Cairn, Clockwork Beetle, Barrow Wight, Deepstone Toad, Rust Golem |
| `2x` | 2 | 4 | 6 | 8 | 10 | 12 | many (off-affinity) |
| `2x − 1` | 1 | 3 | 5 | 7 | 9 | 11 | Patchwork Golem, Grave Hound, Clockwork Beetle |
| `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 | many (off-affinity) |
| `x` | 1 | 2 | 3 | 4 | 5 | 6 | many (off-affinity) |
| `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 | many (off-affinity) |

The full per-pet listing is generated by `python tools/gen_pet_cards.py --table`. Once a student has *added* modifiers and collected like terms, mark from the `nx + c` lookup table in [`../rulebook/answer-key.md`](../rulebook/answer-key.md) §2 instead.

## 6. Deck size for a class

22 designs × **3 copies each = 66 cards** → every student in a class of 30 draws 2, with duplicates possible but uncommon. For a bigger class, print more copies rather than adding designs.

## 7. Print layout

**Files:** [`../cards/pets.md`](../cards/pets.md) → `tools/gen_pet_cards.py` → `../cards/pets.html`.

- Same 63 mm × 88 mm card and A4 sheet as the other decks (shared `tools/cardsheet.py`). 22 cards → **3 pages** (9 + 9 + 4); `cardsheet.py` forces a page break every 9 cards.
- HP shown large in the header; archetype + affinity as a sub-line.
- Each attack row: type label · name · equation (equation in the serif face used for maths elsewhere) · `(min 1)` badge where present · the 1→6 range in grey.
- Black on white; no red needed (pets carry no defensive / enemy-Strength content).
- Self-contained HTML; "Print to PDF" gives the deck.
- The generator derives affinity, the min-badge, and the range; it validates every constraint in §3 and exits non-zero on a violation.

## 8. Changes to existing documents

- **`core-rules.md` §7** — replace the scope summary with a pointer here and the archetype/number model.
- **`core-rules.md` §13** — mark the pet open questions resolved (22 pets; HP/coefficients per §3; capture still moot since loss = elimination).
- **`core-rules.md` §14** — mark the pet collection done.
- **`rulebook/teacher-guide.md` §2** — pet deck prep: "22 designs, 3 copies each".
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
- [x] Print preview: 22 cards over 3 A4 pages (9 / 9 / 4), forced break every 9, nothing clipped.

## 10. Out of scope

- Extreme pets (Hill Giant, 200 HP, no heal) — core-rules §12 marks these V2.
- Pet art, card backs.
- Any per-pet special rule, keyword, typing, or ability beyond the three equations.
- Captured-pet card handling — still moot while a loss is an elimination (core-rules §13).
