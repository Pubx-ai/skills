#!/usr/bin/env python3
"""Look up authoritative AdTech doc sources from the bundled reference CSV.

Usage: python3 lookup.py <term> [<term> ...]
A row matches when every term appears (case-insensitive) in its name,
organization, category, or keywords. Rows whose name matches a term rank
first (a name hit is almost always the intended source), then by priority
(P0 first).
"""
import csv
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "references" / "reference-sources.csv"


def main() -> int:
    terms = [t.lower() for t in sys.argv[1:]]
    if not terms:
        print(__doc__.strip())
        return 2
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    hits = []
    for r in rows:
        haystack = " ".join(
            (r.get(k) or "") for k in ("source_name", "organization", "category", "keywords")
        ).lower()
        if all(t in haystack for t in terms):
            hits.append(r)
    def rank(r):
        name = (r.get("source_name") or "").lower()
        name_hit = 0 if any(t in name for t in terms) else 1
        return (name_hit, r.get("priority") or "P9", r.get("source_name") or "")

    hits.sort(key=rank)
    if not hits:
        print(f"no match for: {' '.join(terms)} — try a broader single term")
        return 1
    for r in hits:
        print(f"[{r['priority']}] {r['source_name']} — {r['organization']} ({r['category']})")
        print(f"    urls:   {r['reference_urls']}")
        print(f"    type:   {r['source_type']} | access: {r['access']}")
        if (r.get("notes") or "").strip():
            print(f"    notes:  {r['notes']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
