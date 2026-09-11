# Algebra Monster Battle — Teacher Guide  *(v2)*

Assumes you have read the student rulebook (`rulebook/student-rulebook.md`). This
covers only what a teacher has to manage.

## 1. Purpose & curriculum

A resolution engine for NSW Mathematics **Stage 4 — Algebraic Techniques**. Every
attack forces the student to:

- assemble a linear expression from `ax + b` plus `±x` / `±2x` terms,
- **collect like terms** into a single `nx + c`,
- **substitute** a D6 roll for `x` and evaluate,
- work with **negative constants** and **floor the result at 0**.

Every modifier is an `x` term — never a bare number — so the like-terms step is
unavoidable. (Confirm the exact outcome code against your own programming.)

Runs as **one lesson** (setup + 2–3 ladder rounds) or **two** (add a full
trading/strategy discussion and a longer ladder).

## 2. Prep

- **Characters:** print one class set of the 7 designs (`cards/characters.html`),
  several copies of each. *(A female-art variant is at `cards/characters-female.html`.)*
- **Pet deck:** `cards/pets.html` — 22 designs; ~**3 copies of each** for a class
  of 30, so every student draws **2 at random**.
- **Environment deck:** `cards/environments.html` — **15 designs**. Print however
  many copies of each you want: **more boost cards = gentler; more Cancel cards =
  harder**. A starting mix of ~2 copies of each is fine. One deck per group of pairs.
- **Battle sheets:** `worksheets/battle-sheet.html` — a bundle, one A4 each. Six
  attack blocks per sheet; a match usually fits on one or two. It also carries
  both pets' HP tracks and the result box.
- **Dice:** one D6 per pair.

## 3. Run sheet

1. **Deal characters** — random is faster and forces adaptation.
2. **Draw pets** — 2 each, at random.
3. **Trading — 5 minutes, timed.** Prompt: *get a pet that matches your High
   stat, and keep a second pet of a different type so the terrain can't strand you.*
4. **Pair students and run the ladder.** Each pair:
   - **draws one environment card first**, and reads what it does to each attack type;
   - **both choose a pet and reveal together**;
   - duels (rulebook §6) — **choose and simplify each attack before rolling**,
     and **no attack type three times running** (rulebook §8) — students don't
     have to cycle all three, just can't spam one every single turn.
   The loser drops to the **second-chance bracket** (see §4); the winner heals to
   full, re-pairs with another winner, and draws a **new** environment.
5. **Call time** — last student standing, or most wins.

## 4. Managing the losers' bracket

About half the class is out of the main ladder after round 1, so the
**second-chance bracket runs by default** — they keep duelling in a parallel
ladder, and its winner can re-enter the main ladder or be named runner-up. This
also softens a loss to bad terrain luck (e.g. your only pet's type got Cancelled).

If you want more marked evidence instead, switch to: eliminated students complete
the battle sheet for **every duel they played**, then **referee two** more,
checking each attack against the answer key. Decide before the first duel and
tell the class.

## 5. The maths students must show

The battle sheet is the **gradable artifact** — one filled block per attack. For
each attack:

1. the **three terms written out** — pet attack `ax + b`, the matching stat buff, the environment term;
2. **like terms collected** into a single `nx + c` (above the dashed line — *before the roll*);
3. the **substitution** (`x =` the roll, shown);
4. the **final damage** (floored at 0).

A bare final number is not complete work. The dashed "all done before you roll"
line on the sheet is also the **gameplay** rule — a student filling the bottom of
a block before the top has broken the turn order, not just skipped working.

## 6. Common errors to watch for

- **A bonus written as a number, not an `x` term** — `+2` instead of `+2x`. The
  classic; catch it in round 1.
- **Rolling before simplifying** — picking the attack *after* seeing the roll.
  The sheet's dashed line is there to stop this; enforce it.
- **Checking the wrong stat.** One rule: magic attack → Magic, strength attack →
  Strength, agility attack → Agility. Nothing else touches the roll.
- **Using a Cancelled attack type.** If the environment Cancels magic, there is
  no legal magic attack this match — the pet must use strength or agility.
- **Spamming one attack type.** Same type three turns running isn't allowed —
  the third must switch. Not the same as being *forced* to rotate through all
  three (some terrain removes one type entirely; that's fine).
- **`+2x` vs `+x`.** A card's Boost/Weaken can be either size; students copy the
  term straight off the card.
- **Letting damage go negative.** After terms, floor at **0**. (A pet's *base*
  attack separately never goes below **1** — the card prints its own `(min 1)`.)
- **Dropping a term at `n = 0`.** `3x + x − 2x` with a further `−2x`… when the
  `x` terms cancel, the answer is the constant, every roll. It is still an answer.

## 7. Worked examples

**A — Boost.** Pet magic attack `3x + 2` · character **High Magic** `+x` ·
environment **Boosts Magic** `+2x`.
→ `3x + 2 + x + 2x = 6x + 2` → roll 5 → `6 × 5 + 2 = 32`.

**B — Weaken (still usable).** Same `3x + 2` · High Magic `+x` · environment
**Weakens Magic** `−2x`.
→ `3x + 2 + x − 2x = 2x + 2` → roll 5 → `12`.
*(A Low-Magic character here: `3x + 2 − x − 2x = 2` — the `+x` is worth a net `−x`.)*

**C — Cancel → forced switch.** Environment **Cancels Magic**. The pet's
**strength** attack is `2x` · character **Average Strength** `0`.
→ `2x + 0 = 2x` → roll 5 → `10`.

**D — everything cancels (`n = 0`).** Pet strength attack `x + 1` · character
**Low Strength** `−x` · environment does not affect strength `0`.
→ `x + 1 − x = 0x + 1 = 1` → **1 every roll** (floored at the base minimum).

**Independent recomputation**
- **A:** `(3 + 1 + 2)x + 2 = 6x + 2`; `x = 5` → `32`. ✔
- **B:** `(3 + 1 − 2)x + 2 = 2x + 2`; `x = 5` → `12`. ✔
- **C:** `2x`; `x = 5` → `10`. ✔
- **D:** `(1 − 1)x + 1 = 1`; every `x` → `1`. ✔

## 8. Differentiation

- **Support:** deal that pair only the **Open Field** environment card — no terms,
  so only the character `±x` applies.
- **Extension:** two environment cards per match; a **D8 or D12** instead of a D6;
  a **written inequality** justifying each trade (e.g. *"my strength attack `3x`
  beats their `2x` whenever `x > 0`"*); the **Challenge pet deck** (§10).

## 9. Answer key

`rulebook/answer-key.md` — a fast-marking lookup table. Once a student has
collected like terms to `nx + c`, find the row (`1x`–`8x`, constant `−3`…`+3`) and
read the value under their die roll. §3 has four fully-worked v2 scenarios.

## 10. Challenge Mode

`cards/pets-challenge.html` — 22 pets whose attacks are unexpanded brackets
(`3(x − 1)`) or negative leading coefficients (`−3x + 10`).

**Note (v2):** the Challenge deck has **not yet been rebalanced for v2** — its HP
and damage are still v1-scale, so it is *not* a drop-in swap for the v2 core deck
in the same ladder. Use it as its own self-contained harder game, or wait for the
Challenge v2 pass. Mark it with answer-key §2a.
