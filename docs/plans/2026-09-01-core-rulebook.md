# Core Rulebook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the phase-1 print-and-play documents for Algebra Monster Battle: a student rulebook, a teacher guide, a fast-marking answer key, and a battle worksheet.

**Architecture:** Plain Markdown documents authored from the approved design at `docs/design/core-rules.md`. No code except one optional helper script that generates the fast-marking lookup table. Every worked example and every table value is verified by hand-recomputation in a dedicated check step before each commit.

**Tech Stack:** Markdown. Optional: a short Python 3 script (`tools/gen_lookup.py`) to emit the lookup table — a teacher aid, not part of the game.

---

## File Structure

| File | Responsibility |
|---|---|
| `rulebook/student-rulebook.md` | Player-facing rules only — setup, trading, how one attack resolves, how a match and the ladder work. ~2 pages. |
| `rulebook/teacher-guide.md` | Running the activity: timing, class management, what to do with eliminated students, differentiation, common student errors, worked examples. |
| `rulebook/answer-key.md` | The fast-marking lookup table (`nx + c` → values at `x = 1..6`) plus fully worked answers for the sample scenarios used in the guide. |
| `worksheets/battle-worksheet.md` | Printable template: one row per attack for the student to show expression → collected like terms → roll → damage. |
| `tools/gen_lookup.py` | *(optional)* Generates the lookup table body so it cannot contain arithmetic slips. |
| `README.md` | Project overview, component list, build status, how to print/play. |

All four documents must agree with `docs/design/core-rules.md`. Where they disagree, the design doc wins and gets a correcting edit.

---

## Task 1: Student rulebook

**Files:**
- Create: `rulebook/student-rulebook.md`

- [ ] **Step 1: Draft the rulebook**

Write these sections, drawing all numbers and rules from `docs/design/core-rules.md`:

1. **What you're doing** — 2 sentences. You are a character with a monster pet; you battle other students; you do the algebra to find your damage.
2. **Your character** — you have three stats (Magic, Strength, Agility), each High / Average / Low.
   - Magic changes your **magic attacks**: High `+x`, Average `0`, Low `−x`.
   - Agility changes your **agility attacks**: High `+x`, Average `0`, Low `−x`.
   - Strength is defence — it changes attacks **against you**: High `−x` to the attacker, Average `0`, Low `+x` to the attacker.
3. **Your pets** — you start with 2 (drawn at random). Each pet has HP and three attacks (magic / strike / agility), each written as an expression like `3x + 1`. You field one pet per match.
   - **Strike (physical) attacks** are never changed by your stats or by the environment. They are only reduced by the enemy's Strength defence.
4. **Trading** — 5 minutes to swap pets by agreement. Aim to cover your weak stat.
5. **The environment** — one card is drawn per match. It names one stat it **boosts** (`+x` to matching attacks) and one it **hurts** (`−x` to matching attacks).
6. **Resolving one attack** — the five steps, with this worked example:
   - Your pet's magic attack: `3x + 1`
   - You have High Magic: `+ x`
   - Environment boosts Magic: `+ x`
   - Enemy has Average Strength: `+ 0`
   - Collect like terms: `3x + 1 + x + x = 5x + 1`
   - Roll the die — you get 4: `5 × 4 + 1 = 21`
   - Enemy pet loses 21 HP.
7. **Minimums** — a pet's base attack never deals less than 1 (the card tells you when this matters). After modifiers, damage can be reduced to 0 but never below.
8. **A match** — draw environment; both choose a pet; flip a coin / roll / RPS for first turn; take turns rolling and attacking; a pet at 0 HP loses.
9. **The ladder** — lose and you're out. Win and you roll the die: a 6 lets you keep the beaten pet. Your pet heals fully. Find another winner, draw a new environment, play again. Most wins (or last standing) takes the session.

Keep it to roughly two printed pages. Use short sentences and one clear worked example, not three.

- [ ] **Step 2: Verify the worked example**

Recompute `3x + 1 + x + x` by hand → `5x + 1`. At `x = 4` → `21`. Confirm the rulebook shows exactly these. Confirm every stat effect (`+x` / `0` / `−x`) matches the §5.2 table in the design doc.

- [ ] **Step 3: Commit**

```bash
git add rulebook/student-rulebook.md
git commit -m "Add student rulebook"
```

