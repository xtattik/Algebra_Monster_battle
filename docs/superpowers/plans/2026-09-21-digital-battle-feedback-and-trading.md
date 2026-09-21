# Digital-game damage reveal + shelf trading Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make CPU/opponent hits readable (a paced reveal + damage callout instead of an instant HP change) and replace opponent-to-opponent trading with a per-player random "trade shelf," per `docs/superpowers/specs/2026-09-21-digital-battle-feedback-and-trading-design.md`.

**Architecture:** Single-file vanilla-JS app (`digital-game/index.html`, no build step, no test runner). All game logic lives in one IIFE with plain `function` declarations and `var` — every new function follows that same style and lives in the same file. Verification is manual, via the Browser pane pointed at the file directly (no dev server config exists or is needed).

**Tech Stack:** Plain HTML/CSS/JS, no framework, no bundler.

---

## Before you start

This file has no build step — you edit `digital-game/index.html` directly and reload it in the browser to see changes. There is no `.claude/launch.json` dev server; open the file directly:

```
file:///C:/Code%20Projects/Algebra_Monster_Battle/digital-game/index.html
```

Use `mcp__Claude_Browser__navigate` with that URL (or `mcp__Claude_Browser__preview_start` with `url` set to it) to open it, and re-navigate to the same URL to reload after each edit. All verification steps below assume this file is open in the Browser pane. After every check, also glance at `mcp__Claude_Browser__read_console_messages` (or pass `onlyErrors: true`) — zero errors is part of "passing" for every step in this plan, even when not called out explicitly.

