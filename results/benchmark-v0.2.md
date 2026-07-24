# Document Parser Benchmark — v0.2 Results

> **Status:** AI-assisted preliminary scoring of actual parser outputs, **pending human review**.
> **Date:** 2026-07 · **Parsers:** 4 · **Documents:** 6 · **vs v0.1:** de-biased Docling & Marker, added an OCR (scanned) document.

v0.2 removes the two biggest v0.1 biases and fills the OCR gap.

## Headline ranking

| Rank | Parser | Weighted avg | Docs scored | Reliability | Avg time |
|:---:|---|:---:|:---:|:---:|:---:|
| 🥇 | **Marker** | **4.13** ⚠️ | 5/6 | 5/6 ⚠️ | 170s |
| 🥈 | **Docling** | **3.30** | 6/6 | 6/6 ✅ | 64s |
| 🥈 | **MinerU** | **3.30** | 6/6 | 6/6 ✅ | 72s |
| 4 | **MarkItDown** | 1.65 | 6/6 | 6/6 ✅ | 1.5s |

> ⚠️ **Marker's 4.13 is still not directly comparable.** Even in `fast` mode it **timed out (1200 s) on the 17 MB NVIDIA report**, so it was scored on 5/6 documents while skipping the largest file. **On a level playing field (all six documents), Docling and MinerU tie at 3.30 as the strongest overall.**

## What v0.2 changed (vs v0.1)

1. **Docling base64 bias → resolved.** Rerun with `--image-export-mode placeholder`. The 126 MB NVIDIA file became 14 KB; the 337 KB NIPS file became 43 KB. Markdown Quality no longer tanks from base64 bloat.
2. **Marker timeout bias → partially resolved.** Rerun with `--mode fast` (avg 346 s → 170 s). It finished five docs (often with byte-identical output to v0.1) but **still times out on the 17 MB NVIDIA report** — so the sample-bias caveat stays.
3. **OCR gap → filled.** Added `scanned-report-cc0.pdf`, an image-only PDF (no text layer) synthesized from CC0 text, with a known ground truth for objective scoring.

## OCR results (the new data point)

On the scanned document (char-level similarity vs ground truth):

| Parser | Char sim | Word recall | Table |
|---|:---:|:---:|---|
| docling | **0.988** | 0.971 | collapsed to one line |
| marker | 0.964 | 0.993 | **perfect Markdown pipe table** |
| mineru | 0.898 | **1.000** | HTML `<table>` mess |
| markitdown | 0.000 | 0.000 | — (no OCR) |

Two surprises worth flagging: **Docling OCRs a clean scan better than anyone (0.988)** despite failing on the complex image-heavy report, and **Marker reconstructed the scanned table perfectly via OCR** — the best table result in the whole benchmark.

## Honest open issues (see [`caveats.md`](./caveats.md))

- **Marker cannot process the 17 MB NVIDIA report** in either `balanced` or `fast` mode within 1200 s on CPU. Its average therefore excludes the hardest file.
- **Docling does not OCR image-heavy pages by default** — `state-of-enterprise-ai` returns only image placeholders (0.20). It OCRs a clean scan fine, so this is a per-document-layout behavior, not a blanket OCR failure.
- **MinerU emits tables as HTML**, not Markdown pipe tables.
- **MarkItDown has no OCR** — it returns nothing from a scanned page.

## Raw data

- Per-document, per-dimension scores: [`scoring-v0.2.md`](./scoring-v0.2.md)
- Run log, timing, success/failure (v0.1 + v0.2): [`benchmark-report.md`](./benchmark-report.md)
- Machine-readable: [`benchmark-report.csv`](./benchmark-report.csv)
- v0.1 archive: [`benchmark-v0.1.md`](./benchmark-v0.1.md) · [`scoring-v0.1.md`](./scoring-v0.1.md)
