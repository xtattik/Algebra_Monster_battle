# Algebra Monster Battle — Teacher Guide

This guide covers what you need to run the game. It assumes you have read the
student rulebook (`rulebook/student-rulebook.md`); it does not re-teach the full
ruleset, only the parts a teacher has to manage.

## 1. Purpose & curriculum

The game is a resolution engine for NSW Mathematics **Stage 4 — Algebraic
Techniques**. Every attack forces the student to:

- assemble a linear expression from `ax + b` plus `±x` modifier terms,
- **collect like terms** into a single `nx + c`,
- **substitute** a D6 roll for `x` and evaluate,
- handle **negative constants** and **floor the result at 0**.

There are no bare-number bonuses anywhere in the system — every modifier is a
`±x` term, so students cannot avoid the like-terms step. (Confirm the exact
current outcome code against your own programming.)

Runs as **one lesson** (setup + two or three ladder rounds) or **two lessons**
(add a full trading/strategy discussion and a longer ladder).

## 2. Prep

- **Characters:** print one class set of the 7 designs (`cards/characters.html`),
  multiple copies of each, so several students can be the same character.
- **Pet deck:** `cards/pets.html` — 22 designs; print about **3 copies of each**
  for a class of 30, so every student draws **2 at random**. Duplicates are fine.
- **Environment deck:** `cards/environments.html` — 8 cards; one small deck per
  group of pairs, drawn once per match.
- **Battle sheets:** `worksheets/battle-sheet.html` — print a bundle (one A4
  page each); students use one per match. It has the guided method, a
  worked-attack template, a scribble area, and an HP track for both pets, so it
  doubles as the HP-tracking method and the gradable working.
- **Dice:** one D6 per pair.
- **Spare HP tracking:** counters or mini-whiteboards if a match outlasts the
  eight rows on the sheet.

## 3. Run sheet

1. **Deal characters** — random deal or free choice, your call. Random is faster
   and forces students to adapt.
2. **Draw pets** — each student draws **2** at random. This is their zoo.
3. **Trading phase** — **5 minutes**, timed. Trades need both students to agree.
   Prompt: cover your character's Low stat, or pick up a pet for terrain you
   expect.
4. **Pair students and run the ladder** — each pair draws an environment, fields
   one pet each, and duels (steps in rulebook §6). Loser is eliminated; winner
   heals to full, re-pairs with another winner, draws a **new** environment.
5. **Call time** — either play to last student standing, or stop and count
   **wins per student**.

## 4. Managing eliminated students

In a class of ~30 running a single-elimination ladder, **about half are out
after round 1**. You must have a plan before you start. Pick one:

- **Option A — worksheet + refereeing.** An eliminated student first completes
  the worksheet for **every match they played**, then referees **two** further
  matches, checking the maths on each attack against the answer key.
- **Option B — second-chance bracket.** Eliminated students form a parallel
  ladder and keep playing. Winner of that bracket can re-enter, or just be named
  runner-up.

Option A produces more markable evidence and more peer-checking; Option B keeps
energy high and everyone rolling dice. Decide which **before** the first duel and
tell the class up front.

## 5. The maths students must show

Direct students to the battle sheet — the worked-attack template on it, then the
same layout continued on the scribble grid. It is the **gradable artifact**. For
each attack the gradable evidence is:

1. the **expression assembled** (base attack + each `±x` term that applies),
2. **like terms collected** into a single `nx + c`,
3. the **substitution** (`x =` the roll, shown),
4. the **final damage** (after flooring at 0).

An answer with only the final number is not complete work.

## 6. Common errors to watch for

- **Modifier written as a number, not an `x` term** — `+1` instead of `+x`. This
  is the most common and it defeats the purpose; catch it early.
- **Buffing a strike attack.** Strike attacks take **no** character modifier and
  **no** environment modifier. Only the enemy's Strength defence applies to them.
- **Forgetting the enemy Strength term** when the defender has High Strength
  (`−x`) or Low Strength (`+x` to the attacker).
- **Letting damage go negative.** After modifiers, damage floors at **0**, not a
  negative number. (Base pet attacks separately never go below **1** — the card
  prints its own floor where needed.)
- **Applying the environment to the wrong attack type.** A card's Boosts / Hinders
  lines only touch magic and agility attacks that match — never strike.
- **Mishandling a `Tests: Strength` environment.** It is resolved against the
  *defender's* Strength tier (High `−x` / Average `0` / Low `+x`), added to the
  enemy-Strength term — and it *does* reach **strike** attacks. Students often
  either skip it on a strike attack or check the wrong player's Strength.
- **Forgetting the environment terms stack.** In Frozen Wastes / Scorching Desert
  a High-Strength defender contributes `−x` (their Strength) **and** another `−x`
  (the test) — two separate terms to collect.

## 7. Worked examples

Examples A–D are from `core-rules.md` §5.5; F, G, H are from `environments.md`
§6 (same lettering). All are reproduced in full, then independently recomputed.

