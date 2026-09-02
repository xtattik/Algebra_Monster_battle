# Algebra Monster Battle — Character Set Design

**Date:** 2026-09-02
**Status:** Draft for review
**Depends on:** [`core-rules.md`](core-rules.md) §6 (character system)
**Scope:** Final content and print layout for the 7 character cards. No rules changes — this doc only fixes flavour, wording, and card format.

---

## 1. Purpose

The core rules doc (§6.2) fixes the 7 characters and their stat lines. This spec turns that table into printable cards: exact on-card wording for each stat effect, a one-line playstyle tip, a flavour line, and a print layout that yields cut-apart playing cards.

Nothing here changes the damage model. If a conflict is found, [`core-rules.md`](core-rules.md) wins and gets a correcting edit.

## 2. What goes on a card

Per core-rules §6.3, each card carries:

1. **Name** and an art area (art is a placeholder box in v1 — teachers or students can draw in it).
2. **The character's three stat tiers** — Magic, Strength, Agility, each shown with:
   - its tier (HIGH / AVERAGE / LOW),
   - its effect in plain words,
   - its `±x` term.
3. **One playstyle line** — how to pilot the character.
4. **One flavour line** — tone only, no rules content.
5. **A card number** (1–7) in the footer, for sorting a class set back into designs.

Only the character's *own* three stats appear — not the full 3×3 grid. A student reads their card, not a matrix.

## 3. Stat-effect wording (canonical)

The `±x` term and the plain-words effect are a pure function of (stat, tier). The card generator owns this table so the wording is identical on every card:

| Stat | Tier | Plain-words effect | Term |
|---|---|---|---|
| Magic | HIGH | your magic attacks gain | `+x` |
| Magic | AVERAGE | your magic attacks are unchanged | `0` |
| Magic | LOW | your magic attacks take | `−x` |
| Agility | HIGH | your agility attacks gain | `+x` |
| Agility | AVERAGE | your agility attacks are unchanged | `0` |
| Agility | LOW | your agility attacks take | `−x` |
| Strength | HIGH | enemy attacks against you take | `−x` |
| Strength | AVERAGE | enemy attacks against you are unchanged | `0` |
| Strength | LOW | enemy attacks against you gain | `+x` |

Notes:
- Strength is **defensive**: a HIGH-Strength card makes the *attacker's* expression `−x`; a LOW-Strength card hands the attacker `+x`. This is **inverted** from Magic/Agility (where HIGH is `+x`), which trips students up. The Strength row is therefore set apart visually so it reads as "the enemy's term, not yours":
  - the whole row sits on a **light red tint**,
  - the tier is tagged **`defence`**,
  - the term is prefixed **`vs you`** and printed in **red**,
  - the effect sentence spells out the direction ("Enemy attacks against you take `−x`").
  None of this changes the maths — the term a student writes on the worksheet is still exactly `−x` / `0` / `+x`. The tint and red are set with `print-color-adjust: exact` so a colour printer keeps them; on a mono photocopy the `vs you` / `defence` labels and the effect sentence still carry the meaning.
- Strike (physical) attacks are never modified by Magic or Agility or the environment — that rule lives in the rulebook, not on the character card, because it is about the *pet's* attack type, not the character.
- The `0` tiers still print a row. Students must write `+ 0` on the worksheet, so the card should not hide the Average stat.

## 4. The 7 characters

Order and stat lines are copied verbatim from core-rules §6.2 (Magic / Strength / Agility). Playstyle and flavour lines are finalised here.

| # | Name | Magic | Strength | Agility |
|---|---|---|---|---|
| 1 | Sorcerer | High | Average | Low |
| 2 | Illusionist | High | Low | Average |
| 3 | Paladin | Average | High | Low |
| 4 | Barbarian | Low | High | Average |
| 5 | Trickster | Average | Low | High |
| 6 | Ranger | Low | Average | High |
| 7 | Bard | Average | Average | Average |

Each character has exactly one High, one Average, one Low — except the Bard (all Average). Every High is matched by a Low somewhere, so no card is strictly stronger than another.

