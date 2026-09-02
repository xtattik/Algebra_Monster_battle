# Algebra Monster Battle — Environment Cards

Source of truth for the 8 environment cards. **Edit the card blocks below**, then run:

```bash
python tools/gen_env_cards.py
```

to regenerate the print sheet at [`environments.html`](environments.html). The model, the
worked examples, and the print spec live in
[`../docs/design/environments.md`](../docs/design/environments.md).

## Card block format

```
## <number>. <Name>

- Boosts: <Magic | Agility | none>
- Hinders: <Magic | Agility | none>
- Tests: <Strength | none>
- Flavour: <one line>
```

Rules the generator enforces:

- `Boosts` and `Hinders` must name different stats (or both be `none`).
- `Tests` is `Strength` or `none` — nothing else in v1.
- Every card needs at least one of Boosts / Hinders / Tests, **except** `Open Field`.

The `±x` terms and the High/Average/Low test table are derived by the generator,
not written here (see the design doc §9).

## At a glance

| # | Name | Boosts | Hinders | Tests |
|---|---|---|---|---|
| 1 | Arcane Nexus | Magic | — | — |
| 2 | Deep Shadow | Agility | — | — |
| 3 | Null Field | — | Magic | — |
| 4 | Blinding Light | — | Agility | — |
| 5 | Frozen Wastes | — | — | Strength |
| 6 | Scorching Desert | — | Agility | Strength |
| 7 | Runic Vault | Magic | Agility | — |
| 8 | Open Field | — | — | — |

---

## 1. Arcane Nexus

- Boosts: Magic
- Hinders: none
- Tests: none
- Flavour: Ley lines converge here; spellcraft comes easy to anyone.

## 2. Deep Shadow

- Boosts: Agility
- Hinders: none
- Tests: none
- Flavour: Deep gloom swallows the field — the sure-footed slip through unseen.

## 3. Null Field

- Boosts: none
- Hinders: Magic
- Tests: none
- Flavour: A dead zone for magic. Spells gutter and fail no matter who casts them.

## 4. Blinding Light

- Boosts: none
- Hinders: Agility
- Tests: none
- Flavour: Relentless glare off every surface — no way to pick your footing.

## 5. Frozen Wastes

- Boosts: none
- Hinders: none
- Tests: Strength
- Flavour: Marrow-deep cold. The hardy endure it; the frail seize up and drop their guard.

## 6. Scorching Desert

- Boosts: none
- Hinders: Agility
- Tests: Strength
- Flavour: Heat and thirst. Every movement drags, and only the tough keep pushing.

## 7. Runic Vault

- Boosts: Magic
- Hinders: Agility
- Tests: none
- Flavour: Old wards feed spellcraft, but the air hangs thick and slow around your feet.

## 8. Open Field

- Boosts: none
- Hinders: none
- Tests: none
- Flavour: Flat, mild, open ground. Nothing here helps you and nothing hinders you.
