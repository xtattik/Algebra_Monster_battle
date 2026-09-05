# Challenge Pet Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a second, harder printing of the 22-pet deck — same names, HP, archetype, flavour, and art — where every attack is either an unexpanded bracket (`a(x ± b)`) or a negative-leading coefficient (`−ax + b`), per `docs/design/pets-challenge.md`.

**Architecture:** Both new forms reduce to the same `ax + b` family the game already handles, so the change is contained to `tools/gen_pet_cards.py` (extend the equation parser and generalize the derived fields to work with a possibly-negative `a`) plus a new content file `cards/pets-challenge.md` authored against that parser. A small shared `--variant` CLI helper moves into `tools/cardsheet.py` first, since `gen_pet_cards.py` needs the same plumbing `gen_cards.py` already has for `--variant female`.

**Tech Stack:** Python 3 (no dependencies beyond the existing `tools/cardsheet.py` / optional Pillow). No test framework in this repo — verification is running the generators and diffing/inspecting their output, the same pattern used for every prior tool change here.

---

## File Structure

| File | Change |
|---|---|
| `tools/cardsheet.py` | Add a shared `variant_arg()` helper (Task 1). |
| `tools/gen_cards.py` | Use the shared helper instead of its own copy (Task 1). |
| `tools/gen_pet_cards.py` | Extend the equation grammar (bracket, negative), generalize affinity/range/min-floor logic, add `--variant challenge` (Task 2). |
| `cards/pets-challenge.md` | New — the 22-pet Challenge content (Task 3). |
| `cards/pets-challenge.html` | Generated output (Task 3). |
| `tools/gen_lookup.py` | Extend to also emit negative-coefficient rows (Task 4). |
| `rulebook/answer-key.md` | Add the extended table + Challenge worked examples (Task 4). |
| `rulebook/student-rulebook.md`, `rulebook/teacher-guide.md` | Add a short "Challenge Mode" note (Task 4). |
| `docs/design/core-rules.md` | Update §11 and §14 pointers (Task 5). |
| `README.md` | Build status (Task 5). |

---

## Task 1: Shared `--variant` CLI helper

**Files:**
- Modify: `tools/cardsheet.py` (add a function after `slug()`, currently ending at line 53)
- Modify: `tools/gen_cards.py:22-41`

- [ ] **Step 1: Add `variant_arg()` to cardsheet.py**

In `tools/cardsheet.py`, immediately after the `slug()` function (after this existing block):

```python
def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
```

insert:

```python


def variant_arg(prog: str, allowed: set) -> str | None:
    """Parse --variant NAME / --variant=NAME from argv. `allowed` is a set of
    legal values including None for "no variant". Dies with a clear message
    if the value given isn't recognized.
    """
    argv = sys.argv[1:]
    val = None
    for i, a in enumerate(argv):
        if a == "--variant" and i + 1 < len(argv):
            val = argv[i + 1]
            break
        if a.startswith("--variant="):
            val = a.split("=", 1)[1]
            break
    if val not in allowed:
        names = ", ".join(repr(v) for v in sorted(x for x in allowed if x is not None))
        die(prog, f"unknown --variant {val!r} (expected: {names})")
    return val
```

`sys` is already imported at the top of `cardsheet.py` (line 11) — no new import needed.

- [ ] **Step 2: Migrate gen_cards.py to the shared helper**

In `tools/gen_cards.py`, replace this block:

```python
import sys

import cardsheet
from cardsheet import MINUS, ROOT, die, esc

PROG = "gen_cards"
SRC = ROOT / "cards" / "characters.md"

VARIANTS = {
    None: ("characters", ROOT / "cards" / "characters.html", ""),
    "female": ("characters/female", ROOT / "cards" / "characters-female.html", " (Female Art)"),
}


def _variant_arg() -> str | None:
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--variant" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--variant="):
            return a.split("=", 1)[1]
    return None


VARIANT = _variant_arg()
if VARIANT not in VARIANTS:
    die(PROG, f"unknown --variant {VARIANT!r} (expected: {', '.join(v for v in VARIANTS if v)})")
ART_DECK, OUT, TITLE_SUFFIX = VARIANTS[VARIANT]
```

with:

```python
import cardsheet
from cardsheet import MINUS, ROOT, die, esc

PROG = "gen_cards"
SRC = ROOT / "cards" / "characters.md"

VARIANTS = {
    None: ("characters", ROOT / "cards" / "characters.html", ""),
    "female": ("characters/female", ROOT / "cards" / "characters-female.html", " (Female Art)"),
}

VARIANT = cardsheet.variant_arg(PROG, set(VARIANTS))
ART_DECK, OUT, TITLE_SUFFIX = VARIANTS[VARIANT]
```

