#!/usr/bin/env python3
"""Char-level OCR accuracy for the synthesized scanned document.

Compares each parser's Markdown output for `scanned-report-cc0.pdf` against
the known ground truth (`scanned-ground-truth.txt`) using a normalized
character-level similarity (difflib SequenceMatcher). This gives an objective,
reproducible number to support the 0-5 OCR Quality score in scoring-v0.2.md.

Usage:
  python scripts/ocr_accuracy.py
  python scripts/ocr_accuracy.py --results results --stem scanned-report-cc0
"""

import argparse
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESULTS = ROOT / "results"
DEFAULT_GT = ROOT / "benchmarks" / "documents" / "scanned-ground-truth.txt"
TOOLS = ["markitdown", "docling", "marker", "mineru"]


def normalize(s: str) -> str:
    """Lowercase, drop markdown/table markup, collapse whitespace."""
    s = s.lower()
    s = re.sub(r"[#|*`>_~]", " ", s)          # strip markdown markers
    s = re.sub(r"[^0-9a-z\s.,()@/-]", " ", s)  # keep readable chars
    s = re.sub(r"\s+", " ", s).strip()
    return s


def char_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def word_recall(gt: str, extracted: str) -> float:
    gt_words = set(gt.split())
    if not gt_words:
        return 0.0
    got = set(extracted.split())
    return len(gt_words & got) / len(gt_words)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=str(DEFAULT_RESULTS))
    ap.add_argument("--gt", default=str(DEFAULT_GT))
    ap.add_argument("--stem", default="scanned-report-cc0")
    args = ap.parse_args()

    results = Path(args.results)
    gt = normalize(Path(args.gt).read_text(encoding="utf-8", errors="replace"))
    print(f"ground-truth chars (normalized): {len(gt)}\n")

    rows = []
    for tool in TOOLS:
        out = results / tool / f"{args.stem}.md"
        if not out.exists():
            print(f"  {tool:12s} (no output at {out})")
            rows.append((tool, None, None))
            continue
        extracted = normalize(out.read_text(encoding="utf-8", errors="replace"))
        sim = char_similarity(gt, extracted)
        recall = word_recall(gt, extracted)
        rows.append((tool, sim, recall))
        print(f"  {tool:12s} char-similarity={sim:.3f}  word-recall={recall:.3f}  (extracted {len(extracted)} chars)")

    print("\nsummary (sorted by char-similarity):")
    for tool, sim, recall in sorted([r for r in rows if r[1] is not None], key=lambda r: r[1], reverse=True):
        print(f"  {tool:12s} {sim:.3f}")


if __name__ == "__main__":
    main()
