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
(see the design doc §3).

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
- Playstyle: Field high-magic pets and lean on their magic attack; watch the environment, because a Magic-hurt terrain turns your main weapon into −x.
- Flavour: Power enough to bend the die — and just enough armour to regret it.

## 2. Illusionist

- Magic: High
- Strength: Low
- Agility: Average
- Playstyle: Same big magic as the Sorcerer but paper defence — every enemy attack gets +x against you, so end fights before they end you.
- Flavour: Every wound is real. So is every second you waste doubting it.

## 3. Paladin

- Magic: Average
- Strength: High
- Agility: Low
- Playstyle: A wall. Enemy attacks take −x, so field a durable pet and win the long game while your magic ticks away.
- Flavour: Stand still long enough and the storm has to go around you.

## 4. Barbarian

- Magic: Low
- Strength: High
- Agility: Average
- Playstyle: Bruiser. Your magic is −x, so field physical-strong pets and swing the strike attack the environment can't touch.
- Flavour: The maths is simple when the answer is always "hit it again".

## 5. Trickster

- Magic: Average
- Strength: Low
- Agility: High
- Playstyle: Fast and fragile. Agility attacks gain +x, but enemies get +x against you — pick agility pets and don't get caught in Blinding Light.
- Flavour: Win the roll, not the fight. There is a difference, and only one of them hurts.

## 6. Ranger

- Magic: Low
- Strength: Average
- Agility: High
- Playstyle: Agility specialist with a solid guard. Thrives where Agility is boosted — Deep Shadow is home turf.
- Flavour: Patience, the right ground, and one clean shot.

## 7. Bard

- Magic: Average
- Strength: Average
- Agility: Average
- Playstyle: No weakness and no spike. Every stat is 0, so you adapt to any terrain and any pet while sharper builds get countered.
- Flavour: Never the strongest in the room. Often the last one standing.
