# Benchmark dataset

Six PDFs (v0.2) chosen to stress the failure modes that matter for RAG — multi-column layout, large files, tables, image-heavy pages, dense text, and OCR. Five are real-world publications a parser might encounter in production; one (`scanned-report-cc0`) is a synthesized image-only PDF added in v0.2 to exercise OCR with a known ground truth.

## What each document stresses

| Stress dimension | Why it breaks parsers | Document |
|---|---|---|
| Multi-column layout | Reading order gets interleaved or scrambled | NIPS — *Attention Is All You Need* |
| Math & equations | Formulas garbled or concatenated without spaces | NIPS — *Attention Is All You Need* |
| Dense numerical tables | Values shifted, columns merged, structure lost | FY25 Q2 financial statements |
| Large multi-page file | Slow inference, memory, timeouts | NVIDIA technical report (17 MB) |
| Image-heavy pages | Images inlined as base64, text lost | State of Enterprise AI 2025 |
| Dense formal text | Heading hierarchy and structure detection | Congressional Record (CREC) |
| **Scanned / OCR** (v0.2) | **No text layer — parser must OCR** | **scanned-report-cc0** |

> v0.1 had no scanned/OCR document; v0.2 adds `scanned-report-cc0` (image-only, synthesized from CC0 text). See [`results/benchmark-v0.2.md`](../results/benchmark-v0.2.md).

## Evaluation goal

Each parser's Markdown output is scored on five dimensions weighted for RAG quality — reading order, heading structure, table extraction, OCR/text accuracy, and Markdown cleanliness. Full rubric: [`results/scoring-v0.2.md`](../results/scoring-v0.2.md).

## File listing

See [`documents/README.md`](./documents/README.md) for the per-document descriptions and provenance.
