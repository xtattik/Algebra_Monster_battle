# Algebra Monster Battle — Pet Cards (v2)

Source of truth for the 22 starter pets. **Edit the card blocks below**, then run:

```bash
python tools/gen_pet_cards.py
```

to regenerate the print sheet at [`pets.html`](pets.html). The number model lives in
[`../docs/design/pets.md`](../docs/design/pets.md); the rules model in
[`../docs/design/core-rules-v2.md`](../docs/design/core-rules-v2.md) §6.

## Card block format

```
## <number>. <Name>

- HP: <integer>
- Archetype: <Glass cannon | Baseline | Tank>
- Magic: <attack name> | <a>x <+/- b>  [(min 1)]
- Strength: <attack name> | <a>x <+/- b>  [(min 1)]
- Agility: <attack name> | <a>x <+/- b>  [(min 1)]
- Flavour: <one line>
```

Rules the generator enforces (**v2**):

- Attack type is **strength** (v1 "strike"), so it matches the Strength stat.
- Coefficient `a` is 1–4; constant `b` is −3…3; every attack has an `x` term.
- Write `(min 1)` when — and only when — `a + b < 1`.
- HP band: **Glass cannon 36–44 · Baseline 68–82 · Tank 95–110.**

Affinity, damage range and the min badge are derived by the generator.

## v2 number model

| Archetype | HP | Affinity attack | Secondary | Third |
|---|---|---|---|---|
| Glass cannon | ~40 | `4x` / `4x + 1` | `2x` | `x − 1 (min 1)` / `x` |
| Baseline | ~75 | `3x + 1` / `3x + 2` | `2x` / `2x + 1` | `x + 1` |
| Tank | ~100 | `3x` / `2x + 2` | `2x` | `x` / `x − 1 (min 1)` |

The **secondary `2x`** is the change from v1 — a pet whose affinity is cancelled by
the terrain still has a real turn.

## At a glance

| # | Name | HP | Archetype | Magic | Strength | Agility | Affinity |
|---|---|---|---|---|---|---|---|
| 1 | Emberwisp | 40 | Glass cannon | 4x + 1 | x − 1 (min 1) | 2x | Magic |
| 2 | Gorehoof | 42 | Glass cannon | x − 1 (min 1) | 4x + 1 | 2x | Strength |
| 3 | Dartclaw | 38 | Glass cannon | x | 2x | 4x + 1 | Agility |
| 4 | Sootmane | 76 | Baseline | x + 1 | 3x + 1 | 2x | Strength |
| 5 | Tidecaller | 74 | Baseline | 3x + 1 | x + 1 | 2x | Magic |
| 6 | Gustling | 72 | Baseline | 2x | x + 1 | 3x + 1 | Agility |
| 7 | Patchwork Golem | 80 | Baseline | 2x | 2x + 1 | 2x | Balanced |
| 8 | Riftmoth | 70 | Baseline | x | 2x | 4x − 2 | Agility |
| 9 | Grave Hound | 74 | Baseline | x − 1 (min 1) | 3x + 1 | 2x − 1 | Strength |
| 10 | Boulderhide | 100 | Tank | 2x | 3x | x | Strength |
| 11 | Old Cairn | 98 | Tank | 3x | 2x | x − 1 (min 1) | Magic |
| 12 | Moss Troll | 104 | Tank | 2x + 1 | 2x + 1 | 2x | Balanced |
| 13 | Sparkhound | 39 | Glass cannon | 4x | x − 1 (min 1) | 2x | Magic |
| 14 | Bristlecharge | 41 | Glass cannon | x − 1 (min 1) | 4x + 1 | 2x | Strength |
| 15 | Quickfin | 38 | Glass cannon | 2x | x | 4x + 1 | Agility |
| 16 | Cindercat | 75 | Baseline | 3x + 2 | x + 1 | 2x | Magic |
| 17 | Ironhide Ram | 78 | Baseline | x + 1 | 3x + 2 | 2x | Strength |
| 18 | Zephyr Kite | 72 | Baseline | 2x | x + 1 | 3x + 2 | Agility |
| 19 | Clockwork Beetle | 80 | Baseline | 2x | 2x + 1 | 2x | Balanced |
| 20 | Barrow Wight | 96 | Tank | 2x | 3x | x | Strength |
| 21 | Deepstone Toad | 98 | Tank | 3x | 2x | x − 1 (min 1) | Magic |
| 22 | Rust Golem | 102 | Tank | x − 1 (min 1) | 3x | 2x | Strength |

---

## 1. Emberwisp

- HP: 40
- Archetype: Glass cannon
- Magic: Cinderburst | 4x + 1
- Strength: Singe | x - 1 (min 1)
- Agility: Flit | 2x
- Flavour: A trapped mote of wildfire that never learned to be careful.

## 2. Gorehoof

- HP: 42
- Archetype: Glass cannon
- Magic: Snort | x - 1 (min 1)
- Strength: Goring Charge | 4x + 1
- Agility: Trample | 2x
- Flavour: Aims first. Thinks later, if at all.

## 3. Dartclaw

