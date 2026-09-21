# Digital Challenge mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a selectable "Challenge" pet deck (unexpanded bracket/negative-coefficient attacks) to the digital game, chosen via a title-screen toggle, without changing Core mode's behavior at all.

**Architecture:** Single-file vanilla-JS app (`digital-game/index.html`, no build step, no test runner, all logic in one IIFE using `var`/plain `function` declarations). A new parallel `CHALLENGE_PETS` data array, a generalized affinity calc, four display call sites that prefer an optional `printed` string over the computed expression, and a `Game.petPool` selected once at match start.

**Tech Stack:** Plain HTML/CSS/JS, no framework, no bundler.

**Note on model selection:** per Nathan's standing preference, do not use an `opus`-model reviewer for the per-task spec-compliance/code-quality reviews in this plan — use the default model. Reserve `opus` for one final review at the very end of the whole implementation (after both this plan and the Tournament mode plan are done), and only if asked.

---

## Before you start

No build step — edit `digital-game/index.html` directly and reload it in the
browser. Open it via `mcp__Claude_Browser__navigate` with url
`file:///C:/Code%20Projects/Algebra_Monster_Battle/digital-game/index.html`
(or `mcp__Claude_Browser__preview_start` with that `url`), and re-navigate to
reload after each edit. After every check, also glance at
`mcp__Claude_Browser__read_console_messages` (`onlyErrors: true`) — zero
errors is part of "passing" for every step below, even when not called out
explicitly.