(`import sys` is dropped — nothing else in the file uses it.)

- [ ] **Step 3: Verify both character sheets are unchanged**

```bash
cd "C:/Code Projects/Algebra_Monster_Battle"
python tools/gen_cards.py --stdout > /tmp/characters_before.html
python tools/gen_cards.py --variant female --stdout > /tmp/characters_female_before.html
```

Run those two commands **before** making the edit (if not already captured), then after Steps 1–2:

```bash
python tools/gen_cards.py --stdout > /tmp/characters_after.html
python tools/gen_cards.py --variant female --stdout > /tmp/characters_female_after.html
diff /tmp/characters_before.html /tmp/characters_after.html
diff /tmp/characters_female_before.html /tmp/characters_female_after.html
```

Expected: both `diff` commands print nothing (byte-identical output — this was a pure refactor).

Also confirm the error path still works:

```bash
python tools/gen_cards.py --variant bogus
```

Expected: exits non-zero, prints `gen_cards: unknown --variant 'bogus' (expected: 'female')`.

- [ ] **Step 4: Commit**

```bash
git add tools/cardsheet.py tools/gen_cards.py
git commit -m "Share --variant CLI parsing between card generators"
```

---

## Task 2: Extend gen_pet_cards.py for bracket and negative-coefficient attacks

**Files:**
- Modify: `tools/gen_pet_cards.py` (full-file replacement — nearly every function changes)

- [ ] **Step 1: Replace the full contents of `tools/gen_pet_cards.py`**

