# Document Parser Benchmark

> An open, reproducible benchmark of open-source document parsers for RAG & LLM pipelines. Real documents, real failures, honest scores.

[![Benchmark](https://img.shields.io/badge/benchmark-v0.1-blue)](./results/benchmark-v0.1.md)
[![Documents](https://img.shields.io/badge/documents-5-green)](./benchmarks/documents)
[![Parsers](https://img.shields.io/badge/parsers-4-orange)](#tested-parsers)
[![Status](https://img.shields.io/badge/status-AI--assisted%20preliminary-yellow)](./results/caveats.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

Document parsing is the single biggest source of silent failures in RAG pipelines. A parser that scrambles reading order, drops tables, or flattens headings produces clean-looking Markdown that quietly destroys retrieval quality. This project measures exactly that — on real documents, with the failures left in.

---

## TL;DR

We ran **4 open-source parsers** on **5 real-world PDFs** (academic, financial, technical, image-heavy, dense-text) and scored every output on **5 dimensions weighted for RAG quality**.

| Rank | Parser | Weighted (0–5) | Reliability | Avg time | Best for |
|:---:|---|:---:|:---:|:---:|---|
| 🥇 | **MinerU** | **3.28** | 5/5 ✅ | 81s | General-purpose — balanced, no blow-ups, image-safe |
| 🥈 | **Docling** | **3.15** | 5/5 ✅ | 52s† | Tables & financial docs (disable base64 first) |
| 🥉 | **Marker** | 3.91 ⚠️ | 4/5 ⚠️ | 346s | Structure & layout (slow, big-file timeout risk) |
| 4 | **MarkItDown** | 1.78 | 5/5 ✅ | 1.7s | Fast drafts only (quality cost is high) |

> ⚠️ **Marker's 3.91 is not directly comparable.** It timed out on the 17 MB NVIDIA report and was scored on only 4/5 documents — conveniently skipping the largest file. On a level playing field, **MinerU and Docling are the strongest overall**. Full breakdown: [`results/caveats.md`](results/caveats.md).
>
> † Docling's average time is inflated by its default base64 image embedding — one output ballooned to **126 MB of Markdown**. See caveats.

---

## Why this project?

Most parser comparisons show a tidy table of green checkmarks. The interesting information lives in what *fails*: which parser turns a financial table into garbage, which one embeds every image as a multi-megabyte string, which one hangs for 20 minutes on a large file. We report those failures, because that's what actually matters when you pick a parser for production RAG.

Poor extraction quality cascades into:

- broken document structure and reading order
- lost or corrupted tables
- missing heading hierarchy
- bad chunk boundaries
- inaccurate retrieval, and wrong LLM answers

---

## Tested parsers

| Parser | Repo | Role |
|---|---|---|
| **MinerU** | [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | PDF parsing + OCR framework |
| **Docling** | [ds-4-real/docling](https://github.com/ds-4-real/docling) | Document intelligence toolkit |
| **Marker** | [VikParuchuri/marker](https://github.com/VikParuchuri/marker) | PDF parser with strong layout understanding |
| **MarkItDown** | [microsoft/markitdown](https://github.com/microsoft/markitdown) | Document-to-Markdown converter |

The runner is [`scripts/run_benchmark.py`](scripts/run_benchmark.py). It invokes each parser's CLI, times every run, and records success/failure plus output size.

---

## Methodology

Each parser output is scored **0–5** on five dimensions, weighted toward what actually moves RAG quality:

| Dimension | Weight | What it measures |
|---|:---:|---|
| Reading Order | 30% | Multi-column flow, logical sequence preserved |
| Heading Structure | 20% | Hierarchy detected, nesting correct |
| Table Extraction | 25% | Tables survive as usable Markdown, values intact |
| OCR Quality | 15% | Text accuracy, math/equations, no garbling |
| Markdown Quality | 10% | Cleanliness, spacing, no base64 bloat, RAG-readiness |

Scores are an **AI-assisted preliminary assessment** of the actual Markdown outputs in `results/`, **pending human review**. The raw scoring rubric and per-document scores are in [`results/scoring-v0.1.md`](results/scoring-v0.1.md).

---

## Results

### Per-document weighted scores (0–5)

| Document | Type | MarkItDown | Docling | Marker | MinerU |
|---|---|:---:|:---:|:---:|:---:|
| NIPS — Attention Is All You Need | Multi-column academic | 1.70 | **4.55** | 3.60 | 4.15 |
| NVIDIA technical report (17 MB) | Technical, large | 2.40 | **2.95** | ⏱ N/A | 2.90 |
| FY25 Q2 financial statements | Tables | 1.55 | **4.75** | 3.55 | 2.45 |
| State of Enterprise AI 2025 | Image-heavy | 2.10 | 0.00 | **4.00** | 3.15 |
| Congressional Record (CREC) | Dense text | 1.15 | 3.50 | **4.50** | 3.75 |

### Speed & reliability

| Parser | Success | Avg time | Best time | Total output |
|---|:---:|:---:|:---:|:---:|
| MarkItDown | 5/5 | 1.71s | 0.44s | 183 KB |
| Docling | 5/5 | 52.15s | 9.72s | 130 MB† |
| Marker | 4/5 | 345.67s | 4.9s | 153 KB |
| MinerU | 5/5 | 81.49s | 21.8s | 165 KB |

† Docling's output total is dominated by one file (NVIDIA) where images were embedded as base64, producing a 126 MB Markdown file.

Full raw data: [`results/benchmark-report.md`](results/benchmark-report.md) · [`results/benchmark-report.csv`](results/benchmark-report.csv)

---

## How to pick a parser

| You need… | Use | Caveat |
|---|---|---|
| A safe default / general purpose | **MinerU** | Tables come out as HTML, not Markdown pipes |
| Best tables & financial docs | **Docling** | Disable base64 image embedding first |
| Best structure & layout | **Marker** | Slow; large files may time out |
| A fast rough draft | **MarkItDown** | Expect broken tables and missing headings |

---

## Reproduce

See [`REPRODUCING.md`](REPRODUCING.md) for environment setup, the isolated-install notes for each parser, and the exact commands. Then:

```bash
python scripts/run_benchmark.py --timeout 1200
```

---

## Related project

[**DocCrush**](https://doccrush.com) — an online document processing workflow that converts documents into clean Markdown optimized for AI/RAG applications. This benchmark exists to be honest about the trade-offs in the open-source landscape.

---

## Contributing

Found a parser failure we missed? Have a document that breaks these tools in a new way? Open an issue with the document and the parser output, or submit a pull request. We especially welcome:

- additional challenging documents (with permission to redistribute)
- corrections to the AI-assisted scores after human review
- new parsers added to the runner

## License

[MIT](./LICENSE) — both the benchmark code and the curated results. Individual source documents retain their original licenses (see [`benchmarks/documents/README.md`](benchmarks/documents/README.md)).
