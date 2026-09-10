# Algebra Monster Battle — Core Rules v2 (design)

**Date:** 2026-09-10
**Status:** Draft for review — decisions locked with the design owner; numbers provisional pending first v2 playtest.
**Supersedes (on implementation):** [`core-rules.md`](core-rules.md) §5, §6.1, §8, §9.3; [`environments.md`](environments.md) wholesale; [`pets.md`](pets.md) §3.
**Keeps:** v1 stays printable and correct until v2 is built. This doc is the decision record; component specs (`environments-v2.md`, `pets-v2.md`) and the rebuild follow.

---

## 1. Why v2

Playtest verdict: **the game works** — the maths-as-resolution loop is sound and the pacing is roughly right. Four problems surfaced:

1. **The battle sheet is too complex for the students.** Too much instruction up top; one match per page wastes paper.
2. **Bonuses are all-or-nothing.** A `−x` hinder on a `3x` attack still gives `2x`, which beats the `x+1` backup — so terrain almost never changes what you should do. And a `−x` hinder is net-zero for a character whose matching stat is High. There is little reason to ever switch off your best attack.
3. **The defence stat is too abstract.** "Your opponent's Strength modifies your roll" is a mechanic students without tabletop-RPG background don't intuit. Students also confused the `strike` attack type with the `Strength` stat.
4. **Nothing forces adaptation between rounds.** A player who builds a one-shot-kill combination is never punished for it.

v2 addresses all four. The changes chain: **§2 (stat model) is the keystone; §6 (pet rebalance) makes adaptation survivable; §4 (terrain) forces it; §8 (sheet) supports the faster play.**

## 2. Stat model — three parallel offensive stats

**All three stats now buff their own attack type. There is no defence stat.**

| Your tier in the stat | Modifier to your matching attack |
|---|---|
| High | `+x` |
| Average | `0` |
| Low | `−x` |

- **Magic** → your **magic** attacks
- **Strength** → your **strength** attacks *(renamed from "strike" — the attack type name now matches the stat name)*
- **Agility** → your **agility** attacks

One rule, three identical cases. A student checks: *what attack am I using? → check that one stat.* No "check the enemy's stat" step, no strike carve-out.

**HP is your defence.** A durable character/pet outlasts; there is no stat that reduces incoming damage. Character stat stays `±x` (see §4 for why the environment goes bigger).

## 3. Damage model v2

The attacker's expression has **at most three terms**:

```
damage = your chosen pet attack            (ax + b)
       + your matching stat modifier        (+x / 0 / −x  — §2)
       + the environment's effect on that attack type   (+2x / +x / 0 / −x / −2x  — §4)
```

Then: **collect like terms → substitute your die roll → floor → subtract from the enemy pet's HP.**

- Every modifier is an **`x` term** — `+x`, `−x`, `+2x`, `−2x`, or `0`. Never a bare number. This is what forces the like-terms step every turn.
- **Cancel** (§4): the attack type cannot be chosen at all this match — there is no expression to build.

### 3.1 Minimums (unchanged from v1)

- A **base pet attack** never evaluates below **1**; the card prints its own floor (`x − 1 (min 1)`).
- **After modifiers**, damage floors at **0**.

### 3.2 Worked examples

**A — Sorcerer casting in boost terrain.** Sorcerer (Magic High) fields a pet with magic attack `3x + 2`, in **Arcane Nexus** (Boost Magic `+2x`).
`3x + 2 + x + 2x = 6x + 2` → roll 5 → `32`.

**B — same Sorcerer, hostile terrain (still usable).** Same pet, in **Mistfen** (Weaken Magic `−2x`).
`3x + 2 + x − 2x = 2x + 2` → roll 5 → `12`. Reduced, not gone — the Sorcerer's `+x` still buys a net `−x` edge over a non-caster (who would land `3x + 2 − x − 2x = 2`).

**C — forced switch.** Same Sorcerer/pet, in **Null Field** (Magic **cancelled**). Magic is off the table. The pet's *strength* attack is `2x` (v2 secondary — §6). Sorcerer is Average Strength → `0`.
`2x + 0 = 2x` → roll 5 → `10`. A worse turn than a boosted `6x + 2`, but a real turn — this is the point.

## 4. Environments v2

### 4.1 The three verbs

| Verb | On the card / sheet | Notes |
|---|---|---|
| **Boost** | `+2x` (primary) or `+x` (secondary) to one attack type | |
| **Weaken** | `−2x` (primary) or `−x` (secondary) | still a pure like-terms term |
| **Cancel** | that attack type **cannot be used** this match | ignores the character bonus entirely — the combo-killer |

