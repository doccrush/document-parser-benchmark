#!/usr/bin/env python3
"""Synthesize a scanned (image-only, no text layer) PDF for OCR benchmarking.

Renders a short CC0-dedicated source text to page images, applies mild scan
artifacts (grayscale + noise + slight rotation), and writes a multi-page PDF
with NO embedded text layer — forcing parsers to run OCR. The exact source
text is also written to a ground-truth file so OCR accuracy can be scored
deterministically (see ocr_accuracy.py).

Outputs:
  benchmarks/documents/scanned-report-cc0.pdf
  benchmarks/documents/scanned-ground-truth.txt
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "benchmarks" / "documents"
PDF_PATH = OUT_DIR / "scanned-report-cc0.pdf"
GT_PATH = OUT_DIR / "scanned-ground-truth.txt"

# CC0 source text — authored here, public domain. Exercises OCR on prose,
# headings, a data table, decimals, units, a phone number and an email.
TEXT = """\
# Crestview Municipal Water Quality Report — 2025

## Summary

This report presents the annual water quality testing results for the Crestview service area. Samples were collected from twelve distribution sites between January and October 2025. All measured values met or exceeded the state minimum standards during the reporting period.

The average daily consumption across the service area was approximately 4.8 million gallons, a decrease of roughly 7 percent compared with the previous year.

## Detected Contaminants

| Parameter | Result (mg/L) | Limit (mg/L) | Status |
| Lead       | 0.004 | 0.015 | Pass |
| Nitrate    | 2.30  | 10.0  | Pass |
| Copper     | 0.082 | 1.30  | Pass |
| Chlorine   | 1.10  | 4.0   | Pass |
| Fluoride   | 0.65  | 4.0   | Pass |

## Field Notes

Field measurements were taken at a depth of 0.5 meters using calibrated probes. Laboratory analysis followed EPA method 200.8. The turbidity reading of 0.12 NTU was well below the regulatory threshold of 0.3 NTU, and the average pH held steady at 7.4 across all sites.

Total dissolved solids ranged from 180 mg/L to 240 mg/L. No volatile organic compounds were detected above the reporting limit of 0.0005 mg/L.

## Contact

For questions about this report, contact the utility office at (555) 014-2273 or write to water@crestview.example.gov.
"""

# Page geometry (~A4 at 150 dpi)
PAGE_W, PAGE_H = 1240, 1754
MARGIN = 110

FONT_CANDIDATES = {
    "sans": [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ],
    "mono": [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ],
}


def load_font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES[kind]:
        if Path(path).exists():
            try:
                # .ttc needs an index
                return ImageFont.truetype(path, size, index=0)
            except Exception:
                continue
    return ImageFont.load_default()


def text_width(font, draw: ImageDraw.ImageDraw, s: str) -> int:
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]


def wrap_prose(font, draw, s: str, max_w: int) -> list[str]:
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(font, draw, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def style_for(line: str):
    if line.startswith("# "):
        return "title"
    if line.startswith("## "):
        return "heading"
    if line.startswith("|"):
        return "table"
    return "body"


def render_label(raw: str, style: str):
    """Strip markdown markers for display, keep the logical text."""
    if style == "title":
        return raw[2:].strip()
    if style == "heading":
        return raw[3:].strip()
    return raw


def render_pages() -> list[Image.Image]:
    title_f = load_font("sans", 40)
    head_f = load_font("sans", 30)
    body_f = load_font("sans", 26)
    mono_f = load_font("mono", 24)

    max_w = PAGE_W - 2 * MARGIN
    pages = []
    img = Image.new("L", (PAGE_W, PAGE_H), 255)
    draw = ImageDraw.Draw(img)
    y = MARGIN

    def new_page():
        nonlocal img, draw, y
        pages.append(img)
        img = Image.new("L", (PAGE_W, PAGE_H), 255)
        draw = ImageDraw.Draw(img)
        return MARGIN

    for raw in TEXT.splitlines():
        if raw.strip() == "":
            y += 18
            continue
        style = style_for(raw)
        font = {"title": title_f, "heading": head_f, "table": mono_f, "body": body_f}[style]
        label = render_label(raw, style)
        lines = [label] if style in ("title", "heading", "table") else wrap_prose(font, draw, label, max_w)
        if style in ("title", "heading"):
            y += 14  # extra space before
        for ln in lines:
            lh = int(font.size * 1.5)
            if y + lh > PAGE_H - MARGIN:
                y = new_page()
            draw.text((MARGIN, y), ln, fill=0, font=font)
            y += lh
        if style in ("title", "heading"):
            y += 10  # extra space after

    pages.append(img)
    return pages


def scan_effect(img: Image.Image, rng: np.random.Generator) -> Image.Image:
    arr = np.asarray(img).astype(np.int16)
    # mild Gaussian noise
    arr = arr + rng.normal(0, 9, arr.shape).astype(np.int16)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    out = Image.fromarray(arr, mode="L")
    # slight rotation to mimic a crooked scan
    angle = float(rng.uniform(-1.6, 1.6))
    out = out.rotate(angle, resample=Image.BICUBIC, fillcolor=255)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)  # deterministic for reproducibility
    pages = [scan_effect(p, rng) for p in render_pages()]
    pages[0].save(PDF_PATH, save_all=True, append_images=pages[1:], format="PDF")
    GT_PATH.write_text(TEXT, encoding="utf-8")
    print(f"wrote {PDF_PATH} ({PDF_PATH.stat().st_size} bytes, {len(pages)} pages)")
    print(f"wrote {GT_PATH} ({GT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
