# Card artwork

Drop an image here and re-run the matching generator — it is embedded into the
print sheet automatically. No file just means the card keeps its plain text
header and a dashed **"art"** placeholder, so you can add pictures one at a time.

## Where

```
cards/art/
  characters/   ← up to 7 files,  e.g. 01-sorcerer.jpg
  environments/ ← up to 8 files,  e.g. 05-frozen-wastes.jpg
  pets/         ← up to 22 files, e.g. 07-patchwork-golem.jpg
```

## Naming

`<NN>-<slug>.<ext>`

- **`<NN>`** — the card's two-digit number (`01` … `22`), from its `## N.`
  heading in the deck's `.md` source. This is what binds the file to the card,
  so it survives a name tweak.
- **`<slug>`** — the card name, lower-cased, every run of non-letters/digits
  turned into one `-` (*Patchwork Golem* → `patchwork-golem`). Readability only;
  not matched strictly. `01.jpg` (no slug) also works.
- **`<ext>`** — `svg`, `png`, `webp`, `jpg`, or `jpeg`. **The extension is
  cosmetic** — the generator detects the real format from the file's bytes, so a
  JPEG named `.png` still works (rename it anyway to keep the folder honest).
  Two files for one card → the generator stops and asks you to remove one.

## What a card with art looks like

When a card has art it switches to **hero mode**:

- The image fills the **top ~26 mm** of the card (full inner width, ~55 mm).
- The card's **printed name header is dropped** — the name is expected to be in
  the artwork. Only a small `N/total` chip is overlaid, top-right.
- Everything below (stats / equations / flavour) stays put.

So: **put the card's name in the image.**

## Shape & safe area

- Target the hero box: **~55 × 26 mm, i.e. about 2.1 : 1** (landscape).
- The image is scaled to **fill** and **centre-cropped** (`object-fit: cover`),
  biased slightly upward (`object-position: 50% 18%`) so faces/heads survive.
- 3 : 2 or 16 : 9 source art works fine — expect the lower third to be cropped.
  Keep the title and any faces in the **upper ~65 %**; keep nothing important in
  the outer ~2 mm (the frame sits on the edge).
- Vector (`svg`) prints sharpest. For raster, ~1500 px wide is plenty; a whole
  deck of multi-MB files makes a heavy `.html`, so ~150–400 KB each is ideal.

Ask if you want the box taller/shorter, the crop focal point moved (globally or
per card), or full-bleed to the cut edge.

## Regenerate

```bash
python tools/gen_cards.py       # characters
python tools/gen_env_cards.py   # environments
python tools/gen_pet_cards.py   # pets
```

Art is base64-embedded, so each `cards/*.html` stays a single self-contained
file you can email or "Print to PDF" from anywhere.