Because this game has real randomness (coin-flip for who goes first, random pet deals, random shelves, d6 rolls), some verification steps may need a restart (the title screen's mode buttons, or `btn-reset` → confirm) to land in the state you need to check (e.g. "it's the CPU's turn at battle start"). That's expected — note it in your verification, don't treat it as a bug.

---

## Task 1: Damage-float and hit-flash CSS

**Files:**
- Modify: `digital-game/index.html` (inside the `<style>` block, right after the `.log-item` rules and before the `/* ---------- result screen ---------- */` comment)

- [ ] **Step 1: Add the new CSS rules**

Find this exact block (near the end of the battle-screen CSS, just before the result-screen section):

```css
  .log-item .who{font-weight:800;color:var(--ink)}
  .log-item .expr{font-family:var(--font-mono);color:var(--ink-dim)}
  .log-item .dmg{font-family:var(--font-mono);font-weight:700;color:var(--danger)}

  /* ---------- result screen ---------- */
```

Replace it with:

```css
  .log-item .who{font-weight:800;color:var(--ink)}
  .log-item .expr{font-family:var(--font-mono);color:var(--ink-dim)}
  .log-item .dmg{font-family:var(--font-mono);font-weight:700;color:var(--danger)}

  /* ---------- damage reveal ---------- */
  .dmg-float{
    position:absolute;top:44%;left:50%;transform:translate(-50%,-50%);
    font-family:var(--font-mono);font-weight:700;font-size:2.2rem;color:var(--danger);
    text-shadow:0 2px 12px rgba(0,0,0,.65);pointer-events:none;z-index:5;
    animation:dmgFloat 1.4s ease-out forwards;
  }
  @keyframes dmgFloat{
    0%{opacity:0;transform:translate(-50%,-40%) scale(.7)}
    15%{opacity:1;transform:translate(-50%,-60%) scale(1.08)}
    75%{opacity:1;transform:translate(-50%,-90%) scale(1)}
    100%{opacity:0;transform:translate(-50%,-110%) scale(1)}
  }
  .fighter.hit{animation:hitFlash .5s ease}
  @keyframes hitFlash{
    0%{box-shadow:inset 0 0 0 999px rgba(255,84,112,0)}
    20%{box-shadow:inset 0 0 0 999px rgba(255,84,112,.35)}
    100%{box-shadow:inset 0 0 0 999px rgba(255,84,112,0)}
  }
  @media (prefers-reduced-motion: reduce){
    .dmg-float{animation:none;opacity:1;top:6px;transform:translate(-50%,0)}
    .fighter.hit{animation:none}
  }

  /* ---------- result screen ---------- */
```

`.fighter` (index.html, `.fighter{padding:16px;position:relative;overflow:hidden}`) is already `position:relative`, so `.dmg-float` will position correctly inside it once it's wired up in Task 2 — nothing else to change here.

- [ ] **Step 2: Visually verify the CSS in isolation**

Nothing calls these classes yet, so verify them by injecting a throwaway test element — this doesn't depend on game state or on any closure-scoped JS function, only on `document` DOM APIs, which are always available.

Open the file in the Browser pane, then run via `mcp__Claude_Browser__javascript_tool`:

```js
(function(){
  var test=document.createElement('div');
  test.id='__csstest';
  test.className='card fighter hit';
  test.style.cssText='position:fixed;top:60px;left:40px;width:240px;height:140px;z-index:9999;background:#151827;';
  var num=document.createElement('div');
  num.className='dmg-float';
  num.textContent='\u221212';
  test.appendChild(num);
  document.body.appendChild(test);
})();
```

Take a screenshot (`mcp__Claude_Browser__computer` with `action:"screenshot"`) within the next second or two — you should see a card-like box with a large red "−12" centered in it, with a brief red inset flash on the box's edges. Then clean up:

```js
document.getElementById('__csstest').remove();
```

Confirm `read_console_messages` shows no errors from either script.

- [ ] **Step 3: Commit**

```bash
git add digital-game/index.html
git commit -m "Add damage-float and hit-flash CSS for the upcoming damage reveal"
```

---

## Task 2: Shared damage resolution + wire it into the player's own attack

**Files:**
- Modify: `digital-game/index.html` (add `spawnDamageFloat`, `clearDamageFloats`, `resolveDamage` after `renderBattle()`; rewrite `applyDamage()`)

- [ ] **Step 1: Add the damage-resolution helpers**

Find:

```js
function renderBattle(){ renderEnvStrip(); renderFighters(); renderLog(); renderActiveArea(); }

function renderActiveArea(){
```

Replace with:

```js
function renderBattle(){ renderEnvStrip(); renderFighters(); renderLog(); renderActiveArea(); }

function spawnDamageFloat(defIdx, dmg){
  var cards = document.querySelectorAll("#battle-fighters .fighter");
  var card = cards[defIdx];
  if(!card) return;
  card.classList.add("hit");
  var el = document.createElement("div");
  el.className = "dmg-float";
  el.textContent = "\u2212"+dmg;
  card.appendChild(el);
}
function clearDamageFloats(){
  document.querySelectorAll(".dmg-float").forEach(function(el){ el.remove(); });
  document.querySelectorAll(".fighter.hit").forEach(function(el){ el.classList.remove("hit"); });
}
// Shared by the player's own Apply-damage click and the CPU reveal sequence
// (Task 3) so both paths render the same paced callout instead of an instant
// HP change. attackerIdx is whichever player's turn it currently is;
// logPartial supplies the attacker-specific log fields (who/attackName/expr/
// roll/clamped) — this function fills in target/hpBefore/hpAfter itself.
function resolveDamage(attackerIdx, dmg, logPartial, onDone){
  var def = Game.players[1-attackerIdx];
  var hpBefore = Math.max(def.curHp,0);
  def.curHp = Math.max(def.curHp-dmg,0);
  Game.log.push({
    p: attackerIdx, who: logPartial.who, attackName: logPartial.attackName,
    expr: logPartial.expr, roll: logPartial.roll, dmg: dmg, clamped: logPartial.clamped,
    target: def.fielded.name, hpBefore: hpBefore, hpAfter: Math.max(def.curHp,0)
  });
  renderEnvStrip(); renderFighters(); renderLog();
  document.getElementById("battle-active").innerHTML="";
  spawnDamageFloat(1-attackerIdx, dmg);
  setTimeout(function(){
    clearDamageFloats();
    onDone(def.curHp<=0);
  }, 1400);
}

function renderActiveArea(){
```

- [ ] **Step 2: Rewrite `applyDamage()` to use `resolveDamage()`**

Find:

```js
function applyDamage(){
  var att=currentPlayer(), def=opponent();
  var hpBefore=Math.max(def.curHp,0);
  def.curHp = Math.max(def.curHp-draft.total,0);
  att.lastTypes.push(draft.type);
  if(att.lastTypes.length>2) att.lastTypes.shift();
  Game.log.push({
    p:Game.turn, who:possessive(att.name)+" "+att.fielded.name, attackName:draft.base.name,
    expr:fmtFull(draft.correctN,draft.correctC), roll:draft.roll, dmg:draft.total,
    clamped: draft.total !== draft.correctN*draft.roll+draft.correctC,
    target:def.fielded.name, hpBefore:hpBefore, hpAfter:Math.max(def.curHp,0)
  });
  draft=null;
  if(def.curHp<=0){ showResult(att,def); return; }
  Game.turn = 1-Game.turn;
  renderBattle();
  if(Game.mode==="cpu" && Game.turn===1) runCpuTurn();
}
```

Replace with:

```js
function applyDamage(){
  var att=currentPlayer();
  var attackerIdx=Game.turn;
  var dmg=draft.total;
  var logPartial={
    who: possessive(att.name)+" "+att.fielded.name, attackName: draft.base.name,
    expr: fmtFull(draft.correctN,draft.correctC), roll: draft.roll,
    clamped: draft.total !== draft.correctN*draft.roll+draft.correctC
  };
  att.lastTypes.push(draft.type);
  if(att.lastTypes.length>2) att.lastTypes.shift();
  draft=null;
  resolveDamage(attackerIdx, dmg, logPartial, function(defeated){
    var attP=Game.players[attackerIdx], defP=Game.players[1-attackerIdx];
    if(defeated){ showResult(attP,defP); return; }
    Game.turn = 1-attackerIdx;
    renderBattle();
    if(Game.mode==="cpu" && Game.turn===1) runCpuTurn();
  });
}
```

- [ ] **Step 3: Verify in the browser — human turn deals damage with a callout**

Reload the file. Click **Vs. Computer** → **Start**. Pick any character (e.g. Sorcerer). On the pet-roll screen click **Continue to trading ▸**. On the trade screen (still the old opponent-trade UI at this point — untouched until Task 6) click through without offering, to **Continue to arena ▸**. Click **Field your pet ▸**, pick either pet.

If it lands on your turn (builder screen with the 3 type buttons), pick a type, enter the correct `n`/`c` in the collect-terms boxes, click **Check**, click **Roll the die**, then click **Apply … damage ▸**. Immediately take a screenshot — you should see a red "−N" number over the CPU's fighter card with a brief flash, and the CPU's HP bar animated down. After ~1.5s it should settle into the CPU's turn (spinner, since Task 3 hasn't changed CPU behavior yet).

