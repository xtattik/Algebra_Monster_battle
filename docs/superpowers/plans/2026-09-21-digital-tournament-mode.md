# Digital Tournament mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a single-player "Tournament" mode: beat all 7 character archetypes in sequence with a persistent, growing zoo, and make the (currently cosmetic) capture roll real.

**Architecture:** Single-file vanilla-JS app (`digital-game/index.html`, no build step, no test runner, all logic in one IIFE using `var`/plain `function` declarations). A new `Game.mode==="tournament"` value threaded through the existing CPU-vs-human code paths (mostly by widening `Game.mode==="cpu"` checks to `Game.mode==="cpu"||Game.mode==="tournament"`, since a tournament round behaves like a Vs. Computer match once it's under way), plus new per-round advance logic, a round indicator, and two new terminal screens (trophy/defeat).

**Tech Stack:** Plain HTML/CSS/JS, no framework, no bundler.

**Dependency:** This plan assumes `docs/superpowers/plans/2026-09-21-digital-challenge-mode.md` has already been fully implemented and merged — its title-screen difficulty toggle, `Game.petPool`/`Game.difficulty`, and the `dealPets()`/`rollShelf()` pool-selection are reused here as-is (Tournament composes with Challenge per the approved design). All old_string anchors below assume that plan's changes are already in the file. If for some reason Challenge mode hasn't landed yet, stop and flag it — don't guess at different anchors.

**Note on model selection:** per Nathan's standing preference, do not use an `opus`-model reviewer for the per-task spec-compliance/code-quality reviews in this plan — use the default model. Reserve `opus` for one final review at the very end of the whole implementation (after this plan and the Challenge mode plan are both done), and only if asked.

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

Because Tournament involves real dice rolls and combat outcomes, several
verification steps below may take more than one playthrough attempt to reach
a particular state (a round win, a round loss, or all 7 rounds won) — that's
expected. Play as many attempts as it takes; you don't need to hit every
outcome on the first try.

---

## Task 1: Title-screen Tournament mode card

**Files:**
- Modify: `digital-game/index.html` (`.mode-grid` CSS; the mode-grid HTML; the mode-card click handler's button text)

- [ ] **Step 1: Widen the mode grid to fit a third card**

Find:

```css
  .mode-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px}
  @media (max-width:620px){.mode-grid{grid-template-columns:1fr}.hero .content{max-width:88%}}
```

Replace with:

```css
  .mode-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
  @media (max-width:620px){.mode-grid{grid-template-columns:1fr}.hero .content{max-width:88%}}
```

- [ ] **Step 2: Add the third mode card**

Find (this is the mode grid as it stands after the Challenge mode plan —
still just two cards; the difficulty toggle/hint that plan added sits right
after this block and is untouched here):

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
        <button class="mode-card" data-mode="tournament">
          <b>Tournament</b>
          <p>Solo gauntlet. Beat all 7 characters in a row — win a roll and their pet joins your zoo.</p>
        </button>
      </div>
```

- [ ] **Step 3: Give the start button a third label**

Find:

```js
    chosenMode = el.getAttribute("data-mode");
    var btn = document.getElementById("btn-start");
    btn.disabled=false;
    btn.textContent = chosenMode==="cpu" ? "Start — Vs. Computer ▸" : "Start — Two Players ▸";
```

Replace with:

```js
    chosenMode = el.getAttribute("data-mode");
    var btn = document.getElementById("btn-start");
    btn.disabled=false;
    btn.textContent = chosenMode==="cpu" ? "Start — Vs. Computer ▸" : chosenMode==="2p" ? "Start — Two Players ▸" : "Start — Tournament ▸";
```

- [ ] **Step 4: Verify**

Reload. Confirm three mode cards now show side by side (desktop width) or
stacked (narrow width), and clicking "Tournament" selects it (border
highlight, same as the other two cards already do) and updates the start
button to "Start — Tournament ▸". Clicking Start at this point will still
just do nothing useful yet (wired in Task 2) — don't click it, or if you do,
it's fine, nothing should error since `chosenMode==="tournament"` isn't
handled by `btn-start`'s existing handler yet and it'll fall through
unchanged (still using the `chosenMode==="cpu"?...` ternary meant for
cpu/2p) — just note that and move to Task 2 rather than trying to fix it
here.

Check `read_console_messages` — zero errors.

- [ ] **Step 5: Commit**

```bash
git add digital-game/index.html
git commit -m "Add a Tournament mode card to the title screen"
```

---

## Task 2: `beginTournament()` — round-1 setup through character select

**Files:**
- Modify: `digital-game/index.html` (`btn-start` handler; new `beginTournament()`; `pickCharacter()`)

- [ ] **Step 1: Route `btn-start` to a dedicated tournament starter**

Find:

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

Replace with:

```js
document.getElementById("btn-start").addEventListener("click", function(){
  if(!chosenMode) return;
  if(chosenMode==="tournament"){ beginTournament(); return; }
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
function beginTournament(){
  Game = {
    mode:"tournament",
    difficulty:chosenDifficulty,
    petPool: chosenDifficulty==="challenge" ? CHALLENGE_PETS : PETS,
    players:[ mkPlayer("You"), mkPlayer("CPU") ],
    environment:null, turn:0, log:[],
    tournament:{round:0, totalRounds:7, queue:shuffled(CHARACTERS)}
  };
  document.getElementById("btn-reset").hidden=false;
  beginSelect(0);
}
```

`beginTournament()` is written as a standalone function (not inlined in the
click handler) because Task 6 also calls it from the trophy/defeat screens'
"New tournament" buttons — one place constructs a fresh tournament `Game`,
reused both from the title screen and from those buttons.

- [ ] **Step 2: Give the CPU its round-1 character from the shuffled queue**

Find:

```js
function pickCharacter(playerIdx,c){
  Game.players[playerIdx].character = c;
  if(Game.mode==="cpu" && playerIdx===0){
    var remaining = CHARACTERS.filter(function(x){ return x.id!==c.id; });
    Game.players[1].character = remaining[Math.floor(Math.random()*remaining.length)];
    dealPets();
  } else if(Game.mode==="2p" && playerIdx===0){
    passTo(1, function(){ beginSelect(1); });
  } else {
    dealPets();
  }
}
```

Replace with:

```js
function pickCharacter(playerIdx,c){
  Game.players[playerIdx].character = c;
  if((Game.mode==="cpu"||Game.mode==="tournament") && playerIdx===0){
    if(Game.mode==="tournament"){
      Game.players[1].character = Game.tournament.queue[Game.tournament.round];
    } else {
      var remaining = CHARACTERS.filter(function(x){ return x.id!==c.id; });
      Game.players[1].character = remaining[Math.floor(Math.random()*remaining.length)];
    }
    dealPets();
  } else if(Game.mode==="2p" && playerIdx===0){
    passTo(1, function(){ beginSelect(1); });
  } else {
    dealPets();
  }
}
```

- [ ] **Step 3: Verify**

Reload. Select "Tournament" on the title screen, click Start. Confirm you
reach character select (same screen as Vs. Computer's), pick a character,
and land on the pet-roll screen showing "You · `<your character>`" and
"CPU · `<a character>`" — the CPU's character should be one of the 7 (it's
allowed to match your own pick, per design). `read_page`/`get_page_text` the
pet-roll screen to confirm both columns have 2 pets each.

Check `read_console_messages` — zero errors.

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Add beginTournament() and route round-1 character select through it"
```

---

## Task 3: Round 1 — trade, field, and battle

**Files:**
- Modify: `digital-game/index.html` (`advanceTrade()`, `pickFielded()`, `applyDamage()`)

- [ ] **Step 1: Let the CPU's round-1 trade resolve for tournaments too**

Find:

```js
function advanceTrade(){
  if(Game.mode==="2p" && pending.tradeIdx===0){
    passTo(1, function(){ startShelfTrade(1); });
    return;
  }
  if(Game.mode==="cpu"){
    resolveCpuShelfTrade();
  }
  showTradeSummary();
}
```

Replace with:

```js
function advanceTrade(){
  if(Game.mode==="2p" && pending.tradeIdx===0){
    passTo(1, function(){ startShelfTrade(1); });
    return;
  }
  if(Game.mode==="cpu"||Game.mode==="tournament"){
    resolveCpuShelfTrade();
  }
  showTradeSummary();
}
```

- [ ] **Step 2: Let the CPU auto-field for tournaments too**

Find:

```js
function pickFielded(idx,pi){
  Game.players[idx].fielded = Game.players[idx].roster[pi];
  if(Game.mode==="2p" && idx===0){ passTo(1,function(){ fieldStepHuman(1); }); return; }
  if(Game.mode==="cpu"){
    var cpu=Game.players[1];
    var choiceIdx = cpuFieldChoice(cpu);
    cpu.fielded = cpu.roster[choiceIdx];
  }
  Game.players.forEach(function(p){ p.curHp=p.fielded.hp; p.maxHp=p.fielded.hp; p.lastTypes=[]; });
  Game.turn = Math.random()<0.5 ? 0 : 1;
  Game.log=[];
  startBattle();
}
```

Replace with:

```js
function pickFielded(idx,pi){
  Game.players[idx].fielded = Game.players[idx].roster[pi];
  if(Game.mode==="2p" && idx===0){ passTo(1,function(){ fieldStepHuman(1); }); return; }
  if(Game.mode==="cpu"||Game.mode==="tournament"){
    var cpu=Game.players[1];
    var choiceIdx = cpuFieldChoice(cpu);
    cpu.fielded = cpu.roster[choiceIdx];
  }
  Game.players.forEach(function(p){ p.curHp=p.fielded.hp; p.maxHp=p.fielded.hp; p.lastTypes=[]; });
  Game.turn = Math.random()<0.5 ? 0 : 1;
  Game.log=[];
  startBattle();
}
```

- [ ] **Step 3: Let the player's turn correctly hand off to the CPU's turn in a tournament**

Find:

```js
  resolveDamage(attackerIdx, dmg, logPartial, function(defeated){
    var attP=Game.players[attackerIdx], defP=Game.players[1-attackerIdx];
    if(defeated){ showResult(attP,defP); return; }
    Game.turn = 1-attackerIdx;
    renderBattle();
    if(Game.mode==="cpu" && Game.turn===1) runCpuTurn();
  });
```

Replace with:

```js
  resolveDamage(attackerIdx, dmg, logPartial, function(defeated){
    var attP=Game.players[attackerIdx], defP=Game.players[1-attackerIdx];
    if(defeated){ showResult(attP,defP); return; }
    Game.turn = 1-attackerIdx;
    renderBattle();
    if((Game.mode==="cpu"||Game.mode==="tournament") && Game.turn===1) runCpuTurn();
  });
```

(This is inside `applyDamage()`. `startBattle()`'s own CPU-turn trigger —
`if(currentPlayer().name==="CPU" || ...)` — already works correctly for
tournaments without changes, since `Game.players[1].name` is `"CPU"` in
tournament mode too, per `beginTournament()` from Task 2. Don't touch that
line.)

- [ ] **Step 4: Verify a full round 1, start to finish**

Reload, start a Tournament, get through character select and pet roll.
Confirm the trade screen appears exactly once (your shelf, pick a swap or
skip), then a trade summary, then "Continue to arena" leads to a fresh
environment reveal, then field select (pick from your 2 pets), then the
battle screen. Play the battle to a win or loss — confirm turns alternate
correctly between you and the CPU (including a CPU live-reveal turn if one
occurs) and the match ends normally at `#scr-result` (still using the OLD
casual capture-box text at this point — that's expected, Tasks 5–6 haven't
run yet).

Check `read_console_messages` — zero errors.

- [ ] **Step 5: Commit**

```bash
git add digital-game/index.html
git commit -m "Route round-1 trading, field select, and battle turns through the existing CPU-mode logic for tournaments"
```

---

## Task 4: Round indicator

**Files:**
- Modify: `digital-game/index.html` (topbar HTML; `show()`)

- [ ] **Step 1: Give the topbar's subtitle an id**

Find:

```html
    <div class="brand"><b>Algebra Monster Battle</b><span>web scaffold</span></div>
```

Replace with:

```html
    <div class="brand"><b>Algebra Monster Battle</b><span id="brand-sub">web scaffold</span></div>
```

- [ ] **Step 2: Update it on every screen change**

Find:

```js
function show(id){
  document.querySelectorAll(".screen").forEach(function(s){ s.hidden = (s.id!==id); });
  window.scrollTo({top:0,behavior:reducedMotion()?"auto":"smooth"});
}
```

Replace with:

```js
function show(id){
  document.querySelectorAll(".screen").forEach(function(s){ s.hidden = (s.id!==id); });
  updateRoundIndicator();
  window.scrollTo({top:0,behavior:reducedMotion()?"auto":"smooth"});
}
function updateRoundIndicator(){
  var el=document.getElementById("brand-sub");
  el.textContent = (Game && Game.mode==="tournament") ? "Round "+(Game.tournament.round+1)+" of "+Game.tournament.totalRounds : "web scaffold";
}
```

- [ ] **Step 3: Verify**

Reload. On the title screen, confirm the topbar still reads "web scaffold".
Start a Tournament — confirm it switches to "Round 1 of 7" and stays that way
through character select, pet roll, trade, environment, field, and battle.
Click the header's Restart button and confirm (or start a Vs. Computer match
instead) — confirm the topbar reverts to "web scaffold" outside tournament
play.

Check `read_console_messages` — zero errors.

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Show a Round X of 7 indicator in the topbar during tournament play"
```

---

## Task 5: Remove the capture roll from casual matches

**Files:**
- Modify: `digital-game/index.html` (`showResult()`; the result screen's row-actions)

- [ ] **Step 1: Give the result screen's button row an id**

Find:

```html
      <div class="row-actions" style="justify-content:center">
        <button class="btn ghost" id="btn-rematch">Rematch — same characters</button>
        <button class="btn" id="btn-newgame">New game</button>
      </div>
```

Replace with:

```html
      <div class="row-actions" id="result-actions" style="justify-content:center">
        <button class="btn ghost" id="btn-rematch">Rematch — same characters</button>
        <button class="btn" id="btn-newgame">New game</button>
      </div>
```

- [ ] **Step 2: Drop the capture box from casual results**

Find:

```js
function showResult(winner,loser){
  document.getElementById("result-title").textContent = winner.name+" "+winsVerb(winner.name)+"!";
  document.getElementById("result-img").src = winner.fielded.art;
  document.getElementById("result-img").alt = winner.fielded.name;
  document.getElementById("result-sub").textContent = winner.fielded.name+" (played by "+winner.name+", the "+winner.character.name+") knocked out "+loser.fielded.name+".";
  var box=document.getElementById("capture-box");
  box.innerHTML = '<p>Roll to try to capture '+loser.fielded.name+' — a 6 adds it to your zoo.</p><button class="btn" id="capture-roll">Roll for capture</button>';
  document.getElementById("capture-roll").addEventListener("click", function(){
    var r=rollD6();
    box.innerHTML = '<p class="mono" style="font-size:1.3rem">Rolled '+r+'</p><p>'+(r===6?('<b style="color:var(--ok)">Captured!</b> '+loser.fielded.name+' joins '+possessive(winner.name)+' zoo.'):('<b style="color:var(--ink-dim)">It escaped.</b> '+loser.fielded.name+' slips away.'))+'</p>';
  });
  pending.lastWinner=winner; pending.lastLoser=loser;
  show("scr-result");
}
```

Replace with:

```js
function showResult(winner,loser){
  document.getElementById("result-actions").hidden=false;
  document.getElementById("result-title").textContent = winner.name+" "+winsVerb(winner.name)+"!";
  document.getElementById("result-img").src = winner.fielded.art;
  document.getElementById("result-img").alt = winner.fielded.name;
  document.getElementById("result-sub").textContent = winner.fielded.name+" (played by "+winner.name+", the "+winner.character.name+") knocked out "+loser.fielded.name+".";
  document.getElementById("capture-box").innerHTML="";
  pending.lastWinner=winner; pending.lastLoser=loser;
  show("scr-result");
}
```

(This function doesn't yet branch for tournament mode — that's Task 6. Right
now this change means a tournament round's win also loses its capture box,
which is fine as a brief intermediate state; Task 6 makes tournament route
elsewhere entirely before this code even runs.)

- [ ] **Step 3: Verify casual matches**

Reload. Play a Vs. Computer match to a win/loss — confirm the result screen
shows the winner announcement and Rematch/New game buttons, with **no**
capture-roll UI at all. Do the same for a Two Players match.

Check `read_console_messages` — zero errors.

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Remove the cosmetic capture-roll from casual match results"
```

---

## Task 6: Real capture, round advancement, trophy and defeat screens

**Files:**
- Modify: `digital-game/index.html` (two new `<section>` screens; `showResult()`; several new functions; two new button handlers)

- [ ] **Step 1: Add the trophy and defeat screens**

Find:

```html
    <section class="screen" id="scr-result" hidden>
      <div class="result-hero card">
        <div class="crown">🏆</div>
        <h2 id="result-title">Winner!</h2>
        <div class="pet-big"><img id="result-img" src="" alt=""></div>
        <p class="sub" id="result-sub" style="margin:0 auto;text-align:center"></p>
      </div>
      <div class="capture-box card" id="capture-box"></div>
      <div class="row-actions" id="result-actions" style="justify-content:center">
        <button class="btn ghost" id="btn-rematch">Rematch — same characters</button>
        <button class="btn" id="btn-newgame">New game</button>
      </div>
    </section>
  </main>
```

Replace with:

```html
    <section class="screen" id="scr-result" hidden>
      <div class="result-hero card">
        <div class="crown">🏆</div>
        <h2 id="result-title">Winner!</h2>
        <div class="pet-big"><img id="result-img" src="" alt=""></div>
        <p class="sub" id="result-sub" style="margin:0 auto;text-align:center"></p>
      </div>
      <div class="capture-box card" id="capture-box"></div>
      <div class="row-actions" id="result-actions" style="justify-content:center">
        <button class="btn ghost" id="btn-rematch">Rematch — same characters</button>
        <button class="btn" id="btn-newgame">New game</button>
      </div>
    </section>

    <section class="screen" id="scr-trophy" hidden>
      <div class="result-hero card">
        <div class="crown">🏆</div>
        <h2>Tournament Champion!</h2>
        <p class="sub" id="trophy-sub" style="margin:0 auto;text-align:center"></p>
      </div>
      <div class="row-actions" style="justify-content:center">
        <button class="btn ghost" id="btn-trophy-newtournament">New tournament</button>
        <button class="btn" id="btn-trophy-title">Back to title</button>
      </div>
    </section>

    <section class="screen" id="scr-defeat" hidden>
      <div class="result-hero card">
        <div class="crown">💀</div>
        <h2 id="defeat-title">Defeated</h2>
        <p class="sub" id="defeat-sub" style="margin:0 auto;text-align:center"></p>
      </div>
      <div class="row-actions" style="justify-content:center">
        <button class="btn ghost" id="btn-defeat-newtournament">New tournament</button>
        <button class="btn" id="btn-defeat-title">Back to title</button>
      </div>
    </section>
  </main>
```

- [ ] **Step 2: Route `showResult()` to a tournament-specific handler**

Find:

```js
function showResult(winner,loser){
  document.getElementById("result-actions").hidden=false;
  document.getElementById("result-title").textContent = winner.name+" "+winsVerb(winner.name)+"!";
  document.getElementById("result-img").src = winner.fielded.art;
  document.getElementById("result-img").alt = winner.fielded.name;
  document.getElementById("result-sub").textContent = winner.fielded.name+" (played by "+winner.name+", the "+winner.character.name+") knocked out "+loser.fielded.name+".";
  document.getElementById("capture-box").innerHTML="";
  pending.lastWinner=winner; pending.lastLoser=loser;
  show("scr-result");
}
```

Replace with:

```js
function showResult(winner,loser){
  if(Game.mode==="tournament"){ showTournamentResult(winner,loser); return; }
  document.getElementById("result-actions").hidden=false;
  document.getElementById("result-title").textContent = winner.name+" "+winsVerb(winner.name)+"!";
  document.getElementById("result-img").src = winner.fielded.art;
  document.getElementById("result-img").alt = winner.fielded.name;
  document.getElementById("result-sub").textContent = winner.fielded.name+" (played by "+winner.name+", the "+winner.character.name+") knocked out "+loser.fielded.name+".";
  document.getElementById("capture-box").innerHTML="";
  pending.lastWinner=winner; pending.lastLoser=loser;
  show("scr-result");
}
function showTournamentResult(winner,loser){
  if(winner!==Game.players[0]){ showTournamentDefeat(); return; }
  document.getElementById("result-actions").hidden=true;
  document.getElementById("result-title").textContent = "You win!";
  document.getElementById("result-img").src = winner.fielded.art;
  document.getElementById("result-img").alt = winner.fielded.name;
  document.getElementById("result-sub").textContent = winner.fielded.name+" knocked out "+loser.fielded.name+".";
  var box=document.getElementById("capture-box");
  box.innerHTML = '<p>Roll to try to capture '+loser.fielded.name+' — a 6 adds it to your zoo.</p><button class="btn" id="capture-roll">Roll for capture</button>';
  document.getElementById("capture-roll").addEventListener("click", function(){
    var r=rollD6();
    var captured = r===6;
    if(captured){ Game.players[0].roster.push(clonePet(loser.fielded)); }
    box.innerHTML = '<p class="mono" style="font-size:1.3rem">Rolled '+r+'</p><p>'+(captured?('<b style="color:var(--ok)">Captured!</b> '+loser.fielded.name+' joins your zoo.'):('<b style="color:var(--ink-dim)">It escaped.</b> '+loser.fielded.name+' slips away.'))+'</p>';
    var lastRound = Game.tournament.round+1>=Game.tournament.totalRounds;
    var cont=document.createElement("button");
    cont.className="btn"; cont.style.marginTop="14px";
    cont.textContent = lastRound ? "See your trophy ▸" : "Continue to next round ▸";
    cont.addEventListener("click", function(){
      Game.tournament.round++;
      if(lastRound){ showTournamentVictory(); } else { startNextRound(); }
    });
    box.appendChild(cont);
  });
  show("scr-result");
}
function dealCpuRoster(){
  var pool=shuffled(Game.petPool);
  Game.players[1].roster=[clonePet(pool[0]),clonePet(pool[1])];
}
function startNextRound(){
  Game.players[1].character = Game.tournament.queue[Game.tournament.round];
  dealCpuRoster();
  resolveCpuShelfTrade();
  drawEnvironment();
}
function showTournamentVictory(){
  document.getElementById("trophy-sub").textContent = Game.players[0].character.name+" swept all 7 rounds. Tournament Champion!";
  show("scr-trophy");
}
function showTournamentDefeat(){
  document.getElementById("defeat-title").textContent = "Defeated in round "+(Game.tournament.round+1)+" of "+Game.tournament.totalRounds;
  document.getElementById("defeat-sub").textContent = "Your run ends here — give it another go.";
  show("scr-defeat");
}
```

- [ ] **Step 3: Wire the trophy/defeat screens' buttons**

Find:

```js
document.getElementById("btn-newgame").addEventListener("click", function(){
  Game=null; document.getElementById("btn-reset").hidden=true; show("scr-title");
});
```

Replace with:

```js
document.getElementById("btn-newgame").addEventListener("click", function(){
  Game=null; document.getElementById("btn-reset").hidden=true; show("scr-title");
});
function backToTitle(){
  Game=null; document.getElementById("btn-reset").hidden=true; show("scr-title");
}
document.getElementById("btn-trophy-newtournament").addEventListener("click", beginTournament);
document.getElementById("btn-defeat-newtournament").addEventListener("click", beginTournament);
document.getElementById("btn-trophy-title").addEventListener("click", backToTitle);
document.getElementById("btn-defeat-title").addEventListener("click", backToTitle);
```

- [ ] **Step 4: Verify round advancement, a capture, and both terminal screens**

Reload and start a Tournament. Win round 1 (build the correct attack,
apply damage until the CPU's HP hits 0). On the result screen, confirm the
Rematch/New game buttons are **hidden** (this screen is tournament-specific
now) and the capture-roll appears. Click it — whichever the outcome, confirm
a "Continue to next round ▸" button appears afterward, and clicking it:
- deals the CPU a fresh 2-pet roster (different from round 1's, most likely —
  spot check the names differ),
- assigns the CPU a new character from the queue,
- draws a fresh environment,
- and lets you field-select from your roster — if the round-1 capture roll
  succeeded, confirm your roster now shows **3** pets to choose from instead
  of 2.

Keep playing rounds (win, capture-roll, continue) until either:
- **you lose a round** — confirm the flow routes to the defeat screen (not
  the old `#scr-result`), showing the correct "Defeated in round N of 7" text,
  and that both its buttons work (New tournament restarts cleanly at
  character select; Back to title returns to `#scr-title` with the topbar
  reverted to "web scaffold"); or
- **you win all 7 rounds** — confirm the trophy screen appears after the
  7th round's capture-roll and "See your trophy ▸" click, showing your
  character's name, and that both its buttons work the same way as the
  defeat screen's.

You don't need to hit both outcomes in one sitting — reaching either one is
sufficient to confirm that terminal path; if you have time, try to observe
both across separate playthroughs.

Check `read_console_messages` — zero errors throughout.

- [ ] **Step 5: Commit**

```bash
git add digital-game/index.html
git commit -m "Make capture real in Tournament mode and wire round advancement plus trophy/defeat screens"
```

---

## Task 7: Full regression check

**Files:** none expected — pure verification. If you find a bug, fix it in
`digital-game/index.html` and commit the fix as its own small commit.

- [ ] **Step 1: Tournament, several rounds, at least one capture**

Play a Tournament run for at least 3 rounds (win or lose is fine past that
point), confirming the round indicator increments correctly each time, the
CPU's character/pets/trade genuinely change round to round, and your own
roster only ever grows (never resets) between rounds.

- [ ] **Step 2: Tournament + Challenge together**

If the Challenge mode plan has landed, start a Tournament with "Challenge"
selected on the title screen. Confirm every round's pets show Challenge's
unexpanded bracket/negative expressions (same as a Challenge Vs. Computer
match would), and that capture still works correctly (a captured Challenge
pet should show its Challenge expressions too, since it's cloned straight
from `Game.petPool`).

- [ ] **Step 3: Casual modes unaffected**

Play a full Vs. Computer match and a few turns of a Two Players match.
Confirm: no capture-roll UI (Task 5), the topbar stays "web scaffold"
throughout (Task 4), and nothing about the trade/field/battle flow changed
from before this plan.

- [ ] **Step 4: Commit only if you made a fix**

```bash
git add digital-game/index.html
git commit -m "Fix <describe the specific regression found>"
```
