import sys, glob, time, json
from playwright.sync_api import sync_playwright

TAG = sys.argv[1] if len(sys.argv) > 1 else "before"
OUT = r"C:\Dev\portfolio\verify\cta-pass"
URL = "http://localhost:8823/index.html"
EDGE = sorted(glob.glob(r"C:\Program Files (x86)\Microsoft\EdgeCore\*\msedge.exe"))[-1]

CTA_SEL = ".row--cta"
LIST_SEL = ".index-list"

def clip_of(page, sel, pad_x, pad_top, pad_bottom):
    box = page.eval_on_selector(sel, "el => { const r = el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; }")
    return {
        "x": max(box["x"] - pad_x, 0),
        "y": max(box["y"] - pad_top, 0),
        "width": box["w"] + pad_x * 2,
        "height": box["h"] + pad_top + pad_bottom,
    }

def dump_vars(page):
    js = """() => {
      const cs = getComputedStyle(document.documentElement);
      const names = ['--cta-layer1','--cta-layer2','--cta-layer3','--cta-bg-size',
        '--cta-lightpass','--cta-edge-lift','--cta-rim','--cta-hover-mist','--cta-press-mist',
        '--cta-text','--cta-index','--shadow-row-active','--accent-hairline','--accent'];
      const o = {theme: document.documentElement.getAttribute('data-theme')};
      for (const n of names) o[n] = cs.getPropertyValue(n).trim();
      const ctaCS = getComputedStyle(document.querySelector('.row--cta'));
      o['cta.boxShadow'] = ctaCS.boxShadow;
      o['cta.backgroundImage'] = ctaCS.backgroundImage;
      return o;
    }"""
    return page.evaluate(js)

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EDGE, headless=True, args=["--no-sandbox","--disable-gpu"])
    for theme in ("light", "dark"):
        page = browser.new_page(viewport={"width":1440,"height":900}, device_scale_factor=2)
        page.goto(URL, wait_until="networkidle")
        page.evaluate("t => { localStorage.setItem('pagefront-theme', t); }", theme)
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(400)
        results[theme] = dump_vars(page)

        # rest crop (tight, ground visible on all sides)
        page.mouse.move(1200, 500)  # park cursor away
        page.wait_for_timeout(300)
        page.screenshot(path=f"{OUT}\\{TAG}-{theme}-rest.png", clip=clip_of(page, CTA_SEL, 24, 20, 20))

        # full row-list context
        page.screenshot(path=f"{OUT}\\{TAG}-{theme}-fullrow.png", clip=clip_of(page, LIST_SEL, 20, 16, 16))

        # hover crop
        page.hover(CTA_SEL)
        page.wait_for_timeout(1100)  # let filter settle + mist lag catch up
        page.screenshot(path=f"{OUT}\\{TAG}-{theme}-hover.png", clip=clip_of(page, CTA_SEL, 24, 20, 20))

        page.close()
    browser.close()

with open(f"{OUT}\\{TAG}-vars.json", "w") as f:
    json.dump(results, f, indent=2)
print(json.dumps(results, indent=2))
