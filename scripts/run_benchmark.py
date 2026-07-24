#!/usr/bin/env python3

import argparse
import csv
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


# ======================
# Path Config
# ======================

# Repo root: this script lives in <repo>/scripts/, so go up one level.
ROOT = Path(__file__).resolve().parent.parent

PDF_DIR = ROOT / "benchmarks" / "documents"

RESULT_DIR = ROOT / "results"

DEFAULT_TIMEOUT = 600


# ======================
# Utils
# ======================

def ensure_dir(path):
    path.mkdir(
        parents=True,
        exist_ok=True
    )


def tool_available(command):
    """True when an executable is on PATH."""

    return shutil.which(command) is not None


def resolve_bin(env_var, command):
    """Resolve an executable path: env override (TOOL_BIN) first, then PATH.

    Lets each tool point at a binary inside an isolated venv
    (uv tool / pipx / manual venv) without relying on the global PATH.
    """

    explicit = os.environ.get(env_var)

    if explicit and Path(explicit).exists():
        return explicit

    return shutil.which(command)


def importable(module):
    """True when a Python module can be imported in the current interpreter."""

    try:
        __import__(module)
        return True
    except Exception:
        return False


def cleanup(path, keep_raw):
    """Remove a raw working dir unless --keep-raw was set."""

    if keep_raw:
        return

    if path and path.exists():
        shutil.rmtree(path, ignore_errors=True)


def char_count(path):
    """Characters in a file (utf-8, replace on bad bytes)."""

    try:
        return len(
            path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        )
    except Exception:
        return 0


def write_text(path, text):
    """Write text to a file; return the character count."""

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text or "")

    return len(text or "")


def run_command(command, timeout, cwd=None):
    """Run a command list safely (no shell)."""

    start = time.time()

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            cwd=cwd
        )

        cost = round(
            time.time() - start,
            2
        )

        return {
            "success": result.returncode == 0,
            "time": cost,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "time": round(time.time() - start, 2),
            "stdout": "",
            "stderr": f"timeout after {timeout}s"
        }

    except Exception as e:

        return {
            "success": False,
            "time": 0,
            "stdout": "",
            "stderr": str(e)
        }


def build_result(run, chars, no_output_hint="empty output"):
    """Decide success from both the process run AND non-empty output."""

    if not run["success"]:

        err = (run.get("stderr") or "").strip()
        reason = err[-500:] if err else "(command failed)"

        success = False

    elif chars == 0:

        reason = no_output_hint
        success = False

    else:

        reason = "ok"
        success = True

    return {
        "success": success,
        "time": run["time"],
        "chars": chars,
        "reason": reason
    }


def finalize_output(stem, source_dir, target):
    """Locate the produced markdown (recursive) and copy it to the
    canonical target path. Returns (found, chars).

    Marker / MinerU / docling write into nested, non-fixed layouts,
    so we search by stem first, then fall back to any .md file.
    """

    candidates = sorted(
        Path(source_dir).rglob(f"{stem}.md")
    )

    if not candidates:
        candidates = sorted(
            Path(source_dir).rglob("*.md")
        )

    if not candidates:
        return False, 0

    shutil.copyfile(candidates[0], target)

    return True, char_count(target)


# ======================
# Parsers
# ======================


def run_markitdown(pdf, output, timeout, keep_raw):

    bin_path = resolve_bin("MARKITDOWN_BIN", "markitdown")

    run = run_command(
        [bin_path, str(pdf)],
        timeout
    )

    chars = write_text(output, run["stdout"])

    return build_result(run, chars)


# docling fallback when the CLI is missing: run the Python API
# through a temp file (avoids the fragile `python3 -c '...'` quoting).

DOCLING_PY = '''\
import sys
from docling.document_converter import DocumentConverter

pdf = sys.argv[1]
out = sys.argv[2]

converter = DocumentConverter()

result = converter.convert(pdf)

markdown = result.document.export_to_markdown()

with open(out, "w", encoding="utf-8") as f:
    f.write(markdown or "")
'''