### Playstyle and flavour lines

The authored content (names, tiers, playstyle, flavour) is the source of truth in [`../../cards/characters.md`](../../cards/characters.md). It is reproduced here for review:

1. **Sorcerer** — *Playstyle:* Field high-magic pets and lean on their magic attack; watch the environment, because a Magic-hurt terrain turns your main weapon into `−x`. *Flavour:* Power enough to bend the die — and just enough armour to regret it.
2. **Illusionist** — *Playstyle:* Same big magic as the Sorcerer but paper defence — every enemy attack gets `+x` against you, so end fights before they end you. *Flavour:* Every wound is real. So is every second you waste doubting it.
3. **Paladin** — *Playstyle:* A wall. Enemy attacks take `−x`, so field a durable pet and win the long game while your magic ticks away. *Flavour:* Stand still long enough and the storm has to go around you.
4. **Barbarian** — *Playstyle:* Bruiser. Your magic is `−x`, so field physical-strong pets and swing the strike attack the environment can't touch. *Flavour:* The maths is simple when the answer is always "hit it again".
5. **Trickster** — *Playstyle:* Fast and fragile. Agility attacks gain `+x`, but enemies get `+x` against you — pick agility pets and don't get caught in Blinding Light. *Flavour:* Win the roll, not the fight. There is a difference, and only one of them hurts.
6. **Ranger** — *Playstyle:* Agility specialist with a solid guard. Thrives where Agility is boosted — Deep Shadow is home turf. *Flavour:* Patience, the right ground, and one clean shot.
7. **Bard** — *Playstyle:* No weakness and no spike. Every stat is `0`, so you adapt to any terrain and any pet while sharper builds get countered. *Flavour:* Never the strongest in the room. Often the last one standing.

## 5. Print layout

**File:** [`../../cards/characters.html`](../../cards/characters.html), generated from [`../../cards/characters.md`](../../cards/characters.md) by [`../../tools/gen_cards.py`](../../tools/gen_cards.py).

Requirements:

- **Card size:** 63 mm × 88 mm (standard poker / "bridge-plus" playing card), the size most sleeve and cutter guillotines expect.
- **Page:** A4 portrait, 9 cards per sheet (3 × 3), centred, with a thin cut outline on each card.
- **Print:** black on white plus one spot colour (red) used only on the Strength/defence row. No bleed, no art dependency. The card must still be fully readable if the red drops to grey on a mono copy — the red is reinforcement, never the only signal. The art area is an empty outlined box labelled "art".
- **Self-contained:** one HTML file, inline CSS, no external fonts or images, so "Print to PDF" from any browser produces the deck.
- **Legibility:** stat terms (`+x`, `−x`, `0`) set larger and bold; plain-words effect in a smaller line beneath. The Strength row gets the §3 defensive treatment (tint + `vs you` + `defence` + red term).
- **Class set:** the sheet prints one of each card. To make a class set, print the sheet as many times as needed (the teacher guide already says "multiple copies of each").

The generator must fail loudly (non-zero exit, message to stderr) if `cards/characters.md` contains a stat tier it does not recognise, rather than emitting a card with a blank effect.

## 6. Verification

Before committing:

- [ ] All 7 stat lines match core-rules §6.2 exactly.
- [ ] Each card shows exactly 3 stat rows, in Magic / Strength / Agility order.
- [ ] Each `±x` term matches the §3 table for that (stat, tier) pair.
- [ ] `python tools/gen_cards.py` runs clean and regenerates `cards/characters.html` with no diff when run twice.
- [ ] The HTML prints to 1 page of 9 cards with nothing clipped (checked in a browser print preview).
- [ ] No card contains a bare-number bonus anywhere in its text.
- [ ] The Strength row on every card is visually distinct from Magic/Agility, and still readable with colour disabled.

## 7. Out of scope

- Card backs (v1 is single-sided).
- Real artwork.
- Any new stat, keyword, or per-character special rule — core-rules §12 forbids these.
- Foil/cardstock/production notes — this is print-and-play.
