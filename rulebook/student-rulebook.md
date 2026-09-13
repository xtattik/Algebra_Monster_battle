# Algebra Monster Battle — Student Rulebook  *(v2)*

## 1. What you're doing

You are a fantasy **character** with a monster **pet**, and you battle other students one on one. Every attack, you build a linear expression, collect like terms, then roll a die and substitute it for `x` to find your damage. You cannot take a turn without doing the maths.

## 2. Your character

Your character card has three stats: **Magic**, **Strength**, **Agility** — each set at **High**, **Average**, or **Low**. Every character has one of each, except the all-rounder (Average in all three).

**Each stat buffs its own attack type:**

| Your tier | Effect on that attack type |
|---|---|
| **High** | `+x` |
| **Average** | `0` |
| **Low** | `−x` |

- **Magic** → your **magic** attacks
- **Strength** → your **strength** attacks
- **Agility** → your **agility** attacks

There is no defence — **your HP is your defence.** A tougher pet outlasts; nothing on your card reduces the damage coming at you.

Every buff is a term with `x` in it (`+x`, `−x`, or `0`) — never a plain number. That is why you always have like terms to collect.

## 3. Your pets

You start with **2 pets**, drawn at random — your zoo. Each pet card shows its **HP** and **three attacks** — a magic, a strength, and an agility attack — each written as an expression like `4x + 1`. A pet is **best at one attack type** (its biggest coefficient) and has a smaller `2x` fallback for the other two. In a match you field **one pet**.

## 4. Trading

You get about **5 minutes** to trade pets by mutual agreement (both players say yes). Aim for:

- **a pet whose best attack matches your High stat** — that's your strongest line, and
- **a second pet of a different type** — so if the terrain shuts your main type down, you're not stuck.

## 5. The environment

One environment card is drawn per match and applies for the whole match, to **both players**. A card can do up to two of:

- **Boost** an attack type — those attacks gain `+2x` (or `+x`).
- **Weaken** an attack type — those attacks take `−2x` (or `−x`).
- **Cancel** an attack type — those attacks **cannot be used at all** this match.

Every card shows all three attack types and what happens to each. **Open Field** does nothing.

The environment's term is bigger than your character's `±x`, so terrain matters — but a Weaken only *reduces* your best attack, it doesn't remove it. A **Cancel** does remove it: that's when you field your other pet, or switch to a different attack type.

## 6. Resolving one attack — five steps

**Choose your attack and build the whole expression *before* you roll.** (Do it during your opponent's turn if you can.)

1. Pick an attack type — magic, strength, or agility (not one the terrain Cancels, and not the **same type as your last two attacks in a row** — see section 8) — and write its equation, e.g. `4x`.
2. Add **your matching stat** buff (`+x` / `0` / `−x`).
3. Add the **environment** term for that attack type (`+2x` / `+x` / `0` / `−x` / `−2x`).
4. **Collect like terms** into a single `nx + c`.
5. **Now roll the die.** Substitute your roll for `x`, work out the number, apply the minimum (section 7), and subtract it from the enemy pet's HP.

**Worked example — a boosted magic attack.** Your pet's magic attack is `3x + 2`. You have **High Magic** (`+x`). The environment **Boosts Magic** (`+2x`).

`3x + 2 + x + 2x = 6x + 2`

Roll a 5: `6 × 5 + 2 = 32`. The enemy pet loses **32 HP**.

**Worked example — a weakened attack (still usable).** Same pet, same magic attack `3x + 2`, but this environment **Weakens Magic** (`−2x`). You still have High Magic (`+x`).

`3x + 2 + x − 2x = 2x + 2`

Roll a 5: `2 × 5 + 2 = 12`. Reduced — but a non-caster here would land only `3x + 2 − x − 2x = 2`, so your `+x` still bought you an edge.

**Worked example — a cancelled attack.** This environment **Cancels Magic**. Your magic attack is off the table, so you use the pet's **strength** attack, `2x`. You have **Average Strength** (`0`).

`2x + 0 = 2x`

Roll a 5: `2 × 5 = 10`. Worse than the boosted `6x + 2` — but a real turn.

## 7. Minimums

- A pet's **base attack** never deals less than **1**. Where a low roll could take it below 1, the card prints its own floor, e.g. `x − 1 (min 1)`.
- **After buffs and terrain**, damage can be reduced all the way to **0**, but never below 0.

## 8. A match

1. **Draw one environment card** — read what it does to each attack type.
2. **Both players choose a pet** and reveal at the same time.
3. Decide who goes first: coin flip, dice roll, or rock-paper-scissors.
4. Take turns. On your turn: choose and build your attack (section 6), **then** roll and substitute.
5. **No attack type three times running.** If your last two attacks were both, say, magic, your next one must be strength or agility. You don't have to use all three types — just not the same one a third time in a row.
6. When a pet reaches **0 HP**, it loses — that duel is over.

## 9. The ladder

- **Lose a duel** → you drop to the **second-chance bracket** and keep playing. (Your teacher may instead run straight knock-out.)
- **Win a duel:**
  - Roll the die. On a **6**, capture the beaten pet into your zoo. Otherwise it's discarded.
  - Your pet **heals to full HP**.
  - Find another winner, draw a **new environment**, play again.
- The session ends at **last player standing**, or **most wins** when time is called.

## 10. Challenge Mode

Some pets come in a harder **Challenge** version — same name, HP, and art as
your normal zoo, so it's a straight swap for whichever pet it replaces.
Everything else about the game is unchanged. The only difference: all three
attacks are written in a form you have to do one extra step on before you can
use section 6.

- **Bracket**, e.g. `3(x + 2)`. Expand it first: `3(x + 2) = 3x + 6`. Then
  build your expression exactly as normal.
- **Negative coefficient**, e.g. `−2x + 8`. No expanding needed, but the
  damage now *shrinks* as your roll goes up — this attack wants a **low**
  roll. A `+x` buff or a Boost doesn't make it hit harder; it **softens** the
  negative, pulling the number toward a flat constant instead.

**Worked example — bracket.** Pet attack `4(x + 1)`. Expand: `4x + 4`. Add
High Magic `+x` and a Boost `+2x`: `4x + 4 + x + 2x = 7x + 4`. Roll a 5:
`7 × 5 + 4 = 39`.

**Worked example — negative coefficient.** Pet attack `−4x + 13`. Add High
Magic `+x` and a Boost `+2x`: `−4x + 13 + x + 2x = −x + 13`. Roll a 1 (your
*best* roll for this attack): `−1 + 13 = 12`. Roll a 6 (your worst): `−6 + 13
= 7` — still a real hit, just smaller. Notice the `+x` and `+2x` **shrank**
the `−4x` down to `−x`, rather than making it more negative.

Ask your teacher which cards (if any) are in play before you draw.