def run_docling(pdf, output, timeout, keep_raw):

    work_dir = output.parent / "docling_output"

    ensure_dir(work_dir)

    bin_path = resolve_bin("DOCLING_BIN", "docling")

    # Prefer the docling CLI (`docling convert ...`).
    # docling has no --output-dir, so we run it with cwd=work_dir
    # and let it write <stem>.md into that folder.
    if bin_path:

        run = run_command(
            [
                bin_path,
                "convert",
                str(pdf),
                "--to", "md"
            ],
            timeout,
            cwd=work_dir
        )

        if not run["success"]:
            cleanup(work_dir, keep_raw)
            return build_result(run, 0)

        found, chars = finalize_output(
            pdf.stem,
            work_dir,
            output
        )

        cleanup(work_dir, keep_raw)

        return build_result(
            run,
            chars,
            "no markdown found in docling output dir" if not found else "empty output"
        )

    # Fallback: Python API via a temp script (docling installed as a lib
    # in this interpreter).
    script_path = work_dir / "_convert.py"

    script_path.write_text(
        DOCLING_PY,
        encoding="utf-8"
    )

    run = run_command(
        [sys.executable, str(script_path), str(pdf), str(output)],
        timeout
    )

    chars = char_count(output) if output.exists() else 0

    cleanup(work_dir, keep_raw)

    return build_result(run, chars)


def run_marker(pdf, output, timeout, keep_raw):

    work_dir = output.parent / "marker_output"

    ensure_dir(work_dir)

    bin_path = resolve_bin("MARKER_BIN", "marker_single")

    run = run_command(
        [
            bin_path,
            str(pdf),
            "--output_dir", str(work_dir),
            "--output_format", "markdown"
        ],
        timeout
    )

    if not run["success"]:
        cleanup(work_dir, keep_raw)
        return build_result(run, 0)

    found, chars = finalize_output(
        pdf.stem,
        work_dir,
        output
    )

    cleanup(work_dir, keep_raw)

    return build_result(
        run,
        chars,
        "no markdown found in marker output dir" if not found else "empty output"
    )


def run_mineru(pdf, output, timeout, keep_raw):

    work_dir = output.parent / "mineru_output"

    ensure_dir(work_dir)

    bin_path = resolve_bin("MINERU_BIN", "mineru")

    # -b pipeline: lighter, CPU-friendly, no multi-GB VLM model download.
    # Switch to the default (hybrid-engine) only if you want VLM accuracy
    # and have the bandwidth/time for the first-run model download.
    run = run_command(
        [
            bin_path,
            "-p", str(pdf),
            "-o", str(work_dir),
            "-b", "pipeline"
        ],
        timeout
    )

    if not run["success"]:
        cleanup(work_dir, keep_raw)
        return build_result(run, 0)

    found, chars = finalize_output(
        pdf.stem,
        work_dir,
        output
    )

    cleanup(work_dir, keep_raw)

    return build_result(
        run,
        chars,
        "no markdown found in mineru output dir" if not found else "empty output"
    )


TOOLS = {

    "markitdown": {
        "command": "markitdown",
        "env_var": "MARKITDOWN_BIN",
        "available": lambda: resolve_bin("MARKITDOWN_BIN", "markitdown") is not None,
        "runner": run_markitdown
    },

    "docling": {
        "command": "docling",
        "env_var": "DOCLING_BIN",
        "available": lambda: (
            resolve_bin("DOCLING_BIN", "docling") is not None
            or importable("docling")
        ),
        "runner": run_docling
    },

    "marker": {
        "command": "marker_single",
        "env_var": "MARKER_BIN",
        "available": lambda: resolve_bin("MARKER_BIN", "marker_single") is not None,
        "runner": run_marker
    },

    "mineru": {
        "command": "mineru",
        "env_var": "MINERU_BIN",
        "available": lambda: resolve_bin("MINERU_BIN", "mineru") is not None,
        "runner": run_mineru
    }
}


# ======================
# Reporting
# ======================


