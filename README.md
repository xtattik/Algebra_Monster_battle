# Algebra Monster Battle

A print-and-play classroom card game for lower-secondary maths. Each student picks a fantasy character, is dealt a pair of monster pets at random, spends a few minutes trading to shore up their weak stat, then fights other students in 1v1 duels. Every match is set in a randomly drawn environment, and every attack is a piece of algebra: the attacker builds a linear expression from the pet's base attack plus signed `±x` modifier terms, collects like terms into a single `nx + c`, then substitutes a D6 roll for `x` to find the damage (floored at zero). You cannot take a turn without doing the maths.

## Learning goal

NSW Mathematics **Stage 4 — Algebraic Techniques**: simplifying expressions by collecting like terms, substituting values into linear expressions and evaluating, and working with negative constants and results that floor at zero. Every modifier in the game is an `x` term rather than a bare number, so the like-terms step is unavoidable. *(Teachers should confirm the exact current outcome code against their own programming.)*

## Components

- 7 character cards (print a class set so several students can share a design)
- a pet deck (enough that every student draws 2 at random)
- an environment deck (one card drawn per match)
- one six-sided die per pair
- HP counters or mini-whiteboards
- [Student rulebook](rulebook/student-rulebook.md)
- [Teacher guide](rulebook/teacher-guide.md)
- [Fast-marking answer key](rulebook/answer-key.md) (lookup table plus worked scenarios)
- [Battle worksheet](worksheets/battle-worksheet.md) — the markable artifact, one row per attack

## Build status

- [x] Core rules design ([`docs/design/core-rules.md`](docs/design/core-rules.md))
- [x] Student rulebook, teacher guide, answer key, battle worksheet
- [ ] Character card set (7 designs) — next
- [ ] Environment deck
- [ ] Pet collection

The card sets each get their own design doc in `docs/design/`. Some V2 ideas (extreme pets such as a 200 HP Hill Giant that never heals; requiring a written inequality to justify each trade) are recorded in the design doc but are out of scope for now.

## Repo layout

- `docs/design/` — design docs
- `docs/plans/` — implementation plans
- `rulebook/` — student rulebook, teacher guide, answer key
- `worksheets/` — the battle worksheet
- `tools/` — `gen_lookup.py`, which regenerates the answer-key lookup table

## How to print and play

1. Teachers start with the [teacher guide](rulebook/teacher-guide.md): prep list, run sheet, timing, what to do with eliminated students, common student errors, and differentiation.
2. Give each student the [student rulebook](rulebook/student-rulebook.md) and a copy of the [battle worksheet](worksheets/battle-worksheet.md).
3. Mark against the [answer key](rulebook/answer-key.md). To regenerate its lookup table, run `python tools/gen_lookup.py`.

The full game design lives in [`docs/design/core-rules.md`](docs/design/core-rules.md).
