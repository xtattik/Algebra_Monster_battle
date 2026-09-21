# Digital game: damage reveal + shelf trading

Status: approved, ready for planning.
Scope: `digital-game/index.html` only (single-file vanilla-JS app, no build step).

## 1. Problem

Two rough edges in the existing digital scaffold (`digital-game/index.html`):

1. **CPU/opponent damage is invisible.** `runCpuTurn()` (index.html:1128) computes the
   CPU's attack, roll and damage inside one 900ms `setTimeout`, then calls
   `renderBattle()` with the HP already changed. The player sees a spinner, then
   suddenly their pet has less HP — no readable moment showing what hit them, for
   how much, or why.
2. **Trading only covers the two match opponents.** `beginTrade()` /
   `renderTradeScreen()` / `resolveTrade()` / `cpuTradeDecision()` (index.html:740-851)
   implement a sealed, simultaneous "offer one pet, mutual agreement swaps it"
   mechanic between the two players in the match. In the classroom, trading happens
   with *any* nearby classmate, not just your eventual opponent — the 1-on-1 model
   doesn't reflect that, and gives no way to decline a trade you don't like (today
   there's no visibility into the other side's offer before it resolves).

## 2. Feature 1 — Damage reveal sequence

### 2.1 Shared damage callout (every hit, either side)

New shared step that runs once damage is known, whoever dealt it:

1. HP is applied to game state.
2. `renderBattle()` runs — the `.hp-fill` bar animates down using its existing
   `transition:width .5s ease`.
3. A floating damage number ("−12") is spawned over the damaged fighter's card
   (absolutely positioned within `.fighter`), rises and fades via CSS animation;
   the card gets a brief flash/shake class.
4. Holds ~1.4s total, then auto-continues: if defender HP ≤ 0 go to
   `showResult()`, else flip `Game.turn`, clear draft/reveal state, re-render.

This replaces the tail end of both `applyDamage()` (index.html:1110) and the
inline resolution at the end of `runCpuTurn()` (index.html:1128) — both funnel
into one new function, e.g. `resolveDamage(attackerIdx, defenderIdx, dmg, logEntry)`,
so the two paths can't drift out of sync. No extra tap is required in either mode
(CPU or 2P) — this is purely a paced reveal, not a confirmation step.

New CSS: a `.dmg-float` (or similar) element + keyframes for rise/fade, and a
`.fighter.hit` flash/shake class, both respecting `prefers-reduced-motion` the
same way `.cpu-turn .spinner` already does (index.html:246).

### 2.2 CPU "live working" reveal (CPU mode only)

`runCpuTurn()` becomes a small auto-advancing sequence instead of one hidden
`setTimeout`, modeled on the existing player `draft` state machine
(`wireBuilder()` / `builderHTML()`, index.html:977-1092) but read-only and
self-paced (no clicks):

1. **Choosing** — spinner, "CPU is choosing an attack…" (~600ms, shortened from
   today's flat 900ms).
2. **Working shown** — a read-only card in the same visual language as the
   player's `.term-lines` (pet attack / stat modifier / terrain modifier),
   collected into the final `nx + c` — computed already, just revealed
   (~900ms hold).
3. **Roll** — reuses the existing `animateRoll()`/`finishRoll()` die-tick visual,
   then shows the substituted total (~900ms hold after it lands).
4. **Damage callout** — hands off to the shared step in §2.1.

This applies to whichever side is CPU/computer-controlled. In **2P mode**, both
players already build and see their own attack interactively in real time, so no
"live working" reveal is added there — only the §2.1 damage callout applies, on
both sides' hits, since that part was explicitly requested for consistency.

### 2.3 Out of scope

- No manual "Continue" tap between CPU reveal steps — always auto-paced.
- No change to the player's own attack-building flow (type pick → collect terms →
  roll → apply) — only what happens *after* they hit Apply.

## 3. Feature 2 — Shelf-based trading

Replaces `beginTrade()` / `tradeStepHuman()` / `renderTradeScreen()` /
`resolveTrade()` / `cpuTradeDecision()` (index.html:740-851) entirely. The
opponent-to-opponent offer/accept mechanic is removed — trading becomes
something each side does independently against a private random pool, mirroring
"there are other classmates around, not just your opponent, and you don't have
to take what's offered."

### 3.1 The shelf

```
function rollShelf(player){
  var ownIds = player.roster.map(function(p){ return p.id; });
  var pool = PETS.filter(function(p){ return ownIds.indexOf(p.id)===-1; });
  return shuffled(pool).slice(0,6).map(clonePet);
}
```

