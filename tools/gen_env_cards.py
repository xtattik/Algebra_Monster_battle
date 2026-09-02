# tools/gen_env_cards.py — build the printable environment-card sheet.
#
# Reads cards/environments.md and writes cards/environments.html (A4, 9-up,
# 63 mm x 88 mm cards) to match the character sheet. Shared page/CSS/CLI live in
# tools/cardsheet.py. The +-x terms and the High/Average/Low test table are
# derived here, never written in the source.
#
# Model (see docs/design/environments.md):
#   BOOSTS  <Magic|Agility>  -> that attack type gains +x   (flat, everyone)
#   HINDERS <Magic|Agility>  -> that attack type takes -x   (flat, everyone)
#   TESTS   Strength         -> defender's Strength tier: High -x / Avg 0 / Low +x,
#                              added to the enemy-Strength slot; reaches strike.
#
# Usage:
#   python tools/gen_env_cards.py            # regenerate cards/environments.html
#   python tools/gen_env_cards.py --check    # exit 1 if the file is out of date
#   python tools/gen_env_cards.py --stdout   # print the HTML instead of writing it
import cardsheet
from cardsheet import MINUS, ROOT, die, esc

PROG = "gen_env_cards"
SRC = ROOT / "cards" / "environments.md"
OUT = ROOT / "cards" / "environments.html"

REQUIRED = ("Boosts", "Hinders", "Tests", "Flavour")
ATTACK_STATS = ("Magic", "Agility")
NONE = "none"

# defender Strength tier -> term added to the enemy-Strength slot
STRENGTH_TEST = (("High", f"{MINUS}x"), ("Avg", "0"), ("Low", "+x"))

EXTRA_CSS = """\
    .env-line .term { font-size: 10.5pt; }
    .none { color: #999; font-weight: 400; }
    .testgrid {
      display: flex; align-items: baseline; gap: 0 4mm; margin-top: 1mm;
      font-size: 7pt; text-transform: uppercase; letter-spacing: 0.3pt; color: #333;
    }
    .testgrid b {
      font-family: "Cambria Math", "Times New Roman", Georgia, serif;
      font-size: 9.5pt; margin-left: 0.6mm; font-weight: 700;
    }
"""


def attack_row(key: str, stat: str, term: str, verb: str) -> str:
    if stat == NONE:
        return (
            f'      <div class="row env-line">\n'
            f'        <div class="line"><span class="key">{key}</span>'
            f'<span class="val none">none</span></div>\n'
            f'      </div>'
        )
    return (
        f'      <div class="row env-line">\n'
        f'        <div class="line"><span class="key">{key}</span>'
        f'<span class="val">{stat.upper()}</span>'
        f'<span class="termwrap"><span class="term">{esc(term)}</span></span></div>\n'
        f'        <div class="effect">Every {stat.lower()} attack here {verb} {esc(term)}.</div>\n'
        f'      </div>'
    )


def tests_row(tests: str) -> str:
    if tests == NONE:
        return (
            f'      <div class="row env-line">\n'
            f'        <div class="line"><span class="key">Tests</span>'
            f'<span class="val none">none</span></div>\n'
            f'      </div>'
        )
    cells = "".join(
        f'<span>{tier}<b class="{"term-def" if t != "0" else "term-zero"}">{esc(t)}</b></span>'
        for tier, t in STRENGTH_TEST
    )
    return (
        f'      <div class="row row-def">\n'
        f'        <div class="line"><span class="key">Tests</span>'
        f'<span class="val">STRENGTH <span class="deftag">defence</span></span></div>\n'
        f'        <div class="testgrid">{cells}</div>\n'
        f'        <div class="effect">Your <b>Strength</b> tier sets the term, added to every '
        f'attack against you &mdash; strike included.</div>\n'
        f'      </div>'
    )


def render_card(card: dict, total: int) -> str:
    return (
        f'    <div class="card">\n'
        f'      <div class="head">'
        f'<span class="name">{esc(card["name"])}</span>'
        f'<span class="num">{card["num"]}/{total}</span></div>\n'
        f'      <div class="art">art</div>\n'
        + attack_row("Boosts", card["boosts"], "+x", "gains") + "\n"
        + attack_row("Hinders", card["hinders"], f"{MINUS}x", "takes") + "\n"
        + tests_row(card["tests"]) + "\n"
        f'      <p class="flavour">{esc(card["flavour"])}</p>\n'
        f'    </div>'
    )


def build_html(blocks: list[dict]) -> str:
    cards = []
    for b in blocks:
        f = b["fields"]
        tag = f"card {b['num']} ({b['name']})"
        missing = [k for k in REQUIRED if k not in f]
        if missing:
            die(PROG, f"{tag} is missing: {', '.join(missing)}")

        boosts, hinders, tests = f["Boosts"], f["Hinders"], f["Tests"]
        for key, val in (("Boosts", boosts), ("Hinders", hinders)):
            if val != NONE and val not in ATTACK_STATS:
                die(PROG, f"{tag}: {key} is {val!r} (expected Magic, Agility or none)")
        if tests not in (NONE, "Strength"):
            die(PROG, f"{tag}: Tests is {tests!r} (expected Strength or none)")
        if boosts != NONE and boosts == hinders:
            die(PROG, f"{tag}: Boosts and Hinders both name {boosts!r}")
        if boosts == NONE and hinders == NONE and tests == NONE and b["name"] != "Open Field":
            die(PROG, f"{tag}: has no Boosts, Hinders or Tests (only 'Open Field' may)")

        cards.append({
            "num": b["num"], "name": b["name"],
            "boosts": boosts, "hinders": hinders, "tests": tests,
            "flavour": f["Flavour"],
        })

    total = len(cards)
    body = "\n".join(render_card(c, total) for c in cards)
    hint = (
        "Generated by <code>tools/gen_env_cards.py</code> from "
        "<code>cards/environments.md</code> — do not edit by hand. "
        "Print to PDF (A4, 100% scale, margins from the file); one card is drawn per match."
    )
    return cardsheet.document("Algebra Monster Battle — Environment Cards", EXTRA_CSS, hint, body)


if __name__ == "__main__":
    cardsheet.run(PROG, SRC, OUT, build_html)
