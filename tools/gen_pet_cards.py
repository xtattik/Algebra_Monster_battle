# tools/gen_pet_cards.py — build the printable pet-card sheet.
#
# Reads cards/pets.md and writes cards/pets.html (A4, 9-up, 63 mm x 88 mm cards;
# 12 pets => 2 pages). Shared page/CSS/CLI live in tools/cardsheet.py.
#
# Each pet has HP, an archetype, and three attack equations (magic / strike /
# agility), each `ax + b` with `(min 1)` where a roll of 1 would deal < 1.
# Affinity, the min badge, and the 1..6 damage range are derived here.
#
# Usage:
#   python tools/gen_pet_cards.py            # regenerate cards/pets.html
#   python tools/gen_pet_cards.py --check    # exit 1 if the file is out of date
#   python tools/gen_pet_cards.py --stdout   # print the HTML instead of writing it
#   python tools/gen_pet_cards.py --table    # print the fast-marking table (Markdown)
import re
import sys

import cardsheet
from cardsheet import MINUS, ROOT, die, esc

PROG = "gen_pet_cards"
SRC = ROOT / "cards" / "pets.md"
OUT = ROOT / "cards" / "pets.html"

ATTACKS = ("Magic", "Strike", "Agility")
REQUIRED = ("HP",) + ("Archetype",) + ATTACKS + ("Flavour",)

# archetype -> (min HP, max HP)
BANDS = {"Glass cannon": (26, 32), "Baseline": (44, 54), "Tank": (76, 84)}

EQN_RE = re.compile(r"^([123]?)x(?:\s*([+-])\s*([0-3]))?(?:\s*\(min\s*(\d+)\))?$")

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


def parse_eqn(prog_tag: str, raw: str):
    s = raw.strip().replace(MINUS, "-").replace("–", "-")
    s = re.sub(r"\s+", " ", s)
    m = EQN_RE.match(s)
    if not m:
        die(PROG, f"{prog_tag}: cannot parse equation {raw!r} (expected e.g. '3x + 2' or 'x - 1 (min 1)')")
    a = int(m.group(1)) if m.group(1) else 1
    b = 0
    if m.group(2):
        b = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
    printed_min = int(m.group(4)) if m.group(4) else None
    needs_min = a + b < 1
    if needs_min and printed_min is None:
        die(PROG, f"{prog_tag}: {raw!r} can deal < 1 at a roll of 1 — add '(min 1)'")
    if not needs_min and printed_min is not None:
        die(PROG, f"{prog_tag}: {raw!r} never drops below 1 — remove the spurious '(min {printed_min})'")
    if needs_min and printed_min != 1:
        die(PROG, f"{prog_tag}: {raw!r} floor must be '(min 1)', not '(min {printed_min})'")
    return {"a": a, "b": b, "min": printed_min, "low": max(1, a + b), "high": a * 6 + b}


def fmt_eqn(e: dict) -> str:
    if e["b"] == 0:
        core = f"{e['a']}x" if e["a"] != 1 else "x"
    else:
        coef = f"{e['a']}x" if e["a"] != 1 else "x"
        core = f"{coef} {'+' if e['b'] > 0 else MINUS} {abs(e['b'])}"
    return core


def affinity(attacks: dict) -> str:
    top = max(e["a"] for e in attacks.values())
    leaders = [t for t in ATTACKS if attacks[t]["a"] == top]
    return leaders[0] if len(leaders) == 1 else "Balanced"


def render_card(pet: dict, total: int) -> str:
    rows = []
    for t in ATTACKS:
        e = pet["attacks"][t]
        sub = f"rolls {e['low']}{MINUS}{e['high']}"
        if e["min"] is not None:
            sub = f'<span class="min">min 1</span> &middot; {sub}'
        rows.append(
            f'      <div class="atk">\n'
            f'        <div class="atk-head">'
            f'<span class="atk-type">{t}</span>'
            f'<span class="atk-name">{esc(pet["names"][t])}</span>'
            f'<span class="atk-eqn">{fmt_eqn(e)}</span></div>\n'
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
        "Generated by <code>tools/gen_pet_cards.py</code> from "
        "<code>cards/pets.md</code> — do not edit by hand. "
        f"Print to PDF (A4, 100% scale); {total} cards over {pages} pages. "
        "Print about 3 copies of the sheet for a class of 30 (each student draws 2 pets)."
    )
    return cardsheet.document("Algebra Monster Battle — Pet Cards", EXTRA_CSS, hint, body)


def print_table(blocks: list[dict]) -> None:
    pets = build_pets(blocks)
    print("| Pet · attack | eqn | 1 | 2 | 3 | 4 | 5 | 6 |")
    print("|---|---|---|---|---|---|---|---|")
    for p in pets:
        for t in ATTACKS:
            e = p["attacks"][t]
            label = fmt_eqn(e) + (" (min 1)" if e["min"] else "")
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