```python
# tools/gen_pet_cards.py — build the printable pet-card sheet.
#
# Reads cards/pets.md (or cards/pets-challenge.md with --variant challenge)
# and writes cards/pets.html / cards/pets-challenge.html (A4, 9-up,
# 63 mm x 88 mm cards). Shared page/CSS/CLI live in tools/cardsheet.py.
#
# Each pet has HP, an archetype, and three attack equations (magic / strike /
# agility). Core pets use plain `ax + b`. Challenge pets (--variant challenge)
# may also use an unexpanded bracket `a(x + b)` / `a(x - b)`, or a negative
# leading coefficient `-ax + b` — both still reduce to the same `ax + b`
# family, so every derived value (affinity, damage range, the `(min 1)`
# floor) is computed from that reduced (a, b) pair regardless of which form
# was authored. Only the printed equation preserves the authored form.
#
# Usage:
#   python tools/gen_pet_cards.py                     # regenerate cards/pets.html
#   python tools/gen_pet_cards.py --variant challenge  # regenerate cards/pets-challenge.html
#   python tools/gen_pet_cards.py --check              # exit 1 if the file is out of date
#   python tools/gen_pet_cards.py --stdout             # print the HTML instead of writing it
#   python tools/gen_pet_cards.py --table              # print the fast-marking table (Markdown)
import re
import sys

import cardsheet
from cardsheet import MINUS, ROOT, die, esc

PROG = "gen_pet_cards"

ATTACKS = ("Magic", "Strike", "Agility")
REQUIRED = ("HP",) + ("Archetype",) + ATTACKS + ("Flavour",)

# archetype -> (min HP, max HP) — identical for Core and Challenge, so a
# Challenge card is a drop-in swap for its Core counterpart.
BANDS = {"Glass cannon": (26, 32), "Baseline": (44, 54), "Tank": (76, 84)}

PLAIN_RE = re.compile(r"^([123]?)x(?:\s*([+-])\s*([0-3]))?(?:\s*\(min\s*(\d+)\))?$")
BRACKET_RE = re.compile(r"^([23])\(x\s*([+-])\s*([12])\)(?:\s*\(min\s*(\d+)\))?$")
NEGATIVE_RE = re.compile(r"^-([123]?)x(?:\s*([+-])\s*(\d{1,2}))?(?:\s*\(min\s*(\d+)\))?$")

VARIANTS = {
    None: (ROOT / "cards" / "pets.md", ROOT / "cards" / "pets.html", "", {"plain"}, False),
    "challenge": (
        ROOT / "cards" / "pets-challenge.md", ROOT / "cards" / "pets-challenge.html",
        " — Challenge", {"plain", "bracket", "negative"}, True,
    ),
}

VARIANT = cardsheet.variant_arg(PROG, set(VARIANTS))
SRC, OUT, TITLE_SUFFIX, ALLOWED_FORMS, REQUIRE_BOTH_HARD_FORMS = VARIANTS[VARIANT]

EXTRA_CSS = """\
    .pethdr { display: flex; align-items: baseline; gap: 2.4mm; margin-top: 0.6mm; }
    .hp { font-size: 15pt; font-weight: 800; letter-spacing: -0.3pt; }
    .hp span { font-size: 6.5pt; font-weight: 600; color: #555; letter-spacing: 0.4pt; }
    .arch { font-size: 6.6pt; text-transform: uppercase; letter-spacing: 0.4pt; color: #444; }
    .atk { margin-bottom: 1.9mm; }
    .atk-head { display: flex; align-items: baseline; gap: 1.4mm; }
    .atk-type {
      font-size: 6.3pt; text-transform: uppercase; letter-spacing: 0.5pt;
      color: #777; width: 11mm; flex: none;
    }
    .atk-name { font-size: 8pt; font-weight: 700; flex: 1; }
    .atk-eqn {
      font-family: "Cambria Math", "Times New Roman", Georgia, serif;
      font-size: 10.5pt; font-weight: 700; white-space: nowrap;
    }
    .atk-sub {
      font-size: 6pt; color: #888; text-align: right; margin: 0.2mm 0 0;
      padding-left: 12.4mm;
    }
    .atk-sub .min { color: #b3261e; font-weight: 600; }
"""


def fmt_plain(a: int, b: int) -> str:
    coef = f"{a}x" if a != 1 else "x"
    if b == 0:
        return coef
    return f"{coef} {'+' if b > 0 else MINUS} {abs(b)}"


def parse_eqn(prog_tag: str, raw: str):
    s = raw.strip().replace(MINUS, "-").replace("\u2013", "-")
    s = re.sub(r"\s+", " ", s)

    m = BRACKET_RE.match(s)
    if m:
        form = "bracket"
        coef = int(m.group(1))
        sign = 1 if m.group(2) == "+" else -1
        inner_b = int(m.group(3))
        a, b = coef, sign * coef * inner_b
        display = f"{coef}(x {'+' if sign > 0 else MINUS} {inner_b})"
    else:
        m = NEGATIVE_RE.match(s)
        if m:
            form = "negative"
            coef = int(m.group(1)) if m.group(1) else 1
            a = -coef
            b = 0
            if m.group(2):
                b = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
            coef_str = "" if coef == 1 else str(coef)
            display = f"{MINUS}{coef_str}x"
            if b:
                display += f" {'+' if b > 0 else MINUS} {abs(b)}"
        else:
            m = PLAIN_RE.match(s)
            if not m:
                die(PROG, f"{prog_tag}: cannot parse equation {raw!r} "
                          f"(expected e.g. '3x + 2', '3(x - 1)', or '-3x + 10')")
            form = "plain"
            a = int(m.group(1)) if m.group(1) else 1
            b = 0
            if m.group(2):
                b = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
            display = fmt_plain(a, b)

    if form not in ALLOWED_FORMS:
        die(PROG, f"{prog_tag}: {raw!r} uses the {form} form, not allowed for "
                  f"--variant {VARIANT!r} (expected: {', '.join(sorted(ALLOWED_FORMS))})")

    printed_min = int(m.group(4)) if m.group(4) else None
    values = [a * x + b for x in range(1, 7)]
    needs_min = min(values) < 1
    if needs_min and printed_min is None:
        die(PROG, f"{prog_tag}: {raw!r} can deal < 1 somewhere in rolls 1-6 — add '(min 1)'")
    if not needs_min and printed_min is not None:
        die(PROG, f"{prog_tag}: {raw!r} never drops below 1 — remove the spurious '(min {printed_min})'")
    if needs_min and printed_min != 1:
        die(PROG, f"{prog_tag}: {raw!r} floor must be '(min 1)', not '(min {printed_min})'")

    return {
        "a": a, "b": b, "form": form, "min": printed_min, "display": display,
        "at1": max(1, values[0]), "at6": max(1, values[5]),
    }


def affinity(attacks: dict) -> str:
    top = max(abs(e["a"]) for e in attacks.values())
    leaders = [t for t in ATTACKS if abs(attacks[t]["a"]) == top]
    return leaders[0] if len(leaders) == 1 else "Balanced"


def render_card(pet: dict, total: int) -> str:
    rows = []
    for t in ATTACKS:
        e = pet["attacks"][t]
        sub = f"rolls {e['at1']}{MINUS}{e['at6']}"
        if e["min"] is not None:
            sub = f'<span class="min">min 1</span> &middot; {sub}'
        rows.append(
            f'      <div class="atk">\n'
            f'        <div class="atk-head">'
            f'<span class="atk-type">{t}</span>'
            f'<span class="atk-name">{esc(pet["names"][t])}</span>'
            f'<span class="atk-eqn">{e["display"]}</span></div>\n'
            f'        <div class="atk-sub">{sub}</div>\n'
            f'      </div>'
        )
    pethdr = (
        f'<div class="pethdr"><span class="hp">{pet["hp"]}<span> HP</span></span>'
        f'<span class="arch">{esc(pet["archetype"])} &middot; {pet["affinity"]}</span></div>'
    )
    return (
        f'    <div class="card">\n'
        + cardsheet.card_top("pets", pet["num"], total, pet["name"], PROG, subhead=pethdr) + "\n"
        + "\n".join(rows) + "\n"
        f'      <p class="flavour">{esc(pet["flavour"])}</p>\n'
        f'    </div>'
    )


def build_pets(blocks: list[dict]) -> list[dict]:
    pets = []
    for b in blocks:
        f = b["fields"]
        tag = f"card {b['num']} ({b['name']})"
        missing = [k for k in REQUIRED if k not in f]
        if missing:
            die(PROG, f"{tag} is missing: {', '.join(missing)}")

        if f["Archetype"] not in BANDS:
            die(PROG, f"{tag}: unknown archetype {f['Archetype']!r} "
                      f"(expected {', '.join(BANDS)})")
        try:
            hp = int(f["HP"])
        except ValueError:
            die(PROG, f"{tag}: HP {f['HP']!r} is not an integer")
        lo, hi = BANDS[f["Archetype"]]
        if not lo <= hp <= hi:
            die(PROG, f"{tag}: HP {hp} outside the {f['Archetype']} band {lo}–{hi}")

        names, attacks = {}, {}
        for t in ATTACKS:
            if "|" not in f[t]:
                die(PROG, f"{tag}: {t} line must be '<name> | <equation>'")
            nm, eq = (p.strip() for p in f[t].split("|", 1))
            if not nm:
                die(PROG, f"{tag}: {t} attack has no name")
            names[t] = nm
            attacks[t] = parse_eqn(f"{tag} {t}", eq)

        if REQUIRE_BOTH_HARD_FORMS:
            forms = {attacks[t]["form"] for t in ATTACKS}
            if not {"bracket", "negative"} <= forms:
                die(PROG, f"{tag}: needs at least one bracket and one negative-coefficient "
                          f"attack among Magic/Strike/Agility (got: {', '.join(sorted(forms))})")

        pets.append({
            "num": b["num"], "name": b["name"], "hp": hp,
            "archetype": f["Archetype"], "names": names, "attacks": attacks,
            "affinity": affinity(attacks), "flavour": f["Flavour"],
        })
    return pets


def build_html(blocks: list[dict]) -> str:
    pets = build_pets(blocks)
    total = len(pets)
    body = "\n".join(render_card(p, total) for p in pets)
    pages = -(-total // 9)
    hint = (
        "Generated by <code>tools/gen_pet_cards.py"
        + (f" --variant {VARIANT}" if VARIANT else "") + "</code> from "
        f"<code>{SRC.relative_to(ROOT).as_posix()}</code> — do not edit by hand. "
        f"Print to PDF (A4, 100% scale); {total} cards over {pages} pages. "
        "Print about 3 copies of the sheet for a class of 30 (each student draws 2 pets)."
    )
    return cardsheet.document(f"Algebra Monster Battle — Pet Cards{TITLE_SUFFIX}", EXTRA_CSS, hint, body)


def print_table(blocks: list[dict]) -> None:
    pets = build_pets(blocks)
    print("| Pet · attack | eqn | 1 | 2 | 3 | 4 | 5 | 6 |")
    print("|---|---|---|---|---|---|---|---|")
    for p in pets:
        for t in ATTACKS:
            e = p["attacks"][t]
            label = e["display"] + (" (min 1)" if e["min"] else "")
            vals = " | ".join(str(max(1, e["a"] * x + e["b"])) for x in range(1, 7))
            print(f"| {p['name']} · {p['names'][t]} | `{label}` | {vals} |")


if __name__ == "__main__":
    if "--table" in sys.argv[1:]:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
        print_table(cardsheet.parse_blocks(SRC.read_text(encoding="utf-8"), PROG))
    else:
        cardsheet.run(PROG, SRC, OUT, build_html)
```

