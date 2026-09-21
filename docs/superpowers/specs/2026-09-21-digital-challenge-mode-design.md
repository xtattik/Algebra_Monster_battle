# Digital game: Challenge mode

Status: approved, ready for planning.
Scope: `digital-game/index.html` only (single-file vanilla-JS app, no build step).

## 1. Problem

The print-and-play game already has a "Challenge" pet deck (`cards/pets-challenge.md`,
design: `docs/design/pets-challenge.md`) — the same 22 pets (name/HP/archetype/art/
flavour identical to Core) but harder attack equations: unexpanded brackets
(`a(x ± b)`) and negative coefficients (`−ax + b`), both of which reduce to the
same `ax + b` family the rest of the game already knows how to resolve. It's an
intermediate step between Core (`ax+b`, no expansion needed) and a not-yet-designed
"Expert" mode (exponents, deferred — needs a monster-stat rebalance, out of scope
here). The digital game currently only has the Core pet deck; this adds Challenge
as a selectable difficulty.

## 2. Data & engine

### 2.1 `CHALLENGE_PETS`

A new array parallel to `PETS` (`digital-game/index.html`), transcribed from
`cards/pets-challenge.md`'s "At a glance" table and per-pet cards — same 22
entries, same `id`/`name`/`hp`/`archetype`/`art`/`flavour` as the matching `PETS`
entry (art is reused as-is per the design doc — "the Challenge deck reuses
`cards/art/pets/` exactly as-is"). Only the three attack objects differ.

The existing attack-object helper:
```js
function A(name,a,b,min){ return {name,a,b,min:min||null}; }
```
gains an optional 5th argument:
```js
function A(name,a,b,min,printed){ return {name,a,b,min:min||null,printed:printed||null}; }
```
- `a`/`b` stay the **canonical** post-expansion pair (used for all damage math,
  unchanged) — e.g. for `3(x − 1)`, `a:3, b:-3`; for `−4x + 13`, `a:-4, b:13`.
- `printed`, new: the **authored** unexpanded string exactly as it appears on the
  physical card — `"3(x − 1)"`, `"−4x + 13"`. `null`/omitted for Core's existing
  `A(...)` calls (all of which already pass only 4 args), which keeps computing
  their display from `a`/`b` via `fmtFull` as today — no change to Core's output.
- `min` stays a literal per-attack value exactly as authored on the card (same
  pattern Core already uses — not derived at runtime), per the design doc's rule:
  printed exactly when the canonical pair evaluates to ≤0 at its worst roll
  (`x=1` for `a>0`, `x=6` for `a<0`).

### 2.2 Display: printed form everywhere a Challenge attack is shown

Every place the engine currently renders `fmtFull(atk.a, atk.b)` for a pet's
attack — `petCardInner()` (pet-selection cards: pet roll, trade shelf, field
select) and the battle term-lines (`builderHTML()` for the player, and the CPU's
live-reveal term-lines from the prior feature) — uses `atk.printed || fmtFull(atk.a,
atk.b)` instead. This is a one-line change at each call site: Core pets have no
`printed`, so they're pixel-identical to today; Challenge pets show their
authored bracket/negative form. This matches the physical card design ("the card
only ever displays the authored form") and is the point of the mode — showing
the pre-expanded number anywhere would trivialize it. No new UI step: the
player folds the expansion into the same "collect into `nx+c`" input they
already do for Core, per the design conversation — the design doc's "zeroth
step" is conceptual, not a separate screen.

### 2.3 Affinity generalization

`petAffinity()` currently does:
```js
var max=Math.max(pet.attacks.magic.a, pet.attacks.strength.a, pet.attacks.agility.a);
var top=TYPES.filter(function(t){ return pet.attacks[t].a===max; });
```
which only works because Core's `a` is always positive. Challenge introduces
negative coefficients, and per the design doc, "affinity is the attack type with
the largest **magnitude** of coefficient." Generalize to:
```js
var max=Math.max(Math.abs(pet.attacks.magic.a), Math.abs(pet.attacks.strength.a), Math.abs(pet.attacks.agility.a));
var top=TYPES.filter(function(t){ return Math.abs(pet.attacks[t].a)===max; });
```
Strict generalization — identical result for Core (always-positive `a`), correct
for Challenge (e.g. correctly reads Tank pets pairing two `|a|=2` attacks as
"Balanced," per the design doc's explicit callout that this is intentional).

### 2.4 Everything else in the engine is unchanged

- Damage math (`buildAttack`, roll, floor-at-0) operates on the canonical
  `a`/`b` regardless of authored form — no change.
- The CPU's attack-choice scoring (`runCpuTurn`: `score=built.n*3.5+built.c`)
  already uses the *signed* collected `n`, which already produces sensible
  behavior against negative coefficients (a steep negative attack scores low,
  as it should). No change needed.
- `cpuFieldChoice`'s `bestN` and `cpuShelfDecision`'s `val()` keep using raw
  `.a` (not magnitude) — this is the same simplistic heuristic Core already
  ships with, imperfect in the same pre-existing way, not worth special-casing
  for this feature (YAGNI — Challenge reusing an existing heuristic against a
  different dataset isn't a new problem to solve).
- Characters, environments, trading, streak-blocking (no-type-3x-in-a-row),
  capture: all untouched, per the design doc's own "what doesn't change" list.

## 3. Mode selection & copy

### 3.1 Title screen toggle

A **Core / Challenge** toggle on the title screen, alongside the existing
`.mode-grid` ("Vs. Computer" / "Two Players" cards) — an independent axis, not a
third mode card, so all four combinations (CPU+Core, CPU+Challenge, 2P+Core,
2P+Challenge) are reachable from one screen. Defaults to **Core**. Visually
similar to the existing `.art-toggle` pattern already used for the male/female
art variant on the character-select screen (small pill toggle), reused/adapted
here rather than inventing a new control style.

When Challenge is selected, a short line of copy appears under the toggle:

> Pets attack with unexpanded expressions like 3(x − 2) or −4x + 9 — expand
> first, then collect terms as usual.

### 3.2 Match-wide pool selection

At `btn-start` click, alongside the existing `Game.mode` assignment, store the
chosen pool once on `Game` (e.g. `Game.petPool = challengeSelected ? CHALLENGE_PETS
: PETS`) and use it everywhere a pet is currently drawn from the module-level
`PETS` constant — `dealPets()`'s initial deal and `rollShelf()`'s trade-shelf
draw. Both players (or the player and CPU) always draw from the same pool for a
given match — no mixing Core and Challenge pets within one match, matching the
"harder printing of the same 22 pets" framing (a Challenge pet is a drop-in
swap for its Core counterpart, not a different roster).

### 3.3 Out of scope

- No Challenge variant of characters or environments (design doc: "only pets
  change in this pass").
- No separate art for Challenge pets (reuses Core's `cards/art/pets/` images,
  already the case for the print version).
- No "Expert" (exponents) mode — explicitly deferred, needs a monster-stat
  rebalance.
- No per-attack "show the correct expansion" reveal beyond what Core's builder
  already offers today (the existing "Show the correct working" reveal-link,
  which shows `fmtFull(atk.a,atk.b)` as the resolved base term, already works
  unchanged since it operates on the canonical `a`/`b` — it just wasn't
  previously distinguishing "printed" from "resolved," and now correctly shows
  the resolved form as the answer to check the printed form against).

## 4. Testing / verification

Manual verification via the browser preview (no build step, no test suite):

- Toggle Core/Challenge on the title screen in both Vs. Computer and Two
  Players modes; confirm the correct pool is dealt (spot-check a pet's
  displayed attack matches `cards/pets-challenge.md` when Challenge is picked,
  and matches today's Core display when it isn't).
- Confirm the trade shelf, when in Challenge mode, only ever shows Challenge
  pets (not a mix), and still correctly excludes pets already in that player's
  own roster (by `id`, unaffected by which pool is active).
- Confirm a Challenge pet's attack shows its authored bracket/negative form on
  every screen it appears (pet roll, trade shelf, field select, the player's
  battle builder, the CPU's live reveal) — never the pre-expanded number.
- Confirm affinity labels for Challenge pets match the design doc's expected
  values (e.g. every Challenge Tank reads "Balanced").
- Confirm a full Challenge-mode match plays end to end with no console errors,
  in both Vs. Computer and Two Players modes.
- Confirm Core mode is pixel-for-pixel unchanged (toggle defaults to Core, and
  a Core match looks identical to before this feature).
