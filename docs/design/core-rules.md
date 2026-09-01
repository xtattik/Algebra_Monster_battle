# Algebra Monster Battle — Core Rules Design

**Date:** 2026-09-01
**Status:** Draft for review
**Scope:** Core game system + full character roster. Environments and pets get their own specs (see §13).

---

## 1. Summary & learning goal

A print-and-play classroom card game. Students pick a fantasy **character**, trade monster **pets**, then fight 1v1 duels in a randomly drawn **environment**. Every attack requires the student to build a linear expression, **collect like terms**, then **substitute a dice roll** to find the damage.

The maths is the game's resolution mechanic — you cannot play a turn without doing it.

## 2. Curriculum alignment

NSW Mathematics Stage 4 — Algebraic Techniques:

- Simplifying algebraic expressions by collecting like terms (e.g. `3x + x + x = 5x`)
- Substituting values into linear expressions and evaluating (e.g. `5x + 1` at `x = 4`)
- Working with negative constants and results that floor at zero

*(Teacher to confirm the exact current outcome code for their programming.)*

## 3. Components

| Item | Notes |
|---|---|
| 7 character cards | One design each; print a class set so multiple students can be the same character |
| Pet deck | Print enough that every student can draw **2 at random**; duplicates are fine |
| Environment deck | Drawn once per match |
| 1 six-sided die per pair | Standard D6 |
| HP trackers | Counters, mini-whiteboards, or a printed HP track per pet |
| Student rulebook | 1–2 pages |
| Teacher guide + answer key | Worked examples, fast-marking lookup table |
| Battle worksheet | Students record each attack's working — the **markable artifact** |

## 4. The variable and the die

- `x` = the result of **one D6 roll**.
- The **attacker rolls once at the start of their turn**; that roll is `x` for that single attack.
- The defender rolls their own fresh `x` on their turn.

## 5. Damage model

### 5.1 The formula

```
damage = pet's base attack
       + your character modifier
       + environment modifier
       − enemy Strength defence
```

Procedure the student follows every attack:

1. Write the pet's base attack expression (`ax + b`).
2. Add/subtract the modifier terms that apply (all are `±x`).
3. **Collect like terms** → a single `nx + c`.
4. Substitute your dice roll for `x`.
5. Apply the minimum (see §5.4).
6. Subtract the result from the enemy pet's HP.

### 5.2 Modifier table

| Source | High | Average | Low |
|---|---|---|---|
| Your **Magic** — applies to *magic* attacks only | `+x` | `0` | `−x` |
| Your **Agility** — applies to *agility* attacks only | `+x` | `0` | `−x` |
| **Environment** — each card names one boosted stat and one hurt stat | `+x` if the attack matches the boosted stat | `0` | `−x` if the attack matches the hurt stat |
| Enemy **Strength** — their defence against *your* attack | `−x` | `0` | `+x` |

All modifiers are coefficient terms (`±x`), never bare numbers — this is what forces the like-terms step. Individual character types may vary slightly in flavour text but stay within this `±x` band.

### 5.3 Physical / strike attacks

A pet's **physical (strike) attack takes no character modifier and no environment modifier.** Strength is a defensive stat, and physical damage is meant to be the *reliable* option — unaffected by hostile terrain.

The enemy's **Strength defence still applies** to it (`−x` vs High-Strength defenders).

This is the strategic core: a Sorcerer stuck in a Null Field can field a physical pet and still deal predictable damage.

### 5.4 Minimums

- **Base pet attacks** never evaluate below **1**. Where an equation could hit 0 or go negative on a low roll, the card prints its own floor, e.g. `x − 1 (min 1)`.
- **After modifiers**, damage floors at **0** — a well-countered attack *can* be fully negated, but only on a low roll combined with a negative constant. A high roll should always connect for something.

*Example:* attack `2x − 2`, enemy environment `−x` → combined `x − 2`. Roll 1–2 → 0 damage. Roll 3+ → still hits.

