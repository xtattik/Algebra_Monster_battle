# tools/gen_env_cards.py — build the printable environment-card sheet (v2).
#
# Reads cards/environments.md and writes cards/environments.html (A4, 9-up,
# 63 mm x 88 mm cards). Shared page/CSS/CLI live in tools/cardsheet.py.
#
# v2 model (see docs/design/core-rules-v2.md §4):
#   Boost:  <Magic|Strength|Agility> <+2x|+x>   -> that attack type gains the term
#   Weaken: <Magic|Strength|Agility> <-2x|-x>   -> that attack type takes the term
#   Cancel: <Magic|Strength|Agility>            -> that attack type is unusable
# A card has at most one of each verb; the types named must all differ.
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

TYPES = ("Magic", "Strength", "Agility")
VERBS = ("Boost", "Weaken", "Cancel")
BOOST_TERMS = ("+2x", "+x")
WEAKEN_TERMS = (f"{MINUS}2x", f"{MINUS}x", "-2x", "-x")  # accept ASCII or U+2212 in source

EXTRA_CSS = """\
    .fx { margin-bottom: 1.8mm; }
    .fx .line { display: flex; align-items: baseline; gap: 1.6mm; }
    .fx .verb {
      font-size: 7pt; text-transform: uppercase; letter-spacing: 0.6pt;
      width: 16mm; color: #333;
    }
    .fx .type { font-size: 8.5pt; font-weight: 700; flex: 1; }
    .fx .term {
      font-size: 12pt; font-weight: 700; margin-left: auto;
      font-family: "Cambria Math", "Times New Roman", Georgia, serif;
    }
    .fx .term-up { color: #1a7f37; }
    .fx .term-down { color: #b3261e; }
    .fx.cancel {
      background: #fbeceb; border-radius: 1mm;
      padding: 1mm 1.4mm; margin-left: -1.4mm; margin-right: -1.4mm;
    }
    .fx.cancel .type { color: #b3261e; }
    .fx.cancel .x { color: #b3261e; font-weight: 700; font-size: 10pt; margin-left: auto; }
    .fx .effect { font-size: 6.6pt; line-height: 1.25; color: #222; margin-top: 0.3mm; }
    .neutral { font-size: 8pt; color: #666; font-style: italic; margin: 1mm 0; }
"""


def _parse_entry(prog_tag, verb, raw):
    parts = raw.split()
    typ = parts[0]
    if typ not in TYPES:
        die(PROG, f"{prog_tag}: {verb} names {typ!r} (expected Magic, Strength or Agility)")
    if verb == "Cancel":
        if len(parts) != 1:
            die(PROG, f"{prog_tag}: Cancel takes only a type, got {raw!r}")
        return {"verb": "Cancel", "type": typ, "term": None}
    if len(parts) != 2:
        die(PROG, f"{prog_tag}: {verb} needs '<type> <term>', got {raw!r}")
    term = parts[1].replace("-", MINUS) if verb == "Weaken" else parts[1]
    allowed = BOOST_TERMS if verb == "Boost" else (f"{MINUS}2x", f"{MINUS}x")
    if term not in allowed:
        die(PROG, f"{prog_tag}: {verb} term {parts[1]!r} (expected {' or '.join(allowed)})")
    return {"verb": verb, "type": typ, "term": term}


def _parse_effects(prog_tag, verb, raw):
    entries = [_parse_entry(prog_tag, verb, e.strip()) for e in raw.split(",")]
    if verb != "Weaken" and len(entries) != 1:
        die(PROG, f"{prog_tag}: only Weaken may list more than one type")
    return entries


def render_effect(fx) -> str:
    typ = fx["type"]
    if fx["verb"] == "Cancel":
        return (
            f'      <div class="fx cancel">\n'
            f'        <div class="line"><span class="verb">Cancel</span>'
            f'<span class="type">{typ.upper()}</span><span class="x">&#10005; unusable</span></div>\n'
            f'        <div class="effect">{typ} attacks <b>cannot be used</b> this match.</div>\n'
            f'      </div>'
        )
    up = fx["verb"] == "Boost"
    cls = "term-up" if up else "term-down"
    word = "gain" if up else "take"
    return (
        f'      <div class="fx">\n'
        f'        <div class="line"><span class="verb">{fx["verb"]}</span>'
        f'<span class="type">{typ.upper()}</span>'
        f'<span class="term {cls}">{esc(fx["term"])}</span></div>\n'
        f'        <div class="effect">Every {typ.lower()} attack here {word}s {esc(fx["term"])}.</div>\n'
        f'      </div>'
    )


def render_card(card: dict, total: int) -> str:
    if card["effects"]:
        fx_html = "\n".join(render_effect(fx) for fx in card["effects"]) + "\n"
    else:
        fx_html = '      <div class="neutral">No effect — a clear, even battleground.</div>\n'
    return (
        f'    <div class="card">\n'
        + cardsheet.card_top("environments", card["num"], total, card["name"], PROG) + "\n"
        + fx_html
        + f'      <p class="flavour">{esc(card["flavour"])}</p>\n'
        f'    </div>'
    )


def build_html(blocks: list[dict]) -> str:
    cards = []
    for b in blocks:
        f = b["fields"]
        tag = f"card {b['num']} ({b['name']})"
        if "Flavour" not in f:
            die(PROG, f"{tag} is missing: Flavour")

        effects, seen_types = [], set()
        for verb in VERBS:
            if verb not in f:
                continue
            for fx in _parse_effects(tag, verb, f[verb]):
                if fx["type"] in seen_types:
                    die(PROG, f"{tag}: {fx['type']} is named by more than one effect")
                seen_types.add(fx["type"])
                effects.append(fx)
        effects.sort(key=lambda fx: VERBS.index(fx["verb"]))

        if len(effects) > 2:
            die(PROG, f"{tag}: {len(effects)} effects (at most 2 per card)")
        if not effects and b["name"] != "Open Field":
            die(PROG, f"{tag}: has no Boost / Weaken / Cancel line (only 'Open Field' may)")

        cards.append({"num": b["num"], "name": b["name"],
                      "effects": effects, "flavour": f["Flavour"]})

    total = len(cards)
    body = "\n".join(render_card(c, total) for c in cards)
    hint = (
        "Generated by <code>tools/gen_env_cards.py</code> from "
        "<code>cards/environments.md</code> — do not edit by hand. "
        f"{total} designs; print as many copies of each as you like to set the mix. "
        "Print to PDF (A4, 100% scale); one card is drawn per match."
    )
    return cardsheet.document("Algebra Monster Battle — Environment Cards", EXTRA_CSS, hint, body)


if __name__ == "__main__":
    cardsheet.run(PROG, SRC, OUT, build_html)
