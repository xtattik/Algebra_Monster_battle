# tools/cardsheet.py — shared layout for the print-and-play card sheets.
#
# Both gen_cards.py (characters) and gen_env_cards.py (environments) build the
# same 63 mm x 88 mm card on the same A4 9-up sheet. This module owns the parts
# that must stay identical between them: the page skeleton, the base CSS, the
# card-block parser, and the red "defence / vs you" treatment for any row that
# modifies the enemy-Strength term.
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MINUS = "−"  # U+2212 MINUS SIGN, matches the rest of the project

_CARD_RE = re.compile(
    r"^## (?P<num>\d+)\. (?P<name>.+?)\s*$\n"
    r"(?P<body>(?:^- .+$\n?)+)",
    re.MULTILINE,
)
_FIELD_RE = re.compile(r"^- (?P<key>[A-Za-z][A-Za-z ]*?): (?P<val>.+?)\s*$", re.MULTILINE)


def die(prog: str, msg: str) -> None:
    print(f"{prog}: {msg}", file=sys.stderr)
    raise SystemExit(1)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def parse_blocks(text: str, prog: str) -> list[dict]:
    """Return [{num, name, fields}] for every '## N. Name' + '- Key: value' block.

    Enforces that the numbers are exactly 1..N in order. Field validation is left
    to the caller.
    """
    blocks = []
    for m in _CARD_RE.finditer(text):
        fields = {fm["key"]: fm["val"] for fm in _FIELD_RE.finditer(m["body"])}
        blocks.append({"num": int(m["num"]), "name": m["name"], "fields": fields})
    if not blocks:
        die(prog, "no card blocks found")
    nums = [b["num"] for b in blocks]
    if nums != list(range(1, len(nums) + 1)):
        die(prog, f"card numbers must be 1..N in order, got {nums}")
    return blocks


BASE_CSS = """\
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
    .row { margin-bottom: 1.6mm; }
    .row-def {
      background: #fbeceb; border-radius: 1mm;
      padding: 0.9mm 1.2mm; margin-left: -1.2mm; margin-right: -1.2mm;
    }
    .line { display: flex; align-items: baseline; gap: 1.4mm; }
    .key {
      font-size: 7pt; text-transform: uppercase; letter-spacing: 0.6pt;
      width: 15mm; color: #333;
    }
    .val { font-size: 8pt; font-weight: 700; flex: 1; }
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
    .rule {
      margin: 1.4mm 0 0; border-top: 0.3mm solid #000; padding-top: 1.4mm;
      font-size: 7pt; line-height: 1.3;
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


def document(title: str, extra_css: str, hint_html: str, body_html: str) -> str:
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        f"<title>{esc(title)}</title>\n"
        "<style>\n" + BASE_CSS + (extra_css or "") + "</style>\n</head>\n<body>\n"
        f'<p class="hint">{hint_html}</p>\n'
        '<div class="sheet">\n' + body_html + "\n</div>\n</body>\n</html>\n"
    )


def run(prog: str, src: Path, out: Path, build_html) -> None:
    """Shared CLI: no args = write; --check = verify up to date; --stdout = print."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    args = set(sys.argv[1:])
    if not src.exists():
        die(prog, f"source not found: {src}")
    blocks = parse_blocks(src.read_text(encoding="utf-8"), prog)
    html = build_html(blocks)

    if "--stdout" in args:
        print(html, end="")
        return
    if "--check" in args:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != html:
            die(prog, f"{out.relative_to(ROOT)} is out of date — run: python tools/{prog}.py")
        print(f"{out.relative_to(ROOT)} is up to date ({len(blocks)} cards)")
        return

    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(blocks)} cards)")
