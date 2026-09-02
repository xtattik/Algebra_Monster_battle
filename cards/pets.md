# Algebra Monster Battle — Pet Cards

Source of truth for the 12 starter pets. **Edit the card blocks below**, then run:

```bash
python tools/gen_pet_cards.py
```

to regenerate the print sheet at [`pets.html`](pets.html). The number model, balance
reasoning, and fast-marking table live in [`../docs/design/pets.md`](../docs/design/pets.md).

## Card block format

```
## <number>. <Name>

- HP: <integer>
- Archetype: <Glass cannon | Baseline | Tank>
- Magic: <attack name> | <a>x <+/- b>  [(min 1)]
- Strike: <attack name> | <a>x <+/- b>  [(min 1)]
- Agility: <attack name> | <a>x <+/- b>  [(min 1)]
- Flavour: <one line>
```

Rules the generator enforces:

- Coefficient `a` is 1, 2 or 3; constant `b` is −3…3; every attack has an `x` term.
- Write `(min 1)` when — and only when — `a + b < 1` (a roll of 1 would deal 0 or less).
- HP must sit in its archetype's band: Glass cannon 26–32, Baseline 44–54, Tank 76–84.

Affinity, the damage range, and the min badge are derived by the generator.

## At a glance

| # | Name | HP | Archetype | Magic | Strike | Agility |
|---|---|---|---|---|---|---|
| 1 | Emberwisp | 28 | Glass cannon | 3x + 2 | x − 1 (min 1) | x + 1 |
| 2 | Gorehoof | 30 | Glass cannon | x − 1 (min 1) | 3x + 2 | x + 1 |
| 3 | Dartclaw | 26 | Glass cannon | x | x + 1 | 3x + 1 |
| 4 | Sootmane | 50 | Baseline | x + 1 | 3x | 2x |
| 5 | Tidecaller | 48 | Baseline | 3x | x + 1 | 2x |
| 6 | Gustling | 46 | Baseline | 2x | x + 1 | 3x |
| 7 | Patchwork Golem | 54 | Baseline | 2x | 2x + 1 | 2x − 1 |
| 8 | Riftmoth | 44 | Baseline | x | x + 1 | 3x − 2 |
| 9 | Grave Hound | 46 | Baseline | x − 1 (min 1) | 3x | 2x − 1 |
| 10 | Boulderhide | 82 | Tank | x − 1 (min 1) | 2x + 1 | x |
| 11 | Old Cairn | 78 | Tank | 2x + 1 | x + 1 | x − 1 (min 1) |
| 12 | Moss Troll | 84 | Tank | 2x | 2x | x + 1 |

---

## 1. Emberwisp

- HP: 28
- Archetype: Glass cannon
- Magic: Cinderburst | 3x + 2
- Strike: Singe | x - 1 (min 1)
- Agility: Flit | x + 1
- Flavour: A trapped mote of wildfire that never learned to be careful.

## 2. Gorehoof

- HP: 30
- Archetype: Glass cannon
- Magic: Snort | x - 1 (min 1)
- Strike: Goring Charge | 3x + 2
- Agility: Trample | x + 1
- Flavour: Aims first. Thinks later, if at all.

## 3. Dartclaw

- HP: 26
- Archetype: Glass cannon
- Magic: Static Lick | x
- Strike: Tail Whip | x + 1
- Agility: Blink Slash | 3x + 1
- Flavour: You feel it a moment before you see it.

## 4. Sootmane

- HP: 50
- Archetype: Baseline
- Magic: Warding Roar | x + 1
- Strike: Pounce | 3x
- Agility: Prowl | 2x
- Flavour: Patient. Then, very suddenly, not.

## 5. Tidecaller

- HP: 48
- Archetype: Baseline
- Magic: Tidal Pulse | 3x
- Strike: Tail Slap | x + 1
- Agility: Slip Away | 2x
- Flavour: It calls the water, and the water always answers.

## 6. Gustling

- HP: 46
- Archetype: Baseline
- Magic: Whisper Gale | 2x
- Strike: Buffet | x + 1
- Agility: Cyclone Kick | 3x
- Flavour: Hard to catch, harder to hold onto.

## 7. Patchwork Golem

- HP: 54
- Archetype: Baseline
- Magic: Spark Seam | 2x
- Strike: Hammer Fist | 2x + 1
- Agility: Lumber | 2x - 1
- Flavour: Assembled from spare parts, none of them a matched set.

## 8. Riftmoth

- HP: 44
- Archetype: Baseline
- Magic: Dust of Ages | x
- Strike: Wing Slam | x + 1
- Agility: Phase Flurry | 3x - 2
- Flavour: Half of it is here. The other half is somewhere worse.

## 9. Grave Hound

- HP: 46
- Archetype: Baseline
- Magic: Baying Howl | x - 1 (min 1)
- Strike: Bone Crush | 3x
- Agility: Lunge | 2x - 1
- Flavour: It has your scent now, and it is not in a hurry.

## 10. Boulderhide

- HP: 82
- Archetype: Tank
- Magic: Dust Cloud | x - 1 (min 1)
- Strike: Shell Bash | 2x + 1
- Agility: Withdraw | x
- Flavour: In no rush to get anywhere, least of all away from you.

## 11. Old Cairn

- HP: 78
- Archetype: Tank
- Magic: Root Surge | 2x + 1
- Strike: Deadfall | x + 1
- Agility: Slow Creak | x - 1 (min 1)
- Flavour: Older than the hill it grew out of.

## 12. Moss Troll

- HP: 84
- Archetype: Tank
- Magic: Spore Cloud | 2x
- Strike: Heavy Club | 2x
- Agility: Shamble | x + 1
- Flavour: Thick, slow, and remarkably hard to convince to fall over.