def write_reports(report):

    md_file = RESULT_DIR / "benchmark-report.md"
    csv_file = RESULT_DIR / "benchmark-report.csv"

    # ---- markdown ----

    with open(
        md_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("# PDF Parser Benchmark Report\n\n")

        f.write("| PDF | Tool | Status | Time | Chars | Note |\n")
        f.write("|---|---|---|---|---|---|\n")

        for item in report:

            status = "✅" if item["success"] else "❌"

            note = (
                (item["reason"] or "")
                .replace("|", "/")
                .replace("\n", " ")
            )[:120]

            f.write(
                f"| {item['pdf']} | "
                f"{item['tool']} | "
                f"{status} | "
                f"{item['time']}s | "
                f"{item['chars']} | "
                f"{note} |\n"
            )

        # per-tool summary

        f.write("\n## Summary by tool\n\n")

        f.write("| Tool | Success | Rate | Avg time | Best time | Total chars |\n")
        f.write("|---|---|---|---|---|---|\n")

        for tool in dict.fromkeys(i["tool"] for i in report):

            items = [i for i in report if i["tool"] == tool]

            ran = [
                i for i in items
                if i["reason"] != "skipped (exists)"
            ]

            base = ran if ran else items

            ok = sum(1 for i in base if i["success"])

            times = [i["time"] for i in base if i["time"] > 0]

            avg = round(sum(times) / len(times), 2) if times else 0

            best = round(min(times), 2) if times else 0

            total_chars = sum(i["chars"] for i in items)

            rate = (
                f"{round(ok / len(base) * 100)}%"
                if base else "0%"
            )

            f.write(
                f"| {tool} | "
                f"{ok}/{len(base)} | "
                f"{rate} | "
                f"{avg}s | "
                f"{best}s | "
                f"{total_chars} |\n"
            )

    # ---- csv ----

    with open(
        csv_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["pdf", "tool", "success", "time", "chars", "reason"]
        )

        for item in report:

            writer.writerow([
                item["pdf"],
                item["tool"],
                item["success"],
                item["time"],
                item["chars"],
                item["reason"]
            ])

    return md_file, csv_file


# ======================
# Main
# ======================


def parse_args():

    parser = argparse.ArgumentParser(
        description="PDF parser benchmark"
    )

    parser.add_argument(
        "--tools",
        default="",
        help="comma-separated tool names (default: all)"
    )

    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="skip PDFs that already have non-empty output"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"per-PDF timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )

    parser.add_argument(
        "--keep-raw",
        action="store_true",
        help="keep raw nested output dirs (marker/mineru/docling)"
    )

    return parser.parse_args()


def select_tools(args):

    if not args.tools.strip():
        return dict(TOOLS)

    names = [
        t.strip() for t in args.tools.split(",")
        if t.strip()
    ]

    unknown = [n for n in names if n not in TOOLS]

    if unknown:
        print(f"❌ Unknown tools: {unknown}")
        print(f"   Available: {list(TOOLS.keys())}")
        return None

    return {n: TOOLS[n] for n in names}


def main():

    args = parse_args()

    print("====================")
    print("PDF Benchmark Start")
    print("====================")

    # select tools

    selected = select_tools(args)

    if not selected:
        return

    # availability pre-check

    ready = {}

    for name, info in selected.items():

        ok = info["available"]()

        ready[name] = ok

        mark = "✅ installed" if ok else "⚠️  not installed"
        print(f"  {name}: {mark}")

    # check pdf folder

    if not PDF_DIR.exists():

        print(f"❌ pdfs directory not found: {PDF_DIR}")

        return

    pdf_files = sorted(
        PDF_DIR.glob("*.pdf")
    )

    if not pdf_files:

        print("❌ No PDF files found")
        print(f"   Put PDFs into: {PDF_DIR}")

        return

    print(f"✅ Found {len(pdf_files)} PDFs")

    for pdf in pdf_files:
        print(f"  - {pdf.name}")

    ensure_dir(RESULT_DIR)

    report = []

    # run benchmark

    for pdf in pdf_files:

        print("\n====================")
        print(f"Testing: {pdf.name}")
        print("====================")

        for tool, info in selected.items():

            tool_dir = RESULT_DIR / tool
            output = tool_dir / f"{pdf.stem}.md"

            # skip existing (resume)

            if (
                args.skip_existing
                and output.exists()
                and output.stat().st_size > 0
            ):

                chars = char_count(output)

                print(f"\n▶ {tool}: ⏭️  skipped (exists)")

                report.append({
                    "pdf": pdf.name,
                    "tool": tool,
                    "success": True,
                    "time": 0.0,
                    "chars": chars,
                    "reason": "skipped (exists)"
                })

                continue

            # not installed

            if not ready.get(tool):

                print(f"\n▶ {tool}: ⚠️  skip (not installed)")

                report.append({
                    "pdf": pdf.name,
                    "tool": tool,
                    "success": False,
                    "time": 0.0,
                    "chars": 0,
                    "reason": "not_installed"
                })

                continue

            # run

            print(f"\n▶ {tool}")

            ensure_dir(tool_dir)

            result = info["runner"](
                pdf,
                output,
                args.timeout,
                args.keep_raw
            )

            status = "✅" if result["success"] else "❌"

            print(
                f"  {status} {result['time']}s "
                f"chars={result['chars']}"
            )

            if not result["success"]:
                print(
                    f"  reason: {result['reason'][:200]}"
                )

            report.append({
                "pdf": pdf.name,
                "tool": tool,
                "success": result["success"],
                "time": result["time"],
                "chars": result["chars"],
                "reason": result["reason"]
            })

    # reports

    md_file, csv_file = write_reports(report)

    print("\n====================")
    print("✅ Benchmark Finished")
    print("====================")

    print(f"Report: {md_file}")
    print(f"CSV:    {csv_file}")


if __name__ == "__main__":

    main()
