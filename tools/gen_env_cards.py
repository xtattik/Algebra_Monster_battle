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
    .fxrows { margin: 0.8mm 0 1.4mm; }
    .fxrow { padding: 1mm 0; border-top: 0.2mm solid #e4e4e4; }
    .fxrow:first-child { border-top: none; }
    .fxrow .line { display: flex; align-items: baseline; gap: 1.6mm; }
    .fxrow .type {
      font-size: 7.2pt; text-transform: uppercase; letter-spacing: 0.6pt;
      width: 17mm; color: #333; font-weight: 600;
    }
    .fxrow .what { flex: 1; font-size: 7.4pt; color: #333; }
    .fxrow .term {
      margin-left: auto; font-size: 12.5pt; font-weight: 700;
      font-family: "Cambria Math", "Times New Roman", Georgia, serif;
    }
    .fxrow.up   .term { color: #1a7f37; }
    .fxrow.down .term { color: #b3261e; }
    .fxrow.none .term { color: #b3b3b3; font-weight: 400; }
    .fxrow.cancel {
      background: #fbeceb; border-radius: 1mm;
      margin: 0 -1.6mm; padding: 1mm 1.6mm;
    }
    .fxrow.cancel .type, .fxrow.cancel .what { color: #b3261e; }
    .fxrow.cancel .term { color: #b3261e; font-size: 10.5pt; }

    .worked {
      font-size: 7pt; color: #555; margin: 0 0 1.6mm;
      border-left: 0.4mm solid #cfcfcf; padding-left: 2mm;
    }
    .worked b { color: #222; }
    .worked .m { font-family: "Cambria Math", "Times New Roman", Georgia, serif; font-weight: 700; }

    .flavour { font-size: 8pt; line-height: 1.35; }
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


def _mag(term: str) -> int:
    """coefficient magnitude of '+2x' / '-x' etc."""
    return 2 if "2" in term else 1


def fx_row(typ: str, fx) -> str:
    """One of the three attack-type rows on a card."""
    if fx is None:
        return (
            f'      <div class="fxrow none">\n'
            f'        <div class="line"><span class="type">{typ}</span>'
            f'<span class="what">no change here</span>'
            f'<span class="term">0</span></div>\n'
            f'      </div>'
        )
    if fx["verb"] == "Cancel":
        return (
            f'      <div class="fxrow cancel">\n'
            f'        <div class="line"><span class="type">{typ}</span>'
            f'<span class="what"><b>cannot be used</b> this match</span>'
            f'<span class="term">&#10005;</span></div>\n'
            f'      </div>'
        )
    up = fx["verb"] == "Boost"
    return (
        f'      <div class="fxrow {"up" if up else "down"}">\n'
        f'        <div class="line"><span class="type">{typ}</span>'
        f'<span class="what">{typ.lower()} attacks {"gain" if up else "take"}&hellip;</span>'
        f'<span class="term">{esc(fx["term"])}</span></div>\n'
        f'      </div>'
    )


def worked_line(effects) -> str:
    """A one-line 'here's the maths' example, keyed off the headline effect."""
    boost = next((e for e in effects if e["verb"] == "Boost"), None)
    weaken = next((e for e in effects if e["verb"] == "Weaken"), None)
    cancel = next((e for e in effects if e["verb"] == "Cancel"), None)
    if boost:
        n = 3 + _mag(boost["term"])
        rhs = f"3x + {boost['term'].lstrip('+')} = {n}x"
        return (f'      <p class="worked">e.g. a {boost["type"].lower()} attack '
                f'<span class="m">3x</span> becomes <span class="m">{rhs}</span> here.</p>')
    if weaken:
        n = 3 - _mag(weaken["term"])
        core = "0" if n == 0 else ("x" if n == 1 else f"{n}x")
        rhs = f"3x {MINUS} {weaken['term'].lstrip(MINUS)} = {core}"
        return (f'      <p class="worked">e.g. a {weaken["type"].lower()} attack '
                f'<span class="m">3x</span> becomes <span class="m">{rhs}</span> here.</p>')
    if cancel:
        t = cancel["type"].lower()
        art = "an" if t[0] in "aeiou" else "a"
        others = [o.lower() for o in TYPES if o != cancel["type"]]
        return (f'      <p class="worked">You cannot choose {art} {t} '
                f'attack here &mdash; field {others[0]} or {others[1]}.</p>')
    return ('      <p class="worked">Nothing to add or take away &mdash; a '
            '<span class="m">3x</span> attack stays <span class="m">3x</span>.</p>')


def render_card(card: dict, total: int) -> str:
    by_type = {fx["type"]: fx for fx in card["effects"]}
    rows = "\n".join(fx_row(t, by_type.get(t)) for t in TYPES)
    return (
        f'    <div class="card">\n'
        + cardsheet.card_top("environments", card["num"], total, card["name"], PROG) + "\n"
        + f'      <div class="fxrows">\n{rows}\n      </div>\n'
        + worked_line(card["effects"]) + "\n"
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
