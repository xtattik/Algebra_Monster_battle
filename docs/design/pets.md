# Algebra Monster Battle — Pet Collection Design

**Date:** 2026-09-02 · **v2 rebalance:** 2026-09-10
**Status:** Draft for review — v2 numbers are provisional, first playtest pending.
**Depends on:** [`core-rules-v2.md`](core-rules-v2.md) §3, §6
**Scope:** The 22-pet starter collection for v2 — HP, the three attack equations per pet, names, flavour.

---

## 1. Purpose

Each pet has an **HP / archetype** and **three attack equations** (magic / **strength** / agility — "strength" renamed from "strike" in v2), each `ax + b` with a printed floor where it could otherwise drop below 1. Affinity is carried **in the equations**, never as a modifier. This spec picks the numbers for the 22-pet starter set.

**v2 rebalance** (from playtest): **HP up** (longer, higher-swing matches; variance evens out) and the **off-affinity secondary attack buffed to `2x`** so a pet whose best attack is cancelled by the terrain still has a real turn.

## 2. What goes on a pet card

1. **Name** and an art box — dashed placeholder until a file lands in `cards/art/pets/` (see [`../cards/art/README.md`](../cards/art/README.md)).
2. **HP** (the pet's health pool) and its **archetype** (Glass cannon / Baseline / Tank).
3. **Affinity** — the attack type with the highest `x`-coefficient (or *Balanced* on a tie). Derived by the generator, not authored; it is a reading aid for the trading phase.
4. **Three attack rows**, always in magic / strength / agility order, each showing:
   - the attack's **name**,
   - its **equation** `ax + b`, with `(min 1)` printed when `a + b < 1`,
   - its **damage range** — the value at a roll of 1 (floored at 1) to the value at a roll of 6, *before* any modifier. A quick "is this worth using" cue.
5. A **flavour line**.
6. A **card number**.

## 3. Number model (v2)

| Archetype | HP band | Affinity attack | Secondary | Third |
|---|---|---|---|---|
| **Glass cannon** | 36–44 | `4x` / `4x + 1` (max 24–25) | `2x` | `x − 1 (min 1)` / `x` |
| **Baseline** | 68–82 | `3x + 1` / `3x + 2` (max 19–20) | `2x` / `2x + 1` | `x + 1` |
| **Tank** | 95–110 | `3x` / `2x + 2` (max 14–18) | `2x` | `x` / `x − 1 (min 1)` |

Constraints the generator enforces:

- Coefficient `a ∈ {1 … 4}`; constant `b ∈ {−3 … 3}`. Every attack has an `x` term.
- `(min 1)` is printed **exactly when** a roll of 1–6 could give less than 1.
- HP must sit inside its archetype's band (v2 bands above; the Challenge deck keeps the v1 bands).
- All three attack types present.

### Balance targets (v2)

- No **un-boosted** attack one-shots any pet.
- A **fully-aligned glass-cannon burst**: `4x + 1` affinity + character `+x` + environment `Boost +2x` → `7x + 1`, roll 6 → **43**. One-shots a ~40 HP glass cannon on a 5–6; takes a 75 HP baseline to about a third (≈3 hits). The glass cannon has ~40 HP and dies to a baseline in ~3–4 turns — a race it wins by spiking, loses by low-rolling.
- **Cancelled affinity → the `2x` secondary** still deals 2–12 per turn: a real turn, not a forfeit.
- Tank affinity tops out at 18 (`3x` at roll 6). Tanks win by outlasting. *(Tank mirrors run ~10 turns each — flagged in [`core-rules-v2.md`](core-rules-v2.md) §10.)*
- Lowest attacks (`x − 1 (min 1)`) still deal 1–5. No attack is dead weight.
- Max coefficient a student's simplified `nx + c` can reach: **`7x`** (a `4x` attack + `+x` + `+2x`). The fast-marking lookup table (`answer-key.md`) extends to `8x`.

## 4. The 22 pets

Authored content is the source of truth in [`../cards/pets.md`](../cards/pets.md); reproduced here for review.

| # | Name | HP | Archetype | Magic | Strength | Agility | Affinity |
|---|---|---|---|---|---|---|---|
| 1 | Emberwisp | 40 | Glass cannon | Cinderburst `4x + 1` | Singe `x − 1 (min 1)` | Flit `2x` | Magic |
| 2 | Gorehoof | 42 | Glass cannon | Snort `x − 1 (min 1)` | Goring Charge `4x + 1` | Trample `2x` | Strength |
| 3 | Dartclaw | 38 | Glass cannon | Static Lick `x` | Tail Whip `2x` | Blink Slash `4x + 1` | Agility |
| 4 | Sootmane | 76 | Baseline | Warding Roar `x + 1` | Pounce `3x + 1` | Prowl `2x` | Strength |
| 5 | Tidecaller | 74 | Baseline | Tidal Pulse `3x + 1` | Tail Slap `x + 1` | Slip Away `2x` | Magic |
| 6 | Gustling | 72 | Baseline | Whisper Gale `2x` | Buffet `x + 1` | Cyclone Kick `3x + 1` | Agility |
| 7 | Patchwork Golem | 80 | Baseline | Spark Seam `2x` | Hammer Fist `2x + 1` | Lumber `2x` | Balanced |
| 8 | Riftmoth | 70 | Baseline | Dust of Ages `x` | Wing Slam `2x` | Phase Flurry `4x − 2` | Agility |
| 9 | Grave Hound | 74 | Baseline | Baying Howl `x − 1 (min 1)` | Bone Crush `3x + 1` | Lunge `2x − 1` | Strength |
| 10 | Boulderhide | 100 | Tank | Dust Cloud `2x` | Shell Bash `3x` | Withdraw `x` | Strength |
| 11 | Old Cairn | 98 | Tank | Root Surge `3x` | Deadfall `2x` | Slow Creak `x − 1 (min 1)` | Magic |
| 12 | Moss Troll | 104 | Tank | Spore Cloud `2x + 1` | Heavy Club `2x + 1` | Shamble `2x` | Balanced |
| 13 | Sparkhound | 39 | Glass cannon | Arc Bite `4x` | Nip `x − 1 (min 1)` | Dash `2x` | Magic |
| 14 | Bristlecharge | 41 | Glass cannon | Huff `x − 1 (min 1)` | Spine Rush `4x + 1` | Sidestep `2x` | Strength |
| 15 | Quickfin | 38 | Glass cannon | Bubble `2x` | Fin Slap `x` | Riptide Dart `4x + 1` | Agility |
| 16 | Cindercat | 75 | Baseline | Ember Purr `3x + 2` | Swipe `x + 1` | Slink `2x` | Magic |
| 17 | Ironhide Ram | 78 | Baseline | Bleat `x + 1` | Headbutt `3x + 2` | Scramble `2x` | Strength |
| 18 | Zephyr Kite | 72 | Baseline | Updraft `2x` | Talon Rake `x + 1` | Divebomb `3x + 2` | Agility |
| 19 | Clockwork Beetle | 80 | Baseline | Spark Coil `2x` | Pincer `2x + 1` | Scuttle `2x` | Balanced |
| 20 | Barrow Wight | 96 | Tank | Chill Touch `2x` | Grave Reach `3x` | Drift `x` | Strength |
| 21 | Deepstone Toad | 98 | Tank | Mud Bolt `3x` | Bellyflop `2x` | Hunker `x − 1 (min 1)` | Magic |
| 22 | Rust Golem | 102 | Tank | Oxide Cloud `x − 1 (min 1)` | Iron Fist `3x` | Grind Forward `2x` | Strength |

Spread: 6 glass cannons, 10 baselines, 6 tanks. Affinity — Magic ×6, Strength ×8, Agility ×5, Balanced ×3.

Swingy pets (a negative constant with no floor, `a + b ≥ 1`): Riftmoth `4x − 2`, Grave Hound `2x − 1`.

## 5. Fast-marking table

12 distinct base equations across the 22 pets. Each attack at `x = 1..6`, floored at 1, **before any modifier** — regenerate with `python tools/gen_pet_cards.py --table`:

| eqn | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `4x + 1` | 5 | 9 | 13 | 17 | 21 | 25 |
| `4x` | 4 | 8 | 12 | 16 | 20 | 24 |
| `4x − 2` | 2 | 6 | 10 | 14 | 18 | 22 |
| `3x + 2` | 5 | 8 | 11 | 14 | 17 | 20 |
| `3x + 1` | 4 | 7 | 10 | 13 | 16 | 19 |
| `3x` | 3 | 6 | 9 | 12 | 15 | 18 |
| `2x + 1` | 3 | 5 | 7 | 9 | 11 | 13 |
| `2x` | 2 | 4 | 6 | 8 | 10 | 12 |
| `2x − 1` | 1 | 3 | 5 | 7 | 9 | 11 |
| `x + 1` | 2 | 3 | 4 | 5 | 6 | 7 |
| `x` | 1 | 2 | 3 | 4 | 5 | 6 |
| `x − 1 (min 1)` | 1 | 1 | 2 | 3 | 4 | 5 |

Once a student has *added* modifiers and collected like terms, mark from the `nx + c` lookup table in [`../rulebook/answer-key.md`](../rulebook/answer-key.md) instead (extended to `8x` for v2).

## 6. Deck size for a class

22 designs × **3 copies each = 66 cards** → every student in a class of 30 draws 2, with duplicates possible but uncommon. For a bigger class, print more copies rather than adding designs.

## 7. Print layout

**Files:** [`../cards/pets.md`](../cards/pets.md) → `tools/gen_pet_cards.py` → `../cards/pets.html`.

- Same 63 mm × 88 mm card and A4 sheet as the other decks (shared `tools/cardsheet.py`). 22 cards → **3 pages** (9 + 9 + 4); `cardsheet.py` forces a page break every 9 cards.
- HP shown large in the header; archetype + affinity as a sub-line.
- Each attack row: type label · name · equation (equation in the serif face used for maths elsewhere) · `(min 1)` badge where present · the 1→6 range in grey.
- Black on white; no red needed (pets carry no defensive / enemy-Strength content).
- Art box: full width × ~26 mm hero image that replaces the name header when present, centre-cropped; embedded from `cards/art/pets/NN-slug.*` when present. See [`../cards/art/README.md`](../cards/art/README.md).
- Self-contained HTML (art is base64-embedded); "Print to PDF" gives the deck.
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