- HP: 38
- Archetype: Glass cannon
- Magic: Static Lick | x
- Strength: Tail Whip | 2x
- Agility: Blink Slash | 4x + 1
- Flavour: You feel it a moment before you see it.

## 4. Sootmane

- HP: 76
- Archetype: Baseline
- Magic: Warding Roar | x + 1
- Strength: Pounce | 3x + 1
- Agility: Prowl | 2x
- Flavour: Patient. Then, very suddenly, not.

## 5. Tidecaller

- HP: 74
- Archetype: Baseline
- Magic: Tidal Pulse | 3x + 1
- Strength: Tail Slap | x + 1
- Agility: Slip Away | 2x
- Flavour: It calls the water, and the water always answers.

## 6. Gustling

- HP: 72
- Archetype: Baseline
- Magic: Whisper Gale | 2x
- Strength: Buffet | x + 1
- Agility: Cyclone Kick | 3x + 1
- Flavour: Hard to catch, harder to hold onto.

## 7. Patchwork Golem

- HP: 80
- Archetype: Baseline
- Magic: Spark Seam | 2x
- Strength: Hammer Fist | 2x + 1
- Agility: Lumber | 2x
- Flavour: Assembled from spare parts, none of them a matched set.

## 8. Riftmoth

- HP: 70
- Archetype: Baseline
- Magic: Dust of Ages | x
- Strength: Wing Slam | 2x
- Agility: Phase Flurry | 4x - 2
- Flavour: Half of it is here. The other half is somewhere worse.

## 9. Grave Hound

- HP: 74
- Archetype: Baseline
- Magic: Baying Howl | x - 1 (min 1)
- Strength: Bone Crush | 3x + 1
- Agility: Lunge | 2x - 1
- Flavour: It has your scent now, and it is not in a hurry.

## 10. Boulderhide

- HP: 100
- Archetype: Tank
- Magic: Dust Cloud | 2x
- Strength: Shell Bash | 3x
- Agility: Withdraw | x
- Flavour: In no rush to get anywhere, least of all away from you.

## 11. Old Cairn

- HP: 98
- Archetype: Tank
- Magic: Root Surge | 3x
- Strength: Deadfall | 2x
- Agility: Slow Creak | x - 1 (min 1)
- Flavour: Older than the hill it grew out of.

## 12. Moss Troll

- HP: 104
- Archetype: Tank
- Magic: Spore Cloud | 2x + 1
- Strength: Heavy Club | 2x + 1
- Agility: Shamble | 2x
- Flavour: Thick, slow, and remarkably hard to convince to fall over.

## 13. Sparkhound

- HP: 39
- Archetype: Glass cannon
- Magic: Arc Bite | 4x
- Strength: Nip | x - 1 (min 1)
- Agility: Dash | 2x
- Flavour: Static crackles off it when it gets excited, which is always.

## 14. Bristlecharge

- HP: 41
- Archetype: Glass cannon
- Magic: Huff | x - 1 (min 1)
- Strength: Spine Rush | 4x + 1
- Agility: Sidestep | 2x
- Flavour: The warning snort is the only warning you get.

## 15. Quickfin

- HP: 38
- Archetype: Glass cannon
- Magic: Bubble | 2x
- Strength: Fin Slap | x
- Agility: Riptide Dart | 4x + 1
- Flavour: Gone before the ripples have finished spreading.

## 16. Cindercat

- HP: 75
- Archetype: Baseline
- Magic: Ember Purr | 3x + 2
- Strength: Swipe | x + 1
- Agility: Slink | 2x
- Flavour: Warm to the touch. Warmer if it has decided it doesn't like you.

## 17. Ironhide Ram

- HP: 78
- Archetype: Baseline
- Magic: Bleat | x + 1
- Strength: Headbutt | 3x + 2
- Agility: Scramble | 2x
- Flavour: Built like a doorstop and twice as stubborn.

## 18. Zephyr Kite

- HP: 72
- Archetype: Baseline
- Magic: Updraft | 2x
- Strength: Talon Rake | x + 1
- Agility: Divebomb | 3x + 2
- Flavour: Rides the wind so you never have to guess where it is — until you do.

## 19. Clockwork Beetle

- HP: 80
- Archetype: Baseline
- Magic: Spark Coil | 2x
- Strength: Pincer | 2x + 1
- Agility: Scuttle | 2x
- Flavour: Wind it up, set it down, and take a step back.

## 20. Barrow Wight

- HP: 96
- Archetype: Tank
- Magic: Chill Touch | 2x
- Strength: Grave Reach | 3x
- Agility: Drift | x
- Flavour: It remembers being alive, and it resents you for still managing it.

## 21. Deepstone Toad

- HP: 98
- Archetype: Tank
- Magic: Mud Bolt | 3x
- Strength: Bellyflop | 2x
- Agility: Hunker | x - 1 (min 1)
- Flavour: Has not moved in a decade and does not plan to start now.

## 22. Rust Golem

- HP: 102
- Archetype: Tank
- Magic: Oxide Cloud | x - 1 (min 1)
- Strength: Iron Fist | 3x
- Agility: Grind Forward | 2x
- Flavour: Slow, heavy, and only ever going one direction: yours.
