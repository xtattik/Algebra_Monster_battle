# Algebra Monster Battle — Character Cards

Source of truth for the 7 character cards. **Edit the card blocks below**, then run:

```bash
python tools/gen_cards.py
```

to regenerate the print sheet at [`characters.html`](characters.html). Design rationale, the
stat-effect wording table, and the print spec live in
[`../docs/design/characters.md`](../docs/design/characters.md).

## Card block format

The generator parses each card block exactly as:

```
## <number>. <Name>

- Magic: <High | Average | Low>
- Strength: <High | Average | Low>
- Agility: <High | Average | Low>
- Playstyle: <one line>
- Flavour: <one line>
```

The plain-words effect and the `±x` term for each stat tier are **not** written here —
the generator derives them from the tier so the wording is identical on every card
(see the design doc §3). **v2:** all three stats are offensive — each buffs its own
attack type (`+x` High / `0` Average / `−x` Low). There is no defence stat.

## At a glance

| # | Name | Magic | Strength | Agility |
|---|---|---|---|---|
| 1 | Sorcerer | High | Average | Low |
| 2 | Illusionist | High | Low | Average |
| 3 | Paladin | Average | High | Low |
| 4 | Barbarian | Low | High | Average |
| 5 | Trickster | Average | Low | High |
| 6 | Ranger | Low | Average | High |
| 7 | Bard | Average | Average | Average |

---

## 1. Sorcerer

- Magic: High
- Strength: Average
- Agility: Low
- Playstyle: Lean on magic-attack pets — High Magic makes every cast +x. A Cancel: Magic terrain shuts the whole plan down, so keep a non-magic pet in reserve.
- Flavour: Power enough to bend the die. Ask them to swing a sword and watch the confidence drain.

## 2. Illusionist

- Magic: High
- Strength: Low
- Agility: Average
- Playstyle: Huge magic like the Sorcerer, but Low Strength makes your strength attacks −x — never plan to win a slugfest. End it with spells.
- Flavour: Every wound is real. So is every second you waste doubting it.

## 3. Paladin

- Magic: Average
- Strength: High
- Agility: Low
- Playstyle: Heavy hitter. High Strength makes strength attacks +x — field a big-strike pet and pound it out. Slow, but it lands.
- Flavour: Not fast. Not clever. But when it connects, things fall down.

## 4. Barbarian

- Magic: Low
- Strength: High
- Agility: Average
- Playstyle: Bruiser. Strength attacks +x, but Low Magic makes any cast −x — a caster pet is wasted on you.
- Flavour: The maths is simple when the answer is always "hit it again".

## 5. Trickster

- Magic: Average
- Strength: Low
- Agility: High
- Playstyle: Fast skirmisher. High Agility gives agility attacks +x; Low Strength means you fold in a straight fight — stay on agility.
- Flavour: Win the roll, not the fight. There is a difference, and only one of them hurts.

## 6. Ranger

- Magic: Low
- Strength: Average
- Agility: High
- Playstyle: Agility specialist. Your +x is on agility attacks; a magic pet does nothing for you. Fear a Cancel: Agility.
- Flavour: Patience, the right ground, and one clean shot.

## 7. Bard

- Magic: Average
- Strength: Average
- Agility: Average
- Playstyle: Every stat is 0 — no spike, but no weakness. Never hard-countered, never cancelled out. The reliable pick.
- Flavour: Never the strongest in the room. Often the last one standing.
