import glob
from playwright.sync_api import sync_playwright
OUT = r"C:\Dev\portfolio\verify\cta-pass"
URL = "http://localhost:8823/index.html"
EDGE = sorted(glob.glob(r"C:\Program Files (x86)\Microsoft\EdgeCore\*\msedge.exe"))[-1]
CTA = ".row--cta"

def clip(page, sel, px, pt, pb):
    b = page.eval_on_selector(sel, "el=>{const r=el.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}}")
    return {"x":max(b["x"]-px,0),"y":max(b["y"]-pt,0),"width":b["w"]+px*2,"height":b["h"]+pt+pb}

def tab_to_cta(page, limit=40):
    for i in range(limit):
        page.keyboard.press("Tab")
        if page.evaluate("()=>document.activeElement && document.activeElement.classList.contains('row--cta')"):
            return True
    return False

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EDGE, headless=True, args=["--no-sandbox","--disable-gpu"])
    page = br.new_page(viewport={"width":1440,"height":900}, device_scale_factor=2)
    page.goto(URL, wait_until="networkidle")
    page.evaluate("localStorage.setItem('pagefront-theme','light')")

    # REST + focus-visible via keyboard
    page.reload(wait_until="networkidle"); page.wait_for_timeout(400)
    ok = tab_to_cta(page)
    page.wait_for_timeout(350)  # let box-shadow transition finish
    print("rest fv match:", page.eval_on_selector(CTA, "el=>el.matches(':focus-visible')"),
          "| shadow:", page.eval_on_selector(CTA, "el=>getComputedStyle(el).boxShadow"))
    page.screenshot(path=f"{OUT}\\after-light-focus-rest.png", clip=clip(page, CTA, 24, 22, 22))

    # OPEN + focus-visible: activate with keyboard (Enter), stays focused via keyboard modality
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    print("is-open:", page.eval_on_selector(CTA, "el=>el.classList.contains('is-open')"),
          "| fv match:", page.eval_on_selector(CTA, "el=>el.matches(':focus-visible')"))
    page.wait_for_timeout(200)
    print("open fv shadow:", page.eval_on_selector(CTA, "el=>getComputedStyle(el).boxShadow"))
    page.screenshot(path=f"{OUT}\\after-light-focus-open.png", clip=clip(page, CTA, 24, 22, 26))
    br.close()
print("done")
