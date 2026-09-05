# Algebra Monster Battle — Challenge Pet Cards

A harder printing of the same 22 pets from `cards/pets.md` — same names, HP,
archetype, flavour, and art. Only the three attack equations change. Full
design: [`../docs/design/pets-challenge.md`](../docs/design/pets-challenge.md).

**Edit the card blocks below**, then run:

```bash
python tools/gen_pet_cards.py --variant challenge
```

to regenerate the print sheet at [`pets-challenge.html`](pets-challenge.html).

## Card block format

Same as `cards/pets.md`, except an attack's equation may be:

- **Bracket**, printed unexpanded: `a(x + b)` or `a(x - b)`, `a` in `{2, 3}`, `b` in `{1, 2}`.
- **Negative coefficient**: `-ax + b`, `a` in `{1, 2, 3}`.
- Plain `ax + b` also parses, but every pet here uses the two harder forms.

```
## <number>. <Name>

- HP: <integer>
- Archetype: <Glass cannon | Baseline | Tank>
- Magic: <attack name> | <equation>  [(min 1)]
- Strike: <attack name> | <equation>  [(min 1)]
- Agility: <attack name> | <equation>  [(min 1)]
- Flavour: <one line>
```

Rules the generator enforces:

- Every pet's three attacks must include **at least one bracket and at least one negative-coefficient** attack.
- `(min 1)` is printed **exactly when** the attack's value at its worst roll — `x = 1` for a positive coefficient, `x = 6` for a negative one — would be 0 or less.
- HP must sit in its archetype's band (same bands as `cards/pets.md`).

Affinity is the attack type with the largest **magnitude** of coefficient (`|a|`) — a negative coefficient can be the "biggest" attack too.

## At a glance

| # | Name | HP | Archetype | Magic | Strike | Agility |
|---|---|---|---|---|---|---|
| 1 | Emberwisp | 28 | Glass cannon | 3(x + 1) | -x + 5 (min 1) | 2(x - 1) (min 1) |
| 2 | Gorehoof | 30 | Glass cannon | 2(x - 1) (min 1) | -3x + 10 (min 1) | -x + 5 (min 1) |
| 3 | Dartclaw | 26 | Glass cannon | -2x + 8 (min 1) | 2(x + 1) | 3(x + 1) |
| 4 | Sootmane | 50 | Baseline | -x + 5 (min 1) | 3(x + 1) | 2(x - 1) (min 1) |
| 5 | Tidecaller | 48 | Baseline | 3(x - 1) (min 1) | 2(x - 1) (min 1) | -2x + 8 (min 1) |
| 6 | Gustling | 46 | Baseline | -x + 5 (min 1) | 2(x + 1) | 3(x - 1) (min 1) |
| 7 | Patchwork Golem | 54 | Baseline | 3(x + 1) | -2x + 8 (min 1) | 2(x - 1) (min 1) |
| 8 | Riftmoth | 44 | Baseline | 2(x - 1) (min 1) | -2x + 8 (min 1) | 3(x - 1) (min 1) |
| 9 | Grave Hound | 46 | Baseline | -x + 5 (min 1) | 3(x - 1) (min 1) | 2(x + 1) |
| 10 | Boulderhide | 82 | Tank | -x + 5 (min 1) | -2x + 8 (min 1) | 2(x - 1) (min 1) |
| 11 | Old Cairn | 78 | Tank | 2(x - 1) (min 1) | -x + 5 (min 1) | -2x + 8 (min 1) |
| 12 | Moss Troll | 84 | Tank | 2(x - 1) (min 1) | -2x + 8 (min 1) | -x + 5 (min 1) |
| 13 | Sparkhound | 29 | Glass cannon | -3x + 10 (min 1) | 2(x - 1) (min 1) | -x + 5 (min 1) |
| 14 | Bristlecharge | 31 | Glass cannon | -x + 5 (min 1) | 3(x + 1) | 2(x + 1) |
| 15 | Quickfin | 27 | Glass cannon | 2(x + 1) | -2x + 8 (min 1) | -3x + 10 (min 1) |
| 16 | Cindercat | 49 | Baseline | 3(x + 1) | -2x + 8 (min 1) | 2(x - 1) (min 1) |
| 17 | Ironhide Ram | 52 | Baseline | -2x + 8 (min 1) | 3(x - 1) (min 1) | 2(x - 1) (min 1) |
| 18 | Zephyr Kite | 45 | Baseline | -x + 5 (min 1) | 2(x + 1) | 3(x - 1) (min 1) |
| 19 | Clockwork Beetle | 53 | Baseline | -2x + 8 (min 1) | 2(x - 1) (min 1) | 3(x - 1) (min 1) |
| 20 | Barrow Wight | 79 | Tank | -x + 5 (min 1) | 2(x - 1) (min 1) | -2x + 8 (min 1) |
| 21 | Deepstone Toad | 80 | Tank | -2x + 8 (min 1) | 2(x - 1) (min 1) | -x + 5 (min 1) |
| 22 | Rust Golem | 83 | Tank | 2(x - 1) (min 1) | -2x + 8 (min 1) | -x + 5 (min 1) |

