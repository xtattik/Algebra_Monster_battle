# tools/cardsheet.py — shared layout for the print-and-play card sheets.
#
# Both gen_cards.py (characters) and gen_env_cards.py (environments) build the
# same 63 mm x 88 mm card on the same A4 9-up sheet. This module owns the parts
# that must stay identical between them: the page skeleton, the base CSS, the
# card-block parser, and the red "defence / vs you" treatment for any row that
# modifies the enemy-Strength term.
import base64
import io
import re
import sys
from pathlib import Path

try:
    from PIL import Image  # optional: enables letterbox auto-trim + recompress
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parent.parent
MINUS = "−"  # U+2212 MINUS SIGN, matches the rest of the project

# Optional per-card artwork. Drop a file at
#   cards/art/<deck>/<NN>-<slug>.<ext>     e.g. cards/art/pets/01-emberwisp.png
# and it is embedded (base64) into the sheet the next time the generator runs.
# <NN> is the two-digit card number; <slug> is the lower-cased name with runs of
# non-alphanumerics turned into single hyphens. Bare "<NN>.<ext>" or
# "<slug>.<ext>" also match. Accepted extensions, in priority order:
ART_DIR = ROOT / "cards" / "art"
_ART_EXTS = (".svg", ".png", ".webp", ".jpg", ".jpeg")
_ART_MIME = {
    ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
}

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


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _find_art(deck: str, num: int, name: str, prog: str):
    d = ART_DIR / deck
    if not d.is_dir():
        return None
    for stem in (f"{num:02d}-{slug(name)}", f"{num:02d}", slug(name)):
        matches = [d / f"{stem}{ext}" for ext in _ART_EXTS if (d / f"{stem}{ext}").is_file()]
        if matches:
            if len(matches) > 1:
                die(prog, f"card {num} ({name}): multiple art files match — keep one of "
                          f"{', '.join(p.name for p in matches)}")
            return matches[0]
    return None


def _sniff_mime(data: bytes, path: Path, prog: str) -> str:
    """Trust the file's actual bytes, not its extension."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    head = data[:512].lstrip().lower()
    if head.startswith(b"<?xml") or head.startswith(b"<svg"):
        return "image/svg+xml"
    die(prog, f"{path.name}: not a recognisable PNG / JPEG / WebP / SVG "
              f"(the extension is ignored — the file's contents are what matter)")


_BAR_MAX = 24        # a pixel this dark (max RGB channel) counts as "letterbox"
_MAX_ART_W = 1800     # downscale wider raster art than this when re-encoding


def _row_is_bar(px, w: int, y: int) -> bool:
    step = max(1, w // 64)
    return all(max(px[x, y][:3]) <= _BAR_MAX for x in range(0, w, step))


def _prep_raster(data: bytes):
    """With Pillow: trim near-solid dark bars from the top/bottom of the image
    (the user's art tool letterboxes non-10:3 exports with black), then re-encode
    as a reasonably sized JPEG. Returns (mime, bytes) or None to embed as-is."""
    if Image is None:
        return None
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return None
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    top, bot = 0, h
    while top < bot and _row_is_bar(px, w, top):
        top += 1
    while bot > top and _row_is_bar(px, w, bot - 1):
        bot -= 1
    trimmed = (top, bot) != (0, h)
    if trimmed and bot - top < h * 0.35:
        trimmed = False          # implausible — leave it alone
    if not trimmed and max(w, h) <= _MAX_ART_W:
        return None              # nothing to do; keep the original file
    if trimmed:
        im = im.crop((0, top, w, bot))
    if im.width > _MAX_ART_W:
        im = im.resize((_MAX_ART_W, round(im.height * _MAX_ART_W / im.width)),
                       Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=88, optimize=True)
    return "image/jpeg", buf.getvalue()


def _data_uri(path: Path, prog: str) -> str:
    data = path.read_bytes()
    mime = _sniff_mime(data, path, prog)
    if mime != "image/svg+xml":
        prepped = _prep_raster(data)
        if prepped is not None:
            mime, data = prepped
    return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")


def card_top(deck: str, num: int, total: int, name: str, prog: str, subhead: str = "") -> str:
    """The top of a card: the identity zone + art.

    No artwork: a text header (name + N/total), then `subhead` (deck-specific,
    e.g. a pet's HP line), then an empty dashed art box.
    Artwork present: a taller "hero" image filling the top of the card, with the
    N/total chip overlaid top-right and the card name in a small pill
    bottom-left (so the card is identifiable even if its name is not painted
    into the art), then `subhead`. Drop a file at
    cards/art/<deck>/<NN>-<slug>.<ext> to switch a card.
    """
    sub = f"\n      {subhead}" if subhead else ""
    path = _find_art(deck, num, name, prog)
    if path is None:
        return (
            f'      <div class="head"><span class="name">{esc(name)}</span>'
            f'<span class="num">{num}/{total}</span></div>'
            f'{sub}\n'
            f'      <div class="art">art</div>'
        )
    return (
        f'      <div class="art has-art art-hero">'
        f'<img alt="{esc(name)}" src="{_data_uri(path, prog)}">'
        f'<span class="cardname">{esc(name)}</span>'
        f'<span class="cardno">{num}/{total}</span></div>'
        f'{sub}'
    )


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
      height: 17mm; margin: 1.6mm 0 2mm;
      border: 0.3mm dashed #999;
      display: flex; align-items: center; justify-content: center;
      font-size: 6.5pt; letter-spacing: 1pt; text-transform: uppercase; color: #aaa;
      overflow: hidden;
    }
    .art.has-art { border: 0.3mm solid #000; }
    .art img { width: 100%; height: 100%; object-fit: cover; display: block; }
    /* "hero" art replaces the text header: taller, name is baked into the art */
    .art-hero {
      height: 26mm; margin: 0 0 2mm; position: relative;
    }
    /* left-anchored: the art template puts its title on the left, so the
       side that gets cropped (box is a touch narrower than the trimmed art)
       is the right */
    .art-hero img { object-position: 0% 45%; }
    .cardno, .cardname {
      position: absolute; bottom: 1mm;
      font-size: 6pt; line-height: 1; color: #fff;
      background: rgba(0, 0, 0, 0.55); padding: 0.6mm 1mm; border-radius: 1mm;
      letter-spacing: 0.3pt;
    }
    .cardno { right: 1.2mm; }
    .cardname { left: 1.2mm; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5pt; }
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
      /* 9 cards per A4 page; force the break so a row is never split */
      .card:nth-child(9n) { break-after: page; }
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
