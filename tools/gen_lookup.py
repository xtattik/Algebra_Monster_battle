# tools/gen_lookup.py — emits the fast-marking table as Markdown.
# Usage: python tools/gen_lookup.py > lookup.md  then paste the body in.
import sys


def main() -> None:
    # The table uses U+2212 (−); force UTF-8 so it prints on Windows consoles too.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    ns = range(1, 7)          # coefficient 1..6
    cs = range(-3, 4)         # constant -3..3
    xs = range(1, 7)          # die faces
    header = "| expr | " + " | ".join(f"x={x}" for x in xs) + " |"
    sep = "|" + "---|" * (len(list(xs)) + 1)
    print(header)
    print(sep)
    for n in ns:
        for c in cs:
            label = f"{n}x" + ("" if c == 0 else (f" + {c}" if c > 0 else f" − {abs(c)}"))
            vals = [max(0, n * x + c) for x in xs]
            print(f"| {label} | " + " | ".join(str(v) for v in vals) + " |")

if __name__ == "__main__":
    main()
