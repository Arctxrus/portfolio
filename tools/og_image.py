#!/usr/bin/env python3
"""Build og-image.png, the 1200x630 social share card (CONCEPT.md section 9).

Build-time tool only. Renders tools/og_source.html at exactly 1200x630 with
headless Chromium (Playwright), using the project's own self-hosted fonts and
design tokens, then flattens the shot onto the solid ground colour (no alpha)
with Pillow and writes og-image.png to the repo root. The page never loads this
file: it is only referenced from the <head> og:image / twitter:image meta and
is fetched by crawlers, not on normal page load.

Usage (run from anywhere, paths resolve from this file):
  python tools/og_image.py

House rules: UK English, no em dashes. Vanilla toolchain, no runtime deps.
"""

import os

from PIL import Image
from playwright.sync_api import sync_playwright

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)

SOURCE = os.path.join(TOOLS_DIR, "og_source.html")
RAW_PNG = os.path.join(TOOLS_DIR, "_raw", "og-image-raw.png")
OUT_PNG = os.path.join(REPO_ROOT, "og-image.png")

WIDTH, HEIGHT = 1200, 630
GROUND = (250, 250, 250)  # --ground #FAFAFA, the flattening colour


def render():
    os.makedirs(os.path.dirname(RAW_PNG), exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Device scale factor 1 so the screenshot is exactly 1200x630 pixels.
        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=1,
        )
        page.goto("file:///" + SOURCE.replace(os.sep, "/"))
        # Wait for the self-hosted fonts to load so the type is the site's own,
        # not a fallback, before the shot.
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(200)
        page.screenshot(path=RAW_PNG, clip={"x": 0, "y": 0, "width": WIDTH, "height": HEIGHT})
        browser.close()


def flatten():
    # Composite onto opaque ground and drop the alpha channel, then optimise.
    img = Image.open(RAW_PNG).convert("RGBA")
    flat = Image.new("RGB", img.size, GROUND)
    flat.paste(img, mask=img.split()[3])
    flat.save(OUT_PNG, format="PNG", optimize=True)


def main():
    render()
    flatten()
    kb = os.path.getsize(OUT_PNG) / 1024
    with Image.open(OUT_PNG) as im:
        w, h = im.size
        mode = im.mode
    print("og-image.png: %dx%d %s, %.1f KB" % (w, h, mode, kb))
    if (w, h) != (WIDTH, HEIGHT):
        raise SystemExit("ERROR: og-image is not exactly %dx%d" % (WIDTH, HEIGHT))
    if mode != "RGB":
        raise SystemExit("ERROR: og-image still has an alpha channel")


if __name__ == "__main__":
    main()
