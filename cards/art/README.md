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

**Only the number has to be right.** `09-grave-hound.jpg`, `09-gravehound.jpg`,
`09-anything.jpg`, or bare `09.jpg` all bind to card 9 — the slug is decoration.
Check the numbers against the deck's `.md` source (`## N.` headings), since
inserting or renaming cards can shift them.

## What a card with art looks like

When a card has art it switches to **hero mode**:

- The image fills the **top ~26 mm** of the card (full inner width, ~55 mm).
- The card's **printed name header is dropped** — the name is expected to be in
  the artwork. Only a small `N/total` chip is overlaid, top-right.
- Everything below (stats / equations / flavour) stays put.

So: **put the card's name in the image.**

## Shape & safe area

- The hero box on the card is **~55 × 26 mm** wide-landscape.
- **Black letterbox bars are trimmed automatically** before embedding (if
  `Pillow` is installed — `pip install Pillow`). So if your art tool pads a
  non-10:3 export to a fixed canvas with black, that padding is removed; the
  card sees just your artwork. Without Pillow the file is embedded as-is.
- After trimming, the image is **left-anchored and centre-cropped**
  (`object-fit: cover`, `object-position: 0% 45%`) — the box is a touch
  narrower than typical trimmed art, so the **right edge** is what gets clipped.
  Keep your title on the **left**, and nothing essential in the outer ~3 mm.
- Anything from ~2 : 1 to ~2.8 : 1 lands with almost no crop. 3 : 2 works too
  (its sides get clipped a little more).
- Vector (`svg`) prints sharpest and is never trimmed/recompressed. Raster is
  re-saved as JPEG q88 and downscaled to 1800 px wide, so source file size
  barely matters — a ~1500 px+ export is plenty.

Ask if you want the box taller/shorter, the crop anchor moved (globally or per
card), or full-bleed to the cut edge.

## Regenerate

```bash
python tools/gen_cards.py       # characters
python tools/gen_env_cards.py   # environments
python tools/gen_pet_cards.py   # pets
```

Art is base64-embedded, so each `cards/*.html` stays a single self-contained
file you can email or "Print to PDF" from anywhere.