A card carries **one primary effect** and **optionally one secondary effect on a different attack type**.
The **`±2x` dial is the environment's job**; the character stat stays `±x`. So a favoured character in weak terrain is penalised *less* than an unfavoured one — strategy, not a wall — while a Cancel bypasses the character bonus for everyone equally.

*(A "Sap" verb — halve the final damage, round down — was considered and cut: it is the only step that isn't algebra. Parked for a possible advanced version.)*

### 4.2 Reveal order

**Terrain is drawn first; then both players choose which pet to field.** (Simultaneously, revealed together.)

Rationale (design owner): a backup pet is unlikely to play to your strength as well, so a Cancel forces you onto a **less-than-perfect setup — but not a forfeit**. If your opponent is hard-countered too, it may not matter. This rewards **trading well** (keeping a pet that isn't your affinity) rather than guessing. A player who built a single one-shot combination and never hedged is the one who gets punished — *that is the accepted risk of a glass-cannon build.*

### 4.3 The deck

Names live in `cards/environments-v2.md` and are cheap to swap; the mechanics are the contract.

| Group | Cards | Effect |
|---|---|---|
| **Pure boost** (3) | Arcane Nexus / Warblood Arena / Dark Cavern | Boost Magic / Strength / Agility `+2x` |
| **Boost + cost** (3) | Runestone Vault / Bonepit / Highcrag Winds | `+2x` one type, `−x` a different type |
| **Hard weaken** (3) | Mistfen / Scorching Desert / Salt Flats | `−2x` to Magic / Strength / Agility |
| **Double slog** (2) | Stormfront / Thin Air | `−x` to two types (one type still lands clean) |
| **Cancel** (3) | Null Field / Black Ice / Ethereal Mist | Magic / Agility / Strength **unusable** |
| **Neutral** (1) | Open Field | nothing |

- **Frequency is a print-time choice.** The teacher prints as many copies of each design as they like — a class deck weighted toward boosts is gentler, one heavy on cancels is a harder challenge. More *designs* is always better; the mix is tuned per class.
- All three attack types are equally cancellable, so no build is safe from every terrain.
- "Ethereal Mist" flavour for the strength cancel: *blows pass through — only spellcraft and speed touch anything here.*
- Room to grow: more `+2x/−x` hybrids and themed doubles can be added as designs without changing the model.
- **Support tier** (differentiation): only ever play Open Field.

## 5. Characters v2

Roster and stat lines are **unchanged** from [`characters.md`](characters.md) §4 — each character is High in one stat, Average in one, Low in one, except the **Bard** (all Average = the terrain-proof generalist, now a real identity). Only the *meaning* of a tier changes and the flavour follows:

| Was (v1, defensive Strength) | Now (v2, offensive Strength) |
|---|---|
| Paladin — "a wall; enemy attacks take `−x`" | Paladin — **heavy hitter**; strength attacks gain `+x` |
| Illusionist — "paper defence; enemies get `+x` vs you" | Illusionist — **glass-cannon caster**; weak in a brawl (`−x` strength attacks) |
| Trickster — "nimble, fragile" | Trickster — **fast**; weak in a straight fight (`−x` strength attacks) |
| Barbarian — "tanky bruiser" | Barbarian — **bruiser**; big strength attacks, poor magic |

**Card layout simplifies:** three identical rows (stat — tier — `±x` term — one line of plain words), no special "defence" row, no red treatment. The generator's effect table just makes the Strength rows mirror Magic/Agility.

## 6. Pets v2 — number model *(provisional; `pets-v2.md` finalises after playtest)*

Two changes: **HP up** (longer matches, bigger swings, variance evens out) and **the secondary attack buffed** so a forced switch (§3.2 C) is playable rather than a forfeit.

| Archetype | HP (v1 → v2) | Affinity attack | **Secondary** | Tertiary |
|---|---|---|---|---|
| Glass cannon | ~28 → **~40** | `4x` or `4x + 1` | **`2x`** | `x − 1 (min 1)` |
| Baseline | ~48 → **~75** | `3x + 1` or `3x + 2` | **`2x` or `2x + 1`** | `x + 1` |
| Tank | ~82 → **~100** | `3x` or `2x + 2` | **`2x`** | `x` |

Coefficient range widens to `a ∈ {1 … 4}`; constants stay `b ∈ {−2 … 2}`. Every attack still has an `x` term.

### 6.1 Balance targets

- No **un-boosted** attack one-shots any pet.
- A **fully-aligned glass-cannon burst** (glass-cannon pet + matching High stat + Boost terrain) — e.g. `4x + x + 2x = 7x` — one-shots a ~40 HP glass cannon on a **5–6** (the payoff for a well-planned trade), and takes a baseline to roughly half.
- A **forced switch to the `2x` secondary** still contributes ~8–12 per turn — losable, not hopeless.
- A **cancelled affinity + an already-bad matchup** is the worst case → the loser drops to the second-chance bracket (§7), not straight out. Accepted: this is the downside of choosing a spike build.
- Typical match: **8–14 total attacks**.
- **No first-turn mitigation.** In a glass-cannon mirror whoever spikes first may just win — that is the archetype's built-in gamble, not a bug.

### 6.2 Trade phase, redefined

v1: "trade to cover your character's weak stat." v2: your best line is **affinity attack matching your High stat**; you trade for **(a)** a pet whose affinity matches your High stat, and **(b)** a second pet of a *different* type so a Cancel doesn't strand you. Specialise for ceiling, hedge for terrain.

## 7. Game flow v2 (changes only)

- **§9.3 step order:** draw terrain → **both choose a pet (simultaneous reveal)** → first turn → play.
- **Choose your attack *before* you roll.** (v1 was roll-then-choose.) You commit an attack type + build its expression — ideally during your opponent's turn — then on your turn you only roll and substitute. Removes "I rolled a 1, so I'll pick the attack with the bigger constant" and speeds play. The battle sheet enforces it with a printed line (§8).
- **Elimination softens:** the loser of a duel drops to the **second-chance bracket by default** rather than out of the session. A terrain-RNG loss shouldn't end a student's game. (Teachers can still run hard single-elimination as an extension.)
- No defender roll for defence (there is no defence) — a player only rolls on their own turn, as the attacker.

## 8. Battle sheet v2

One A4 page, **multiple attack blocks** (target 4–6), simplified.

- **No method panel.** The five steps become five labelled blanks *inside* each block:
  1. Attack (◦ magic ◦ strength ◦ agility): `____`  — *your pet's chosen attack equation*
  2. `+` my stat bonus: `____`
  3. `+` environment: `____`
  4. simplify → `nx + c`: `____`
  5. **roll** `x = ___` → `____` damage   → enemy HP: `___ − ___ = ___`
- A **printed rule line between step 3 and step 5**: *"fill everything above this line before you touch the die."* — the choose-before-roll rule, enforced by layout.
- Match setup (character + tiers, pets, environment card + its effects) written **once** at the top.
- **HP columns** down the side: one running track per pet for the whole sheet; a long match continues on sheet 2, carrying HP forward.
- A one-line **result** box (won / lost / pet captured) for the ladder.
- Keep: the fast-marking value (each block ends in `nx + c` then a substitution — the gradable evidence).

## 9. What needs rebuilding

| Component | Work |
|---|---|
| `core-rules.md` | rewrite §5, §6.1, §8, §9.3 to v2 (or replace with this doc promoted) |
| Environment deck | new `environments-v2.md` + `cards/environments-v2.md` + generator changes (3 verbs: Boost `+2x`/`+x`, Weaken `−2x`/`−x`, Cancel); ~15 designs |
| Core pet deck | `pets-v2.md`; new HP + buffed secondary attack on all 22; rename `strike` → `strength`. **Challenge deck deferred** — rebuild after Core v2 has settled (§10.3). |
| Character cards | generator effect-table: Strength rows mirror Magic/Agility; drop the defence/red treatment; re-flavour playstyle lines |
| Battle sheet | rebuild per §8 |
| Student rulebook / teacher guide | rewrite the damage-model, environment, and flow sections; new worked examples A–D above |
| Answer key | extend the fast-marking lookup table to `8x` (boost `+2x` + char `+x` on a `4x` attack); new scenario answers |
| Fast-marking generator | `tools/gen_lookup.py` coefficient range → `1..8` |

### Decided

- **Cancel frequency** — keep all 3 cancel designs; the teacher tunes the mix by how many copies of each card they print (§4.3).
- **Sap** — cut. Scorching Desert is a plain `−2x` Weaken Strength. (§4.1)
- **First-turn advantage in a glass-cannon mirror** — no mitigation; it is the archetype's accepted gamble. (§6.1)
- **Challenge deck** — deferred; rebuild after Core v2 has settled. (§9)

### Still open for playtest

1. **Exact HP + coefficients** — the §6 model is a first target; the second playtest tunes per-pet.
2. **Tank mirrors** — a 100-HP tank vs 100-HP tank with `3x`-ish attacks is ~9 turns each. Acceptable, or tanks to ~90 / call it on HP-remaining?
3. **Secondary-attack ceiling** — is `2x` enough to make a forced switch feel like a real turn, or does it want `2x + 1`?
4. **Environment count** — is ~15 designs the right variety for a class ladder, or push to 20+?

## 11. Migration

- v1 stays in the repo, printable, unchanged, until v2 is built and playtested.
- On approval, this doc drives a branch that rebuilds the components in §9. Suggested order: **characters + sheet first** (cheap, low-risk, testable), then the environment/pet rebalance with data from a second playtest.
