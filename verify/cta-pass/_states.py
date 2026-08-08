import glob
from playwright.sync_api import sync_playwright
OUT = r"C:\Dev\portfolio\verify\cta-pass"
URL = "http://localhost:8823/index.html"
EDGE = sorted(glob.glob(r"C:\Program Files (x86)\Microsoft\EdgeCore\*\msedge.exe"))[-1]
CTA = ".row--cta"

def clip(page, sel, px, pt, pb):
    b = page.eval_on_selector(sel, "el=>{const r=el.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}}")
    return {"x":max(b["x"]-px,0),"y":max(b["y"]-pt,0),"width":b["w"]+px*2,"height":b["h"]+pt+pb}

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EDGE, headless=True, args=["--no-sandbox","--disable-gpu"])
    page = br.new_page(viewport={"width":1440,"height":900}, device_scale_factor=2)
    page.goto(URL, wait_until="networkidle")
    page.evaluate("localStorage.setItem('pagefront-theme','light')")
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(400)
    page.mouse.move(1200, 500)

    # OPEN / grown: click CTA -> is-open (grow + card shadow). Park cursor away after.
    page.click(CTA)
    page.wait_for_timeout(500)
    page.mouse.move(1200, 500)
    page.wait_for_timeout(300)
    print("is-open:", page.eval_on_selector(CTA, "el=>el.classList.contains('is-open')"))
    page.screenshot(path=f"{OUT}\\after-light-open.png", clip=clip(page, CTA, 24, 22, 26))

    # FOCUS-VISIBLE: force focus-visible via focus({focusVisible:true})
    page.eval_on_selector(CTA, "el=>el.focus({focusVisible:true})")
    page.wait_for_timeout(200)
    fv = page.eval_on_selector(CTA, "el=>el.matches(':focus-visible')")
    print("focus-visible match:", fv, "| shadow:", page.eval_on_selector(CTA, "el=>getComputedStyle(el).boxShadow"))
    page.mouse.move(1200, 500)
    page.wait_for_timeout(150)
    page.screenshot(path=f"{OUT}\\after-light-focus-open.png", clip=clip(page, CTA, 24, 22, 26))

    # reset: reload fresh (not open) to capture focus-visible at REST
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(400)
    page.eval_on_selector(CTA, "el=>el.focus({focusVisible:true})")
    page.wait_for_timeout(150)
    print("rest focus-visible shadow:", page.eval_on_selector(CTA, "el=>getComputedStyle(el).boxShadow"))
    page.mouse.move(1200,500); page.wait_for_timeout(150)
    page.screenshot(path=f"{OUT}\\after-light-focus-rest.png", clip=clip(page, CTA, 24, 22, 22))

    # PRESS BLOOM: pointerdown near an edge to test clipping by the pill
    page.evaluate("document.activeElement.blur()")
    b = page.eval_on_selector(CTA, "el=>{const r=el.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}}")
    # press near the right end, mid-height
    px = b["x"] + b["w"] - 40
    py = b["y"] + b["h"]/2
    page.mouse.move(px, py)
    page.mouse.down()
    page.wait_for_timeout(220)  # mid-bloom
    print("bloom nodes:", page.eval_on_selector(CTA, "el=>el.querySelectorAll('.cta-bloom').length"))
    page.screenshot(path=f"{OUT}\\after-light-press.png", clip=clip(page, CTA, 24, 22, 22))
    page.mouse.up()

    br.close()
print("done")