**A. Sorcerer + Sprite, magic attack, in Arcane Nexus, vs a Barbarian (Avg Strength)**
Sprite "Fairy Lights" `3x + 1` · Sorcerer High Magic `+x` · Arcane Nexus `Boosts: Magic` `+x` · enemy Avg Strength `0`
→ `3x + 1 + x + x = 5x + 1`
→ roll 4 → `5(4) + 1 = 21 damage`

**B. Same attack, but the defender is a Paladin (High Strength)**
→ `3x + 1 + x + x − x = 4x + 1`
→ roll 4 → `17 damage`

**C. Physical attack ignores terrain**
Ogre "Strike" `2x + 2` · trainer is a Ranger (no strike buff) · Arcane Nexus (no effect on physical) · enemy Avg Strength
→ expression stays `2x + 2`
→ roll 3 → `8 damage`
Against a High-Strength defender → `2x + 2 − x = x + 2` → roll 3 → `5 damage`

**D. Hitting zero on a low roll**
Pet agility attack `2x − 2` · Sunken Marsh `Hinders: Agility` `−x`
→ `2x − 2 − x = x − 2`
→ roll 2 → `0` · roll 5 → `3 damage`

**F. Hinder cancels a caster's edge**
Illusionist (High Magic) pet magic `3x + 1` · Null Field `Hinders: Magic` `−x` · enemy Avg Strength `0`
→ `3x + 1 + x − x = 3x + 1`
→ roll 4 → `13 damage`

**G. `Tests: Strength` hits a strike attack, fragile defender**
Barbarian pet strike `2x + 2` · Frozen Wastes `Tests: Strength` · defender is an Illusionist (Low Strength)
→ enemy Strength `+x` · environment test (defender Low) `+x`
→ `2x + 2 + x + x = 4x + 2`
→ roll 3 → `14 damage`

**H. Same, tough defender (the "fortress")**
Same strike `2x + 2` · Frozen Wastes · defender is a Paladin (High Strength)
→ enemy Strength `−x` · environment test (defender High) `−x`
→ `2x + 2 − x − x = 2`
→ any roll → `2 damage`

**Independent recomputation**

- **A:** `3x + 1 + x + x` → `(3 + 1 + 1)x + 1 = 5x + 1`. At `x = 4`: `5 × 4 + 1 = 20 + 1 = 21`. ✔
- **B:** `3x + 1 + x + x − x` → `(3 + 1 + 1 − 1)x + 1 = 4x + 1`. At `x = 4`: `4 × 4 + 1 = 16 + 1 = 17`. ✔
- **C:** strike takes no buffs, so `2x + 2` is unchanged. At `x = 3`: `2 × 3 + 2 = 6 + 2 = 8`. ✔
  vs High Strength: `2x + 2 − x = x + 2`. At `x = 3`: `3 + 2 = 5`. ✔
- **D:** `2x − 2 − x = x − 2`. At `x = 2`: `2 − 2 = 0` (floored at 0, and already 0). At `x = 5`: `5 − 2 = 3`. ✔
- **F:** `3x + 1 + x − x` → `(3 + 1 − 1)x + 1 = 3x + 1`. At `x = 4`: `3 × 4 + 1 = 13`. ✔
- **G:** `2x + 2 + x + x` → `(2 + 1 + 1)x + 2 = 4x + 2`. At `x = 3`: `4 × 3 + 2 = 14`. ✔
- **H:** `2x + 2 − x − x` → `(2 − 1 − 1)x + 2 = 0x + 2 = 2`. Any `x` → `2`. ✔

All match the design docs and the student rulebook.

## 8. Differentiation

- **Support:** always play the **Open Field** environment card — it has no terms,
  so only the character `±x` modifier and the enemy Strength term apply.
- **Extension:** draw **two** environment cards per match; use a **D8 or D12**
  instead of a D6; hand out the **Challenge pet deck** (section 10 below —
  same pets, same art, harder attacks); require a **written inequality**
  justifying each trade (e.g. "Ogre strike beats Sprite magic whenever
  `x > 3`").

## 9. Answer key

See `rulebook/answer-key.md`. It is a fast-marking lookup table: for each
simplified form `nx + c` that the starter pets and environments can produce, it
lists the value at `x = 1..6` so you can check a worksheet row at a glance
without re-deriving it.

## 10. Challenge Mode (optional)

`cards/pets-challenge.html` is a drop-in swap for the pet deck — same 22
pets, same HP, same art — where every attack is either an unexpanded
bracket (`3(x − 1)`) or a negative leading coefficient (`−3x + 10`). Hand it
to pairs who are breezing through the standard deck; it needs no extra setup
and no rule changes anywhere else. Full design and balance reasoning:
`docs/design/pets-challenge.md`.

Mark it exactly as in §9, using `rulebook/answer-key.md` §2a for the
negative-coefficient rows. The two worked examples in the student rulebook's
"Challenge Mode" section are the ones to walk through if a table gets stuck.