### 5.5 Worked examples

**A. Sorcerer + Sprite, magic attack, in Arcane Nexus, vs a Barbarian (Avg Strength)**
Sprite "Fairy Lights" `3x + 1` · Sorcerer High Magic `+x` · Arcane Nexus boosts Magic `+x` · enemy Avg Strength `0`
→ `3x + 1 + x + x = 5x + 1`
→ roll 4 → `5(4) + 1 = 21 damage`

**B. Same attack, but the defender is a Paladin (High Strength)**
→ `3x + 1 + x + x − x = 4x + 1`
→ roll 4 → `17 damage`

**C. Physical attack ignores terrain**
Ogre "Strike" `2x + 2` · trainer is a Ranger (no strike buff) · Arcane Nexus (no effect on physical) · enemy Avg Strength
→ expression stays `2x + 2`
→ roll 3 → `8 damage`
Against a High-Strength defender → `2x + 2 − x = x + 2` → roll 3 → `5 damage`

**D. Hitting zero on a low roll**
Pet agility attack `2x − 2` · enemy in Blinding Light (Agility hurt, `−x`)
→ `2x − 2 − x = x − 2`
→ roll 2 → `0` · roll 5 → `3 damage`

### 5.6 Balance ceiling (50 HP baseline pet, standard D6)

| Scenario | Simplified | Roll 6 | Outcome |
|---|---|---|---|
| Strong hit, no environment | `4x + 1` | 25 | 2 hits to drop 50 HP |
| Full favourable stack | `5x + 1` | 31 | still 2 hits on 50 HP |
| Full stack vs 30 HP glass cannon | `5x + 1` | 31 | **one-shot — the intended payoff** |
| Everything against you | `1x` | 6 | grindy, never zero |

No configuration one-shots a normal pet. A fully-aligned character + pet + environment can burst a 30 HP glass cannon — the designed reward for a well-planned trade.

## 6. Characters (full roster)

### 6.1 Stat system

Three stats: **Magic**, **Strength**, **Agility**. Each is fixed per character at **High / Average / Low**. Every character has exactly one High, one Average, one Low — except the all-rounder (all Average).

- **Magic** buffs your magic attacks (`±x` per §5.2)
- **Agility** buffs your agility attacks (`±x`)
- **Strength** is defensive — it worsens the enemy's rolls against you (`−x` at High), or leaves you exposed (`+x` to the enemy at Low)

There is no separate flat "roll +1" bonus — the `±x` term system is the only modifier system.

### 6.2 The 7 characters

Order: **Magic / Strength / Agility**

| # | Name | Magic | Strength | Agility | Playstyle tip |
|---|---|---|---|---|---|
| 1 | Sorcerer | High | Avg | Low | Field high-magic pets; fear Null Fields |
| 2 | Illusionist | High | Low | Avg | Big magic, paper defence — end fights fast |
| 3 | Paladin | Avg | High | Low | Tanky; let pets grind while your defence holds |
| 4 | Barbarian | Low | High | Avg | Bruiser; lean on physical-strong pets |
| 5 | Trickster | Avg | Low | High | Nimble skirmisher; agility pets, avoid Blinding Light |
| 6 | Ranger | Low | Avg | High | Agility specialist; thrives in Deep Shadow |
| 7 | Bard | Avg | Avg | Avg | No weakness, no spike — flexible in any terrain |

### 6.3 Character card layout

- Name + art
- The three stat tiers, each with its effect in plain words **and** its `±x` term, e.g.
  - *Magic — HIGH: your magic attacks gain `+x`*
  - *Strength — LOW: enemy attacks against you gain `+x`*
- One-line playstyle tip
- Short flavour line

## 7. Pets (scope summary — dedicated spec to follow)

Each pet card carries:

- Name + art
- **HP** and archetype: baseline (~50), glass cannon (~30, high damage), tank (~80, low damage)
- **Three attack equations** — magic / strike / agility — each `ax + b` with a printed min where needed