- [ ] **Step 2: Verify Core pet output is byte-identical**

Before this change, capture a baseline (if not already done):

```bash
cd "C:/Code Projects/Algebra_Monster_Battle"
python tools/gen_pet_cards.py --stdout > /tmp/pets_before.html
python tools/gen_pet_cards.py --table > /tmp/pets_table_before.md
```

After Step 1:

```bash
python tools/gen_pet_cards.py --stdout > /tmp/pets_after.html
python tools/gen_pet_cards.py --table > /tmp/pets_table_after.md
diff /tmp/pets_before.html /tmp/pets_after.html
diff /tmp/pets_table_before.md /tmp/pets_table_after.md
```

Expected: both `diff`s print nothing. `cards/pets.md` only authors the `plain` form, so nothing about Core's output should change — this proves the refactor is behavior-preserving for Core.

- [ ] **Step 3: Verify the new forms parse correctly (ad hoc, no content file needed yet)**

```bash
python -c "
import sys
sys.path.insert(0, 'tools')
sys.argv = ['x']
import gen_pet_cards as g

# Simulate variant=challenge's allowed forms directly for this smoke test.
g.ALLOWED_FORMS = {'plain', 'bracket', 'negative'}

cases = [
    ('3(x + 1)', 3, 3, 'bracket', None),
    ('3(x - 1) (min 1)', 3, -3, 'bracket', 1),
    ('2(x + 1)', 2, 2, 'bracket', None),
    ('2(x - 1) (min 1)', 2, -2, 'bracket', 1),
    ('-x + 5 (min 1)', -1, 5, 'negative', 1),
    ('-2x + 8 (min 1)', -2, 8, 'negative', 1),
    ('-3x + 10 (min 1)', -3, 10, 'negative', 1),
]
for raw, a, b, form, mn in cases:
    e = g.parse_eqn('test', raw)
    assert e['a'] == a, (raw, e)
    assert e['b'] == b, (raw, e)
    assert e['form'] == form, (raw, e)
    assert e['min'] == mn, (raw, e)
print('all 7 templates parse correctly')
"
```

