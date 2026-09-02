# Algebra Monster Battle — Environment Set Design

**Date:** 2026-09-02
**Status:** Draft for review
**Depends on:** [`core-rules.md`](core-rules.md) §5, §8
**Changes:** [`core-rules.md`](core-rules.md) §5.2, §5.3, §5.5, §6.2, §8 — see §9 below
**Scope:** The environment model and an 8-card starter deck, with content and print layout.

---

## 1. Purpose & what changed

Core-rules §8 originally gave each environment a flat "one stat boosted `+x`, one stat hurt `−x`", matching the *attack type*. That only reaches Magic and Agility attacks, so the deck could hold at most two or three distinct cards.

This spec replaces it with a **two-part card** so environments can vary widely and so *physically* harsh terrain (ice, heat) can wear down a fighter's **defence** — the effect a flat attack-type modifier can't express.

The die, the base-attack model, the character stats, and the "every modifier is a `±x` term" rule are all unchanged.

## 2. The environment card

Each card has up to two lines. **At least one** must be present; a card may have both.

```
FAVOURS:  <Magic | Agility>        matching attacks gain +x
TESTS:    <Magic | Strength | Agility>   resolved against your character's tier
```

Plus a name, a flavour line, and a card number.

**Constraint:** if a card has both lines, they must name **different stats**. (`FAVOURS: Magic` + `TESTS: Magic` would stack two `+x` on the same attack for a High-Magic character and break the balance ceiling — see §7.)

## 3. FAVOURS — the unconditional boon

`FAVOURS: Magic` → every **magic attack** made in this environment gains `+x`.
`FAVOURS: Agility` → every **agility attack** gains `+x`.

- No character check — the terrain simply suits that style.
- Never applies to **strike** attacks (unchanged from core-rules §5.3).
- There is no `FAVOURS: Strength` — Strength is not an attack type.

## 4. TESTS — the conditional check

`TESTS: <stat>` is resolved against the acting character's **own tier** in that stat, exactly mirroring the stat ladder:

| Your tier in the tested stat | Environment term |
|---|---|
| High | `+x` |
| Average | `0` |
| Low | `−x` |

Where the term lands depends on which stat is tested:

| Tested stat | Whose tier is checked | Term is added to | Reaches strike? |
|---|---|---|---|
| **Magic** | the **attacker** | the attacker's **magic attacks** | no |
| **Agility** | the **attacker** | the attacker's **agility attacks** | no |
| **Strength** | the **defender** | the **enemy-Strength term** on every attack *against that defender* | **yes** |

Rationale: Magic and Agility are *offensive* stats, so testing them checks the attacker and modifies that attack type. Strength is a *defensive* stat, so testing it checks the defender and modifies incoming damage — and because it rides the enemy-Strength term, it is felt by strike attacks too. "The blizzard wears down anyone who can't take it, even against a club."

### 4.1 Sign direction for `TESTS: Strength`

The enemy-Strength term already in core-rules §5.2 is: High defender Strength → `−x` to the attacker, Low → `+x` to the attacker. The environment's Strength test **adds another term in the same slot, with the same convention**:

| Defender's Strength tier | From §5.2 (unchanged) | From a `TESTS: Strength` environment | Combined enemy-Strength contribution |
|---|---|---|---|
| High | `−x` | `−x` | `−2x` (a fortress) |
| Average | `0` | `0` | `0` |
| Low | `+x` | `+x` | `+2x` (fully exposed) |

So a High-Strength defender in Frozen Wastes is *harder* to hurt than normal; a Low-Strength defender is a sitting duck.

## 5. The damage formula with an environment

Extends core-rules §5.1. The attacker builds:

```
damage = pet base attack                (ax + b)
       + your character stat modifier   (magic/agility attacks only; §5.2)
       + environment FAVOURS term       (+x if this attack's type is favoured)
       + environment TESTS term         (if TESTS Magic/Agility and matches this attack's type,
                                         using the attacker's tier)
       + enemy Strength term            (§5.2; applies to strike too)
       + environment TESTS: Strength term  (if the environment tests Strength,
                                            using the defender's tier; applies to strike too)
```

Then: collect like terms → substitute the roll → floor per §5.4 → subtract from HP.

Only one of FAVOURS / TESTS can touch a single attack's **offence** (they name different stats, §2), so the most an environment adds to one attack's offensive side is `+x`.

## 6. Worked examples

**E. Attacker thrives on a test.** Ranger (Agi High) pet agility attack `2x + 1`, in **Storm Front** (`FAVOURS: Agility`, `TESTS: Magic`), vs a Bard (Str Avg).
- base `2x + 1`
- Ranger High Agility (§5.2): `+x`
- Storm Front FAVOURS Agility: `+x`
- Storm Front TESTS Magic — this is an *agility* attack, no match: `0`
- enemy Strength, Bard Average: `0`
- → `2x + 1 + x + x = 4x + 1` → roll 4 → **17**