If it instead lands on the CPU's turn first, just wait for the CPU to move (unchanged spinner behavior for now) and it'll be your turn next — repeat the check above.

Check `read_console_messages` — zero errors.

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Add shared damage-callout reveal and wire it into the player's Apply-damage flow"
```

---

## Task 3: Auto-paced CPU turn reveal

**Files:**
- Modify: `digital-game/index.html` (add `var cpuReveal = null;`; replace `runCpuTurn()` with `runCpuTurn()` + `renderCpuReveal()` + `animateCpuRoll()` + `finishCpuRoll()`)

- [ ] **Step 1: Add the `cpuReveal` state variable**

Find:

```js
/* ---------- battle ---------- */
var draft = null;
function startBattle(){ renderBattle(); show("scr-battle"); if(currentPlayer().name==="CPU" || (Game.mode==="cpu" && Game.turn===1)) runCpuTurn(); }
```

Replace with:

```js
/* ---------- battle ---------- */
var draft = null;
var cpuReveal = null;
function startBattle(){ renderBattle(); show("scr-battle"); if(currentPlayer().name==="CPU" || (Game.mode==="cpu" && Game.turn===1)) runCpuTurn(); }
```

- [ ] **Step 2: Replace `runCpuTurn()` with the auto-paced reveal sequence**

Find:

```js
function runCpuTurn(){
  var root=document.getElementById("battle-active");
  root.innerHTML='<div class="card cpu-turn"><div class="spinner"></div><div>CPU is choosing an attack…</div></div>';
  setTimeout(function(){
    var cpu=currentPlayer();
    var allowed=allowedTypes(cpu,Game.environment);
    var best=null,bestScore=-Infinity, builtBest=null;
    allowed.forEach(function(t){
      var built=buildAttack(cpu,t,Game.environment);
      var score=built.n*3.5+built.c;
      if(score>bestScore){ bestScore=score; best=t; builtBest=built; }
    });
    var roll=rollD6();
    var raw=builtBest.n*roll+builtBest.c;
    var total=Math.max(raw,0);
    var def=opponent();
    var hpBefore=Math.max(def.curHp,0);
    def.curHp=Math.max(def.curHp-total,0);
    cpu.lastTypes.push(best); if(cpu.lastTypes.length>2) cpu.lastTypes.shift();
    Game.log.push({
      p:Game.turn, who:possessive(cpu.name)+" "+cpu.fielded.name, attackName:builtBest.atk.name,
      expr: fmtFull(builtBest.atk.a,builtBest.atk.b)+" "+fmtSignedInline(builtBest.sMod)+" "+fmtSignedInline(builtBest.eMod)+" = "+fmtFull(builtBest.n,builtBest.c),
      roll:roll, dmg:total, clamped: total!==raw, target:def.fielded.name, hpBefore:hpBefore, hpAfter:Math.max(def.curHp,0)
    });
    if(def.curHp<=0){ showResult(cpu,def); return; }
    Game.turn=1-Game.turn;
    renderBattle();
  }, 900);
}
```

Replace with:

```js
function runCpuTurn(){
  var cpu=currentPlayer();
  var allowed=allowedTypes(cpu,Game.environment);
  var bestType=null,bestScore=-Infinity, built=null;
  allowed.forEach(function(t){
    var b=buildAttack(cpu,t,Game.environment);
    var score=b.n*3.5+b.c;
    if(score>bestScore){ bestScore=score; bestType=t; built=b; }
  });
  cpuReveal={type:bestType, built:built, roll:null};
  renderCpuReveal("choosing");
  setTimeout(function(){
    renderCpuReveal("working");
    setTimeout(function(){
      renderCpuReveal("rolling");
      animateCpuRoll();
    }, 900);
  }, 600);
}
function renderCpuReveal(stage){
  var root=document.getElementById("battle-active");
  var cpu=currentPlayer();
  if(stage==="choosing"){
    root.innerHTML='<div class="card cpu-turn"><div class="spinner"></div><div>'+possessive(cpu.name)+" "+cpu.fielded.name+' is choosing an attack…</div></div>';
    return;
  }
  var b=cpuReveal.built, t=cpuReveal.type;
  var html='<div class="card builder"><h3>'+possessive(cpu.name)+" turn — "+b.atk.name+"</h3>";
  html+='<div class="term-lines">'+
    '<div class="term-line"><span class="label">Pet attack — '+b.atk.name+'</span><span class="expr">'+fmtFull(b.atk.a,b.atk.b)+'</span></div>'+
    '<div class="term-line"><span class="label">'+cpu.name+"'s "+TYPE_LABEL[t]+' stat ('+cpu.character.stats[t]+')</span><span class="expr">'+fmtSigned(b.sMod)+'</span></div>'+
    '<div class="term-line"><span class="label">'+Game.environment.name+'</span><span class="expr">'+fmtSigned(b.eMod)+'</span></div>'+
    '</div>';
  html+='<p class="sub" style="margin-top:14px">Collected: <b>'+fmtFull(b.n,b.c)+'</b></p>';
  if(stage==="rolling" || stage==="rolled"){
    html+='<div class="roll-zone"><div class="die" id="cpu-die">'+(cpuReveal.roll||"?")+'</div>';
    if(stage==="rolled"){
      html+='<div class="roll-result">Substitute <b>x = '+cpuReveal.roll+'</b> into <b>'+fmtFull(b.n,b.c)+'</b> — floors at 0.</div>';
    }
    html+='</div>';
  }
  html+='</div>';
  root.innerHTML=html;
}
function animateCpuRoll(){
  var dieEl=document.getElementById("cpu-die");
  var final=rollD6();
  if(reducedMotion()){ finishCpuRoll(final); return; }
  var ticks=0, max=10;
  var iv=setInterval(function(){
    dieEl.textContent = 1+Math.floor(Math.random()*6);
    ticks++;
    if(ticks>=max){ clearInterval(iv); finishCpuRoll(final); }
  },60);
}
function finishCpuRoll(final){
  cpuReveal.roll=final;
  renderCpuReveal("rolled");
  setTimeout(function(){
    var cpu=currentPlayer();
    var attackerIdx=Game.turn;
    var b=cpuReveal.built, t=cpuReveal.type;
    var raw=b.n*cpuReveal.roll+b.c;
    var total=Math.max(raw,0);
    var logPartial={
      who: possessive(cpu.name)+" "+cpu.fielded.name, attackName: b.atk.name,
      expr: fmtFull(b.n,b.c), roll: cpuReveal.roll, clamped: total!==raw
    };
    cpu.lastTypes.push(t); if(cpu.lastTypes.length>2) cpu.lastTypes.shift();
    cpuReveal=null;
    resolveDamage(attackerIdx, total, logPartial, function(defeated){
      var attP=Game.players[attackerIdx], defP=Game.players[1-attackerIdx];
      if(defeated){ showResult(attP,defP); return; }
      Game.turn=1-attackerIdx;
      renderBattle();
    });
  }, 900);
}
```

Note: `fmtSignedInline` (used by the old inline CPU log expression) is no longer called from here — leave its definition alone, it's a small formatting helper and removing it isn't part of this plan's scope.

- [ ] **Step 3: Verify the CPU reveal sequence in the browser**

Reload the file, start a **Vs. Computer** match (character, pets, trade-through — unchanged for now, environment, field). If the CPU goes first, watch the battle screen:
- ~0ms: spinner "… is choosing an attack…"
- ~600ms: a card headed "CPU turn — <attack name>" with three term-lines (pet attack / CPU's stat / terrain) and a "Collected: nx + c" line
- ~1500ms: a die appears and visibly ticks
- ~2400ms: the die settles and shows "Substitute x = N into nx+c"
- ~3300ms: the damage float appears over your fighter's card, HP bar drops
- ~4700ms: turn returns to you

Take 3–4 screenshots spaced roughly 800ms–1s apart across that window to confirm the stages appear in order (exact timings will drift a little due to tool round-trip latency — that's fine, just confirm the sequence, not exact ms). If the human goes first instead, play one turn to hand it to the CPU, then observe.

Check `read_console_messages` — zero errors throughout.

- [ ] **Step 4: Commit**

```bash
git add digital-game/index.html
git commit -m "Give the CPU turn an auto-paced live-working reveal instead of resolving instantly"
```

---

## Task 4: Feature 1 regression check (both modes)

**Files:** none expected — pure verification. If you find a bug, fix it in `digital-game/index.html` and commit the fix as its own small commit before moving on.

- [ ] **Step 1: Play a full Vs. Computer match to completion**

From the title screen, play through to a win or loss (restart with the header's **Restart** button if you need to retry for a particular outcome). Confirm:
- Every hit (yours and the CPU's) shows the damage-float callout.
- The CPU reveal sequence from Task 3 plays every CPU turn, not just the first.
- On defeat, the result screen and capture-roll flow (`showResult`, "Roll for capture") still work.
- `read_console_messages` shows no errors across the whole match.

- [ ] **Step 2: Play a few turns of Two Players mode**

Start a **Two Players** match, get through both pass-device select/field steps, and play at least 2 turns (one per player). Confirm:
- Both players' hits show the damage-float callout (no CPU reveal card appears for either — 2P has no CPU).
- The pass-device interstitial (`scr-pass`) still appears correctly between turns of setup (it's not used between battle turns, only setup — confirm that's still the case, i.e. battle turns don't unexpectedly show a pass screen).

- [ ] **Step 3: Commit only if you made a fix**

```bash
git add digital-game/index.html
git commit -m "Fix <describe the specific regression found>"
```

---

## Task 5: Trade screen copy update

**Files:**
- Modify: `digital-game/index.html` (the `#scr-trade` section markup)

