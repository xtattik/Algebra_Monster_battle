# Digital game: Tournament mode

Status: approved, ready for planning.
Scope: `digital-game/index.html` only (single-file vanilla-JS app, no build step).
Depends on nothing from the Challenge mode spec structurally, but composes with it
(both read/write `Game.petPool`, introduced there — see `2026-09-21-digital-challenge-mode-design.md`).
If Challenge mode's plan hasn't landed yet when this one is implemented, `Game.petPool`
can default straight to `PETS` and the composition still holds once Challenge lands.

## 1. Problem

The single/casual match flow's "Roll for capture" after a win (`showResult()`,
`digital-game/index.html:1322-1335`) is purely cosmetic today — it shows flavour
text ("Captured! `<pet>` joins your zoo.") but never actually mutates
`winner.roster`. It's a leftover from the print-and-play game, where capture
feeds a class tournament ladder played over a whole lesson — it doesn't do
anything useful in a single digital match that ends immediately after. This
adds a genuine single-player **Tournament** mode where capture is real and
matters: beat all 7 character archetypes in sequence with a persistent,
growing zoo, and get a trophy screen at the end.

## 2. Removing casual capture

`showResult(winner, loser)` currently always builds the capture-roll box.
Per this session's design conversation: **remove the capture-roll UI entirely
from casual Vs. Computer / Two Players matches** — it adds nothing to a match
that ends immediately. `showResult()` branches on `Game.mode`:

- `Game.mode==="cpu"` or `"2p"` (casual): winner announcement only, straight to
  the existing Rematch/New game buttons. No capture box at all.
- `Game.mode==="tournament"`: capture roll shown as today, **but now real** — a
  rolled 6 pushes a clone of `loser.fielded` into `winner.roster` (see §3.3),
  and the flow continues into the tournament's own round-advance logic instead
  of stopping at a static result screen.

## 3. Tournament structure

### 3.1 Entry point

A third title-screen mode card, `data-mode="tournament"`, alongside the
existing `.mode-card[data-mode="cpu"]` / `[data-mode="2p"]` in `.mode-grid`
(`digital-game/index.html:314-323`). Single-player vs CPU only — no pass-device
variant. Reuses the existing mode-card click-handling/`btn-start` pattern
(`:611-621`) with a third `data-mode` value.

### 3.2 Setup (once, before round 1)

Runs exactly like today's Vs. Computer setup, unchanged:
1. Character select (`beginSelect`/`pickCharacter`, `:694-707`) — player picks
   1 of the 7 `CHARACTERS`.