Expected: `all 7 templates parse correctly`. If any `assert` fails, the traceback names which template and field is wrong — fix `parse_eqn` before continuing.

- [ ] **Step 4: Verify the affinity generalization**

```bash
python -c "
import sys
sys.path.insert(0, 'tools')
sys.argv = ['x']
import gen_pet_cards as g

g.ALLOWED_FORMS = {'plain', 'bracket', 'negative'}
attacks = {
    'Magic': g.parse_eqn('t', '-3x + 10 (min 1)'),   # |a| = 3
    'Strike': g.parse_eqn('t', '2(x - 1) (min 1)'),  # |a| = 2
    'Agility': g.parse_eqn('t', '-x + 5 (min 1)'),   # |a| = 1
}
assert g.affinity(attacks) == 'Magic', g.affinity(attacks)
print('affinity-by-magnitude OK')
"
```

Expected: `affinity-by-magnitude OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/gen_pet_cards.py
git commit -m "Extend gen_pet_cards.py with bracket and negative-coefficient forms"
```

---

## Task 3: Author the Challenge pet content

**Files:**
- Create: `cards/pets-challenge.md`
- Create (generated): `cards/pets-challenge.html`

- [ ] **Step 1: Write `cards/pets-challenge.md`**

```markdown
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
```

- [ ] **Step 2: Generate the Challenge sheet and confirm it validates cleanly**

```bash
cd "C:/Code Projects/Algebra_Monster_Battle"
python tools/gen_pet_cards.py --variant challenge
```

Expected: `wrote cards\pets-challenge.html (22 cards)` (or `cards/pets-challenge.html` on non-Windows) — no `die()` errors. If any pet trips the "needs at least one bracket and one negative" check or a `(min 1)` mismatch, the error names the exact card and attack — fix that row in `cards/pets-challenge.md` and rerun.

- [ ] **Step 3: Confirm Core is still unaffected**

```bash
python tools/gen_pet_cards.py --check
```

Expected: `cards\pets.html is up to date (22 cards)` — proves adding the Challenge content file didn't touch Core's own output.

- [ ] **Step 4: Spot-check the design doc's worked ceiling numbers against the generated table**

```bash
python tools/gen_pet_cards.py --variant challenge --table 2>&1 | head -5
```

Confirm the Emberwisp Magic row reads `3(x + 1)` with values `6 | 9 | 12 | 15 | 18 | 21` (matches design doc §5's B3 row and the `docs/design/pets-challenge.md` §4 template table). Confirm the Sparkhound Magic row reads `-3x + 10 (min 1)` with values `7 | 4 | 1 | 1 | 1 | 1` (matches §4's N3 row exactly).

- [ ] **Step 5: Commit**

```bash
git add cards/pets-challenge.md cards/pets-challenge.html
git commit -m "Author the 22-pet Challenge deck"
```

