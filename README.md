# Algebra Monster Battle

A print-and-play classroom card game for lower-secondary maths. Each student picks a fantasy character, is dealt two monster pets at random, spends a few minutes trading, then duels other students 1v1 in a randomly drawn environment. Every attack is a piece of algebra: pick an attack, build a linear expression from the pet's base attack plus signed `±x` / `±2x` terms, collect like terms into a single `nx + c`, then substitute a D6 roll for `x` to find the damage (floored at zero). You cannot take a turn without doing the maths.

> **This branch is Rules v2** — parallel offensive stats (each stat buffs its own attack type; no defence stat), a `±2x` environment dial with a **Cancel** verb, rebalanced pets, and a simpler choose-then-roll battle sheet. Design record: [`docs/design/core-rules-v2.md`](docs/design/core-rules-v2.md). The v1 design is kept in [`docs/design/core-rules.md`](docs/design/core-rules.md).

## Learning goal

NSW Mathematics **Stage 4 — Algebraic Techniques**: collecting like terms, substituting values into linear expressions and evaluating, and working with negative constants and results that floor at zero. Every modifier is an `x` term rather than a bare number, so the like-terms step is unavoidable. *(Teachers should confirm the exact current outcome code against their own programming.)*

## Components

- [7 character cards](cards/characters.html) (print a class set so several students can share a design)
- [22 pet cards](cards/pets.html) (print ~3 copies each so every student draws 2 at random)
- [15 environment cards](cards/environments.html) (one drawn per match; print your own mix of copies)
- [optional Challenge pet deck](cards/pets-challenge.html) — harder attacks (unexpanded brackets, negative coefficients); **not yet rebalanced for v2**
- one six-sided die per pair
- [Student rulebook](rulebook/student-rulebook.md)
- [Teacher guide](rulebook/teacher-guide.md)
- [Fast-marking answer key](rulebook/answer-key.md) (lookup table plus worked scenarios)
- [Battle sheet](worksheets/battle-sheet.html) — six attack blocks + HP tracks, one per match

## Build status (v2)

- [x] Core rules v2 ([`docs/design/core-rules-v2.md`](docs/design/core-rules-v2.md))
- [x] Character cards — parallel stats, no defence ([design doc](docs/design/characters.md))
- [x] Battle sheet — choose-then-roll, six blocks per page
- [x] Environment deck — 15 designs, 3-verb model ([design doc](docs/design/environments.md))
- [x] Pet collection — 22 pets rebalanced ([design doc](docs/design/pets.md))
- [x] Student rulebook + teacher guide + answer key rewritten for v2
- [ ] Playtest v2, then act on the open questions in `core-rules-v2.md` §10
- [ ] Challenge pet deck — still v1 balance; v2 pass deferred

## Repo layout

- `docs/design/` — design docs
- `docs/plans/` — implementation plans
- `rulebook/` — student rulebook, teacher guide, answer key
- `worksheets/` — the printable battle sheet (guided working + HP track)
- `cards/` — card content (source of truth `.md`) and generated print sheets (`.html`)
- `cards/art/` — optional per-card artwork, embedded into the sheets on regenerate ([convention](cards/art/README.md))
- `tools/` — `gen_lookup.py` (answer-key table), `gen_cards.py` / `gen_env_cards.py` / `gen_pet_cards.py` (print sheets), `cardsheet.py` (shared layout)

## How to print and play

1. Teachers start with the [teacher guide](rulebook/teacher-guide.md): prep, run sheet, timing, the losers' bracket, common errors, differentiation.
2. Give each student the [student rulebook](rulebook/student-rulebook.md) and a bundle of [battle sheets](worksheets/battle-sheet.html).
3. Print the card sheets (`cards/characters.html`, `cards/pets.html`, `cards/environments.html`) — open in a browser and "Print to PDF" at A4, 100% scale. After editing a `cards/*.md` source, re-run the matching `tools/gen_*.py`.
4. Mark against the [answer key](rulebook/answer-key.md) (`python tools/gen_lookup.py` regenerates its table).

The full v2 game design lives in [`docs/design/core-rules-v2.md`](docs/design/core-rules-v2.md).
