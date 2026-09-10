# Algebra Monster Battle — Character Set Design

**Date:** 2026-09-02 · **v2 revision:** 2026-09-10
**Status:** Draft for review
**Depends on:** [`core-rules-v2.md`](core-rules-v2.md) §2, §5
**Scope:** Content and print layout for the 7 character cards.
**v2 change:** all three stats are now **offensive and parallel** — each buffs its own attack type (`+x` High / `0` Average / `−x` Low). There is no defence stat, so the Strength row is now identical in format to Magic and Agility (no red / "vs you" / "defence" treatment). Stat *lines* per character are unchanged.

---

## 1. Purpose

The core rules doc (§6.2) fixes the 7 characters and their stat lines. This spec turns that table into printable cards: exact on-card wording for each stat effect, a one-line playstyle tip, a flavour line, and a print layout that yields cut-apart playing cards.

Nothing here changes the damage model. If a conflict is found, [`core-rules.md`](core-rules.md) wins and gets a correcting edit.

## 2. What goes on a card

Per core-rules §6.3, each card carries:

1. **Name** and an art area. With no art file: a printed name header + a dashed placeholder box students can draw in. With an image in `cards/art/characters/` ([`../../cards/art/README.md`](../../cards/art/README.md)): "hero mode" — the image fills the top ~26 mm and the printed name header is dropped (the name is expected to be in the artwork), leaving only a small `N/7` chip.
2. **The character's three stat tiers** — Magic, Strength, Agility, each shown with:
   - its tier (HIGH / AVERAGE / LOW),
   - its effect in plain words,
   - its `±x` term.
3. **One playstyle line** — how to pilot the character.
4. **One flavour line** — tone only, no rules content.
5. **A card number** (1–7), for sorting a class set back into designs — in the header, or overlaid on the art in hero mode.

Only the character's *own* three stats appear — not the full 3×3 grid. A student reads their card, not a matrix.

## 3. Stat-effect wording (canonical)

The `±x` term and the plain-words effect are a pure function of (stat, tier). The card generator owns this table so the wording is identical on every card:

The `±x` term and the plain-words effect are a pure function of (stat, tier), identical in form for all three stats:

| Stat | Tier | Plain-words effect | Term |
|---|---|---|---|
| Magic | HIGH | your magic attacks gain | `+x` |
| Magic | AVERAGE | your magic attacks are unchanged | `0` |
| Magic | LOW | your magic attacks take | `−x` |
| Strength | HIGH | your strength attacks gain | `+x` |
| Strength | AVERAGE | your strength attacks are unchanged | `0` |
| Strength | LOW | your strength attacks take | `−x` |
| Agility | HIGH | your agility attacks gain | `+x` |
| Agility | AVERAGE | your agility attacks are unchanged | `0` |
| Agility | LOW | your agility attacks take | `−x` |

Notes:
- One rule, three identical cases: *what attack am I using → check that one stat.* No defence, no "your opponent's stat affects you" indirection.
- The pet attack type is now **"strength"** (renamed from "strike" in v1) so it matches the stat name.
- The `0` tiers still print a row — students write `+ 0` on the sheet, so Average must not be hidden.

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

1. **Sorcerer** (M-High / S-Avg / A-Low) — *Playstyle:* Lean on magic-attack pets — High Magic makes every cast `+x`. A Cancel: Magic terrain shuts the whole plan down, so keep a non-magic pet in reserve. *Flavour:* Power enough to bend the die. Ask them to swing a sword and watch the confidence drain.
2. **Illusionist** (M-High / S-Low / A-Avg) — *Playstyle:* Huge magic like the Sorcerer, but Low Strength makes your strength attacks `−x` — never plan to win a slugfest. End it with spells. *Flavour:* Every wound is real. So is every second you waste doubting it.
3. **Paladin** (M-Avg / S-High / A-Low) — *Playstyle:* Heavy hitter. High Strength makes strength attacks `+x` — field a big-strike pet and pound it out. Slow, but it lands. *Flavour:* Not fast. Not clever. But when it connects, things fall down.
4. **Barbarian** (M-Low / S-High / A-Avg) — *Playstyle:* Bruiser. Strength attacks `+x`, but Low Magic makes any cast `−x` — a caster pet is wasted on you. *Flavour:* The maths is simple when the answer is always "hit it again".
5. **Trickster** (M-Avg / S-Low / A-High) — *Playstyle:* Fast skirmisher. High Agility gives agility attacks `+x`; Low Strength means you fold in a straight fight — stay on agility. *Flavour:* Win the roll, not the fight. There is a difference, and only one of them hurts.
6. **Ranger** (M-Low / S-Avg / A-High) — *Playstyle:* Agility specialist. Your `+x` is on agility attacks; a magic pet does nothing for you. Fear a Cancel: Agility. *Flavour:* Patience, the right ground, and one clean shot.
7. **Bard** (all Average) — *Playstyle:* Every stat is `0` — no spike, but no weakness. Never hard-countered, never cancelled out. The reliable pick. *Flavour:* Never the strongest in the room. Often the last one standing.

## 5. Print layout

**File:** [`../../cards/characters.html`](../../cards/characters.html), generated from [`../../cards/characters.md`](../../cards/characters.md) by [`../../tools/gen_cards.py`](../../tools/gen_cards.py).

Requirements:

- **Card size:** 63 mm × 88 mm (standard poker / "bridge-plus" playing card), the size most sleeve and cutter guillotines expect.
- **Page:** A4 portrait, 9 cards per sheet (3 × 3), centred, with a thin cut outline on each card.
- **Print:** black on white, no bleed. **v2: no spot colour** — the Strength row is now identical to the others. Art is optional per card (see §2 item 1 and [`../../cards/art/README.md`](../../cards/art/README.md)); with no art the card is fully functional.
- **Self-contained:** one HTML file, inline CSS, no external fonts or images, so "Print to PDF" from any browser produces the deck.
- **Legibility:** stat terms (`+x`, `−x`, `0`) set larger and bold; plain-words effect in a smaller line beneath. All three stat rows use the same format.
- **Class set:** the sheet prints one of each card. To make a class set, print the sheet as many times as needed (the teacher guide already says "multiple copies of each").

The generator must fail loudly (non-zero exit, message to stderr) if `cards/characters.md` contains a stat tier it does not recognise, rather than emitting a card with a blank effect.

## 6. Verification

Before committing:

- [x] All 7 stat lines unchanged from v1 (Magic / Strength / Agility per character).
- [x] Each card shows exactly 3 stat rows in Magic / Strength / Agility order, **all in the same format** (no defence treatment).
- [x] Each `±x` term matches the §3 table — every stat: High `+x`, Average `0`, Low `−x`.
- [x] `python tools/gen_cards.py` (and `--variant female`) run clean and idempotent.
- [ ] Prints to 1 page of 7 cards, nothing clipped (browser print preview).
- [x] No bare-number bonus anywhere.

## 7. Out of scope

- Card backs (v1 is single-sided).
- Real artwork.
- Any new stat, keyword, or per-character special rule — core-rules §12 forbids these.
- Foil/cardstock/production notes — this is print-and-play.
