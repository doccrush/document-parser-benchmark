# PDF Parser Benchmark — Scoring Sheet v0.2

> **AI-assisted preliminary scoring** of the actual Markdown outputs, **pending human review**.
> Weights: Reading Order 30% / Heading Structure 20% / Table Extraction 25% / OCR Quality 15% / Markdown Quality 10%. Each dimension 0–5.

## What changed in v0.2

Two de-biasing reruns + one new document:

- **Docling** rerun with `--image-export-mode placeholder` (v0.1 used `embedded`, which inlined base64 and produced a 126 MB file). The base64 bloat is gone (NVIDIA: 126 MB → 14 KB).
- **Marker** rerun with `--mode fast` (v0.1 used `balanced`, whose VLM timed out on the 17 MB NVIDIA report). Fast mode is much faster (NIPS: 305 s → 84 s) but **still times out on the 17 MB NVIDIA report**, so Marker's average remains sample-biased (5/6 docs).
- **New scanned document** (`scanned-report-cc0.pdf`, image-only, no text layer) — the first real OCR test. OCR accuracy is also measured objectively as char-level similarity vs the known ground truth (`scripts/ocr_accuracy.py`).

markitdown and mineru were rerun **only on the new scanned doc**; their v0.1 scores stand for the other five.

## 1. Detail scores (0–5)

RO = Reading Order · HS = Heading Structure · TE = Table Extraction · OCR = OCR Quality · MD = Markdown Quality

| PDF | Tool | RO | HS | TE | OCR | MD |
|---|---|:---:|:---:|:---:|:---:|:---:|
| NIPS (two-column paper) | markitdown | 2 | 1 | 2 | 2 | 1 |
| | docling | 5 | 4 | 5 | 4 | 4 |
| | marker | 5 | 3 | 3 | 3 | 3 |
| | mineru | 5 | 5 | 2 | 5 | 4 |
| NVIDIA (technical report) | markitdown | 3 | 1 | 2 | 4 | 2 |
| | docling | 4 | 4 | 1 | 4 | 3 |
| | marker | N/A | N/A | N/A | N/A | N/A |
| | mineru | 4 | 3 | 1 | 3 | 4 |
| FY25 (financial statements) | markitdown | 2 | 1 | 1 | 2 | 2 |
| | docling | 5 | 5 | 4 | 5 | 5 |
| | marker | 4 | 4 | 2 | 5 | 3 |
| | mineru | 3 | 4 | 1 | 2 | 2 |
| state-of-enterprise-ai | markitdown | 2 | 1 | 2 | 4 | 2 |
| | docling | 0 | 0 | 0 | 0 | 2 |
| | marker | 4 | 4 | 4 | 4 | 4 |
| | mineru | 4 | 3 | 3 | 2 | 3 |
| CREC (Congressional Record) | markitdown | 1 | 1 | 1 | 2 | 1 |
| | docling | 4 | 2 | 4 | 4 | 3 |
| | marker | 5 | 5 | 3 | 5 | 5 |
| | mineru | 5 | 3 | 2 | 5 | 4 |
| scanned-report-cc0 (NEW, OCR) | markitdown | 1 | 1 | 1 | 1 | 1 |
| | docling | 4 | 4 | 2 | 5 | 4 |
| | marker | 5 | 5 | 5 | 5 | 5 |
| | mineru | 4 | 4 | 2 | 4 | 3 |

## 2. Weighted total (out of 5)

| PDF | markitdown | docling | marker | mineru |
|---|:---:|:---:|:---:|:---:|
| NIPS | 1.70 | 4.55 | 3.60 | 4.15 |
| NVIDIA | 2.40 | 3.15 | N/A | 2.90 |
| FY25 | 1.55 | 4.75 | 3.55 | 2.45 |
| state-of-enterprise-ai | 2.10 | 0.20 | 4.00 | 3.15 |
| CREC | 1.15 | 3.50 | 4.50 | 3.75 |
| scanned-report-cc0 | 1.00 | 3.65 | 5.00 | 3.40 |
| **Weighted average** | **1.65** | **3.30** | **4.13\*** | **3.30** |
| # documents scored | 6 | 6 | 5 | 6 |

**Ranking: marker 4.13\* > docling 3.30 = mineru 3.30 > markitdown 1.65**

\* Marker is scored on 5/6 documents — it **still times out on the 17 MB NVIDIA report even in `fast` mode**, so its average is **not directly comparable** to the others. On a level playing field (all six documents), **Docling and MinerU tie at 3.30** as the strongest overall.

## 3. OCR accuracy on the scanned document (objective)

Char-level similarity and word recall of each parser's output vs the known ground truth (`scripts/ocr_accuracy.py`):

| Parser | Char similarity | Word recall | Extracted |
|---|:---:|:---:|:---:|
| docling | **0.988** | 0.971 | 1229 chars |
| marker | 0.964 | 0.993 | 1306 chars |
| mineru | 0.898 | **1.000** | 1440 chars |
| markitdown | 0.000 | 0.000 | 0 chars (no OCR) |

Notable: on a clean scan, **Marker reconstructed the data table as a perfect Markdown pipe table with every value correct** — the strongest table-via-OCR result in the benchmark. Docling OCR'd the prose best (0.988) but collapsed the table into one line. Mineru recovered every word (1.000 recall) but with more character-level noise and an HTML `<table>` mess. MarkItDown has no OCR capability and returned nothing.

## 4. Per-tool movement vs v0.1

- **docling 3.15 → 3.30.** The base64 bloat is fixed (NVIDIA 126 MB → 14 KB, MD 1→3; NIPS 337 K → 43 K). But this exposed an honest remaining weakness: docling does **not OCR image-heavy pages by default**, so `state-of-enterprise-ai` still returns near-empty output (image placeholders, 0.20). It does, however, OCR a clean scan excellently (0.988).
- **marker 3.91\* → 4.13\*.** Fast mode is far quicker (NIPS 305 s → 84 s; average 346 s → 170 s) and produced byte-identical output to v0.1 on four docs. But **NVIDIA still times out**, so the sample-bias caveat persists. It aced the new scanned doc (5.00 — perfect table via OCR).
- **mineru 3.28 → 3.30.** Unchanged on the original five; solid OCR on the scan (3.40, all words recalled).
- **markitdown 1.78 → 1.65.** Slightly lower only because the new scanned doc (which it cannot OCR, 1.00) drags the average. Still fastest by far.

## 5. RAG selection guidance (updated)

- Want stability / general purpose → **mineru** (runs everything, balanced, no bloat)
- Want tables / financial docs → **docling** (best on digital tables; OCRs clean scans well)
- Want layout / structure / scanned tables → **marker** (accept slow + big-file timeout risk)
- Want OCR of clean scans → **docling** or **marker** (both ≥0.96); avoid markitdown
- Want speed / rough draft → **markitdown** (high quality cost; no OCR)