---

## Task 4: Extend the answer key and add the Challenge Mode rulebook note

**Files:**
- Modify: `tools/gen_lookup.py`
- Modify: `rulebook/answer-key.md`
- Modify: `rulebook/student-rulebook.md`
- Modify: `rulebook/teacher-guide.md`

- [ ] **Step 1: Read the current `tools/gen_lookup.py` and `rulebook/answer-key.md` §2 before editing**

```bash
cat "C:/Code Projects/Algebra_Monster_Battle/tools/gen_lookup.py"
```

Confirm its current signature (as of the core rulebook build): a `main()` with no parameters, hardcoded `ns = range(1, 7)`, `cs = range(-3, 4)`, `xs = range(1, 7)`, printing one Markdown table.

- [ ] **Step 2: Parameterize `gen_lookup.py` and add a Challenge table**

Replace the body of `tools/gen_lookup.py` with:

```python
# tools/gen_lookup.py — emits fast-marking tables as Markdown.
# Usage: python tools/gen_lookup.py > lookup.md  then paste the body in.
import sys


def emit_table(ns, cs, xs=range(1, 7)) -> None:
    header = "| expr | " + " | ".join(f"x={x}" for x in xs) + " |"
    sep = "|" + "---|" * (len(list(xs)) + 1)
    print(header)
    print(sep)
    for n in ns:
        for c in cs:
            sign = "" if c == 0 else (f" + {c}" if c > 0 else f" − {abs(c)}")
            label = f"{n}x{sign}" if n >= 0 else f"−{abs(n)}x{sign}"
            vals = [max(0, n * x + c) for x in xs]
            print(f"| {label} | " + " | ".join(str(v) for v in vals) + " |")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    print("### Core (n = 1x .. 6x)")
    print()
    emit_table(range(1, 7), range(-3, 4))
    print()
    print("### Challenge negative-coefficient rows (n = -1x .. -3x)")
    print()
    emit_table(range(-1, -4, -1), (5, 8, 10))


if __name__ == "__main__":
    main()
```

The Challenge table only covers the three constants (`5, 8, 10`) the §4 templates in `docs/design/pets-challenge.md` actually use, combined with modifier shifts of `±1, ±2, ±3` on the coefficient — matching the same "small curated set, not every integer" discipline Core's own table used.

- [ ] **Step 3: Run it and verify**

```bash
cd "C:/Code Projects/Algebra_Monster_Battle"
python tools/gen_lookup.py | head -10
python tools/gen_lookup.py | tail -15
```

Confirm the Core section's first data row is still `| 1x − 3 | 0 | 0 | 0 | 1 | 2 | 3 |` (unchanged from before), and the new Challenge section includes a row `| −3x + 10 | 7 | 4 | 1 | 0 | 0 | 0 |`. Hand-check that row: `−3(1)+10=7`, `−3(2)+10=4`, `−3(3)+10=1`, `−3(4)+10=−2→0`, `−3(5)+10=−5→0`, `−3(6)+10=−8→0`. Matches.

- [ ] **Step 4: Update `rulebook/answer-key.md`**

Read the current file first:

```bash
cat "C:/Code Projects/Algebra_Monster_Battle/rulebook/answer-key.md"
```

At the end of its existing §2 ("Lookup table") section — after the closing note that currently reads something like *"Generated by `tools/gen_lookup.py` (42 rows). Re-run `python tools/gen_lookup.py` to regenerate if the modifier ranges ever change."* — insert a new subsection:

```markdown
### 2a. Challenge deck — negative-coefficient rows

The Challenge pet deck (`cards/pets-challenge.md`) adds attacks with a
**negative** leading coefficient — damage that *shrinks* as the roll grows.
Once a student has collected like terms, these still resolve to a single
`nx + c`, just with `n` possibly negative. Use this table exactly like §2,
but note the roll-1 column is now usually the *biggest* number, not the
smallest.

| expr | x=1 | x=2 | x=3 | x=4 | x=5 | x=6 |
|---|---|---|---|---|---|---|
| −1x + 5 | 4 | 3 | 2 | 1 | 0 | 0 |
| −1x + 8 | 7 | 6 | 5 | 4 | 3 | 2 |
| −1x + 10 | 9 | 8 | 7 | 6 | 5 | 4 |
| −2x + 5 | 3 | 1 | 0 | 0 | 0 | 0 |
| −2x + 8 | 6 | 4 | 2 | 0 | 0 | 0 |
| −2x + 10 | 8 | 6 | 4 | 2 | 0 | 0 |
| −3x + 5 | 2 | 0 | 0 | 0 | 0 | 0 |
| −3x + 8 | 5 | 2 | 0 | 0 | 0 | 0 |
| −3x + 10 | 7 | 4 | 1 | 0 | 0 | 0 |

Generated by `python tools/gen_lookup.py` alongside §2 (see its Challenge
section). Bracket-form Challenge attacks (`a(x ± b)`) expand to the *same*
`ax + b` family as Core — once a student expands the bracket, mark them
against the §2 table exactly as normal.
```