- 6 pets, freshly randomized per player per match.
- Never duplicates a pet already in *that player's own* roster (no filtering
  against the other player's roster — plain random otherwise).
- Each side (human/CPU, or P1/P2) gets its own independently-rolled shelf — not
  shared — so both have roughly even, but different, options.

### 3.2 Human trade screen

Reuses `scr-trade` and the existing `.trade-cols` / `.art-card` / `petCardInner()`
building blocks, restructured to one player at a time:

- **Left column — "Your zoo"**: the player's current 2 pets. Click to mark one as
  the pet you'd give up (toggle, like today's "Offering" flag) — at most one
  selected.
- **Right column — "Trade shelf"**: the 6 rolled pets. Click to mark one as the
  pet you'd take — at most one selected.
- Button reads **"Confirm swap ▸"** once both a give and a take are selected,
  otherwise **"Skip trading ▸"**.
- Confirming swaps the selected roster pet for the selected shelf pet (at most
  one swap — matches the paper rulebook's single-trade framing). Skipping leaves
  the roster untouched.
- After confirm/skip, the existing result-summary pattern (`resolveTrade`'s
  redraw of both rosters with a "Traded in" flag, index.html:830-849) is reused
  to show the outcome before continuing.

Screen copy (`#trade-title`, the `.sub` under "One trade, before battle") is
updated to describe browsing a shelf rather than "offer a pet" / "mutual
agreement."

### 3.3 Per-mode flow

- **CPU mode:** only the human uses the shelf UI (`beginTrade()` → shelf for
  player 0 → confirm/skip). Once the human is done, the CPU is dealt its own
  private shelf and resolves silently via `cpuShelfDecision()` (§3.4) — no CPU
  screen shown, matching how CPU character/pet choices already resolve off-screen
  elsewhere in the file. A combined summary of both final rosters is then shown
  before "Continue to arena ▸" → `drawEnvironment()`.
- **2P mode:** sequential, reusing the existing `passTo()` interstitial
  (index.html:609): player 1 gets their shelf and decides, device is passed,
  player 2 gets a *different* freshly-rolled shelf and decides, then the summary.

### 3.4 CPU shelf decision

Replaces `cpuTradeDecision()` (index.html:807-813). Keeps the existing
"trade toward my High stat" heuristic, extended to evaluate the shelf instead of
comparing its own two pets to each other:

```
function cpuShelfDecision(cpu, shelf){
  var ht = highStatType(cpu.character);
  if(!ht) return null; // no High stat (Bard) — never bothers trading
  function val(pet){ return pet.attacks[ht].a; }
  var worseIdx = val(cpu.roster[0]) <= val(cpu.roster[1]) ? 0 : 1;
  var bestShelfIdx = -1, bestVal = val(cpu.roster[worseIdx]);
  shelf.forEach(function(pet,i){
    if(val(pet) > bestVal){ bestVal = val(pet); bestShelfIdx = i; }
  });
  return bestShelfIdx===-1 ? null : {give: worseIdx, take: bestShelfIdx};
}
```

Swaps its weaker (by High-stat attack) roster pet for the best shelf pet, only if
one actually beats it. Returns `null` (no trade) otherwise — same shape of
outcome as today's "no deal" case, just without another party to disagree.

### 3.5 Out of scope

- No trading between the two match opponents at all (fully replaced, not
  additive).
- No multi-swap — one give/take pair max per player per match.
- No persistence/identity for shelf pets ("classmate" flavour is implied by the
  copy, not modeled as NPCs).

## 4. Testing / verification

Manual verification via the browser preview (`digital-game/index.html` has no
build step or test suite):

- CPU mode: play a full match, confirm the CPU-turn reveal sequence (choosing →
  working shown → roll → damage callout) auto-plays without input, and that a
  player's own Apply-damage click also shows the same damage callout before the
  turn flips.
- 2P mode: confirm both players' own hits show the damage callout, and that no
  "live working" reveal is added to opponent turns (since they already build
  their own attack interactively).
- Trading, CPU mode: confirm the human's shelf never contains a pet already in
  their roster, confirm/skip both work, and the CPU's own trade (or lack of one)
  shows correctly in the summary.
- Trading, 2P mode: confirm each player gets a distinct shelf and the pass-device
  interstitial still gates visibility between the two trade steps.
- `prefers-reduced-motion`: confirm the damage-float/flash and any new animated
  reveal steps degrade sensibly (matching the existing spinner's reduced-motion
  handling).
