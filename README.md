# Algebra Monster Battle

A print-and-play classroom card game for lower-secondary maths. Each student picks a fantasy character, is dealt two monster pets at random, spends a few minutes trading to cover their weak stat, then duels other students 1v1 in a randomly drawn environment. Every attack is a piece of algebra: build a linear expression from the pet's base attack plus signed `±x` modifier terms, collect like terms into a single `nx + c`, then substitute a D6 roll for `x` to find the damage (floored at zero). You cannot take a turn without doing the maths.

## Learning goal

NSW Mathematics **Stage 4 — Algebraic Techniques**: collecting like terms, substituting values into linear expressions and evaluating, and working with negative constants and results that floor at zero. Every modifier is an `x` term rather than a bare number, so the like-terms step is unavoidable. *(Teachers should confirm the exact current outcome code against their own programming.)*

## Components

- [7 character cards](cards/characters.html) (print a class set so several students can share a design)
- [22 pet cards](cards/pets.html) (print ~3 copies each so every student draws 2 at random)
- [8 environment cards](cards/environments.html) (one card drawn per match)
- one six-sided die per pair
- HP counters or mini-whiteboards
- [Student rulebook](rulebook/student-rulebook.md)
- [Teacher guide](rulebook/teacher-guide.md)
- [Fast-marking answer key](rulebook/answer-key.md) (lookup table plus worked scenarios)
- [Battle sheet](worksheets/battle-sheet.html) — the guided working + HP-tracking pad, one per match

## Build status

- [x] Core rules design ([`docs/design/core-rules.md`](docs/design/core-rules.md))
- [x] Student rulebook, teacher guide, answer key, battle sheet
- [x] Character card set — 7 designs, [design doc](docs/design/characters.md) + [print sheet](cards/characters.html)
- [x] Environment deck — 8 cards, [design doc](docs/design/environments.md) + [print sheet](cards/environments.html)
- [x] Pet collection — 22 pets, [design doc](docs/design/pets.md) + [print sheet](cards/pets.html)

All card sets drafted — next is playtesting.

Each card set gets its own design doc in `docs/design/`. Some V2 ideas (extreme pets such as a 200 HP Hill Giant that never heals; a written inequality to justify each trade) are noted in the design doc but are out of scope for now.

## Repo layout

- `docs/design/` — design docs
- `docs/plans/` — implementation plans
- `rulebook/` — student rulebook, teacher guide, answer key
- `worksheets/` — the printable battle sheet (guided working + HP track)
- `cards/` — card content (source of truth `.md`) and generated print sheets (`.html`)
- `cards/art/` — optional per-card artwork, embedded into the sheets on regenerate ([convention](cards/art/README.md))
- `tools/` — `gen_lookup.py` (answer-key table), `gen_cards.py` / `gen_env_cards.py` / `gen_pet_cards.py` (print sheets), `cardsheet.py` (shared layout)

## How to print and play

1. Teachers start with the [teacher guide](rulebook/teacher-guide.md): prep list, run sheet, timing, what to do with eliminated students, common student errors, and differentiation.
2. Give each student the [student rulebook](rulebook/student-rulebook.md) and a copy of the [battle sheet](worksheets/battle-sheet.html).
3. Print the three card sheets (`cards/*.html`) — open in a browser and "Print to PDF" at A4, 100% scale. To regenerate a sheet after editing its `cards/*.md` source, run the matching `tools/gen_*.py`.
4. Mark against the [answer key](rulebook/answer-key.md). To regenerate its lookup table, run `python tools/gen_lookup.py`.

The full game design lives in [`docs/design/core-rules.md`](docs/design/core-rules.md).
