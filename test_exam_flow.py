"""Headless-browser end-to-end test of Phase 3 (hub bars, locked/ready/passed exam, scoring, timer expiry, resume, preview, E.04 on concept pages).
Usage: python3 tools/test_exam_flow.py project      (needs playwright + chromium)"""
import sys, os, json
from playwright.sync_api import sync_playwright
folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "project")
cases = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "a4_cases.json")))
url = lambda f, q="": "file://" + os.path.join(folder, f) + q
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)

def set_mastered(pg, ids):
    pg.evaluate("ids => ids.forEach(id => localStorage.setItem('astro_'+id+'_support', JSON.stringify({level:3,hintsUsedTotal:0,cleanLevel3:true})))", ids)

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 820, 'height': 1100}); pg = ctx.new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('dialog', lambda d: d.accept())
    mods = pg.evaluate("1")  # warm-up
    # ---- 1. fresh state
    pg.goto(url('index.html')); pg.evaluate("localStorage.clear(); sessionStorage.clear()"); pg.reload(); pg.wait_for_timeout(200)
    check(pg.locator('.exam-bar.locked').count() == 4, "hub: 4 locked exam bars (A1-A4) on a fresh profile")
    check(pg.locator('.exam-bar.soon').count() == 2, "hub: 2 'not built yet' exam bars (A5, A6)")
    check('0 Mission Ready' in pg.inner_text('#missionTotal'), "hub: Mission Ready pill shows 0")
    pg.goto(url('earth.html')); pg.wait_for_timeout(200)
    check('0/10' in pg.inner_text('#missionBanner'), "concept page: banner shows 0/10 mastered")
    check(pg.locator('.rung.current .code').inner_text() == 'E.01', "concept page: ladder at E.01")
    # ---- 2. locked exam page
    pg.goto(url('exam.html', '?m=A4')); pg.wait_for_timeout(200)
    check(pg.locator('#startBtn').count() == 0 and 'locked' in pg.inner_text('#view').lower(), "exam page: locked, no start button")
    pg.goto(url('exam.html', '?m=A5')); pg.wait_for_timeout(200)
    check('not finished' in pg.inner_text('#view'), "exam page: unfinished module shows 'not finished'")
    pg.goto(url('exam.html', '?m=ZZ')); pg.wait_for_timeout(200)
    check('not found' in pg.inner_text('#view'), "exam page: unknown module handled")
    # ---- 3. unlock A4 and pass it with model answers
    a4ids = [f[:-5] for f in cases]
    pg.goto(url('index.html')); set_mastered(pg, a4ids); pg.reload(); pg.wait_for_timeout(200)
    check(pg.locator('.exam-bar.ready').count() == 1, "hub: A4 exam bar is 'ready' once all 15 are mastered")
    pg.goto(url('exam.html', '?m=A4')); pg.wait_for_timeout(200)
    check(pg.locator('#startBtn').count() == 1, "exam page: start button when unlocked")
    pg.click('#startBtn'); pg.wait_for_timeout(200)
    run = pg.evaluate("JSON.parse(sessionStorage.getItem('astro_examrun_A4'))")
    check(len(run['ids']) == 8 and len(set(run['ids'])) == 8, "exam: 8 distinct questions for a 15-concept module")
    check(abs((run['endAt'] - run['startedAt'])/1000 - 8*180) < 2, "exam: timer is 8 x 180 s")
    check(pg.locator('#timer').count() == 0 and '⏱' not in pg.inner_text('body'), "exam: no countdown shown on screen (quiet time limit)")
    # mid-exam resume: answer Q1, reload, still there
    first = run['ids'][0]
    pg.fill('#answerBox', cases[first + '.html'][0]); pg.wait_for_timeout(100); pg.reload(); pg.wait_for_timeout(200)
    check(pg.input_value('#answerBox') == cases[first + '.html'][0], "exam: answer + position survive a page reload")
    for i, cid in enumerate(run['ids']):
        pg.fill('#answerBox', cases[cid + '.html'][0])
        pg.click('#nextBtn'); pg.wait_for_timeout(120)
    check('100%' in pg.inner_text('.score'), "results: model answers score 100%")
    check(pg.locator('#overlay.show').count() == 1, "results: Mission Ready overlay appears on first pass")
    rec = pg.evaluate("JSON.parse(localStorage.getItem('astro_exam_A4'))")
    check(rec and rec['passed'] and rec['bestPct'] == 100 and rec['attempts'] == 1, "storage: pass saved (passed, best 100, 1 attempt)")
    pg.goto(url('index.html')); pg.wait_for_timeout(200)
    check(pg.locator('.exam-bar.passed').count() == 1 and '1 Mission Ready' in pg.inner_text('#missionTotal'), "hub: A4 bar passed + pill shows 1")
    check(pg.locator('.lvl-badge', has_text='E.04').count() == 15, "hub: all 15 A4 cards show E.04")
    pg.goto(url('moonorbit.html')); pg.wait_for_timeout(200)
    check(pg.locator('.rung.current .code').inner_text() == 'E.04', "concept page: E.04 rung lit after pass")
    check('Mission Ready' in pg.inner_text('#missionBanner'), "concept page: Mission Ready banner")
    # ---- 4. failing attempt does not remove a pass, counts attempts
    pg.goto(url('exam.html', '?m=A4')); pg.wait_for_timeout(200)
    pg.evaluate("sessionStorage.clear()"); pg.reload(); pg.click('#startBtn'); pg.wait_for_timeout(150)
    run = pg.evaluate("JSON.parse(sessionStorage.getItem('astro_examrun_A4'))")
    for cid in run['ids']:
        pg.fill('#answerBox', 'I do not know'); pg.click('#nextBtn'); pg.wait_for_timeout(100)
    check('Not yet' in pg.inner_text('#view') and '0%' in pg.inner_text('.score'), "results: blank-ish answers score 0% and say 'Not yet'")
    rec = pg.evaluate("JSON.parse(localStorage.getItem('astro_exam_A4'))")
    check(rec['passed'] and rec['bestPct'] == 100 and rec['attempts'] == 2 and rec['lastPct'] == 0, "storage: pass kept, best kept, attempts=2, last=0")
    check(pg.locator('#overlay.show').count() == 0, "results: no overlay on a failed attempt")
    # ---- 5. fail on a fresh module (A3) leaves it not passed
    a3ids = ['earthorbit','tilt','summer','winter','spring','autumn','solstice','equinox','sunangle','daylength']
    pg.goto(url('index.html')); set_mastered(pg, a3ids); pg.goto(url('exam.html', '?m=A3')); pg.wait_for_timeout(200)
    pg.click('#startBtn'); pg.wait_for_timeout(150)
    run = pg.evaluate("JSON.parse(sessionStorage.getItem('astro_examrun_A3'))")
    check(len(run['ids']) == 5, "exam: 5 questions for a 10-concept module")
    # timer expiry: push endAt into the past and reload
    pg.evaluate("() => { const r = JSON.parse(sessionStorage.getItem('astro_examrun_A3')); r.endAt = Date.now() - 1000; sessionStorage.setItem('astro_examrun_A3', JSON.stringify(r)); }")
    pg.reload(); pg.wait_for_timeout(250)
    check('Time is up' in pg.inner_text('#view'), "timer: expired exam is marked automatically with a 'Time is up' note")
    rec = pg.evaluate("JSON.parse(localStorage.getItem('astro_exam_A3'))")
    check(rec and not rec['passed'] and rec['attempts'] == 1, "storage: timed-out attempt saved as not passed")
    pg.click('#againBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#startBtn').count() == 1, "retry: 'Try again' returns to the intro for a fresh set")
    # ---- 6. preview mode saves nothing
    pg.goto(url('exam.html', '?m=A2&preview=1')); pg.wait_for_timeout(200)
    check(pg.locator('#startBtn').count() == 1 and 'PREVIEW' in pg.inner_text('#titleEl'), "preview: A2 starts without mastery and is labelled PREVIEW")
    pg.click('#startBtn'); pg.wait_for_timeout(150)
    run = pg.evaluate("JSON.parse(sessionStorage.getItem('astro_examrun_A2_preview'))")
    for cid in run['ids']:
        pg.fill('#answerBox', 'x'); pg.click('#nextBtn'); pg.wait_for_timeout(100)
    check(pg.evaluate("localStorage.getItem('astro_exam_A2')") is None, "preview: nothing saved to localStorage")
    check(not errs, "no JavaScript errors anywhere (" + "; ".join(errs[:2]) + ")")
    b.close()
print("\nFAILED:" if fails else "\nALL PASSED", fails if fails else "")
sys.exit(1 if fails else 0)
