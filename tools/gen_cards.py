# tools/gen_cards.py — build the printable character-card sheet.
#
# Reads the authored card blocks in cards/characters.md and writes a
# self-contained print sheet to cards/characters.html (A4, 9 cards per page,
# 63 mm x 88 mm each). The plain-words stat effect and the +-x term are derived
# here from the tier, so every card is worded identically.
#
# Usage:
#   python tools/gen_cards.py            # regenerate cards/characters.html
#   python tools/gen_cards.py --check    # exit 1 if the file is out of date
#   python tools/gen_cards.py --stdout   # print the HTML instead of writing it
#
# Exits non-zero with a message on stderr if a card block is malformed or names
# a stat tier it does not recognise.
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "cards" / "characters.md"
OUT = ROOT / "cards" / "characters.html"

MINUS = "−"  # U+2212 MINUS SIGN, matches the rest of the project

# (stat, tier) -> (plain-words effect, term shown in the chip)
EFFECTS = {
    ("Magic", "High"): ("Your magic attacks gain +x.", "+x"),
    ("Magic", "Average"): ("Your magic attacks are unchanged.", "0"),
    ("Magic", "Low"): (f"Your magic attacks take {MINUS}x.", f"{MINUS}x"),
    ("Agility", "High"): ("Your agility attacks gain +x.", "+x"),
    ("Agility", "Average"): ("Your agility attacks are unchanged.", "0"),
    ("Agility", "Low"): (f"Your agility attacks take {MINUS}x.", f"{MINUS}x"),
    ("Strength", "High"): (f"Enemy attacks against you take {MINUS}x.", f"{MINUS}x"),
    ("Strength", "Average"): ("Enemy attacks against you are unchanged.", "0"),
    ("Strength", "Low"): ("Enemy attacks against you gain +x.", "+x"),
}

STAT_ORDER = ("Magic", "Strength", "Agility")

CARD_RE = re.compile(
    r"^## (?P<num>\d+)\. (?P<name>.+?)\s*$\n"
    r"(?P<body>(?:^- .+$\n?)+)",
    re.MULTILINE,
)
FIELD_RE = re.compile(r"^- (?P<key>Magic|Strength|Agility|Playstyle|Flavour): (?P<val>.+?)\s*$", re.MULTILINE)


