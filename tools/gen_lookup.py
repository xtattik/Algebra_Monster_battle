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


def emit_rows(pairs, xs=range(1, 7)) -> None:
    """Like emit_table, but for an explicit, pre-computed (n, c) list rather
    than a full ns x cs grid — used where only some combinations are ever
    reachable."""
    for n, c in pairs:
        sign = "" if c == 0 else (f" + {c}" if c > 0 else f" − {abs(c)}")
        label = f"{n}x{sign}" if n >= 0 else f"−{abs(n)}x{sign}"
        vals = [max(0, n * x + c) for x in xs]
        print(f"| {label} | " + " | ".join(str(v) for v in vals) + " |")


def challenge_rows():
    """Every (n, c) an assembled Challenge attack can reach. Each base attack
    is (a, c); a modifier is a character +-x plus an environment +-2x/+-x,
    net in {-3..3} (every integer in range is reachable). n = a + delta,
    excluding n = 0 (handled separately in the rulebook as a bare constant).
    Positive n can occur too — a small enough negative a can be pushed
    positive by a full favourable stack — so this isn't just negative rows."""
    templates = [(-1, 5), (-2, 8), (-4, 13)]  # (a, c) for N1, N2, N4
    out = []
    for a, c in templates:
        ns = sorted({a + d for d in range(-3, 4) if a + d != 0}, reverse=True)
        out += [(n, c) for n in ns]
    return out


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    # v2: a 4x affinity attack + character +x + environment Boost +2x = 7x;
    # give one row of headroom to 8x.
    print("### Core (n = 1x .. 8x, c = -3..3)")
    print()
    emit_table(range(1, 9), range(-3, 4))
    print()
    print("### Extra: c = 4 (the Challenge glass-cannon bracket 4(x+1) = 4x+4;")
    print("### reachable n is 1..7, one 4x affinity + up to +-3 from modifiers)")
    print()
    print("| expr | x=1 | x=2 | x=3 | x=4 | x=5 | x=6 |")
    print("|---|---|---|---|---|---|---|")
    emit_rows([(n, 4) for n in range(7, 0, -1)])
    print()
    print("### Challenge deck rows (v2) — grouped by base attack (N1/N2/N4)")
    print()
    print("| expr | x=1 | x=2 | x=3 | x=4 | x=5 | x=6 |")
    print("|---|---|---|---|---|---|---|")
    emit_rows(challenge_rows())


if __name__ == "__main__":
    main()
