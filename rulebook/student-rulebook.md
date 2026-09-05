# Algebra Monster Battle — Student Rulebook

## 1. What you're doing

You are a fantasy character with a monster pet, and you battle other students one on one. On every attack you build a linear expression, collect like terms, then roll a die and substitute it for `x` to find your damage.

## 2. Your character

Your character card has three stats: **Magic**, **Strength**, and **Agility**. Each stat is set at **High**, **Average**, or **Low**. Every character has one High, one Average, and one Low — except the all-rounder, who is Average in all three.

- **Magic** changes your **magic attacks**.
- **Agility** changes your **agility attacks**.
- **Strength** is your **defence**. It changes attacks made **against you**, helping or hurting the attacker's roll.

| Stat | High | Average | Low |
|---|---|---|---|
| Magic (your magic attacks) | `+x` | `0` | `−x` |
| Agility (your agility attacks) | `+x` | `0` | `−x` |
| Strength (enemy attacks against you) | `−x` to the attacker | `0` | `+x` to the attacker |

Every modifier is a term with `x` in it, never a plain number. That is why you always have like terms to collect.

## 3. Your pets

You start with **2 pets**, drawn at random. This is your zoo. Each pet card shows the pet's **HP** and **three attacks**: a magic attack, a strike attack, and an agility attack. Each attack is written as an expression like `3x + 1`. In a match you field **one pet**.

**Strike (physical) attacks are special.** They are never changed by your stats or by the environment. The only thing that reduces a strike attack is the enemy's Strength defence. Strike is your reliable option when the environment is against you.

## 4. Trading

You get about **5 minutes** to trade pets with other students. Trades happen by mutual agreement — both players must say yes. Aim to pick up a pet that covers your character's weak stat, or one that suits an environment you expect to face.

## 5. The environment

One environment card is drawn per match and applies for the whole match. A card can do up to three things:

- **Boosts** an attack type — every magic (or agility) attack gains `+x`, for both players.
- **Hinders** an attack type — every magic (or agility) attack takes `−x`, for both players.
- **Tests Strength** — a harsh place (ice, heat). Check **your character's Strength** tier: High `−x`, Average `0`, Low `+x`. That term is added to attacks **against you** — and unlike Boosts/Hinders, it *does* affect **strike** attacks aimed at you.

Boosts and Hinders never touch strike attacks. Some cards (like **Open Field**) do none of the three.

## 6. Resolving one attack

On your turn, roll the die once. That roll is your `x` for this attack. Then work through these steps:

1. Write your pet's base attack expression.
2. Add the modifier terms that apply, each `+x`, `−x` or `0`:
   - your character modifier (Magic on magic attacks, Agility on agility attacks),
   - the environment's **Boosts** / **Hinders** term, if it matches this attack's type,
   - the enemy's **Strength** modifier,
   - the environment's **Tests Strength** term, if the card has one (based on the *defender's* Strength).
   Strike attacks skip the character modifier and the Boosts/Hinders term — but still take the enemy Strength modifier *and* any Tests Strength term.
3. Collect like terms into a single `nx + c`.
4. Substitute your die roll for `x` and work out the number.
5. Apply the minimum (see section 7), then subtract the result from the enemy pet's HP.

**Worked example 1 — a magic attack.** Your pet's magic attack is `3x + 1`. You have High Magic, so you add `+ x`. The environment **Boosts Magic**, so you add another `+ x`. The enemy has Average Strength, so you add `+ 0`.

`3x + 1 + x + x = 5x + 1`

You roll a 4: `5 × 4 + 1 = 21`. The enemy pet loses **21 HP**.

**Worked example 2 — a strike attack in Frozen Wastes.** Your pet's strike attack is `2x + 2`. Strike takes no character or Boosts/Hinders term. The enemy has **Low Strength** (`+ x`), and **Frozen Wastes Tests Strength** — the enemy is Low Strength, so that is another `+ x`.

`2x + 2 + x + x = 4x + 2`

You roll a 3: `4 × 3 + 2 = 14`. The enemy pet loses **14 HP** — the cold left them exposed even to a plain hit.

## 7. Minimums

A pet's **base attack** never deals less than **1**. When this could happen on a low roll, the card prints its own floor, such as `x − 1 (min 1)`.

**After modifiers**, damage can be reduced all the way to **0**, but never below 0. A well-countered attack can be fully blocked on a low roll, but a high roll should always connect for something.

## 8. A match

1. Draw one environment card.
2. Both players secretly choose which pet to field, then reveal.
3. Decide who goes first: coin flip, dice roll, or rock-paper-scissors.
4. Take turns. On your turn, roll and make one attack using the steps in section 6.
5. When a pet reaches **0 HP**, it loses and that player is out of the ladder.

## 9. The ladder

If you lose, you are out — but stay involved by completing your battle sheet, refereeing a match, or joining a second-chance bracket.

If you win:

- Roll the die. On a **6**, you capture the beaten pet and add it to your zoo. Otherwise it is discarded.
- Your pet **heals to full HP**.
- Find another winner, draw a **new environment**, and play again.

The session ends when one player is left standing, or when time is called and the player with the **most wins** takes it.

## 10. Challenge Mode (optional)

Some pets come in a **Challenge** version (`cards/pets-challenge.html`) —
same pet, same HP, same art, but harder attacks. Everything above still
applies. Two new things you'll see on a Challenge card:

**A bracket you have to expand first**, e.g. `3(x − 1)`. Multiply it out
before you do anything else: `3(x − 1) = 3x − 3`. Then carry on exactly as
in section 6 — add your modifiers, collect like terms, substitute your roll.

**A negative coefficient**, e.g. `−3x + 10`. This attack gets *weaker* as
your roll gets *better* — a 1 might deal 7, a 6 might floor at the attack's
minimum of 1. Watch what a modifier does to it: your own `+x` buff doesn't
make a negative-coefficient attack hit harder — it partially cancels the
negative coefficient instead. Work it out term by term and you won't be
caught out.

**Worked example (bracket).** Base attack `3(x − 1)`, you have High Magic
(`+x`), the environment boosts Magic (`+x`), enemy is Average Strength
(`+0`).

- Expand first: `3(x − 1) = 3x − 3`
- Add modifiers: `3x − 3 + x + x + 0`
- Collect like terms: `5x − 3`
- Roll a 4: `5 × 4 − 3 = 17`

**Worked example (negative coefficient).** Base attack `−3x + 10`, you have
High Magic (`+x`), the environment boosts Magic (`+x`), enemy is Average
Strength (`+0`).

- Add modifiers straight away (no expansion needed): `−3x + 10 + x + x + 0`
- Collect like terms: `−x + 10`
- Roll a 4: `−4 + 10 = 6`
- Roll a 1 instead: `−1 + 10 = 9` — a *worse* roll deals *more* damage here.
