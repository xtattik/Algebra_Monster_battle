# tools/gen_lookup.py — emits fast-marking tables as Markdown.
# Usage: python tools/gen_lookup.py > lookup.md  then paste the body in.
import sys


def emit_table(ns, cs, xs=range(1, 7)) -> None:
    header = "| expr | " + " | ".join(f"x={x}" for x in xs) + " |"
    sep = "|" + "---|" * (len(list(xs)) + 1)
    print(header)
    print(sep)
    for n in ns:
        for c in cs:
            sign = "" if c == 0 else (f" + {c}" if c > 0 else f" − {abs(c)}")
            label = f"{n}x{sign}" if n >= 0 else f"−{abs(n)}x{sign}"
            vals = [max(0, n * x + c) for x in xs]
            print(f"| {label} | " + " | ".join(str(v) for v in vals) + " |")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    print("### Core (n = 1x .. 6x)")
    print()
    emit_table(range(1, 7), range(-3, 4))
    print()
    print("### Challenge negative-coefficient rows (n = -1x .. -6x)")
    print()
    emit_table(range(-1, -7, -1), (5, 8, 10))


if __name__ == "__main__":
    main()
