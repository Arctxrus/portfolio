import json
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8795"
OUT = "C:/Dev/portfolio/verify/restyle-10"
results = {}

INIT_SCRIPT = """
window.__scrollToCalls = [];
const origScrollTo = window.scrollTo.bind(window);
window.scrollTo = function(...args) {
    window.__scrollToCalls.push({t: Math.round(performance.now()), args: args, before: window.scrollY});
    return origScrollTo(...args);
};
window.__popstateCount = 0;
window.addEventListener('popstate', () => { window.__popstateCount++; });
"""

def rec_trace(page, ms=1800):
    page.evaluate("""(ms) => {
        window.__rec = [];
        const start = performance.now();
        function loop() {
            window.__rec.push([Math.round(performance.now()-start), window.scrollY, document.documentElement.scrollHeight]);
            if (performance.now() - start < ms) requestAnimationFrame(loop);
        }
        requestAnimationFrame(loop);
    }""", ms)

def compress(trace):
    out, last = [], None
    for t in trace:
        if t[1] != last:
            out.append(t); last = t[1]
    return out

def new_page(browser, w=360, h=740, reduced=None):
    kw = {"viewport": {"width": w, "height": h}}
    if reduced: kw['reduced_motion'] = reduced
    ctx = browser.new_context(**kw)
    ctx.add_init_script(INIT_SCRIPT)
    page = ctx.new_page()
    page.goto(f"{BASE}/index.html")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(400)
    return ctx, page