---

## 1. Emberwisp

- HP: 28
- Archetype: Glass cannon
- Magic: Cinderburst | 3(x + 1)
- Strike: Singe | -x + 5 (min 1)
- Agility: Flit | 2(x - 1) (min 1)
- Flavour: A trapped mote of wildfire that never learned to be careful.

## 2. Gorehoof

- HP: 30
- Archetype: Glass cannon
- Magic: Snort | 2(x - 1) (min 1)
- Strike: Goring Charge | -3x + 10 (min 1)
- Agility: Trample | -x + 5 (min 1)
- Flavour: Aims first. Thinks later, if at all.

## 3. Dartclaw

- HP: 26
- Archetype: Glass cannon
- Magic: Static Lick | -2x + 8 (min 1)
- Strike: Tail Whip | 2(x + 1)
- Agility: Blink Slash | 3(x + 1)
- Flavour: You feel it a moment before you see it.

## 4. Sootmane

- HP: 50
- Archetype: Baseline
- Magic: Warding Roar | -x + 5 (min 1)
- Strike: Pounce | 3(x + 1)
- Agility: Prowl | 2(x - 1) (min 1)
- Flavour: Patient. Then, very suddenly, not.

## 5. Tidecaller

- HP: 48
- Archetype: Baseline
- Magic: Tidal Pulse | 3(x - 1) (min 1)
- Strike: Tail Slap | 2(x - 1) (min 1)
- Agility: Slip Away | -2x + 8 (min 1)
- Flavour: It calls the water, and the water always answers.

## 6. Gustling

- HP: 46
- Archetype: Baseline
- Magic: Whisper Gale | -x + 5 (min 1)
- Strike: Buffet | 2(x + 1)
- Agility: Cyclone Kick | 3(x - 1) (min 1)
- Flavour: Hard to catch, harder to hold onto.

## 7. Patchwork Golem

- HP: 54
- Archetype: Baseline
- Magic: Spark Seam | 3(x + 1)
- Strike: Hammer Fist | -2x + 8 (min 1)
- Agility: Lumber | 2(x - 1) (min 1)
- Flavour: Assembled from spare parts, none of them a matched set.

## 8. Riftmoth

- HP: 44
- Archetype: Baseline
- Magic: Dust of Ages | 2(x - 1) (min 1)
- Strike: Wing Slam | -2x + 8 (min 1)
- Agility: Phase Flurry | 3(x - 1) (min 1)
- Flavour: Half of it is here. The other half is somewhere worse.

## 9. Grave Hound

- HP: 46
- Archetype: Baseline
- Magic: Baying Howl | -x + 5 (min 1)
- Strike: Bone Crush | 3(x - 1) (min 1)
- Agility: Lunge | 2(x + 1)
- Flavour: It has your scent now, and it is not in a hurry.

## 10. Boulderhide

