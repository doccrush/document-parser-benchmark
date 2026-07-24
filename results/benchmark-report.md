# PDF Parser Benchmark Report

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

## Summary by tool

| Tool | Success | Rate | Avg time | Best time | Total chars |
|---|---|---|---|---|---|
| markitdown | 5/5 | 100% | 1.71s | 0.44s | 183242 |
| docling | 5/5 | 100% | 52.15s | 9.72s | 130026922 |
| marker | 4/5 | 80% | 345.67s | 4.9s | 152983 |
| mineru | 5/5 | 100% | 81.49s | 21.8s | 164609 |

> Note: docling's character total is dominated by the NVIDIA run (126,173,302 chars ≈ 126 MB), where images were embedded as base64. This inflates both its output size and average runtime relative to its actual parsing throughput.