---

## Task 2: Teacher guide

**Files:**
- Create: `rulebook/teacher-guide.md`

- [ ] **Step 1: Draft the guide**

Sections:

1. **Purpose & curriculum** — NSW Stage 4 Algebraic Techniques: collecting like terms, substitution, negative constants, flooring at zero. One session or two.
2. **Prep** — print 1 character set (7 designs, multiple copies), the pet deck (enough for every student to draw 2), the environment deck, one worksheet per student. One D6 per pair. HP tracking method (counters or mini-whiteboards).
3. **Run sheet**
   - Deal characters (random or choice).
   - Each student draws 2 pets.
   - 5-minute trading phase.
   - Pair students; run the ladder.
   - Call time; count wins.
4. **Managing eliminated students** — they are not idle: they complete the worksheet for every match they played, then referee and check the maths for two more matches, or enter a second-chance bracket. Decide before you start which you'll use.
5. **The maths students must show** — point them at the worksheet. The gradable evidence is: expression assembled, like terms collected, substitution, final damage.
6. **Common errors to watch for**
   - Adding the modifier as a number instead of an `x` term (`+1` instead of `+x`).
   - Applying a stat buff to a strike attack (strike takes none).
   - Forgetting the enemy Strength term.
   - Letting damage go negative instead of flooring at 0.
   - Applying the environment to the wrong attack type.
7. **Worked examples** — reproduce examples A–D from design doc §5.5 in full, with every line of working shown.
8. **Differentiation** — support: ignore the environment term. Extension: two environment cards; D8 or D12; pets with negative constants; require a written inequality to justify each trade.
9. **Answer key** — see `rulebook/answer-key.md`.

- [ ] **Step 2: Verify the worked examples**

Recompute examples A–D independently:
- A: `3x + 1 + x + x = 5x + 1`; `x = 4` → `21`.
- B: `3x + 1 + x + x − x = 4x + 1`; `x = 4` → `17`.
- C: `2x + 2` unchanged; `x = 3` → `8`. Against High Strength: `2x + 2 − x = x + 2`; `x = 3` → `5`.
- D: `2x − 2 − x = x − 2`; `x = 2` → `0`; `x = 5` → `3`.

Every result must match the guide and the design doc. Fix whichever is wrong (design doc wins on rules, arithmetic wins on numbers).

- [ ] **Step 3: Commit**

```bash
git add rulebook/teacher-guide.md
git commit -m "Add teacher guide"
```

---

## Task 3: Fast-marking answer key

**Files:**
- Create: `rulebook/answer-key.md`
- Create *(optional)*: `tools/gen_lookup.py`

- [ ] **Step 1 (optional): Write the lookup generator**

```python
# tools/gen_lookup.py — emits the fast-marking table as Markdown.
# Usage: python tools/gen_lookup.py > /tmp/lookup.md  then paste the body in.
def main() -> None:
    ns = range(1, 7)          # coefficient 1..6
    cs = range(-3, 4)         # constant -3..3
    xs = range(1, 7)          # die faces
    header = "| expr | " + " | ".join(f"x={x}" for x in xs) + " |"
    sep = "|" + "---|" * (len(list(xs)) + 1)
    print(header)
    print(sep)
    for n in ns:
        for c in cs:
            label = f"{n}x" + ("" if c == 0 else (f" + {c}" if c > 0 else f" − {abs(c)}"))
            vals = [max(0, n * x + c) for x in xs]
            print(f"| {label} | " + " | ".join(str(v) for v in vals) + " |")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Build the answer key**

Contents:

1. **How to use** — after a student collects like terms to `nx + c`, find that row; read the value under their die roll; that is the damage (already floored at 0).
2. **Lookup table** — coefficient `1x`–`6x`, constant `−3` to `+3`, columns `x = 1..6`, every cell floored at 0. Generate with the script or build by hand.
3. **Sample-scenario answers** — the full resolution of examples A–D (from Task 2) and any extra scenarios the teacher guide references.

- [ ] **Step 3: Verify the table**

Spot-check at least 10 cells against direct calculation, including:
- `5x + 1` at `x = 4` → `21`
- `x − 2` at `x = 2` → `0` (floored, not `0` by chance — confirm `x = 1` also gives `0` not `−1`)
- `6x + 3` at `x = 6` → `39`
- `3x − 3` at `x = 1` → `0`

If the script was used, also read three rows and confirm they match hand calculation.

- [ ] **Step 4: Commit**

```bash
git add rulebook/answer-key.md tools/gen_lookup.py
git commit -m "Add fast-marking answer key and lookup generator"
```

---

## Task 4: Battle worksheet

**Files:**
- Create: `worksheets/battle-worksheet.md`

- [ ] **Step 1: Draft the worksheet**

A printable template. Header fields: student name, character, environment card, my pet, opponent's pet.

Then a repeating block (fit 6–8 per page):

```
Attack #___   Attack name & type: ____________________