- [ ] **Step 1: Update the static trade-screen copy**

Find:

```html
    <section class="screen" id="scr-trade" hidden>
      <div class="screen-head">
        <div class="eyebrow">One trade, before battle</div>
        <h2 id="trade-title">Offer a pet?</h2>
        <p class="sub">Put one pet on the block, or keep both. A swap only happens if <em>both</em> sides offer one — that's the "mutual agreement" rule.</p>
      </div>
      <div class="trade-cols" id="trade-grid"></div>
      <div id="trade-result-box"></div>
      <div class="row-actions"><button class="btn" id="trade-continue">Confirm &amp; continue ▸</button></div>
    </section>
```

Replace with:

```html
    <section class="screen" id="scr-trade" hidden>
      <div class="screen-head">
        <div class="eyebrow">One trade, before battle</div>
        <h2 id="trade-title">Browse the trade shelf</h2>
        <p class="sub">Six other pets are up for grabs. Swap one of yours for one of theirs, or skip if nothing beats what you've already got.</p>
      </div>
      <div class="trade-cols" id="trade-grid"></div>
      <div id="trade-result-box"></div>
      <div class="row-actions"><button class="btn" id="trade-continue">Skip trading ▸</button></div>
    </section>
```

(The JS in Task 6 overwrites `#trade-title` and `#trade-continue`'s text as the flow progresses — this step only changes what's shown before any JS has touched them.)

