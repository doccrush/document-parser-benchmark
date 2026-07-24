# Benchmark dataset

Five real-world PDFs chosen to stress the failure modes that matter for RAG — multi-column layout, large files, tables, image-heavy pages, and dense text. No synthetic or generated documents: every file is a real publication a parser might encounter in production.

## What each document stresses

| Stress dimension | Why it breaks parsers | Document |
|---|---|---|
| Multi-column layout | Reading order gets interleaved or scrambled | NIPS — *Attention Is All You Need* |
| Math & equations | Formulas garbled or concatenated without spaces | NIPS — *Attention Is All You Need* |
| Dense numerical tables | Values shifted, columns merged, structure lost | FY25 Q2 financial statements |
| Large multi-page file | Slow inference, memory, timeouts | NVIDIA technical report (17 MB) |
| Image-heavy pages | Images inlined as base64, text lost | State of Enterprise AI 2025 |
| Dense formal text | Heading hierarchy and structure detection | Congressional Record (CREC) |

> v0.1 does **not** include a scanned/native-OCR document. That's a known gap scheduled for v0.2 — see [`results/benchmark-v0.1.md`](../results/benchmark-v0.1.md).

## Evaluation goal

Each parser's Markdown output is scored on five dimensions weighted for RAG quality — reading order, heading structure, table extraction, OCR/text accuracy, and Markdown cleanliness. Full rubric: [`results/scoring-v0.1.md`](../results/scoring-v0.1.md).

## File listing

See [`documents/README.md`](./documents/README.md) for the per-document descriptions and provenance.
