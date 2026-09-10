# Algebra Monster Battle — Environment Cards (v2)

Source of truth for the environment deck. **Edit the card blocks below**, then run:

```bash
python tools/gen_env_cards.py
```

to regenerate the print sheet at [`environments.html`](environments.html). The model lives in
[`../docs/design/core-rules-v2.md`](../docs/design/core-rules-v2.md) §4.

## Card block format

```
## <number>. <Name>

- Boost:  <Type> <+2x | +x>
- Weaken: <Type> <-2x | -x>[, <Type> <-2x | -x>]
- Cancel: <Type>
- Flavour: <one line>
```

`<Type>` is `Magic`, `Strength` or `Agility`. Rules the generator enforces:

- **Weaken** may list two types (comma-separated); `Boost` and `Cancel` name one.
- Every effect names a **different** attack type; at most **2 effects** per card.
- `Boost` is `+2x`/`+x`; `Weaken` is `-2x`/`-x`; `Cancel` takes no term.
- Every card has at least one effect line, **except** `Open Field`.

## At a glance

| # | Name | Effect | Art |
|---|---|---|---|
| 1 | Arcane Nexus | Boost Magic +2x | have |
| 2 | Dark Cavern | Boost Agility +2x | have |
| 3 | Null Field | Cancel Magic | have |
| 4 | Sunken Marsh | Weaken Agility −2x | have |
| 5 | Frozen Wastes | Cancel Agility | have |
| 6 | Scorching Desert | Weaken Strength −2x | have |
| 7 | Runic Vault | Boost Magic +2x · Weaken Agility −x | have |
| 8 | Open Field | — | have |
| 9 | Coliseum | Boost Strength +2x | **new** |
| 10 | Bonepit | Boost Strength +2x · Weaken Magic −x | **new** |
| 11 | Highcrag | Boost Agility +2x · Weaken Strength −x | **new** |
| 12 | Dead Grove | Weaken Magic −2x | **new** |
| 13 | Thunderhead | Weaken Magic −x · Weaken Agility −x | **new** |
| 14 | Cloud Peak | Weaken Strength −x · Weaken Agility −x | **new** |
| 15 | The Veil | Cancel Strength | **new** |

---

## 1. Arcane Nexus

- Boost: Magic +2x
- Flavour: Ley lines converge here — raw magic answers the call.

## 2. Dark Cavern

- Boost: Agility +2x
- Flavour: Pitch black and close. Footwork and feel win down here.

## 3. Null Field

- Cancel: Magic
- Flavour: A dead zone. Spells gutter and die no matter who casts them.

## 4. Sunken Marsh

- Weaken: Agility -2x
- Flavour: Knee-deep mud and black water. Every quick move turns slow.

## 5. Frozen Wastes

- Cancel: Agility
- Flavour: Sheet ice from edge to edge. Nobody moves with any control.

## 6. Scorching Desert

- Weaken: Strength -2x
- Flavour: Heat and thirst drain the power out of every swing.

## 7. Runic Vault

- Boost: Magic +2x
- Weaken: Agility -x
- Flavour: Old wards feed spellwork; the air hangs thick around your feet.

## 8. Open Field

- Flavour: Flat, mild, open ground. Nothing helps and nothing hinders.

## 9. Coliseum

- Boost: Strength +2x
- Flavour: Packed stands, hard sand, and a crowd that came to see a hit land.

## 10. Bonepit

- Boost: Strength +2x
- Weaken: Magic -x
- Flavour: A pit of old bones. Good footing for a brawl; the air fights your casting.

## 11. Highcrag

- Boost: Agility +2x
- Weaken: Strength -x
- Flavour: A knife-edge ledge in a hard wind. Quick feet thrive; a big swing overbalances.

## 12. Dead Grove

- Weaken: Magic -2x
- Flavour: Petrified trees, no birdsong, no wind. Magic will barely flow.

## 13. Thunderhead

- Weaken: Magic -x, Agility -x
- Flavour: Lightning every few seconds. Spells scatter, footing is a gamble — but a fist still lands.

## 14. Cloud Peak

- Weaken: Strength -x, Agility -x
- Flavour: Thin air above the clouds. Every hard effort costs double — slow, careful magic still works.

## 15. The Veil

- Cancel: Strength
- Flavour: Half-real fog. Blows pass straight through — only spellcraft and speed touch anything here.