def die(msg: str) -> None:
    print(f"gen_cards: {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_cards(text: str) -> list[dict]:
    cards = []
    for m in CARD_RE.finditer(text):
        fields = {fm["key"]: fm["val"] for fm in FIELD_RE.finditer(m["body"])}
        missing = [k for k in ("Magic", "Strength", "Agility", "Playstyle", "Flavour") if k not in fields]
        if missing:
            die(f"card {m['num']} ({m['name']}) is missing: {', '.join(missing)}")
        for stat in STAT_ORDER:
            if (stat, fields[stat]) not in EFFECTS:
                die(f"card {m['num']} ({m['name']}): unknown {stat} tier {fields[stat]!r} "
                    f"(expected High, Average or Low)")
        cards.append({
            "num": int(m["num"]),
            "name": m["name"],
            "stats": {s: fields[s] for s in STAT_ORDER},
            "playstyle": fields["Playstyle"],
            "flavour": fields["Flavour"],
        })
    if not cards:
        die(f"no card blocks found in {SRC}")
    nums = [c["num"] for c in cards]
    if nums != sorted(nums) or nums != list(range(1, len(nums) + 1)):
        die(f"card numbers must be 1..N in order, got {nums}")
    return cards


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_card(card: dict, total: int) -> str:
    rows = []
    for stat in STAT_ORDER:
        tier = card["stats"][stat]
        effect, term = EFFECTS[(stat, tier)]
        # Strength is defensive and its sign is inverted vs Magic/Agility
        # (HIGH gives the *attacker* -x). Flag the row so students read it as
        # "the enemy's term", not their own: tinted row, "vs you" label, red term.
        is_def = stat == "Strength"
        stat_cls = "stat stat-def" if is_def else "stat"
        term_cls = "term"
        if term == "0":
            term_cls += " term-zero"
        elif is_def:
            term_cls += " term-def"
        prefix = '<span class="vsyou">vs you</span>' if is_def else ""
        tier_label = f"{tier.upper()} <span class=\"deftag\">defence</span>" if is_def else tier.upper()
        rows.append(
            f'      <div class="{stat_cls}">\n'
            f'        <div class="statline">'
            f'<span class="statname">{stat}</span>'
            f'<span class="tier">{tier_label}</span>'
            f'<span class="termwrap">{prefix}<span class="{term_cls}">{esc(term)}</span></span></div>\n'
            f'        <div class="effect">{esc(effect)}</div>\n'
            f'      </div>'
        )
    return (
        f'    <div class="card">\n'
        f'      <div class="head">'
        f'<span class="name">{esc(card["name"])}</span>'
        f'<span class="num">{card["num"]}/{total}</span></div>\n'
        f'      <div class="art">art</div>\n'
        + "\n".join(rows) + "\n"
        f'      <p class="playstyle">{esc(card["playstyle"])}</p>\n'
        f'      <p class="flavour">{esc(card["flavour"])}</p>\n'
        f'    </div>'
    )


CSS = """\
    :root { color-scheme: light; }
    * { box-sizing: border-box; }
    body {
      margin: 0; background: #d8d8d8;
      font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      color: #000;
      -webkit-print-color-adjust: exact; print-color-adjust: exact;
    }
    .sheet {
      display: grid;
      grid-template-columns: repeat(3, 63mm);
      grid-auto-rows: 88mm;
      justify-content: center;
      align-content: start;
      gap: 0;
      background: #fff;
      width: 210mm;
      min-height: 297mm;
      margin: 12mm auto;
      padding: 12mm 10.5mm;
    }
    .card {
      width: 63mm; height: 88mm;
      border: 0.3mm solid #000;
      padding: 3.4mm 3.6mm;
      display: flex; flex-direction: column;
      overflow: hidden;
      break-inside: avoid;
    }
    .head { display: flex; justify-content: space-between; align-items: baseline; }
    .name { font-size: 12.5pt; font-weight: 700; letter-spacing: 0.2pt; }
    .num { font-size: 7pt; color: #444; }
    .art {
      height: 12mm; margin: 1.6mm 0 2mm;
      border: 0.3mm dashed #999;
      display: flex; align-items: center; justify-content: center;
      font-size: 6.5pt; letter-spacing: 1pt; text-transform: uppercase; color: #aaa;
    }
    .stat { margin-bottom: 1.6mm; }
    .stat-def {
      background: #fbeceb; border-radius: 1mm;
      padding: 0.9mm 1.2mm; margin-left: -1.2mm; margin-right: -1.2mm;
    }
    .statline { display: flex; align-items: baseline; gap: 1.4mm; }
    .statname {
      font-size: 7pt; text-transform: uppercase; letter-spacing: 0.6pt;
      width: 15mm; color: #333;
    }
    .tier { font-size: 8pt; font-weight: 700; flex: 1; }
    .deftag {
      font-size: 5.6pt; font-weight: 600; letter-spacing: 0.4pt;
      text-transform: uppercase; color: #b3261e;
    }
    .termwrap {
      margin-left: auto; display: flex; align-items: baseline;
      gap: 1mm; white-space: nowrap;
    }
    .vsyou {
      font-size: 5.8pt; font-weight: 600; letter-spacing: 0.4pt;
      text-transform: uppercase; color: #b3261e;
    }
    .term {
      font-size: 11pt; font-weight: 700;
      font-family: "Cambria Math", "Times New Roman", Georgia, serif;
    }
    .term-zero { color: #777; }
    .term-def { color: #b3261e; }
    .effect { font-size: 6.6pt; line-height: 1.25; color: #222; margin-top: 0.3mm; }
    .playstyle {
      font-size: 7pt; line-height: 1.3; margin: 1.4mm 0 0;
      border-top: 0.3mm solid #000; padding-top: 1.4mm;
    }
    .flavour { font-size: 6.6pt; font-style: italic; color: #444; margin: auto 0 0; }
    @media print {
      body { background: #fff; }
      .sheet { margin: 0; padding: 0; width: auto; min-height: 0; box-shadow: none; }
      .hint { display: none; }
    }
    @page { size: A4; margin: 8mm; }
    .hint {
      max-width: 210mm; margin: 12mm auto -6mm; padding: 0 10.5mm;
      font-size: 9pt; color: #555;
    }
"""


def render_html(cards: list[dict]) -> str:
    total = len(cards)
    body = "\n".join(render_card(c, total) for c in cards)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        "<title>Algebra Monster Battle — Character Cards</title>\n"
        "<style>\n" + CSS + "</style>\n</head>\n<body>\n"
        '<p class="hint">Generated by <code>tools/gen_cards.py</code> from '
        "<code>cards/characters.md</code> — do not edit by hand. "
        "Print to PDF (A4, 100% scale, margins from the file) for a cut-apart deck; "
        "reprint the sheet once per copy you need.</p>\n"
        '<div class="sheet">\n' + body + "\n</div>\n</body>\n</html>\n"
    )


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    args = set(sys.argv[1:])
    if not SRC.exists():
        die(f"source not found: {SRC}")
    cards = parse_cards(SRC.read_text(encoding="utf-8"))
    html = render_html(cards)

    if "--stdout" in args:
        print(html, end="")
        return
    if "--check" in args:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != html:
            die(f"{OUT.relative_to(ROOT)} is out of date — run: python tools/gen_cards.py")
        print(f"{OUT.relative_to(ROOT)} is up to date ({len(cards)} cards)")
        return

    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(cards)} cards)")


if __name__ == "__main__":
    main()