2. Pet roll (`dealPets`, `:708-...`) — 2 random pets each, drawn from
   `Game.petPool` (the pool selected by the Core/Challenge toggle — see the
   Challenge mode spec; if that hasn't landed yet, this is just `PETS`).
3. **One** trade-shelf opportunity for the player (the existing shelf-trading
   flow from this session's earlier work) — the CPU does not trade here; its
   trade happens per-round instead (§3.3).

At the end of setup, generate the round queue:
```js
Game.tournament = {
  round: 0,                                  // 0-indexed; round 1 of 7 is index 0
  totalRounds: 7,
  queue: shuffled(CHARACTERS)                 // independent of the player's own pick
};
```
`shuffled()` (existing helper) gives a full random permutation of all 7
characters — the player's own pick is not excluded, so a round *could* pit
them against a CPU using the same archetype. That's intentional (confirmed in
design discussion) and requires no special-casing.

### 3.3 Each round

Reuses existing per-match setup logic, re-run once per round for the CPU side
only:
1. CPU character = `Game.tournament.queue[Game.tournament.round]`.
2. CPU gets 2 fresh random pets from `Game.petPool` (same shape as `dealPets`'s
   CPU-half, just re-invoked, not reusing the player's original deal).
3. CPU resolves its own silent shelf-trade — reuses `rollShelf`/
   `cpuShelfDecision` from the trading feature verbatim, same as a normal CPU
   match already does once per match; here it runs once per round.
4. A fresh environment is drawn (`drawEnvironment`, `:917-...`), same as today.
5. Field select: the player picks from their **current full roster** — which
   only ever grows via capture, never shrinks or resets — using the existing
   field-select screen/logic (`beginField`/`pickFielded`, `:935-961`). The CPU
   fields via the existing `cpuFieldChoice` heuristic, unchanged.
6. Battle plays out exactly as today, including the paced damage-reveal work
   from earlier this session (shared `resolveDamage`, the CPU live-reveal
   sequence) — no tournament-specific battle-engine changes.

**No explicit "healing" step is needed.** `pickFielded()` already does
`p.curHp=p.fielded.hp; p.maxHp=p.fielded.hp;` (`:961` area) — HP lives on the
*player* object, derived fresh from whichever pet is fielded, not persisted
per-pet. Every pet — freshly captured or already owned — starts at full HP the
moment it's fielded, in every mode, already. This is existing behavior, not a
change.

### 3.4 On a round result

**Win:** capture roll shown (§2), and on a rolled 6, `winner.roster.push(clonePet(loser.fielded))`
(`clonePet` is the existing deep-clone helper already used by `dealPets`/
`rollShelf`). Then:
- If `Game.tournament.round + 1 < Game.tournament.totalRounds`: increment
  `Game.tournament.round`, and advance into the next round's setup (§3.3
  step 1) — fresh CPU deal/trade, fresh environment, field select. No
  re-trading for the player.
- Else (round 7 just won): show the trophy screen (§4).

**Loss:** the tournament ends immediately — show a defeat screen (§4) stating
how far the player got (e.g. "Defeated in round 4 of 7"). No retry of the same
round; a fresh tournament run starts over from character select.

### 3.5 Progress indicator

A small "Round X of 7" indicator is shown during tournament play (e.g. in the
topbar, alongside or replacing the existing brand label while
`Game.mode==="tournament"`), so the player has a sense of progress through the
gauntlet.

## 4. New screens

- **Trophy (tournament complete):** simple celebration — crown/trophy visual,
  "Tournament Champion!", the player's character name. Buttons: start a new
  tournament, or return to the title. No full run history/summary (rounds
  won, pets captured, etc.) in this version — explicitly out of scope, see §5.
- **Defeat (tournament ended early):** same visual family as the trophy
  screen, showing the round reached (e.g. "Defeated in round 4 of 7"). Same
  two buttons (new tournament / title).

Both are new screens (new `<section class="screen">` entries), distinct from
the existing `#scr-result` (which stays exactly as-is for casual matches, minus
the capture box per §2).

## 5. Out of scope

- No re-trading after round 1 — the player's roster only grows via capture.
- No full run-history summary on the trophy/defeat screens (just the
  celebration/defeat state, not a list of captured pets or round-by-round
  detail).
- No streamlined/compressed round ceremony — every round shows the full
  existing environment-reveal and field-select screens, same as a normal
  match, per design discussion (consistency and simplicity over pacing).
- No mid-tournament retry of a lost round — a loss ends the run.
- No tournament variant of Two Players mode.
- Casual mode's capture-roll removal (§2) is part of this feature's scope
  (it's what makes Tournament's capture meaningful to build), but no other
  casual-match behavior changes.

## 6. Testing / verification

Manual verification via the browser preview (no build step, no test suite):

- Casual Vs. Computer and Two Players matches: confirm the result screen no
  longer shows any capture-roll UI, just the winner announcement and
  Rematch/New game buttons.
- Start a Tournament: confirm the one-time trade-shelf step appears before
  round 1 and never again in later rounds.
- Play through multiple rounds: confirm each round deals the CPU fresh pets,
  resolves a silent CPU trade, draws a fresh environment, and lets the player
  field-select from their full (possibly grown) roster.
- Force a capture (or run enough rounds to hit one): confirm a rolled 6
  actually adds the pet to the player's roster and it's selectable in the next
  round's field-select screen; confirm a non-6 roll does not add anything.
- Win all 7 rounds: confirm the trophy screen appears and both its buttons
  work.
- Lose a round: confirm the defeat screen appears showing the correct round
  number and both its buttons work.
- Confirm the round indicator updates correctly each round.
- Confirm a full Tournament run has no console errors, in both Core and
  Challenge pet-pool settings (once Challenge mode is available).