- [ ] **Step 5: Add a "Challenge Mode" note to `rulebook/student-rulebook.md`**

Read the file first to find its final section (currently "## 9. The ladder"), then append after it:

```markdown

## 10. Challenge Mode (optional)

Some pets come in a **Challenge** version (`cards/pets-challenge.html`) —
same pet, same HP, same art, but harder attacks. Everything above still
applies. Two new things you'll see on a Challenge card:

**A bracket you have to expand first**, e.g. `3(x − 1)`. Multiply it out
before you do anything else: `3(x − 1) = 3x − 3`. Then carry on exactly as
in section 6 — add your modifiers, collect like terms, substitute your roll.

**A negative coefficient**, e.g. `−3x + 10`. This attack gets *weaker* as
your roll gets *better* — a 1 might deal 7, a 6 might floor at the attack's
minimum of 1. Watch what a modifier does to it: your own `+x` buff doesn't
make a negative-coefficient attack hit harder — it partially cancels the
negative coefficient instead. Work it out term by term and you won't be
caught out.

**Worked example (bracket).** Base attack `3(x − 1)`, you have High Magic
(`+x`), the environment boosts Magic (`+x`), enemy is Average Strength
(`+0`).

- Expand first: `3(x − 1) = 3x − 3`
- Add modifiers: `3x − 3 + x + x + 0`
- Collect like terms: `5x − 3`
- Roll a 4: `5 × 4 − 3 = 17`

**Worked example (negative coefficient).** Base attack `−3x + 10`, you have
High Magic (`+x`), the environment boosts Magic (`+x`), enemy is Average
Strength (`+0`).

- Add modifiers straight away (no expansion needed): `−3x + 10 + x + x + 0`
- Collect like terms: `−x + 10`
- Roll a 4: `−4 + 10 = 6`
- Roll a 1 instead: `−1 + 10 = 9` — a *worse* roll deals *more* damage here.
```

- [ ] **Step 6: Add a short paragraph to `rulebook/teacher-guide.md`**

Read the file first to find its final section (currently "## 9. Answer key"), then append after it:

```markdown

## 10. Challenge Mode (optional)

`cards/pets-challenge.html` is a drop-in swap for the pet deck — same 22
pets, same HP, same art — where every attack is either an unexpanded
bracket (`3(x − 1)`) or a negative leading coefficient (`−3x + 10`). Hand it
to pairs who are breezing through the standard deck; it needs no extra setup
and no rule changes anywhere else. Full design and balance reasoning:
`docs/design/pets-challenge.md`.

Mark it exactly as in §9, using `rulebook/answer-key.md` §2a for the
negative-coefficient rows. The two worked examples in the student rulebook's
"Challenge Mode" section are the ones to walk through if a table gets stuck.
```

- [ ] **Step 7: Commit**

```bash
git add tools/gen_lookup.py rulebook/answer-key.md rulebook/student-rulebook.md rulebook/teacher-guide.md
git commit -m "Extend the answer key and rulebooks for Challenge Mode"
```

---

## Task 5: Update core-rules.md and README, final consistency pass

**Files:**
- Modify: `docs/design/core-rules.md` (§11, §14)
- Modify: `README.md`

- [ ] **Step 1: Update core-rules.md §11**

Find this line (currently in §11 "Differentiation"):

```markdown
- **Extension:** two environment cards per match; larger die (D8/D12); pets with negative constants; the inequality trade-justification.
```

Replace it with:

```markdown
- **Extension:** two environment cards per match; larger die (D8/D12); the **Challenge pet deck** (`docs/design/pets-challenge.md`) — unexpanded brackets and negative leading coefficients on every attack, same HP/art/names as Core; the inequality trade-justification.
```

- [ ] **Step 2: Update core-rules.md §14**

Find:

```markdown
## 14. Build sequence

1. **Core rulebook** (this doc → student rulebook + teacher guide) — done
2. **Character set** — 7 cards ([`characters.md`](characters.md)) — done
3. **Environment deck** — 8 cards ([`environments.md`](environments.md)) — done
4. **Pet collection** — 22 pets ([`pets.md`](pets.md)) — done

All phase-1 and phase-2 components are drafted. Next: playtest, then act on the open questions in §13.
```

