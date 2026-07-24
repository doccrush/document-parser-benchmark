# PDF Parser Benchmark Report

Raw run log: per-document success, time, and output size. **v0.1** = original settings (docling `embedded` images, marker `balanced`). **v0.2** = de-biased (docling `--image-export-mode placeholder`, marker `--mode fast`) plus the new scanned document. markitdown/mineru were rerun on the scanned doc only in v0.2.

## v0.1

| PDF | Tool | Status | Time | Chars | Note |
|---|---|---|---|---|---|
| CREC-2026-07-21-dailydigest.pdf | markitdown | ✅ | 0.89s | 85489 | ok |
| CREC-2026-07-21-dailydigest.pdf | docling | ✅ | 9.72s | 95827 | ok |
| CREC-2026-07-21-dailydigest.pdf | marker | ✅ | 6.25s | 66494 | ok |
| CREC-2026-07-21-dailydigest.pdf | mineru | ✅ | 242.57s | 63408 | ok |
| FY25_Q2_Consolidated_Financial_Statements.pdf | markitdown | ✅ | 0.48s | 18578 | ok |
| FY25_Q2_Consolidated_Financial_Statements.pdf | docling | ✅ | 11.76s | 20480 | ok |
| FY25_Q2_Consolidated_Financial_Statements.pdf | marker | ✅ | 4.9s | 16875 | ok |
| FY25_Q2_Consolidated_Financial_Statements.pdf | mineru | ✅ | 21.8s | 10528 | ok |
| NIPS-2017-attention-is-all-you-need-Paper.pdf | markitdown | ✅ | 0.51s | 31687 | ok |
| NIPS-2017-attention-is-all-you-need-Paper.pdf | docling | ✅ | 17.31s | 336847 | ok |
| NIPS-2017-attention-is-all-you-need-Paper.pdf | marker | ✅ | 305.11s | 37913 | ok |
| NIPS-2017-attention-is-all-you-need-Paper.pdf | mineru | ✅ | 37.51s | 37513 | ok |
| NVIDIA.pdf | markitdown | ✅ | 0.44s | 13672 | ok |
| NVIDIA.pdf | docling | ✅ | 208.4s | 126173302 | ok |
| NVIDIA.pdf | marker | ❌ | 1200.11s | 0 | timeout after 1200s |
| NVIDIA.pdf | mineru | ✅ | 60.98s | 21052 | ok |
| the-state-of-enterprise-ai_2025-report.pdf | markitdown | ✅ | 6.24s | 33816 | ok |
| the-state-of-enterprise-ai_2025-report.pdf | docling | ✅ | 13.58s | 3400466 | ok |
| the-state-of-enterprise-ai_2025-report.pdf | marker | ✅ | 211.97s | 31701 | ok |
| the-state-of-enterprise-ai_2025-report.pdf | mineru | ✅ | 44.61s | 32108 | ok |

## v0.2 (de-biased reruns + scanned doc)

| PDF | Tool | Status | Time | Chars | Note |
|---|---|---|---|---|---|
| CREC-2026-07-21-dailydigest.pdf | docling | ✅ | 11.55s | 74093 | placeholder |
| CREC-2026-07-21-dailydigest.pdf | marker | ✅ | 17.63s | 66494 | fast |
| FY25_Q2_Consolidated_Financial_Statements.pdf | docling | ✅ | 14.7s | 20480 | placeholder |
| FY25_Q2_Consolidated_Financial_Statements.pdf | marker | ✅ | 5.52s | 16875 | fast |
| NIPS-2017-attention-is-all-you-need-Paper.pdf | docling | ✅ | 30.48s | 43329 | placeholder (was 336847) |
| NIPS-2017-attention-is-all-you-need-Paper.pdf | marker | ✅ | 83.66s | 37913 | fast (was 305.11s) |
| NVIDIA.pdf | docling | ✅ | 286.33s | 13960 | placeholder (was 126173302) |
| NVIDIA.pdf | marker | ❌ | 1200.03s | 0 | timeout after 1200s — fast |
| scanned-report-cc0.pdf | markitdown | ✅ | 0.32s | 1 | no OCR (no text layer) |
| scanned-report-cc0.pdf | docling | ✅ | 26.28s | 1290 | placeholder (OCR) |
| scanned-report-cc0.pdf | marker | ✅ | 550.06s | 1501 | fast (OCR) |
| scanned-report-cc0.pdf | mineru | ✅ | 23.45s | 1572 | OCR |
| the-state-of-enterprise-ai_2025-report.pdf | docling | ✅ | 14.87s | 280 | placeholder (was 3400466) |
| the-state-of-enterprise-ai_2025-report.pdf | marker | ✅ | 194.15s | 31701 | fast |

## v0.2 summary by tool

| Tool | Success | Rate | Avg time | Best time |
|---|---|---|---|---|
| markitdown | 6/6 | 100% | 1.48s | 0.32s |
| docling | 6/6 | 100% | 64.04s | 11.55s |
| marker | 5/6 | 83% | 170.20s | 5.52s |
| mineru | 6/6 | 100% | 71.82s | 21.8s |

> Times use v0.2 runs where rerun (docling/marker on all six; markitdown/mineru on the scanned doc) and v0.1 runs otherwise. Marker's average excludes the timed-out NVIDIA file. Output-character totals are omitted in v0.2 because the placeholder/fast reruns make them non-comparable across tools (docling's v0.1 base64 totals were meaningless); per-run chars are in the tables above and in [`benchmark-report.csv`](./benchmark-report.csv).