def enter_and_deep_scroll(page, row_idx=0, pre_scroll=120):
    page.evaluate("window.scrollTo(0," + str(pre_scroll) + ")")
    page.wait_for_timeout(150)
    page.locator('.row').nth(row_idx).click()
    page.wait_for_timeout(900)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(350)
    return page.evaluate("window.scrollY")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # 1. exact original FAIL: 360x740 button deep
    ctx, page = new_page(browser, 360, 740)
    y_deep = enter_and_deep_scroll(page)
    page.screenshot(path=OUT + "/fix2-s1-before.png")
    rec_trace(page, 1800)
    page.evaluate("window.__scrollToCalls = []")
    page.locator('[data-detail-back]').click()
    page.wait_for_timeout(2000)
    trace = compress(page.evaluate("window.__rec"))
    final_y = page.evaluate("window.scrollY")
    max_scroll = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
    calls = page.evaluate("window.__scrollToCalls")
    page.screenshot(path=OUT + "/fix2-s1-after.png")
    page.mouse.wheel(0, 300)
    page.wait_for_timeout(400)
    after_manual_scroll = page.evaluate("window.scrollY")
    page.wait_for_timeout(600)
    after_manual_scroll_settled = page.evaluate("window.scrollY")
    results['s1_button_deep_360'] = {
        'y_deep': y_deep, 'trace': trace, 'final_y': final_y, 'max_scroll': max_scroll,
        'scrollTo_calls': calls, 'touched_zero': any(t[1] == 0 for t in trace),
        'post_settle_manual_scroll_immediate': after_manual_scroll,
        'post_settle_manual_scroll_after_wait': after_manual_scroll_settled,
    }
    ctx.close()

    # 2. Escape deep (keyboard, focus-return expected)
    ctx, page = new_page(browser, 360, 740)
    y_deep2 = enter_and_deep_scroll(page)
    rec_trace(page, 1800)
    page.keyboard.press('Escape')
    page.wait_for_timeout(2000)
    trace2 = compress(page.evaluate("window.__rec"))
    final_y2 = page.evaluate("window.scrollY")
    max_scroll2 = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
    focused_after2 = page.evaluate("document.activeElement.className")
    origin_rect2 = page.evaluate("""() => {
        const r = document.activeElement.getBoundingClientRect();
        return {top: r.top, bottom: r.bottom};
    }""")
    results['s2_escape_deep_360'] = {
        'y_deep': y_deep2, 'trace': trace2, 'final_y': final_y2, 'max_scroll': max_scroll2,
        'focused_after': focused_after2, 'focused_rect_viewport': origin_rect2,
    }
    ctx.close()

    # 3. keyboard-activated button (Tab into back button, Enter)
    ctx, page = new_page(browser, 360, 740)
    y_deep3 = enter_and_deep_scroll(page)
    page.locator('[data-detail-back]').focus()
    page.wait_for_timeout(100)
    rec_trace(page, 1800)
    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)
    trace3 = compress(page.evaluate("window.__rec"))
    final_y3 = page.evaluate("window.scrollY")
    max_scroll3 = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
    focused_after3 = page.evaluate("document.activeElement.className")
    results['s3_keyboard_activated_button_360'] = {
        'y_deep': y_deep3, 'trace': trace3, 'final_y': final_y3, 'max_scroll': max_scroll3,
        'focused_after': focused_after3,
    }
    ctx.close()

    # 4. hardware back deep (page.go_back())
    ctx, page = new_page(browser, 360, 740)
    y_deep4 = enter_and_deep_scroll(page, row_idx=1)
    rec_trace(page, 1800)
    page.go_back()
    page.wait_for_timeout(2000)
    trace4 = compress(page.evaluate("window.__rec"))
    final_y4 = page.evaluate("window.scrollY")
    max_scroll4 = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
    results['s4_hardware_back_deep_360'] = {
        'y_deep': y_deep4, 'trace': trace4, 'final_y': final_y4, 'max_scroll': max_scroll4,
        'touched_zero_permanently': (trace4[-1][1] == 0) if trace4 else None,
    }
    ctx.close()

    # 5. reduced motion deep, button click
    ctx, page = new_page(browser, 360, 740, reduced='reduce')
    y_deep5 = enter_and_deep_scroll(page, row_idx=2)
    rec_trace(page, 1500)
    page.locator('[data-detail-back]').click()
    page.wait_for_timeout(1700)
    trace5 = compress(page.evaluate("window.__rec"))
    final_y5 = page.evaluate("window.scrollY")
    max_scroll5 = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
    results['s5_reduced_motion_deep_360'] = {
        'y_deep': y_deep5, 'trace': trace5, 'final_y': final_y5, 'max_scroll': max_scroll5,
    }
    ctx.close()

    # 6. shallow (y=120, no deep scroll), button click
    ctx, page = new_page(browser, 360, 740)
    page.evaluate("window.scrollTo(0,120)")
    page.wait_for_timeout(150)
    page.locator('.row').nth(0).click()
    page.wait_for_timeout(900)
    rec_trace(page, 1500)
    page.locator('[data-detail-back]').click()
    page.wait_for_timeout(1700)
    trace6 = compress(page.evaluate("window.__rec"))
    final_y6 = page.evaluate("window.scrollY")
    results['s6_shallow_120_360'] = {'trace': trace6, 'final_y': final_y6}
    ctx.close()

    # 7. user-scroll-during-morph: click back, then immediately wheel-scroll during the exit window
    ctx, page = new_page(browser, 360, 740)
    y_deep7 = enter_and_deep_scroll(page)
    rec_trace(page, 1800)
    page.locator('[data-detail-back]').click()
    page.wait_for_timeout(30)
    page.mouse.wheel(0, -400)
    page.wait_for_timeout(2000)
    trace7 = compress(page.evaluate("window.__rec"))
    final_y7 = page.evaluate("window.scrollY")
    results['s7_user_scroll_during_morph_360'] = {
        'y_deep': y_deep7, 'trace': trace7, 'final_y': final_y7,
    }
    ctx.close()

    # 8. 390 button deep
    ctx, page = new_page(browser, 390, 780)
    y_deep8 = enter_and_deep_scroll(page, pre_scroll=150)
    rec_trace(page, 1800)
    page.locator('[data-detail-back]').click()
    page.wait_for_timeout(2000)
    trace8 = compress(page.evaluate("window.__rec"))
    final_y8 = page.evaluate("window.scrollY")
    max_scroll8 = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
    results['s8_button_deep_390'] = {
        'y_deep': y_deep8, 'trace': trace8, 'final_y': final_y8, 'max_scroll': max_scroll8,
    }
    ctx.close()

    browser.close()

with open(OUT + "/fix2_verify_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(json.dumps(results, indent=2))