- [ ] **Step 2: Verify the copy landed**

Reload the file. Run via `mcp__Claude_Browser__javascript_tool`:

```js
({title: document.getElementById('trade-title').textContent, sub: document.querySelector('#scr-trade .sub').textContent, btn: document.getElementById('trade-continue').textContent})
```

Confirm the result matches the new copy exactly (this works even though `#scr-trade` is `hidden` — `textContent` doesn't care about visibility).

- [ ] **Step 3: Commit**

```bash
git add digital-game/index.html
git commit -m "Update trade-screen copy to describe the upcoming shelf-trading flow"
```

---

## Task 6: Replace opponent trading with shelf trading

**Files:**
- Modify: `digital-game/index.html` (replace the entire `/* ---------- trade ---------- */` section: `beginTrade`, `tradeStepHuman`, `renderTradeScreen`, the `trade-continue` click handler, `cpuTradeDecision`, `resolveTrade`)

- [ ] **Step 1: Replace the trade section**

Find this exact block (starts right after the pet-roll section's continue-button listener, ends right before the `/* ---------- environment ---------- */` comment):

```js
/* ---------- trade ---------- */
function beginTrade(){
  pending.offers=[null,null];
  pending.tradeDone=false;
  pending.tradeStage=0;
  document.getElementById("trade-continue").textContent="Confirm & continue ▸";
  if(Game.mode==="cpu"){
    document.getElementById("trade-title").textContent="Offer a pet?";
    renderTradeScreen(0,true);
    show("scr-trade");
  } else {
    tradeStepHuman(0);
  }
}
function tradeStepHuman(idx){
  document.getElementById("trade-title").textContent = Game.players[idx].name+": offer a pet?";
  renderTradeScreen(idx,false);
  show("scr-trade");
}
function renderTradeScreen(activeIdx, showBoth){
  var grid=document.getElementById("trade-grid");
  grid.innerHTML="";
  document.getElementById("trade-result-box").innerHTML="";
  Game.players.forEach(function(p,idx){
    var col=document.createElement("div");
    col.className="trade-col";
    var interactive = showBoth || idx===activeIdx;
    var h=document.createElement("h3"); h.textContent=p.name+(interactive?"":" (hidden)");
    col.appendChild(h);
    if(!interactive){
      var note=document.createElement("p"); note.className="sub"; note.textContent="Choice locked in.";
      col.appendChild(note);
    } else {
      var list=document.createElement("div"); list.className="list";
      p.roster.forEach(function(pet,pi){
        var offered = pending.offers[idx]===pi;
        var card=document.createElement("div");
        card.className="art-card"+(offered?" chosen":"");
        card.innerHTML = petCardInner(pet, offered?{flagText:"Offering",flagColor:"var(--danger)"}:null);
        card.addEventListener("click", function(){
          pending.offers[idx] = offered ? null : pi;
          if(Game.mode==="cpu") renderTradeScreen(0,true); else renderTradeScreen(idx,false);
        });
        list.appendChild(card);
      });
      col.appendChild(list);
    }
    grid.appendChild(col);
  });
}
document.getElementById("trade-continue").addEventListener("click", function(){
  if(pending.tradeDone){
    pending.tradeDone=false;
    drawEnvironment();
    return;
  }
  if(Game.mode==="2p" && pending.tradeStage!==1){
    pending.tradeStage=1;
    passTo(1, function(){ tradeStepHuman(1); });
    return;
  }
  if(Game.mode==="cpu"){
    var cpu = Game.players[1];
    var cpuOff = cpuTradeDecision(cpu);
    pending.offers[1] = cpuOff;
  }
  resolveTrade();
});
function cpuTradeDecision(cpu){
  var ht = highStatType(cpu.character);
  if(!ht) return null;
  var a=cpu.roster[0].attacks[ht].a, b=cpu.roster[1].attacks[ht].a;
  if(a===b) return null;
  return a<b?0:1;
}
function resolveTrade(){
  var off0=pending.offers[0], off1=pending.offers[1];
  var box=document.getElementById("trade-result-box");
  var dealMade = off0!=null && off1!=null;
  var swappedNames = null;
  if(dealMade){
    var p0=Game.players[0], p1=Game.players[1];
    var a=p0.roster[off0], b=p1.roster[off1];
    p0.roster[off0]=b; p1.roster[off1]=a;
    swappedNames = {a:a.name,b:b.name};
    box.innerHTML='<div class="trade-result"><b style="color:var(--ok)">Deal made:</b> '+a.name+' ↔ '+b.name+'.</div>';
  } else {
    box.innerHTML='<div class="trade-result">No deal — a swap needs an offer from both sides. Rosters stay as dealt.</div>';
  }
  pending.tradeStage=0;
  pending.tradeDone=true;
  document.getElementById("trade-title").textContent = dealMade ? "Trade complete" : "No trade";
  var grid=document.getElementById("trade-grid");
  grid.innerHTML="";
  Game.players.forEach(function(p){
    var col=document.createElement("div");
    col.className="trade-col";
    var h=document.createElement("h3"); h.textContent=p.name;
    col.appendChild(h);
    var list=document.createElement("div"); list.className="list";
    p.roster.forEach(function(pet){
      var justTraded = swappedNames && (pet.name===swappedNames.a || pet.name===swappedNames.b);
      var card=document.createElement("div");
      card.className="art-card"+(justTraded?" chosen":"");
      card.style.cursor="default";
      card.innerHTML = petCardInner(pet, justTraded?{flagText:"Traded in",flagColor:"var(--ok)"}:null);
      list.appendChild(card);
    });
    col.appendChild(list);
    grid.appendChild(col);
  });
  document.getElementById("trade-continue").textContent="Continue to arena ▸";
}
```

Replace it with:

```js
/* ---------- trade ---------- */
function rollShelf(player){
  var ownIds = player.roster.map(function(p){ return p.id; });
  var pool = PETS.filter(function(p){ return ownIds.indexOf(p.id)===-1; });
  return shuffled(pool).slice(0,6).map(clonePet);
}
function cpuShelfDecision(cpu, shelf){
  var ht = highStatType(cpu.character);
  if(!ht) return null;
  function val(pet){ return pet.attacks[ht].a; }
  var worseIdx = val(cpu.roster[0]) <= val(cpu.roster[1]) ? 0 : 1;
  var bestShelfIdx = -1, bestVal = val(cpu.roster[worseIdx]);
  shelf.forEach(function(pet,i){
    if(val(pet) > bestVal){ bestVal = val(pet); bestShelfIdx = i; }
  });
  return bestShelfIdx===-1 ? null : {give:worseIdx, take:bestShelfIdx};
}
function beginTrade(){
  pending.shelfResults=[null,null];
  pending.tradeSummaryShown=false;
  startShelfTrade(0);
}
function startShelfTrade(idx){
  pending.tradeIdx=idx;
  pending.shelf=rollShelf(Game.players[idx]);
  pending.give=null;
  pending.take=null;
  document.getElementById("trade-title").textContent = Game.players[idx].name+", pick a swap";
  renderShelfScreen();
  show("scr-trade");
}
function renderShelfScreen(){
  var idx=pending.tradeIdx, p=Game.players[idx];
  var grid=document.getElementById("trade-grid");
  grid.innerHTML="";
  document.getElementById("trade-result-box").innerHTML="";

  var mineCol=document.createElement("div"); mineCol.className="trade-col";
  var mineH=document.createElement("h3"); mineH.textContent="Your zoo"; mineCol.appendChild(mineH);
  var mineList=document.createElement("div"); mineList.className="list";
  p.roster.forEach(function(pet,pi){
    var chosen = pending.give===pi;
    var card=document.createElement("div");
    card.className="art-card"+(chosen?" chosen":"");
    card.innerHTML = petCardInner(pet, chosen?{flagText:"Giving up",flagColor:"var(--danger)"}:null);
    card.addEventListener("click", function(){
      pending.give = chosen ? null : pi;
      renderShelfScreen();
    });
    mineList.appendChild(card);
  });
  mineCol.appendChild(mineList);

  var shelfCol=document.createElement("div"); shelfCol.className="trade-col";
  var shelfH=document.createElement("h3"); shelfH.textContent="Trade shelf"; shelfCol.appendChild(shelfH);
  var shelfList=document.createElement("div"); shelfList.className="list";
  pending.shelf.forEach(function(pet,si){
    var chosen = pending.take===si;
    var card=document.createElement("div");
    card.className="art-card"+(chosen?" chosen":"");
    card.innerHTML = petCardInner(pet, chosen?{flagText:"Taking",flagColor:"var(--ok)"}:null);
    card.addEventListener("click", function(){
      pending.take = chosen ? null : si;
      renderShelfScreen();
    });
    shelfList.appendChild(card);
  });
  shelfCol.appendChild(shelfList);

  grid.appendChild(mineCol);
  grid.appendChild(shelfCol);

  document.getElementById("trade-continue").textContent =
    (pending.give!=null && pending.take!=null) ? "Confirm swap ▸" : "Skip trading ▸";
}
document.getElementById("trade-continue").addEventListener("click", function(){
  if(pending.tradeSummaryShown){
    pending.tradeSummaryShown=false;
    drawEnvironment();
    return;
  }
  var idx=pending.tradeIdx, p=Game.players[idx];
  var traded = pending.give!=null && pending.take!=null;
  var gaveName=null, tookName=null;
  if(traded){
    gaveName = p.roster[pending.give].name;
    tookName = pending.shelf[pending.take].name;
    p.roster[pending.give] = pending.shelf[pending.take];
  }
  pending.shelfResults[idx] = {traded:traded, gaveName:gaveName, tookName:tookName};
  advanceTrade();
});
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
function resolveCpuShelfTrade(){
  var cpu=Game.players[1];
  var shelf=rollShelf(cpu);
  var decision=cpuShelfDecision(cpu, shelf);
  if(decision){
    pending.shelfResults[1] = {traded:true, gaveName:cpu.roster[decision.give].name, tookName:shelf[decision.take].name};
    cpu.roster[decision.give] = shelf[decision.take];
  } else {
    pending.shelfResults[1] = {traded:false, gaveName:null, tookName:null};
  }
}
function showTradeSummary(){
  document.getElementById("trade-title").textContent = "Trading complete";
  var grid=document.getElementById("trade-grid");
  grid.innerHTML="";
  Game.players.forEach(function(p,idx){
    var result=pending.shelfResults[idx];
    var col=document.createElement("div");
    col.className="trade-col";
    var h=document.createElement("h3"); h.textContent=p.name;
    col.appendChild(h);
    var list=document.createElement("div"); list.className="list";
    p.roster.forEach(function(pet){
      var justTraded = result && result.traded && pet.name===result.tookName;
      var card=document.createElement("div");
      card.className="art-card"+(justTraded?" chosen":"");
      card.style.cursor="default";
      card.innerHTML = petCardInner(pet, justTraded?{flagText:"Traded in",flagColor:"var(--ok)"}:null);
      list.appendChild(card);
    });
    col.appendChild(list);
    grid.appendChild(col);
  });
  var box=document.getElementById("trade-result-box");
  box.innerHTML = Game.players.map(function(p,idx){
    var r=pending.shelfResults[idx];
    var msg = (r && r.traded) ? (p.name+" traded "+r.gaveName+" for "+r.tookName+".") : (p.name+" kept both pets.");
    return '<div class="trade-result">'+msg+'</div>';
  }).join("");
  document.getElementById("trade-continue").textContent="Continue to arena ▸";
  pending.tradeSummaryShown=true;
}
```

- [ ] **Step 2: Verify shelf trading — CPU mode, confirming a swap**

Reload. Start **Vs. Computer**, pick a character, get through pet roll to the trade screen. Confirm via `mcp__Claude_Browser__read_page` (or `get_page_text`) that:
- The left column is headed "Your zoo" with exactly 2 pets.
- The right column is headed "Trade shelf" with exactly 6 pets, and none of those 6 names match either of your 2 "Your zoo" pets (rollShelf's own-roster exclusion).

Click one of your zoo pets (it should flag "Giving up") and one shelf pet (it should flag "Taking"); confirm the button text changes to **"Confirm swap ▸"**. Click it. Confirm the resulting summary screen shows your roster with the shelf pet flagged "Traded in" in place of the one you gave up, and a line of text under it like "You traded `<old>` for `<new>`." (CPU's row will show either a swap or "CPU kept both pets." depending on its random shelf — either is correct). Click **"Continue to arena ▸"** and confirm it proceeds to the environment screen.

- [ ] **Step 3: Verify shelf trading — skip path**

Restart (header **Restart** → confirm, or **New game** from a finished match). Get back to the trade screen. Without clicking any pet, confirm the button reads **"Skip trading ▸"**. Click it, confirm the summary shows "You kept both pets." with no "Traded in" flag, and continuing still works.

- [ ] **Step 4: Verify shelf trading — Two Players mode**

Start a **Two Players** match, get to the trade screen for Player 1. Note the 6 shelf pet names shown. Pick a swap (or skip), click through — this should trigger the existing pass-device interstitial before Player 2's own trade screen appears. Confirm Player 2's shelf shows a *different* set of 6 pet names than Player 1 saw (independently rolled — an occasional overlap in one or two names by chance is fine, but they shouldn't be the identical set of 6 in the identical order every time; if in doubt, repeat once). Confirm Player 2 can also swap or skip, and the final summary shows both players' outcomes before continuing.

- [ ] **Step 5: Commit**

```bash
git add digital-game/index.html
git commit -m "Replace opponent-to-opponent trading with a per-player random trade shelf"
```

---

## Task 7: Full end-to-end regression check

**Files:** none expected — pure verification. If you find a bug, fix it in `digital-game/index.html` and commit the fix as its own small commit.

- [ ] **Step 1: Full Vs. Computer playthrough**

Title → Vs. Computer → character select → pet roll → trade shelf (swap or skip) → environment reveal → field select → battle (confirm both the player Apply-damage callout from Task 2 and the CPU live-reveal sequence from Task 3 both still work, repeatedly, across a whole match) → result screen → capture roll. Confirm **Rematch** and **New game** both still work afterward. Check `read_console_messages` for zero errors across the whole run.

- [ ] **Step 2: Full Two Players playthrough**

Title → Two Players → both players' character select (with pass-device screens) → pet roll → both players' trade shelf steps → environment → both players' field select → battle (both players' hits show the damage callout; no CPU reveal card ever appears) → result → capture roll. Check `read_console_messages` for zero errors.

- [ ] **Step 3: Commit only if you made a fix**

```bash
git add digital-game/index.html
git commit -m "Fix <describe the specific regression found>"
```