Base attack expression:            ______________________
+ my Magic / Agility modifier:     ______________________
+ environment modifier:            ______________________
− enemy Strength modifier:         ______________________

Collect like terms  →              ______________________

My dice roll (x) =  ____

Substitute  →                      ______________________  =  ______  damage
(if negative, damage = 0)

Opponent HP:  ______  −  ______  =  ______
```

Add a footer line: "Show every line even if a modifier is 0 or not used — write `+0`."

- [ ] **Step 2: Verify against the resolution steps**

Walk example A through the worksheet block field by field. Every field in the template must have a home for each part of the §5.1 procedure. Adjust the template if any step has nowhere to go.

- [ ] **Step 3: Commit**

```bash
git add worksheets/battle-worksheet.md
git commit -m "Add battle worksheet template"
```

---

## Task 5: Consistency pass

**Files:**
- Modify: any of the above, and/or `docs/design/core-rules.md`

- [ ] **Step 1: Cross-check every document against the design doc**

Build a small checklist and tick each:
- Stat effects (`+x` / `0` / `−x`) identical in rulebook, teacher guide, worksheet, design doc §5.2.
- Strike attacks: "no character modifier, no environment modifier, enemy Strength still applies" — stated the same way everywhere.
- Starting zoo = 2 pets everywhere.
- Minimums: base ≥ 1, post-modifier ≥ 0 — stated the same everywhere.
- Loss = elimination; win → D6, a 6 captures — stated the same everywhere.
- Character names and stat lines match design doc §6.2 (if the rulebook lists them).

- [ ] **Step 2: Recompute all worked examples one final time**

Every worked example in every document, recomputed from scratch. List each: location, expression, result, PASS/FAIL. Fix any FAIL.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "Reconcile rulebook documents with core design"
```

---

## Task 6: Project README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write the README**

Sections: one-paragraph description; the learning goal (Stage 4 algebra); component list; build status (core rulebook done; character/environment/pet card sets to follow); "how to print and play" pointing at `rulebook/student-rulebook.md` and `rulebook/teacher-guide.md`; link to `docs/design/core-rules.md`.

- [ ] **Step 2: Commit and push**

```bash
git add README.md
git commit -m "Add project README"
git push
```

---

## Self-Review (completed by plan author)

**Spec coverage** — design doc sections mapped to tasks:
- §1–§2 goal/curriculum → README T6, teacher guide T2
- §3 components → teacher guide T2 prep list
- §4 the die → rulebook T1 §"resolving one attack"
- §5 damage model → rulebook T1, teacher guide T2, worksheet T4, answer key T3
- §5.5 worked examples → teacher guide T2, verified T2/T5
- §5.6 ceiling → not reproduced in player docs (internal balance note); acceptable, no task needed
- §6 characters → rulebook T1 (summary), full card content deferred to the character spec (design doc §14)
- §7–§8 pets/environments → out of scope for phase 1 by design; rulebook T1 explains how they're used
- §9 game flow → rulebook T1, teacher guide T2 run sheet
- §10 teacher materials → T2, T3, T4
- §11 differentiation → teacher guide T2
- §12 non-goals → README T6 (brief)
- §13 open questions → carried forward to the character/environment/pet specs, not this plan

**Placeholder scan:** `tools/gen_lookup.py` is complete runnable code. All worked examples show full working. Document sections list concrete content, not "write about X". The optional script is explicitly optional with a hand-built fallback.

**Type consistency:** the resolution procedure is described identically in T1 step 1 item 6, T3, and T4 (base + Magic/Agility + environment − enemy Strength → collect → substitute → floor). Modifier values `+x`/`0`/`−x` used consistently.
