# Document Parser Benchmark — v0.1 Results

> **Status:** AI-assisted preliminary scoring of actual parser outputs, **pending human review**.
> **Date:** 2026-07 · **Parsers:** 4 · **Documents:** 5

The first release of this benchmark. Four open-source parsers were run on five real-world PDFs covering the cases that actually break in production RAG: multi-column academic layout, large technical reports, financial tables, image-heavy reports, and dense text.

## Headline ranking

Scores are weighted across five dimensions (Reading Order 30% / Heading Structure 20% / Table Extraction 25% / OCR Quality 15% / Markdown Quality 10%), each 0–5. See [`scoring-v0.1.md`](./scoring-v0.1.md) for the per-document breakdown.

| Rank | Parser | Weighted avg | Docs scored | Reliability | Avg time |
|:---:|---|:---:|:---:|:---:|:---:|
| 🥇 | **MinerU** | **3.28** | 5/5 | 5/5 ✅ | 81s |
| 🥈 | **Docling** | **3.15** | 5/5 | 5/5 ✅ | 52s† |
| 🥉 | **Marker** | 3.91 ⚠️ | 4/5 | 4/5 ⚠️ | 346s |
| 4 | **MarkItDown** | 1.78 | 5/5 | 5/5 ✅ | 1.7s |

> ⚠️ **Marker's 3.91 is sample-biased and not directly comparable.** It timed out on the 17 MB NVIDIA report, so it was scored on 4/5 documents while skipping the largest, hardest file. Read it as "best on the files it could finish," not "best overall." On a level playing field, MinerU and Docling are the strongest.
>
> † Docling's average time is inflated by base64 image embedding (see [caveats](./caveats.md)).

## Per-document weighted scores

| Document | Type | MarkItDown | Docling | Marker | MinerU |
|---|---|:---:|:---:|:---:|:---:|
| NIPS — Attention Is All You Need | Multi-column academic | 1.70 | **4.55** | 3.60 | 4.15 |
| NVIDIA technical report (17 MB) | Technical, large | 2.40 | **2.95** | ⏱ timeout | 2.90 |
| FY25 Q2 financial statements | Tables | 1.55 | **4.75** | 3.55 | 2.45 |
| State of Enterprise AI 2025 | Image-heavy | 2.10 | 0.00 | **4.00** | 3.15 |
| Congressional Record (CREC) | Dense text | 1.15 | 3.50 | **4.50** | 3.75 |

## What each parser is good at

- **MinerU** — the safe default. Ran every document, no catastrophic failures, best math/equation quality, references images as files instead of inlining them. Weakness: tables come out as HTML `<table>`, not Markdown.
- **Docling** — highest ceiling, unstable. The only parser to produce a clean financial table with correct values. But its default base64 image embedding turned an image-heavy report into a 0 and one file into 126 MB of Markdown.
- **Marker** — best structure and layout restoration. But slow (VLM inference, avg 346s) and it hung for 20 minutes on the largest file.
- **MarkItDown** — blindingly fast (avg 1.7s) and produces clean plain text, but with almost no Markdown structure, shattered tables, and garbled spacing. Not suitable as a primary RAG parser.

## Known data-quality caveats

These affect the scores and are reported honestly. Details in [`caveats.md`](./caveats.md):

1. **Docling base64 images** — the `state-of-enterprise-ai` (0.00) and NVIDIA (MD=1) failures are caused by default image embedding, not raw parsing ability. Rerunning with `--image-export-mode placeholder` should lift Docling's ranking.
2. **Marker NVIDIA timeout** — CPU VLM inference on a 17 MB multi-page file exceeded the 1200s limit. `--mode fast` avoids it at a small accuracy cost.
3. **CREC language** — `CREC-2026-07-21-dailydigest` is the U.S. Congressional Record (English), not a non-English daily digest; it was scored on its actual English content.

## Raw data

- Per-document, per-dimension scores: [`scoring-v0.1.md`](./scoring-v0.1.md)
- Run log, timing, success/failure: [`benchmark-report.md`](./benchmark-report.md)
- Machine-readable: [`benchmark-report.csv`](./benchmark-report.csv)

## What's next (v0.2)

- Rerun Docling with `--image-export-mode placeholder` and Marker with `--mode fast` to remove the two biggest biases.
- Add a scanned/OCR-native document (none in v0.1).
- Human review of the AI-assisted scores.
- Add more parsers (e.g. Unstructured, LlamaParse open components).
