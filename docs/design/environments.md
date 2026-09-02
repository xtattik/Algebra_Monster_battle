# Algebra Monster Battle — Environment Set Design

**Date:** 2026-09-02
**Status:** Implemented — model confirmed with the design owner; cards, generator, and rulebook reconciliation are in the repo. Open playtest question flagged in §7.
**Depends on:** [`core-rules.md`](core-rules.md) §5, §8
**Changes applied:** [`core-rules.md`](core-rules.md) §5.1–§5.3, §8, §13; student rulebook §5–6; teacher guide §6–8; answer key §1, §3 — see §8 below
**Scope:** The environment model and an 8-card starter deck, with content and print layout.

---

## 1. Purpose & what changed

Core-rules §8 gave each environment a flat "one stat boosted `+x`, one stat hurt `−x`", matched to the *attack type*. That only ever reaches Magic and Agility attacks.

This spec keeps that flat attack-type model **and adds one thing**: an environment can **test Strength** — physically harsh terrain (cold, heat) that wears down a fighter's *defence* unless they are hardy enough to cope. That is the piece a flat attack-type modifier can't express, because Strength is not an attack type.

The die, the base-attack model, the character stats, and "every modifier is a `±x` term" are all unchanged.

## 2. The environment card

Each card has up to three lines. **At least one** must be present (except the deliberate neutral card, §7 #8).

```
BOOSTS:   <Magic | Agility>     matching attacks gain +x   (everyone, no check)
HINDERS:  <Magic | Agility>     matching attacks take −x   (everyone, no check)
TESTS:    Strength              checked against the defender's Strength tier
```

**Constraints:**
- `BOOSTS` and `HINDERS` must name **different** stats.
- `TESTS` only ever names **Strength** in v1. A Magic/Agility "test" would just be a flat boost or hinder with extra words — use those.

## 3. BOOSTS / HINDERS — the flat attack-type modifiers

`BOOSTS: Magic` → every **magic attack** in this environment gains `+x`.
`HINDERS: Magic` → every **magic attack** takes `−x`.
Same for Agility.

- **No character check.** The terrain suits (or fights) that style for everyone. A High-Magic Sorcerer in a Magic-hindering Null Field still takes the `−x` — their character bonus and the environment penalty are separate terms that partly cancel (`+x − x`).
- **Never touches strike attacks** (unchanged from core-rules §5.3).
- There is no `BOOSTS: Strength` / `HINDERS: Strength` — Strength is handled by `TESTS`.

## 4. TESTS: Strength — the conditional defence check

`TESTS: Strength` is resolved against the **defender's own Strength tier**, mirroring the stat ladder, and the resulting term is added to the **enemy-Strength slot** for every attack made *against that defender*:

| Defender's Strength tier | Environment term (added to the enemy-Strength slot) |
|---|---|
| High | `−x` |
| Average | `0` |
| Low | `+x` |

- **Same sign convention as core-rules §5.2** (High defence → `−x` to the attacker), so it simply **stacks** with the existing enemy-Strength term:

  | Defender Strength | §5.2 term | `TESTS: Strength` term | Combined |
  |---|---|---|---|
  | High | `−x` | `−x` | `−2x` — a fortress |
  | Average | `0` | `0` | `0` |
  | Low | `+x` | `+x` | `+2x` — fully exposed |

- **Reaches strike attacks.** Strike takes no BOOSTS/HINDERS term, but the enemy-Strength slot has always applied to it (§5.3), and the environment's Strength term rides that slot. "The blizzard wears you down even against a club."
- Checked once per defender per match (their character's tier doesn't change), so in practice it is a fixed `+x` / `0` / `−x` the attacker adds every turn against that opponent.

## 5. The damage formula with an environment

Extends core-rules §5.1. The attacker builds:

```
damage = pet base attack             (ax + b)
       + your character stat modifier   (magic/agility attacks only; §5.2)
       + environment BOOSTS term        (+x if this attack's type is boosted)
       + environment HINDERS term       (−x if this attack's type is hindered)
       + enemy Strength term            (§5.2; applies to strike too)
       + environment TESTS: Strength term  (defender's tier; applies to strike too)
```

Then collect like terms → substitute the roll → floor per §5.4 → subtract from HP.

## 6. Worked examples

**E. Boost (unchanged from example A).** Sorcerer (Magic High) pet magic `3x + 1`, in **Arcane Nexus** (`BOOSTS: Magic`), vs a Bard (Str Avg).
→ `3x + 1 + x + x = 5x + 1` → roll 4 → **21**

**F. Hinder cancels the caster's edge.** Illusionist (Magic High) pet magic `3x + 1`, in **Null Field** (`HINDERS: Magic`), vs a Bard.
- Illusionist High Magic (§5.2): `+x`
- Null Field HINDERS Magic: `−x`
- enemy Strength, Bard Average: `0`
→ `3x + 1 + x − x = 3x + 1` → roll 4 → **13**

**G. Strength test, fragile defender, strike attack.** Barbarian pet **strike** `2x + 2`, in **Frozen Wastes** (`TESTS: Strength`), vs an Illusionist (Str Low).
- strike: no character, BOOSTS or HINDERS term
- enemy Strength, Illusionist Low (§5.2): `+x`
- Frozen Wastes TESTS Strength, defender Illusionist Low: `+x`
→ `2x + 2 + x + x = 4x + 2` → roll 3 → **14**  (vs `2x + 2` → 8 on open ground)

**H. Strength test, tough defender.** Same strike `2x + 2`, same Frozen Wastes, vs a Paladin (Str High).
- enemy Strength, Paladin High: `−x`
- Frozen Wastes TESTS Strength, defender Paladin High: `−x`
→ `2x + 2 − x − x = 2` → roll anything → **2**  (a bare constant — the Paladin in a blizzard is nearly untouchable by a club)

**I. Hybrid card, attacker's speed cancelled.** Trickster (Agi High) pet agility `2x + 1`, in **Scorching Desert** (`HINDERS: Agility`, `TESTS: Strength`), vs a Ranger (Str Avg).
- Trickster High Agility (§5.2): `+x`
- Scorching Desert HINDERS Agility: `−x`
- Scorching Desert TESTS Strength, defender Ranger Average: `0`
- enemy Strength, Ranger Average: `0`
→ `2x + 1 + x − x = 2x + 1` → roll 5 → **11**

**Independent recomputation**
- **E:** `(3 + 1 + 1)x + 1 = 5x + 1`; `x=4` → `21`. ✔
- **F:** `(3 + 1 − 1)x + 1 = 3x + 1`; `x=4` → `13`. ✔
- **G:** `(2 + 1 + 1)x + 2 = 4x + 2`; `x=3` → `14`. ✔
- **H:** `(2 − 1 − 1)x + 2 = 2`; any `x` → `2`. ✔
- **I:** `(2 + 1 − 1)x + 1 = 2x + 1`; `x=5` → `11`. ✔

## 7. Balance check (50 HP baseline pet, D6)

| Stack | Simplified | Roll 6 | Note |
|---|---|---|---|
| Offence fully aligned: character `+x` + BOOSTS `+x` on `3x + 1` | `5x + 1` | 31 | same ceiling as core-rules §5.6 |
| Attacking a Low-Strength character in a Strength-testing environment: enemy Strength `+x` + `TESTS` `+x` on top of the above | `7x + 1` | 43 | **new max**, and needs a BOOSTS-Magic + TESTS-Strength card — the v1 deck (§7.1) has none, so the real v1 ceiling is `6x + 1` → 37 |
| Fortress (example H): High-Strength defender in a Strength-testing environment | base `− 2x` | — | most base attacks become a bare constant; grindy but never below the printed min |

The `TESTS`/§5.2 stack against a Low-Strength *character* (not just pet) is the sharpest edge. It requires the defender's character to be wrong for the terrain and full attacker alignment; the defender can soften it with a tank pet but not remove it. **Left as-is for playtest** per the design owner. If it proves unfair, the fix is to cap the enemy-Strength slot at `±x` total.

### 7.1 The 8-card starter deck

| # | Name | BOOSTS | HINDERS | TESTS | Flavour hook |
|---|---|---|---|---|---|
| 1 | Arcane Nexus | Magic | — | — | Ley lines converge; spellcraft comes easy. |
| 2 | Deep Shadow | Agility | — | — | Deep gloom; the sure-footed slip through unseen. |
| 3 | Null Field | — | Magic | — | A dead zone. Spells gutter and fail. |
| 4 | Blinding Light | — | Agility | — | Relentless glare; no way to pick your footing. |
| 5 | Frozen Wastes | — | — | Strength | Marrow-deep cold. The hardy endure; the frail seize up. |
| 6 | Scorching Desert | — | Agility | Strength | Heat and thirst: every move drags, and only the tough push on. |
| 7 | Runic Vault | Magic | Agility | — | Old wards feed spellcraft, but the air hangs thick and slow. |
| 8 | Open Field | — | — | — | Flat, mild, open. Nothing helps and nothing hinders. |

Spread: BOOSTS Magic ×2, Agility ×1, none ×5. HINDERS Magic ×1, Agility ×2, none ×5. TESTS Strength ×2, none ×6. No card boosts and hinders the same stat. Card 8 (**Open Field**) is the neutral / pacing card and the differentiation "support" tier in core-rules §11 ("only ever play Open Field").

Names and flavour live in `cards/environments.md` and are cheap to swap; the mechanics above are the contract.

## 8. Changes required to existing documents

Small, because the flat attack-type model is unchanged:

**`core-rules.md`**
- **§5.1 / §5.2** — the environment row becomes: up to one `BOOSTS` (`+x`) and one `HINDERS` (`−x`) attack-type term, still flat and unconditional, **plus** an optional `TESTS: Strength` term (§4 here) added to the enemy-Strength slot.
- **§5.3** — physical attacks still take no BOOSTS/HINDERS term; add one sentence that a `TESTS: Strength` environment *does* affect them, through the enemy-Strength slot.
- **§5.5** — examples A–D still hold verbatim (Arcane Nexus = `BOOSTS: Magic`; Blinding Light = `HINDERS: Agility`). No rewrite; optionally add a cross-reference.
- **§6.2** — no change. "Sorcerer: fear Null Fields" and "Trickster: avoid Blinding Light" are both still correct under the flat model.
- **§8** — replace the scope summary with the model above and a pointer to this doc.
- **§13** — mark the environment open questions resolved (count 8; Open Field is the neutral card; the temperature ideas map onto `TESTS: Strength`).

**`rulebook/student-rulebook.md`** — §5 "The environment": add that some cards instead/also **test Strength** — check your character's Strength tier, and it changes every attack against you, *including strike*. Add one worked example (F or G).

**`rulebook/teacher-guide.md`** — §6 common errors: add "used the Strength test without checking the defender's tier" and "forgot the Strength test reaches strike attacks". §7: add worked examples F–I. §8 differentiation: support = Open Field only.

**`rulebook/answer-key.md`** — add the simplified forms and answers for F–I. The lookup table (`1x`–`6x`, `−3`..`+3`) still covers the v1 deck's reachable forms; add a note that two-environment extension play can exceed `6x`.

**`cards/characters.md`** — no change needed (playstyle lines already match).

## 9. Card layout & print

**Files:** `cards/environments.md` (authored source of truth) → `tools/gen_env_cards.py` → `cards/environments.html`.

Mirror the character-card setup:
- Same 63 mm × 88 mm card, A4 9-up sheet, self-contained HTML, black on white + the one red spot colour.
- **BOOSTS** row: stat name + `+x`. **HINDERS** row: stat name + `−x`. Missing line prints `—`.
- **TESTS: Strength** shown as a mini 3-row table (High `−x` / Average `0` / Low `+x`) with the same red "defence · vs you" treatment as the character cards, plus a one-line "also affects strike attacks" note.
- Flavour line at the foot; card number in the header.
- The generator derives every `±x` term; it reads only name / boosts / hinders / tests / flavour from the source. It exits non-zero on: an unknown stat, `BOOSTS == HINDERS`, `TESTS` not equal to `Strength`, or a card with no lines that is not named `Open Field`.

## 10. Verification checklist

- [x] core-rules.md §5.1–§5.3, §8, §13 reconciled; no document still describes only the flat model.
- [x] Worked examples A–I recomputed from scratch (`ev(n,c,x)=max(0,nx+c)`), all PASS.
- [x] Each of the 8 cards: BOOSTS ≠ HINDERS; TESTS is Strength or absent; at least one line (Open Field excepted). Enforced by the generator.
- [x] Every doc that mentions the Strength test also says it reaches strike attacks (core-rules §5.3/§8, student rulebook §5/§6, teacher guide §6/§7, answer key §1/§3, card face).
- [x] `python tools/gen_env_cards.py` runs clean, is idempotent (`--check` after two runs), and rejects a bad stat / `BOOSTS==HINDERS` / `TESTS: Agility` / an empty non-Open-Field card.
- [x] Print preview: 8 cards on one A4 page, nothing clipped; Strength-test rows still distinguishable in greyscale.
- [x] No card or doc introduces a bare-number bonus or a coefficient other than `x`.

## 11. Out of scope

- Two-environments-per-match (core-rules §11 extension) — the model allows it; the answer key stays single-environment for v1.
- Magic/Agility graded tests, or any `TESTS` result other than `+x / 0 / −x`.
- Environment cards that alter HP, the die, turn order, or pet choice (core-rules §12).
- Real artwork; card backs.