Source data for the Challenge pet deck: `cards/pets-challenge.md` (the "At a
glance" table and per-pet card blocks) and `docs/design/pets-challenge.md`
(the design rationale) — already fully transcribed into Task 3 below, you
don't need to re-read those files.

---

## Task 1: Generalize `petAffinity()` to magnitude

**Files:**
- Modify: `digital-game/index.html` (`petAffinity()` function)

- [ ] **Step 1: Make the edit**

Find:

```js
function petAffinity(pet){
  // null means "Balanced" — all three attacks share the same top coefficient
  // (Patchwork Golem, Moss Troll, Clockwork Beetle in the source deck).
  var max=Math.max(pet.attacks.magic.a,pet.attacks.strength.a,pet.attacks.agility.a);
  var top=TYPES.filter(function(t){ return pet.attacks[t].a===max; });
  return top.length===1 ? top[0] : null;
}
```

Replace with:

```js
function petAffinity(pet){
  // null means "Balanced" — all three attacks share the same top magnitude.
  // Magnitude (not raw value) because Challenge pets can have a negative
  // coefficient that's still the pet's "biggest" attack.
  var max=Math.max(Math.abs(pet.attacks.magic.a),Math.abs(pet.attacks.strength.a),Math.abs(pet.attacks.agility.a));
  var top=TYPES.filter(function(t){ return Math.abs(pet.attacks[t].a)===max; });
  return top.length===1 ? top[0] : null;
}
```

This is a strict generalization: Core's `a` is always positive, so
`Math.abs(a)===a` for every existing pet — output is identical for Core.

- [ ] **Step 2: Verify Core is unchanged**

Reload the file. Click **Vs. Computer** → **Start** → pick any character →
on the pet-roll screen, check via `mcp__Claude_Browser__read_page` (or
`get_page_text`) that the two dealt pets show the same affinity pill text
they would have before this change — e.g. if you land on Patchwork Golem,
confirm it still reads "Balanced" (its three Core attacks are `2,2,2` — a
three-way tie, unaffected by the `Math.abs` change since all values are
already positive). Spot-check one pet with a clear affinity too (e.g.
Emberwisp should read "Magic affinity").

Check `read_console_messages` — zero errors.

- [ ] **Step 3: Commit**

```bash
git add digital-game/index.html
git commit -m "Generalize petAffinity to magnitude, ahead of Challenge mode's negative coefficients"
```

---

## Task 2: Prefer a `printed` display form over the computed expression

**Files:**
- Modify: `digital-game/index.html` (four call sites)

- [ ] **Step 1: `petCardInner()`'s stat-chip**

Find:

```js
      '<div class="pillrow">'+TYPES.map(function(t){
        var atk=pet.attacks[t];
        return '<span class="stat-chip '+t+'">'+TYPE_LABEL[t]+' '+fmtFull(atk.a,atk.b)+(atk.min?' (min '+atk.min+')':'')+'</span>';
      }).join('')+'</div>'+
```

Replace with:

```js
      '<div class="pillrow">'+TYPES.map(function(t){
        var atk=pet.attacks[t];
        return '<span class="stat-chip '+t+'">'+TYPE_LABEL[t]+' '+(atk.printed||fmtFull(atk.a,atk.b))+(atk.min?' (min '+atk.min+')':'')+'</span>';
      }).join('')+'</div>'+
```

- [ ] **Step 2: The battle builder's type-picker button**

Find:

```js
    html += '<button class="type-btn '+t+(chosen?" chosen":"")+'" data-type="'+t+'" '+(disabled?"disabled":"")+'>'+
      '<b>'+TYPE_LABEL[t]+'</b><div class="eq">'+atk.name+' · '+fmtFull(atk.a,atk.b)+(atk.min?' (min '+atk.min+')':'')+'</div>'+
```

Replace with:

```js
    html += '<button class="type-btn '+t+(chosen?" chosen":"")+'" data-type="'+t+'" '+(disabled?"disabled":"")+'>'+
      '<b>'+TYPE_LABEL[t]+'</b><div class="eq">'+atk.name+' · '+(atk.printed||fmtFull(atk.a,atk.b))+(atk.min?' (min '+atk.min+')':'')+'</div>'+
```

- [ ] **Step 3: The player's own term-lines "Pet attack" row**

Find:

```js
    html += '<div class="term-lines">'+
      '<div class="term-line"><span class="label">Pet attack — '+d.base.name+'</span><span class="expr">'+fmtFull(d.base.a,d.base.b)+'</span></div>'+
```

Replace with:

```js
    html += '<div class="term-lines">'+
      '<div class="term-line"><span class="label">Pet attack — '+d.base.name+'</span><span class="expr">'+(d.base.printed||fmtFull(d.base.a,d.base.b))+'</span></div>'+
```

Leave the "Show the correct working" reveal a few lines below **unchanged** —
it intentionally shows the *resolved* `fmtFull(d.base.a,d.base.b)` form, since
that's the worked answer the student is checking their expansion against, not
the prompt.

- [ ] **Step 4: The CPU reveal's term-lines "Pet attack" row**

Find:

```js
  html+='<div class="term-lines">'+
    '<div class="term-line"><span class="label">Pet attack — '+b.atk.name+'</span><span class="expr">'+fmtFull(b.atk.a,b.atk.b)+'</span></div>'+
```

Replace with:

```js
  html+='<div class="term-lines">'+
    '<div class="term-line"><span class="label">Pet attack — '+b.atk.name+'</span><span class="expr">'+(b.atk.printed||fmtFull(b.atk.a,b.atk.b))+'</span></div>'+
```

(This is inside `renderCpuReveal`. Leave the "Collected: `fmtFull(b.n,b.c)`"
line and the roll-substitution text elsewhere in the same function
unchanged — those show the final collected numeric expression, not the base
attack term, so they're correct as-is regardless of Core or Challenge.)

- [ ] **Step 5: Verify Core is unchanged**

Reload. Play up through a battle turn (either side). Confirm every place an
attack's expression is shown (pet-roll cards, trade shelf, field-select
cards, the type-picker buttons, the term-lines "Pet attack" row, and — if you
reach a CPU turn — its reveal card) looks pixel-identical to before this
change. This is expected: none of today's `PETS` entries have a `printed`
field yet, so `atk.printed||fmtFull(...)` always falls through to
`fmtFull(...)`.

Check `read_console_messages` — zero errors.

- [ ] **Step 6: Commit**

```bash
git add digital-game/index.html
git commit -m "Prefer an attack's printed display form over its computed expression, where present"
```

---

## Task 3: Add the `CHALLENGE_PETS` data array

**Files:**
- Modify: `digital-game/index.html` (extend the `A()` helper; add `CHALLENGE_PETS` after `PETS`)

- [ ] **Step 1: Extend the `A()` helper with an optional `printed` argument**

Find:

```js
function A(name,a,b,min){ return {name,a,b,min:min||null}; }
```

Replace with:

```js
function A(name,a,b,min,printed){ return {name,a,b,min:min||null,printed:printed||null}; }
```

Every existing call to `A(...)` in the `PETS` array passes exactly 4
arguments, so `printed` is `undefined` for all of them → `printed:null` —
`PETS` is unaffected by this change.

- [ ] **Step 2: Add `CHALLENGE_PETS` right after the `PETS` array**

Find (the end of `PETS` and the start of the next section):

```js
  {id:22,name:"Rust Golem",hp:102,archetype:"Tank",flavour:"Slow, heavy, and only ever going one direction: yours.",art:"art/pets/22-rust-golem.jpg",
    attacks:{magic:A("Oxide Cloud",1,-1,1),strength:A("Iron Fist",3,0),agility:A("Grind Forward",2,0)}},
];

function E(type,kind,amount){ return {type,kind,amount:amount||null}; }
```

Replace with:

```js
  {id:22,name:"Rust Golem",hp:102,archetype:"Tank",flavour:"Slow, heavy, and only ever going one direction: yours.",art:"art/pets/22-rust-golem.jpg",
    attacks:{magic:A("Oxide Cloud",1,-1,1),strength:A("Iron Fist",3,0),agility:A("Grind Forward",2,0)}},
];

/* Challenge pet deck — same 22 pets (id/name/hp/archetype/flavour/art all
   identical to PETS, transcribed from cards/pets-challenge.md), only the
   three attack equations differ: unexpanded brackets a(x±b) or negative
   coefficients −ax+b, both reduced to the canonical (a,b) pair here with
   the authored form kept in `printed` for display (see A(), above). */
const CHALLENGE_PETS = [
  {id:1,name:"Emberwisp",hp:40,archetype:"Glass cannon",flavour:"A trapped mote of wildfire that never learned to be careful.",art:"art/pets/01-emberwisp.jpg",
    attacks:{magic:A("Cinderburst",4,4,null,"4(x + 1)"),strength:A("Singe",-1,5,1,"−x + 5"),agility:A("Flit",2,-2,1,"2(x − 1)")}},
  {id:2,name:"Gorehoof",hp:42,archetype:"Glass cannon",flavour:"Aims first. Thinks later, if at all.",art:"art/pets/02-gorehoof.jpg",
    attacks:{magic:A("Snort",2,-2,1,"2(x − 1)"),strength:A("Goring Charge",-4,13,1,"−4x + 13"),agility:A("Trample",-1,5,1,"−x + 5")}},
  {id:3,name:"Dartclaw",hp:38,archetype:"Glass cannon",flavour:"You feel it a moment before you see it.",art:"art/pets/03-dartclaw.jpg",
    attacks:{magic:A("Static Lick",-2,8,1,"−2x + 8"),strength:A("Tail Whip",2,2,null,"2(x + 1)"),agility:A("Blink Slash",4,4,null,"4(x + 1)")}},
  {id:4,name:"Sootmane",hp:76,archetype:"Baseline",flavour:"Patient. Then, very suddenly, not.",art:"art/pets/04-sootmane.jpg",
    attacks:{magic:A("Warding Roar",-1,5,1,"−x + 5"),strength:A("Pounce",3,3,null,"3(x + 1)"),agility:A("Prowl",2,-2,1,"2(x − 1)")}},
  {id:5,name:"Tidecaller",hp:74,archetype:"Baseline",flavour:"It calls the water, and the water always answers.",art:"art/pets/05-tidecaller.jpg",
    attacks:{magic:A("Tidal Pulse",3,-3,1,"3(x − 1)"),strength:A("Tail Slap",2,-2,1,"2(x − 1)"),agility:A("Slip Away",-2,8,1,"−2x + 8")}},
  {id:6,name:"Gustling",hp:72,archetype:"Baseline",flavour:"Hard to catch, harder to hold onto.",art:"art/pets/06-gustling.jpg",
    attacks:{magic:A("Whisper Gale",-1,5,1,"−x + 5"),strength:A("Buffet",2,2,null,"2(x + 1)"),agility:A("Cyclone Kick",3,-3,1,"3(x − 1)")}},
  {id:7,name:"Patchwork Golem",hp:80,archetype:"Baseline",flavour:"Assembled from spare parts, none of them a matched set.",art:"art/pets/07-patchwork-golem.jpg",
    attacks:{magic:A("Spark Seam",2,2,null,"2(x + 1)"),strength:A("Hammer Fist",-2,8,1,"−2x + 8"),agility:A("Lumber",3,-3,1,"3(x − 1)")}},
  {id:8,name:"Riftmoth",hp:70,archetype:"Baseline",flavour:"Half of it is here. The other half is somewhere worse.",art:"art/pets/08-riftmoth.jpg",
    attacks:{magic:A("Dust of Ages",2,-2,1,"2(x − 1)"),strength:A("Wing Slam",-2,8,1,"−2x + 8"),agility:A("Phase Flurry",3,-3,1,"3(x − 1)")}},
  {id:9,name:"Grave Hound",hp:74,archetype:"Baseline",flavour:"It has your scent now, and it is not in a hurry.",art:"art/pets/09-gravehound.jpg",
    attacks:{magic:A("Baying Howl",-1,5,1,"−x + 5"),strength:A("Bone Crush",3,-3,1,"3(x − 1)"),agility:A("Lunge",2,2,null,"2(x + 1)")}},
  {id:10,name:"Boulderhide",hp:100,archetype:"Tank",flavour:"In no rush to get anywhere, least of all away from you.",art:"art/pets/10-boulderhide.jpg",
    attacks:{magic:A("Dust Cloud",-1,5,1,"−x + 5"),strength:A("Shell Bash",-2,8,1,"−2x + 8"),agility:A("Withdraw",2,-2,1,"2(x − 1)")}},
  {id:11,name:"Old Cairn",hp:98,archetype:"Tank",flavour:"Older than the hill it grew out of.",art:"art/pets/11-old-cairn.jpg",
    attacks:{magic:A("Root Surge",2,-2,1,"2(x − 1)"),strength:A("Deadfall",-1,5,1,"−x + 5"),agility:A("Slow Creak",-2,8,1,"−2x + 8")}},
  {id:12,name:"Moss Troll",hp:104,archetype:"Tank",flavour:"Thick, slow, and remarkably hard to convince to fall over.",art:"art/pets/12-moss-troll.jpg",
    attacks:{magic:A("Spore Cloud",2,-2,1,"2(x − 1)"),strength:A("Heavy Club",-2,8,1,"−2x + 8"),agility:A("Shamble",-1,5,1,"−x + 5")}},
  {id:13,name:"Sparkhound",hp:39,archetype:"Glass cannon",flavour:"Static crackles off it when it gets excited, which is always.",art:"art/pets/13-sparkhound.jpg",
    attacks:{magic:A("Arc Bite",-4,13,1,"−4x + 13"),strength:A("Nip",2,-2,1,"2(x − 1)"),agility:A("Dash",-1,5,1,"−x + 5")}},
  {id:14,name:"Bristlecharge",hp:41,archetype:"Glass cannon",flavour:"The warning snort is the only warning you get.",art:"art/pets/14-bristelcharge.jpg",
    attacks:{magic:A("Huff",-1,5,1,"−x + 5"),strength:A("Spine Rush",4,4,null,"4(x + 1)"),agility:A("Sidestep",2,2,null,"2(x + 1)")}},
  {id:15,name:"Quickfin",hp:38,archetype:"Glass cannon",flavour:"Gone before the ripples have finished spreading.",art:"art/pets/15-quickfin.jpg",
    attacks:{magic:A("Bubble",2,2,null,"2(x + 1)"),strength:A("Fin Slap",-2,8,1,"−2x + 8"),agility:A("Riptide Dart",-4,13,1,"−4x + 13")}},
  {id:16,name:"Cindercat",hp:75,archetype:"Baseline",flavour:"Warm to the touch. Warmer if it has decided it doesn't like you.",art:"art/pets/16-cindercat.jpg",
    attacks:{magic:A("Ember Purr",3,3,null,"3(x + 1)"),strength:A("Swipe",-2,8,1,"−2x + 8"),agility:A("Slink",2,-2,1,"2(x − 1)")}},
  {id:17,name:"Ironhide Ram",hp:78,archetype:"Baseline",flavour:"Built like a doorstop and twice as stubborn.",art:"art/pets/17-ironhide-ram.jpg",
    attacks:{magic:A("Bleat",-2,8,1,"−2x + 8"),strength:A("Headbutt",3,-3,1,"3(x − 1)"),agility:A("Scramble",2,-2,1,"2(x − 1)")}},
  {id:18,name:"Zephyr Kite",hp:72,archetype:"Baseline",flavour:"Rides the wind so you never have to guess where it is — until you do.",art:"art/pets/18-zephyr-kite.jpg",
    attacks:{magic:A("Updraft",-1,5,1,"−x + 5"),strength:A("Talon Rake",2,2,null,"2(x + 1)"),agility:A("Divebomb",3,-3,1,"3(x − 1)")}},
  {id:19,name:"Clockwork Beetle",hp:80,archetype:"Baseline",flavour:"Wind it up, set it down, and take a step back.",art:"art/pets/19-clockwork-beetle.jpg",
    attacks:{magic:A("Spark Coil",-2,8,1,"−2x + 8"),strength:A("Pincer",2,-2,1,"2(x − 1)"),agility:A("Scuttle",3,-3,1,"3(x − 1)")}},
  {id:20,name:"Barrow Wight",hp:96,archetype:"Tank",flavour:"It remembers being alive, and it resents you for still managing it.",art:"art/pets/20-barrow-wight.jpg",
    attacks:{magic:A("Chill Touch",-1,5,1,"−x + 5"),strength:A("Grave Reach",2,-2,1,"2(x − 1)"),agility:A("Drift",-2,8,1,"−2x + 8")}},
  {id:21,name:"Deepstone Toad",hp:98,archetype:"Tank",flavour:"Has not moved in a decade and does not plan to start now.",art:"art/pets/21-deepstone-toad.jpg",
    attacks:{magic:A("Mud Bolt",-2,8,1,"−2x + 8"),strength:A("Bellyflop",2,-2,1,"2(x − 1)"),agility:A("Hunker",-1,5,1,"−x + 5")}},
  {id:22,name:"Rust Golem",hp:102,archetype:"Tank",flavour:"Slow, heavy, and only ever going one direction: yours.",art:"art/pets/22-rust-golem.jpg",
    attacks:{magic:A("Oxide Cloud",-2,8,1,"−2x + 8"),strength:A("Iron Fist",-1,5,1,"−x + 5"),agility:A("Grind Forward",2,-2,1,"2(x − 1)")}},
];

function E(type,kind,amount){ return {type,kind,amount:amount||null}; }
```

- [ ] **Step 3: Verify it parses cleanly**

Reload the file. Since nothing references `CHALLENGE_PETS` yet, there's no
UI change to check — just confirm the page still loads to the title screen
normally and `read_console_messages` shows zero errors (a syntax mistake
anywhere in that large array would break the whole script).

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Add the CHALLENGE_PETS data array (unwired)"
```

---

## Task 4: Title-screen Core/Challenge toggle (UI only, unwired)

**Files:**
- Modify: `digital-game/index.html` (title-screen HTML; a new small JS block)

- [ ] **Step 1: Add the toggle markup**

Find:

```html
      <div class="mode-grid">
        <button class="mode-card" data-mode="cpu">
          <b>Vs. Computer</b>
          <p>Play solo. The computer picks a character, trades, and fights back using its own (visible) working.</p>
        </button>
        <button class="mode-card" data-mode="2p">
          <b>Two Players</b>
          <p>Pass the device between turns. Good for a quick 1v1 at one desk.</p>
        </button>
      </div>
      <div class="row-actions">
        <button class="btn wide" id="btn-start" disabled>Choose a mode to begin</button>
      </div>
```

Replace with:

```html
      <div class="mode-grid">
        <button class="mode-card" data-mode="cpu">
          <b>Vs. Computer</b>
          <p>Play solo. The computer picks a character, trades, and fights back using its own (visible) working.</p>
        </button>
        <button class="mode-card" data-mode="2p">
          <b>Two Players</b>
          <p>Pass the device between turns. Good for a quick 1v1 at one desk.</p>
        </button>
      </div>
      <div class="art-toggle" id="difficulty-toggle" style="margin-top:22px">
        <span>Pets</span>
        <button data-d="core" class="active">Core</button>
        <button data-d="challenge">Challenge</button>
      </div>
      <p class="sub" id="difficulty-hint" hidden>Pets attack with unexpanded expressions like 3(x − 2) or −4x + 9 — expand first, then collect terms as usual.</p>
      <div class="row-actions">
        <button class="btn wide" id="btn-start" disabled>Choose a mode to begin</button>
      </div>
```

This reuses the existing `.art-toggle` pill-button styling (already used for
the male/female character-art toggle) rather than introducing a new control.

- [ ] **Step 2: Wire the toggle's own state (not yet connected to `Game`)**

Find:

```js
/* ---------- title / mode select ---------- */
var chosenMode = null;
document.querySelectorAll(".mode-card").forEach(function(el){
```

Replace with:

```js
/* ---------- title / mode select ---------- */
var chosenMode = null;
var chosenDifficulty = "core";
document.querySelectorAll("#difficulty-toggle button").forEach(function(btn){
  btn.addEventListener("click", function(){
    document.querySelectorAll("#difficulty-toggle button").forEach(function(b){ b.classList.remove("active"); });
    btn.classList.add("active");
    chosenDifficulty = btn.getAttribute("data-d");
    document.getElementById("difficulty-hint").hidden = chosenDifficulty!=="challenge";
  });
});
document.querySelectorAll(".mode-card").forEach(function(el){
```

- [ ] **Step 3: Verify the toggle works visually**

Reload. On the title screen, click "Challenge" — confirm it becomes the
active pill (matches the existing "Core" pill's prior visual state) and the
hint paragraph below it appears. Click "Core" — confirm the hint disappears
and "Core" is active again. This has no effect on gameplay yet (Task 5 wires
it up) — you're only confirming the control itself works.

Check `read_console_messages` — zero errors.

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Add title-screen Core/Challenge toggle (UI only, not yet wired to game state)"
```

---

## Task 5: Wire the toggle into `Game.petPool`

**Files:**
- Modify: `digital-game/index.html` (`btn-start` handler, `btn-rematch` handler, `dealPets()`, `rollShelf()`)

- [ ] **Step 1: Store the pool at match start**

Find:

```js
document.getElementById("btn-start").addEventListener("click", function(){
  if(!chosenMode) return;
  Game = {
    mode:chosenMode,
    players:[ mkPlayer(chosenMode==="cpu"?"You":"Player 1"), mkPlayer(chosenMode==="cpu"?"CPU":"Player 2") ],
    environment:null, turn:0, log:[]
  };
  document.getElementById("btn-reset").hidden=false;
  beginSelect(0);
});
```

Replace with:

```js
document.getElementById("btn-start").addEventListener("click", function(){
  if(!chosenMode) return;
  Game = {
    mode:chosenMode,
    difficulty:chosenDifficulty,
    petPool: chosenDifficulty==="challenge" ? CHALLENGE_PETS : PETS,
    players:[ mkPlayer(chosenMode==="cpu"?"You":"Player 1"), mkPlayer(chosenMode==="cpu"?"CPU":"Player 2") ],
    environment:null, turn:0, log:[]
  };
  document.getElementById("btn-reset").hidden=false;
  beginSelect(0);
});
```

- [ ] **Step 2: Preserve the pool across a rematch**

Find:

```js
document.getElementById("btn-rematch").addEventListener("click", function(){
  var chars=[Game.players[0].character, Game.players[1].character];
  var mode=Game.mode;
  Game = { mode:mode, players:[mkPlayer(mode==="cpu"?"You":"Player 1"), mkPlayer(mode==="cpu"?"CPU":"Player 2")], environment:null, turn:0, log:[] };
  Game.players[0].character=chars[0]; Game.players[1].character=chars[1];
  dealPets();
});
```

Replace with:

```js
document.getElementById("btn-rematch").addEventListener("click", function(){
  var chars=[Game.players[0].character, Game.players[1].character];
  var mode=Game.mode, difficulty=Game.difficulty, petPool=Game.petPool;
  Game = { mode:mode, difficulty:difficulty, petPool:petPool, players:[mkPlayer(mode==="cpu"?"You":"Player 1"), mkPlayer(mode==="cpu"?"CPU":"Player 2")], environment:null, turn:0, log:[] };
  Game.players[0].character=chars[0]; Game.players[1].character=chars[1];
  dealPets();
});
```

Without this, rematching a Challenge-mode match would silently fall back to
Core (since a fresh `Game` object would have no `petPool` at all).

- [ ] **Step 3: Deal from the selected pool**

Find:

```js
function dealPets(){
  var pool = shuffled(PETS);
```

Replace with:

```js
function dealPets(){
  var pool = shuffled(Game.petPool);
```

- [ ] **Step 4: Roll the trade shelf from the selected pool**

Find:

```js
function rollShelf(player){
  var ownIds = player.roster.map(function(p){ return p.id; });
  var pool = PETS.filter(function(p){ return ownIds.indexOf(p.id)===-1; });
  return shuffled(pool).slice(0,6).map(clonePet);
}
```

Replace with:

```js
function rollShelf(player){
  var ownIds = player.roster.map(function(p){ return p.id; });
  var pool = Game.petPool.filter(function(p){ return ownIds.indexOf(p.id)===-1; });
  return shuffled(pool).slice(0,6).map(clonePet);
}
```

- [ ] **Step 5: Verify a full Challenge-mode playthrough, Vs. Computer**

Reload. On the title screen, select "Challenge", pick **Vs. Computer** →
**Start** → pick a character. On the pet-roll screen, confirm the two dealt
pets show bracket/negative expressions (e.g. `"2(x − 1)"`, `"−x + 5"`, not
plain `"2x + 4"`-style output) in their stat-chips. Cross-check one pet's
displayed attacks against its row in `cards/pets-challenge.md`'s "At a
glance" table to confirm they match. Continue to the trade shelf — confirm
all 6 shelf pets also show Challenge expressions, and that a swap still
excludes pets already in your roster (by id, same as before). Continue
through environment/field-select — confirm field-select cards also show
Challenge expressions. Start the battle: confirm the type-picker buttons and
the "Pet attack" term-line both show the printed unexpanded form, and that
you can still correctly enter `n`/`c` (using the *canonical* expanded values —
e.g. for `"2(x − 1)"` you'd still enter `n=2, c=-2`) and complete a turn
normally. If a CPU turn occurs, confirm its reveal card also shows the
printed form for "Pet attack" and resolves damage correctly.

- [ ] **Step 6: Verify affinity labels for a couple of Challenge pets**

Spot-check against `docs/design/pets-challenge.md` §4's authoring guidance —
in particular, confirm a Tank pet (e.g. Boulderhide: `−x+5` / `−2x+8` /
`2(x−1)`, magnitudes 1/2/2) reads **"Balanced"** (the design doc calls this out
explicitly: "every Challenge Tank reads Balanced").

- [ ] **Step 7: Verify Core mode still works exactly as before**

Toggle back to "Core" on the title screen, play a few steps of a match (pet
roll through to the battle screen), and confirm everything looks identical
to how it did before this whole plan — plain `ax+b` expressions everywhere,
no Challenge-specific text.

Check `read_console_messages` — zero errors throughout both playthroughs.

- [ ] **Step 8: Commit**

```bash
git add digital-game/index.html
git commit -m "Wire the Core/Challenge toggle into Game.petPool for dealing and trading"
```

---

## Task 6: Full regression check (both difficulties, both modes)

**Files:** none expected — pure verification. If you find a bug, fix it in
`digital-game/index.html` and commit the fix as its own small commit.

- [ ] **Step 1: Challenge mode, Two Players**

Start a **Two Players** match with "Challenge" selected. Confirm both
players' pet-roll, trade-shelf, and field-select screens show Challenge
expressions, and that a full battle (both players taking turns) resolves
correctly (damage math is unaffected by display form — verify a few hits
compute the expected damage by hand against the printed expression).

- [ ] **Step 2: Core mode, both game modes**

Play a full Core-mode Vs. Computer match and a few turns of a Core-mode Two
Players match, confirming no Challenge-related regressions (wrong labels,
stray `printed` text, console errors) appear anywhere.

- [ ] **Step 3: Commit only if you made a fix**

```bash
git add digital-game/index.html
git commit -m "Fix <describe the specific regression found>"
```
