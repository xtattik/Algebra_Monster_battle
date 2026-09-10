# Algebra Monster Battle — Environment Set Design (v2)

**Date:** 2026-09-02 · **v2 rewrite:** 2026-09-10
**Status:** Draft for review — provisional, first v2 playtest pending.
**Model:** [`core-rules-v2.md`](core-rules-v2.md) §4. **Source:** [`../cards/environments.md`](../cards/environments.md) · **Generator:** [`../tools/gen_env_cards.py`](../tools/gen_env_cards.py)

---

## 1. What v2 changed

v1 had a flat `±x` per attack type plus a "Tests: Strength" defence check. Playtest: too weak to matter, and the defence check was opaque. v2:

- The environment is the **`±2x` dial** (`±x` as a secondary), with **Cancel** as a third verb. Character stats stay `±x` (so a favoured character is penalised *less*, not walled).
- Attack type is **strength** (was "strike"), matching the stat.
- No defence — HP is defence.

## 2. The three verbs

| Verb | Card line | Term |
|---|---|---|
| **Boost** | `Boost: <Type> <+2x\|+x>` | added to that attack type |
| **Weaken** | `Weaken: <Type> <-2x\|-x>` (may list two types) | subtracted from that attack type |
| **Cancel** | `Cancel: <Type>` | that attack type is **unusable** this match — ignores the character bonus |

One card: at most one Boost, at most one Cancel, up to two Weaken types; every effect names a different type; ≤ 2 effects total. `Open Field` has none.

## 3. The 15 designs

| # | Name | Effect | Art |
|---|---|---|---|
| 1 | Arcane Nexus | Boost Magic `+2x` | ✅ have |
| 2 | Dark Cavern | Boost Agility `+2x` | ✅ have |
| 3 | Null Field | **Cancel Magic** | ✅ have |
| 4 | Sunken Marsh | Weaken Agility `−2x` | ✅ have |
| 5 | Frozen Wastes | **Cancel Agility** | ✅ have (icy — "too slick to move") |
| 6 | Scorching Desert | Weaken Strength `−2x` | ✅ have |
| 7 | Runic Vault | Boost Magic `+2x` · Weaken Agility `−x` | ✅ have |
| 8 | Open Field | — (neutral) | ✅ have |
| 9 | Coliseum | Boost Strength `+2x` | 🆕 need |
| 10 | Bonepit | Boost Strength `+2x` · Weaken Magic `−x` | 🆕 need |
| 11 | Highcrag | Boost Agility `+2x` · Weaken Strength `−x` | 🆕 need |
| 12 | Dead Grove | Weaken Magic `−2x` | 🆕 need |
| 13 | Thunderhead | Weaken Magic `−x` · Weaken Agility `−x` | 🆕 need |
| 14 | Cloud Peak | Weaken Strength `−x` · Weaken Agility `−x` | 🆕 need |
| 15 | The Veil | **Cancel Strength** | 🆕 need |

**Art still to make (7):** Coliseum · Bonepit · Highcrag · Dead Grove · Thunderhead · Cloud Peak · The Veil. The eight v1 environment images map straight onto cards 1–8 (same numbers, same files — no renaming). Names in the source are cheap to swap.

Coverage: every attack type gets a pure `+2x` boost, a hybrid `+2x` boost, a `−2x` weaken, and a Cancel.

## 4. Frequency

There is **no fixed ratio**. The teacher prints however many copies of each design they want — a deck weighted to boosts is gentler, one heavy on Cancels is a harder challenge. Cancel designs are 3 of 15; two or three copies each in a class deck ≈ a real but survivable threat to a specialist.

## 5. Reveal order

Terrain drawn first → both players pick a pet (simultaneous reveal). A Cancel forces a specialist onto their backup pet — a worse setup, not a forfeit ([`core-rules-v2.md`](core-rules-v2.md) §4.2).

## 6. Verification

- [x] `python tools/gen_env_cards.py` runs clean, idempotent; rejects a bad type / term, `>2` effects, a non-Weaken multi-type line, a card with no effect that isn't Open Field.
- [x] 15 cards, every effect a different type, ≤ 2 per card.
- [ ] Print preview: 15 cards over 2 A4 pages, nothing clipped, Cancel rows legible in mono.
- [ ] Playtest: is `±2x` the right size? are 3 Cancel designs too many?

## 7. Out of scope

- "Sap" (halve the final number) — considered, cut; parked for an advanced version.
- Environments that alter HP, the die, turn order, or pet choice.
- Real artwork; card backs.
