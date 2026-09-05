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

PLAIN_RE = re.compile(r"^([123]?)x(?:\s*([+-])\s*([0-3]))?(?:\s*\(min\s*(?P<min>\d+)\))?$")
BRACKET_RE = re.compile(r"^([23])\(x\s*([+-])\s*([12])\)(?:\s*\(min\s*(?P<min>\d+)\))?$")
NEGATIVE_RE = re.compile(r"^-([123]?)x(?:\s*([+-])\s*(\d{1,2}))?(?:\s*\(min\s*(?P<min>\d+)\))?$")

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
    s = raw.strip().replace(MINUS, "-").replace("–", "-")
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

    printed_min = int(m.group("min")) if m.group("min") else None
    values = [a * x + b for x in range(1, 7)]
    needs_min = min(values) < 1
    if needs_min and printed_min is None:
        die(PROG, f"{prog_tag}: {raw!r} can deal < 1 somewhere in rolls 1-6 — add '(min 1)'")
    if not needs_min and printed_min is not None:
        die(PROG, f"{prog_tag}: {raw!r} never drops below 1 — remove the spurious '(min {printed_min})'")
    if needs_min and printed_min != 1:
        die(PROG, f"{prog_tag}: {raw!r} floor must be '(min 1)', not '(min {printed_min})'")

    at1, at6 = max(1, values[0]), max(1, values[5])
    return {
        "a": a, "b": b, "form": form, "min": printed_min, "display": display,
        "lo": min(at1, at6), "hi": max(at1, at6),
    }


def affinity(attacks: dict) -> str:
    top = max(abs(e["a"]) for e in attacks.values())
    leaders = [t for t in ATTACKS if abs(attacks[t]["a"]) == top]
    return leaders[0] if len(leaders) == 1 else "Balanced"


def render_card(pet: dict, total: int) -> str:
    rows = []
    for t in ATTACKS:
        e = pet["attacks"][t]
        sub = f"rolls {e['lo']}{MINUS}{e['hi']}"
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