**F. Physical harshness hits a fragile defender.** Barbarian pet **strike** `2x + 2`, in **Frozen Wastes** (`TESTS: Strength`), vs an Illusionist (Str Low).
- base `2x + 2` (strike takes no character or FAVOURS term)
- enemy Strength, Illusionist Low (§5.2): `+x`
- Frozen Wastes TESTS Strength, defender Illusionist Low: `+x`
- → `2x + 2 + x + x = 4x + 2` → roll 3 → **14**  (vs `2x + 2` → 8 on open ground)

**G. Physical harshness bounces off a tough defender.** Same strike `2x + 2`, same Frozen Wastes, vs a Paladin (Str High).
- enemy Strength, Paladin High: `−x`
- Frozen Wastes TESTS Strength, defender Paladin High: `−x`
- → `2x + 2 − x − x = 2x + 2 − 2x = 2` (a bare constant) → roll anything → **2**
- Note: this is a *base pet attack* reduced by modifiers; §5.4 floors post-modifier damage at 0, and here it is a flat 2. The Paladin in a blizzard is nearly untouchable by a club.

**H. Low-tier attacker suffers a test.** Barbarian (Magic Low) pet magic attack `3x + 1`, in **Runic Vault** (`TESTS: Magic`), vs a Bard.
- base `3x + 1`
- Barbarian Low Magic (§5.2): `−x`
- Runic Vault TESTS Magic, attacker Barbarian Low: `−x`
- enemy Strength, Bard Average: `0`
- → `3x + 1 − x − x = x + 1` → roll 2 → **3**  (the Barbarian should not have cast)

**Independent recomputation**
- **E:** `(2 + 1 + 1)x + 1 = 4x + 1`; `x=4` → `16 + 1 = 17`. ✔
- **F:** `(2 + 1 + 1)x + 2 = 4x + 2`; `x=3` → `12 + 2 = 14`. ✔
- **G:** `(2 − 1 − 1)x + 2 = 0x + 2 = 2`; any `x` → `2`. ✔
- **H:** `(3 − 1 − 1)x + 1 = x + 1`; `x=2` → `2 + 1 = 3`. ✔

## 7. Balance check (50 HP baseline pet, D6)

Worst-case favourable stack on **one attack**:

| Side | Terms | Max |
|---|---|---|
| Offence | character stat `+x` + (FAVOURS **or** TESTS, never both) `+x` | `+2x` |
| Defence (attacking a Low-Strength character in a Strength-testing environment) | enemy Strength `+x` + environment TESTS: Strength `+x` | `+2x` |

- **Magic/agility attack, everything offensive aligned:** `3x + 1` → `5x + 1`, roll 6 → **31**. Same ceiling as core-rules §5.6 — the different-stats constraint (§2) is what holds it here.
- **Everything aligned, defender also a Low-Strength character in hostile terrain:** `3x + 1` → `7x + 1`, roll 6 → **43**. New maximum. Requires the *defender's character* (not just their pet) to be the wrong one for the terrain; they can soften it by fielding a tank pet, but not remove it. Flag for playtest — if this feels unfair, the fix is to cap the enemy-Strength slot at `±x` total (environment test does not stack with §5.2, only replaces `0`).
- **Fortress case (example G):** a High-Strength defender in a Strength-testing environment turns most base attacks into a bare constant. Grindy but never zero — acceptable, and a strong incentive to pick your terrain.

No configuration one-shots a 50 HP pet. The 30 HP glass cannon can be one-shot by a fully aligned attacker, as in §5.6 — unchanged intent.

## 8. The 8-card starter deck

| # | Name | FAVOURS | TESTS | Flavour hook |
|---|---|---|---|---|
| 1 | Arcane Nexus | Magic | — | Ley lines converge; raw magic is amplified for everyone. |
| 2 | Deep Shadow | Agility | — | Total darkness; the light-footed own the ground. |
| 3 | Runic Vault | — | Magic | Dense old wards: trained casters channel them, dabblers catch the feedback. |
| 4 | Blinding Light | — | Agility | Relentless glare; only the genuinely nimble still move well. |
| 5 | Frozen Wastes | — | Strength | Marrow-deep cold. The hardy endure; the frail are left exposed. |
| 6 | Molten Cavern | Magic | Strength | Heat-charged air feeds spellwork but saps the body. |
| 7 | Storm Front | Agility | Magic | Howling wind scatters spellcraft; the agile ride the gusts. |
| 8 | Open Field | — | — | Flat, mild, featureless. Nothing helps and nothing hinders. |

Spread: FAVOURS Magic ×2, Agility ×2, none ×4. TESTS Magic ×2, Agility ×1, Strength ×2, none ×3. Every stat is tested at least once; two pure boons, two pure hazards, two hybrids, one neutral. All hybrid cards satisfy the different-stats constraint.