Replace with:

```markdown
## 14. Build sequence

1. **Core rulebook** (this doc → student rulebook + teacher guide) — done
2. **Character set** — 7 cards ([`characters.md`](characters.md)) — done
3. **Environment deck** — 8 cards ([`environments.md`](environments.md)) — done
4. **Pet collection** — 22 pets ([`pets.md`](pets.md)) — done
5. **Challenge pet deck** — same 22 pets, harder attacks ([`pets-challenge.md`](pets-challenge.md)) — done

All phase-1 and phase-2 components are drafted. Next: playtest, then act on the open questions in §13.
```

- [ ] **Step 3: Update README.md**

Read the current README:

```bash
cat "C:/Code Projects/Algebra_Monster_Battle/README.md"
```

In its "Build status" checklist, add a line for the Challenge deck (placed after the pet-collection line):

```markdown
- [x] Challenge pet deck — same 22 pets, harder attacks ([`docs/design/pets-challenge.md`](docs/design/pets-challenge.md))
```

If the README has a components list mentioning `cards/pets.html`, add `cards/pets-challenge.html` alongside it with a one-line description ("optional harder attacks — same pets, same art").

- [ ] **Step 4: Full regeneration + consistency pass**

```bash
cd "C:/Code Projects/Algebra_Monster_Battle"
python tools/gen_cards.py --check
python tools/gen_cards.py --variant female --check
python tools/gen_env_cards.py --check
python tools/gen_pet_cards.py --check
python tools/gen_pet_cards.py --variant challenge --check
python tools/gen_lookup.py > /tmp/lookup_final.md
```

Expected: all five `--check` calls report "up to date", nothing exits non-zero. Skim `/tmp/lookup_final.md` for both sections present.

Re-verify the two design-doc claims that gate this task:

- **§5 ceiling:** `3(x+1)` (Emberwisp's Magic) + character High `+x` + environment boost `+x` → `5x+3` → roll 6 → 33. Confirm: `5*6+3 == 33`.
- **§5 negative-attack floor:** `−3x+10` (Sparkhound's Magic) with environment hinder `−x` and enemy High Strength `−x` → `−5x+10` → roll 6 → `−20`, floors to 0 post-modifier (not the base attack's own `(min 1)`, which only applies before modifiers). Confirm: `-5*6+10 == -20`.

- [ ] **Step 5: Commit**

```bash
git add docs/design/core-rules.md README.md
git commit -m "Point core-rules.md and README at the Challenge pet deck"
```

- [ ] **Step 6: Push**

```bash
git push
```

---

## Self-Review (completed by plan author)

**Spec coverage** — `docs/design/pets-challenge.md` sections mapped to tasks:
- §2 (the two forms) → Task 2 (parser)
- §3 (floor generalization, modifier-softens-negative) → Task 2 (floor logic) + Task 4 (rulebook worked examples make the softening explicit)
- §4 (template pool, archetype guidance) → Task 3 (all 7 templates used; every pet has ≥1 bracket + ≥1 negative; glass-cannon/baseline/tank affinity slots follow the guidance)
- §5 (balance check) → Task 5 Step 4 (both worked numbers reproduced and asserted)
- §6 (what doesn't change) → no task needed; nothing else is touched, confirmed by Task 1/2's byte-identical diffs and Task 3 Step 3's `--check` on Core
- §7 (tooling) → Tasks 1–3
- §8 (answer key) → Task 4
- §9 (doc changes) → Task 4 (rulebooks) + Task 5 (core-rules.md, README)
- §10 (verification checklist) → covered across Task 2 Steps 3–4, Task 3 Steps 2–4, Task 5 Step 4
- §11 (out of scope) → nothing in this plan touches indices, characters, environments, or art — confirmed by the file list only ever naming pet-deck files

**Placeholder scan:** every step has literal, runnable content — the full replacement source for `gen_pet_cards.py`, the full 22-pet Markdown content, the full `gen_lookup.py` body, and literal text for every doc insertion. No "TBD"/"fill in".

**Type consistency:** `parse_eqn` returns keys `a, b, form, min, display, at1, at6` — `render_card`, `print_table`, `affinity`, and `build_pets` all read exactly those keys and no others across every task. `VARIANT`, `SRC`, `OUT`, `TITLE_SUFFIX`, `ALLOWED_FORMS`, `REQUIRE_BOTH_HARD_FORMS` are unpacked once from `VARIANTS[VARIANT]` and used consistently through `build_html`/`build_pets`.