Affinity is expressed **in the equations themselves**, not as a modifier: a strong-physical pet has a strike like `2x + 2` and a weak magic attack like `x − 1 (min 1)`.

**V2 only:** extreme pets (e.g. Hill Giant, 200 HP, strong, but does **not** heal between matches — dominates early, becomes a liability later).

## 8. Environments (scope summary — dedicated spec to follow)

Each environment card carries a **modifier table** naming:

- one **boosted** stat → matching attacks gain `+x`
- one **hurt** stat → matching attacks take `−x`

Working examples to develop: Arcane Nexus, Null Field, Deep Shadow, Blinding Light, Frozen Wastes.

## 9. Game flow

### 9.1 Setup

1. Each student takes a **character card** (random or choice — teacher's call).
2. Each student draws **2 pets at random** from the pet deck. Duplicates allowed. This is their starting **zoo**.

### 9.2 Trading phase

- Timed (≈5 minutes). Students trade pets freely by mutual agreement.
- Goal: acquire pets that cover your character's weak stat and suit environments you expect.
- **V2 extension (assessment):** a trade must be accompanied by a written inequality justifying it (e.g. "Ogre strike beats Sprite magic whenever `x > 3`").

### 9.3 Battle (one match)

1. Draw **one environment card** — it applies for the whole match.
2. Both players choose which pet to field (secretly, then reveal).
3. Determine first turn: coin flip / dice roll / rock-paper-scissors.
4. **On your turn:** roll `x` → choose one of your pet's three attacks → build and simplify the expression → substitute → subtract from the enemy pet's HP.
5. Alternate turns until one pet reaches **0 HP**.
6. The player whose pet fell is **eliminated** from the ladder.
7. The winner rolls a D6: a **6** captures the defeated pet into their zoo; otherwise it is discarded.
8. The winner's pet **heals to full**.

### 9.4 Ladder / session end

- Winners re-pair with other winners, draw a **new environment**, and play again.
- Session ends at **last player standing**, or **most wins** when time is called.
- **Eliminated students** stay engaged via the teacher guide: complete the battle worksheet, referee a match, or join a second-chance bracket.

## 10. Teacher materials

- **Worked example** for each attack type × modifier combination.
- **Fast-marking lookup:** for each simplified form `nx + c`, a table of its value at `x = 1..6`, so a teacher can check a worksheet at a glance.
- **Battle worksheet:** one row per attack — expression built, like terms collected, roll, final damage. This is the gradable artifact.
- **Answer key** for the sample pets/environments in the starter set.

## 11. Differentiation

- **Support:** ignore the environment modifier — only the character `±x` applies.
- **Core:** full rules as written.
- **Extension:** two environment cards per match; larger die (D8/D12); pets with negative constants; the inequality trade-justification.

## 12. Non-goals / YAGNI

- No digital version — physical only.
- No character HP and no character attacks — pets are the only combatants.
- No initiative stat, status effects, or elemental typing beyond the three stats.
- No items, healing, or levelling.
- Extreme pets and formal inequality assessment are **V2 only**.

## 13. Open questions for later specs

**Pets spec:**
- How many distinct pets in the starter set? (enough that a class of ~30 drawing 2 each gets reasonable variety)
- Exact HP values and equation coefficients per archetype
- Do captured pets transfer the physical card, or is it drawn fresh from the box? (affects whether a player can be attritioned below 1 pet before elimination — currently moot since losing = elimination)

**Environments spec:**
- Final list and count of environment cards
- Whether any environment is "neutral" (no modifier) for pacing
- Mapping the original temperature / city / library ideas onto the three-stat model

**Core (revisit after playtest):**
- Trading phase length
- Whether starting zoo size should be 2 or 3

## 14. Build sequence

1. **Core rulebook** (this doc → student rulebook + teacher guide) ← current
2. **Character set** — 7 cards, final flavour, print layout
3. **Environment deck**
4. **Pet collection**

Each subsequent component gets its own design doc in `docs/design/`.