Card 8 (**Open Field**) is the pacing / support card: the differentiation "support" tier in core-rules §11 becomes "only ever play Open Field", and it gives a tired class a low-load round.

## 9. Changes required to existing documents

This model contradicts several statements written under the old flat model. All must be reconciled in the same change:

**`core-rules.md`**
- **§5.1 / §5.2** — replace the single "environment modifier" row with the FAVOURS + TESTS model (§4–§5 here). Keep "every modifier is a `±x` term".
- **§5.3** — physical attacks still take no FAVOURS term and no Magic/Agility TESTS term, but a `TESTS: Strength` environment **does** reach them via the enemy-Strength term. Update the wording.
- **§5.5** — examples A–D: A, B, C still hold (Arcane Nexus is now `FAVOURS: Magic`, same result). Example D referenced "Blinding Light (Agility hurt, `−x`)" as unconditional — rewrite it as a `TESTS: Agility` result for a Low- or Average-Agility attacker, or repoint it at `TESTS` explicitly.
- **§6.2** — playstyle tips that assume the old model:
  - Sorcerer "fear Null Fields" → a High-Magic character now *thrives* where Magic is tested. Change to a real weakness: Sorcerer is Low Agility, so it fears `TESTS: Agility` terrain (Blinding Light).
  - Trickster "avoid Blinding Light" → Trickster is High Agility and now *thrives* there. Trickster is Low Strength, so it should avoid `TESTS: Strength` terrain (Frozen Wastes, Molten Cavern).
  - Ranger "thrives in Deep Shadow" — still true (unconditional `FAVOURS: Agility`). No change.
- **§8** — replace the scope summary with a pointer to this doc.
- **§13** — mark the environment open questions resolved (count = 8; Open Field is the neutral card; the temperature ideas map onto `TESTS: Strength`).

**`rulebook/student-rulebook.md`** — §5 "The environment" and §6 step 2: describe FAVOURS and TESTS, and that a Strength-testing environment can change a strike attack against you. One new worked example.

**`rulebook/teacher-guide.md`** — §6 common errors (add: "applied a TESTS term without checking the character's tier"; "forgot a `TESTS: Strength` term touches strike"), §7 worked examples (add E–H), §8 differentiation (support = Open Field only).

**`rulebook/answer-key.md`** — add the simplified forms and scenario answers for E–H; the lookup table already covers `1x`–`6x`, `−3`..`+3` so most new forms are in range (`7x + 1` from §7 is out of range — add a note or extend to `7x`).

**`cards/characters.md`** — Sorcerer and Trickster playstyle lines currently name the wrong terrain; rewrite per the §6.2 changes above, then regenerate `characters.html`.

## 10. Card layout & print

**Files:** `cards/environments.md` (authored source of truth) → `tools/gen_env_cards.py` → `cards/environments.html`.

Mirror the character-card setup:
- Same 63 mm × 88 mm card, A4 9-up sheet, self-contained HTML, black on white + the one red spot colour.
- **FAVOURS** line: stat name + `+x`, styled like a character card's boon row.
- **TESTS** line: shown as a mini 3-row table (High `+x` / Average `0` / Low `−x`) so the student can read their own result directly. If `TESTS: Strength`, the row is given the same red "defence — vs you" treatment as the character cards, and carries a one-line "affects strike attacks too" note.
- A card missing a line prints "—" for it, not a blank.
- Flavour line at the foot. Card number in the header.
- The generator derives all `±x` terms from the tier; it only reads name / favours / tests / flavour from the source. It exits non-zero on an unknown stat, on FAVOURS == TESTS, or on a card with neither line.

## 11. Verification checklist

- [ ] core-rules.md and all three rulebook docs reconciled (§9); no document still describes the flat model.
- [ ] Every worked example (A–H, everywhere) recomputed from scratch, PASS/FAIL listed.
- [ ] Each of the 8 cards: FAVOURS and TESTS name different stats (or one is absent); at least one is present.
- [ ] `TESTS: Strength` cards state that strike is affected; `TESTS: Magic/Agility` cards state that strike is not.
- [ ] Character-card playstyle lines for Sorcerer and Trickster name terrain that actually matches the new model; `characters.html` regenerated.
- [ ] `python tools/gen_env_cards.py` runs clean, is idempotent, and validates the constraints.
- [ ] Print preview: 8 cards on one A4 page, nothing clipped, Strength-test rows readable with colour off.
- [ ] No card or doc introduces a bare-number bonus or a coefficient other than `x` (no `2x` modifiers).

## 12. Out of scope

- Two-environments-per-match (core-rules §11 extension) — the model supports it, but the answer key stays single-environment for v1.
- Environment cards that alter HP, the die, turn order, or pet choice — core-rules §12 forbids environmental status effects beyond the `±x` term.
- Real artwork; card backs.
- Any TESTS result other than `+x / 0 / −x`.
