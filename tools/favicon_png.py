#!/usr/bin/env python3
"""Build the PNG favicon fallbacks from favicon.svg (CONCEPT.md section 9).

Build-time tool only. Renders the hand-authored favicon.svg with headless
Chromium (Playwright) at high resolution, then downsamples with Pillow (LANCZOS)
for crisp anti-aliasing at the small target sizes:

  favicon-32.png       32x32,   ink on transparent (matches the SVG)
  apple-touch-icon.png 180x180, ink on the solid ground colour

The apple-touch-icon is flattened onto the ground rather than left transparent:
iOS composites a transparent touch icon onto black, which would invert the mark,
so it gets the site ground (#FAFAFA) to stay on-brand. Noted in PROGRESS.md.

Usage (run from anywhere, paths resolve from this file):
  python tools/favicon_png.py

House rules: UK English, no em dashes. Vanilla toolchain, no runtime deps.
"""

import os

from PIL import Image
from playwright.sync_api import sync_playwright

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)

SVG = os.path.join(REPO_ROOT, "favicon.svg")
RAW_PNG = os.path.join(TOOLS_DIR, "_raw", "favicon-raw.png")

GROUND = (250, 250, 250)  # --ground #FAFAFA
RENDER = 512              # oversample, then downsample for clean edges

# (output filename, size in px, background) -> None background keeps alpha.
TARGETS = [
    ("favicon-32.png", 32, None),
    ("apple-touch-icon.png", 180, GROUND),
]


def render_master():
    """Render favicon.svg to a large transparent PNG master."""
    os.makedirs(os.path.dirname(RAW_PNG), exist_ok=True)
    with open(SVG, "r", encoding="utf-8") as f:
        svg = f.read()
    html = (
        "<!doctype html><meta charset='utf-8'>"
        "<style>*{margin:0;padding:0}"
        "html,body{width:%dpx;height:%dpx;background:transparent}"
        "svg{width:%dpx;height:%dpx;display:block}</style>%s"
        % (RENDER, RENDER, RENDER, RENDER, svg)
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": RENDER, "height": RENDER},
            device_scale_factor=1,
        )
        page.set_content(html)
        page.wait_for_timeout(100)
        page.screenshot(path=RAW_PNG, omit_background=True)
        browser.close()


def build_targets():
    master = Image.open(RAW_PNG).convert("RGBA")
    for name, size, bg in TARGETS:
        out = os.path.join(REPO_ROOT, name)
        scaled = master.resize((size, size), Image.LANCZOS)
        if bg is None:
            scaled.save(out, format="PNG", optimize=True)
        else:
            flat = Image.new("RGB", (size, size), bg)
            flat.paste(scaled, mask=scaled.split()[3])
            flat.save(out, format="PNG", optimize=True)
        kb = os.path.getsize(out) / 1024
        with Image.open(out) as im:
            print("%s: %dx%d %s, %.1f KB" % (name, im.size[0], im.size[1], im.mode, kb))


def main():
    render_master()
    build_targets()


if __name__ == "__main__":
    main()
