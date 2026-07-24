# Data-quality caveats — what actually broke

> The honest part of the benchmark. Most parser comparisons publish a tidy green table and hide the failures. We don't — these are the findings that most change how you should read the scores, and they're the reason "highest score" ≠ "best parser for you." Updated for **v0.2** (status noted per item).

## 1. Docling + image-heavy PDFs — base64 fixed (v0.2); OCR-of-images still missing

**v0.1 problem (fixed).** Docling inlined every image as base64 by default, producing a 126 MB NVIDIA file and making `state-of-enterprise-ai` unusable. **v0.2 reruns Docling with `--image-export-mode placeholder`** — the bloat is gone (NVIDIA 126 MB → 14 KB; NIPS 337 KB → 43 KB).

**What v0.2 revealed (still open).** Strip the base64 and an honest limitation appears: **Docling does not OCR image-heavy pages by default.** `state-of-enterprise-ai` now returns just `<!-- image -->` placeholders (280 bytes, scored 0.20) — the document's text lives in page images Docling won't OCR. Notably, Docling **does** OCR a clean, simple scan excellently (0.988 char-similarity on the scanned doc), so this is a per-layout behavior (complex multi-image pages), not a blanket OCR failure.

**Impact:** v0.1 `state` Docling = 0.00 (base64) → v0.2 = 0.20 (no text, but clean format); NVIDIA Docling MD 1 → 3 (bloat gone).

## 2. Marker + large files on CPU — timeout PERSISTS in v0.2 (fast mode)

Marker's VLM layout model is too slow on CPU for the 17 MB, multi-page NVIDIA report. **v0.2 reruns Marker with `--mode fast`** (lightweight CPU detectors). It is much faster on other docs (NIPS 305 s → 84 s; average 346 s → 170 s) and produced byte-identical output to v0.1 on four of them — but **the 17 MB NVIDIA report still exceeds the 1200 s timeout and produces nothing, even in fast mode.**

So the sample-bias caveat **still applies**: Marker is scored on 5/6 documents, skipping the largest, hardest file. Its 4.13 average is **not directly comparable** to the others. On a level playing field (all six documents), **Docling and MinerU tie at 3.30 as the strongest overall.** A GPU run would likely change this.

**Impact:** Marker NVIDIA = N/A in both v0.1 and v0.2; averages over 5 docs, not 6.

## 3. MinerU emits tables as HTML, not Markdown

MinerU is the most reliable parser — it ran every document with no disasters and references images as files (no base64 bloat). But its tables come out as HTML `<table>` blocks rather than Markdown pipe tables. If your RAG pipeline expects pure Markdown, MinerU's tables may not be parsed as tables without a preprocessing step (this cost it table-extraction scores, e.g. FY25 = 1, and a messy HTML+pipe hybrid on the scanned doc). Trade-off, not a defect — but you only discover it after deployment.

## 4. The "CREC daily digest" is the U.S. Congressional Record (in English)

`CREC-2026-07-21-dailydigest.pdf` is the **Congressional Record** — English-language proceedings of the U.S. Congress — not a non-English daily digest as the filename might suggest. Scored on its actual English content. Noted so anyone reproducing the test isn't confused about language/content type.

## 5. OCR: clean scans vs. complex image-heavy pages behave very differently (new in v0.2)

v0.2 adds the first OCR test (`scanned-report-cc0.pdf`, image-only). The spread is wide and instructive:

| Parser | Char-similarity | Word recall | What it did with the scanned table |
|---|:---:|:---:|---|
| docling | **0.988** | 0.971 | best prose OCR; **collapsed the table to one line** |
| marker | 0.964 | 0.993 | **perfect Markdown pipe table, every value correct** |
| mineru | 0.898 | **1.000** | all words; HTML `<table>` + pipe hybrid mess |
| markitdown | 0.000 | 0.000 | **no OCR** — returned 1 character |

Two things to internalize: (a) **MarkItDown has no OCR at all** — a scanned page yields nothing; (b) **Docling OCRs a clean scan best but still fails on the complex image-heavy report** — OCR quality depends heavily on page complexity, not just "does it OCR."

---

## Why we report this

A benchmark that only shows the winners is an ad. The useful information — for anyone building a real RAG pipeline — is the failure mode of each tool, because that's what you'll hit in production. Treat the caveats above as the actual decision criteria:

| You care about… | Avoid | Prefer |
|---|---|---|
| Image-heavy / complex page PDFs | Docling (won't OCR them) | Marker, MinerU |
| Large multi-page PDFs on CPU | Marker (timeout) | MinerU, Docling |
| Pure-Markdown table pipelines | MinerU (HTML tables) | Docling, Marker |
| Scanned / OCR input | MarkItDown (no OCR) | Docling or Marker |
| Anything mission-critical | MarkItDown (low quality) | MinerU |

See [`scoring-v0.2.md`](./scoring-v0.2.md) for the full per-document scores, [`benchmark-v0.2.md`](./benchmark-v0.2.md) for the v0.2 headline, and [`scoring-v0.1.md`](./scoring-v0.1.md) / [`benchmark-v0.1.md`](./benchmark-v0.1.md) for the v0.1 archive.
