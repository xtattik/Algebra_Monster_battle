# Card artwork

Drop image files here and re-run the matching generator — the art is embedded
into the print sheet automatically. No art file just means the card keeps its
dashed **"art"** placeholder box, so you can add pictures one at a time.

## Where

```
cards/art/
  characters/   ← 7 files,  e.g. 01-sorcerer.png
  environments/ ← 8 files,  e.g. 05-frozen-wastes.png
  pets/         ← 22 files, e.g. 07-patchwork-golem.png
```

## Naming

`<NN>-<slug>.<ext>`

- **`<NN>`** — the card's two-digit number (`01`, `02`, … `22`), from its
  `## N.` heading in the deck's `.md` source. This is what actually binds the
  file to the card, so it survives a name tweak.
- **`<slug>`** — the card name, lower-cased, with every run of
  non-letters/digits turned into a single `-` (e.g. *Patchwork Golem* →
  `patchwork-golem`, *Old Cairn* → `old-cairn`). It is there so the folder is
  readable; it is not matched strictly.
- **`<ext>`** — one of `svg`, `png`, `webp`, `jpg`, `jpeg`. If several exist for
  one card the generator stops and asks you to remove the extras; otherwise the
  order listed here is the priority.

`01.png` or `sorcerer.png` (no number, or no slug) also match, in that order of
preference, but `01-sorcerer.png` is the convention.

## Shape

The art box is the full card width by **17 mm** tall — a wide banner, roughly
**3.3 : 1**. Images are scaled to fill and **centre-cropped** (`object-fit:
cover`), so compose loosely and keep anything important away from the edges.
Vector (`svg`) prints sharpest; for raster aim for at least ~1000 px wide.

## Regenerate

```bash
python tools/gen_cards.py       # characters
python tools/gen_env_cards.py   # environments
python tools/gen_pet_cards.py   # pets
```

Art is base64-embedded, so each `cards/*.html` stays a single self-contained
file you can email or "Print to PDF" from anywhere.