- HP: 82
- Archetype: Tank
- Magic: Dust Cloud | -x + 5 (min 1)
- Strike: Shell Bash | -2x + 8 (min 1)
- Agility: Withdraw | 2(x - 1) (min 1)
- Flavour: In no rush to get anywhere, least of all away from you.

## 11. Old Cairn

- HP: 78
- Archetype: Tank
- Magic: Root Surge | 2(x - 1) (min 1)
- Strike: Deadfall | -x + 5 (min 1)
- Agility: Slow Creak | -2x + 8 (min 1)
- Flavour: Older than the hill it grew out of.

## 12. Moss Troll

- HP: 84
- Archetype: Tank
- Magic: Spore Cloud | 2(x - 1) (min 1)
- Strike: Heavy Club | -2x + 8 (min 1)
- Agility: Shamble | -x + 5 (min 1)
- Flavour: Thick, slow, and remarkably hard to convince to fall over.

## 13. Sparkhound

- HP: 29
- Archetype: Glass cannon
- Magic: Arc Bite | -3x + 10 (min 1)
- Strike: Nip | 2(x - 1) (min 1)
- Agility: Dash | -x + 5 (min 1)
- Flavour: Static crackles off it when it gets excited, which is always.

## 14. Bristlecharge

- HP: 31
- Archetype: Glass cannon
- Magic: Huff | -x + 5 (min 1)
- Strike: Spine Rush | 3(x + 1)
- Agility: Sidestep | 2(x + 1)
- Flavour: The warning snort is the only warning you get.

## 15. Quickfin

- HP: 27
- Archetype: Glass cannon
- Magic: Bubble | 2(x + 1)
- Strike: Fin Slap | -2x + 8 (min 1)
- Agility: Riptide Dart | -3x + 10 (min 1)
- Flavour: Gone before the ripples have finished spreading.

## 16. Cindercat

- HP: 49
- Archetype: Baseline
- Magic: Ember Purr | 3(x + 1)
- Strike: Swipe | -2x + 8 (min 1)
- Agility: Slink | 2(x - 1) (min 1)
- Flavour: Warm to the touch. Warmer if it has decided it doesn't like you.

## 17. Ironhide Ram

- HP: 52
- Archetype: Baseline
- Magic: Bleat | -2x + 8 (min 1)
- Strike: Headbutt | 3(x - 1) (min 1)
- Agility: Scramble | 2(x - 1) (min 1)
- Flavour: Built like a doorstop and twice as stubborn.

## 18. Zephyr Kite

- HP: 45
- Archetype: Baseline
- Magic: Updraft | -x + 5 (min 1)
- Strike: Talon Rake | 2(x + 1)
- Agility: Divebomb | 3(x - 1) (min 1)
- Flavour: Rides the wind so you never have to guess where it is — until you do.

## 19. Clockwork Beetle

- HP: 53
- Archetype: Baseline
- Magic: Spark Coil | -2x + 8 (min 1)
- Strike: Pincer | 2(x - 1) (min 1)
- Agility: Scuttle | 3(x - 1) (min 1)
- Flavour: Wind it up, set it down, and take a step back.

## 20. Barrow Wight

- HP: 79
- Archetype: Tank
- Magic: Chill Touch | -x + 5 (min 1)
- Strike: Grave Reach | 2(x - 1) (min 1)
- Agility: Drift | -2x + 8 (min 1)
- Flavour: It remembers being alive, and it resents you for still managing it.

## 21. Deepstone Toad

- HP: 80
- Archetype: Tank
- Magic: Mud Bolt | -2x + 8 (min 1)
- Strike: Bellyflop | 2(x - 1) (min 1)
- Agility: Hunker | -x + 5 (min 1)
- Flavour: Has not moved in a decade and does not plan to start now.

## 22. Rust Golem

- HP: 83
- Archetype: Tank
- Magic: Oxide Cloud | 2(x - 1) (min 1)
- Strike: Iron Fist | -2x + 8 (min 1)
- Agility: Grind Forward | -x + 5 (min 1)
- Flavour: Slow, heavy, and only ever going one direction: yours.
