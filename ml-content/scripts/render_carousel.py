"""
ml-content — carousel render template.

Reads a single carousel.html, splits into per-slide sections,
renders each as a 1080×1350 PNG via weasyprint → PDF → pdftoppm.

CLI:
  python render_carousel.py        # render all slides
  python render_carousel.py 5 5    # just slide 5
  python render_carousel.py 1 3    # slides 1-3

Edit SRC and OUT for your project.
"""

import re
import subprocess
import sys
from pathlib import Path

import weasyprint

# -----------------------------------------------------------------------------
# Paths — edit for your project
# -----------------------------------------------------------------------------

SRC = Path("/path/to/project/carousel.html")
OUT = Path("/path/to/project/slides")
OUT.mkdir(parents=True, exist_ok=True)

TMP = Path("/tmp/ml-content-render")
TMP.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# @page CSS — locks 1080×1350, removes margins / shadows / labels
# -----------------------------------------------------------------------------

PAGE_CSS = (
    "<style>"
    "@page { size: 1080px 1350px; margin: 0; } "
    "html,body { background: #0E1014 !important; margin:0 !important; padding:0 !important; } "
    "body { display: block !important; gap: 0 !important; } "
    ".slide { margin:0 !important; box-shadow: none !important; } "
    ".slide-label { display: none !important; }"
    "</style>"
)

# -----------------------------------------------------------------------------
# Render
# -----------------------------------------------------------------------------

def main():
    html = SRC.read_text()
    head_match = re.search(r"<head>.*?</head>", html, re.DOTALL)
    if not head_match:
        sys.exit("carousel.html missing <head>")
    head = head_match.group(0)

    slides = re.findall(
        r'(<section class="slide"[^>]*id="s\d+"[^>]*>.*?</section>)',
        html, re.DOTALL,
    )
    print(f"found {len(slides)} slides", flush=True)
    if not slides:
        sys.exit("no <section class='slide' id='sN'> found")

    # CLI args
    start, end = 1, len(slides)
    if len(sys.argv) >= 3:
        start, end = int(sys.argv[1]), int(sys.argv[2])

    for idx in range(start, end + 1):
        sh = slides[idx - 1]
        doc = f"<!DOCTYPE html><html>{head}{PAGE_CSS}<body>{sh}</body></html>"

        pdf = TMP / f"slide_{idx:02d}.pdf"
        weasyprint.HTML(string=doc, base_url=str(SRC.parent)).write_pdf(str(pdf))

        out_prefix = OUT / f"slide_{idx:02d}"
        out_png = OUT / f"slide_{idx:02d}.png"
        if out_png.exists():
            out_png.unlink()

        subprocess.run(
            ["pdftoppm", "-png", "-r", "96", "-singlefile",
             str(pdf), str(out_prefix)],
            capture_output=True, text=True,
        )
        size = out_png.stat().st_size if out_png.exists() else 0
        print(f"slide {idx}: {size} bytes", flush=True)

    print("done.")


if __name__ == "__main__":
    main()
