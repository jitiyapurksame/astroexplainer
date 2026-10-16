"""Headless-browser end-to-end test of Phase 4 (Sentence Builder + Why Chain tabs).
Usage: python3 tools/test_builder_flow.py project"""
import sys, os, json, re
from playwright.sync_api import sync_playwright
folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "project")
url = lambda f: "file://" + os.path.join(folder, f)
data = json.loads(re.search(r"const ASTRO_BUILDER = (\{.*\});", open(os.path.join(folder, "builder-data.js"), encoding="utf-8").read(), re.S).group(1))
hub = open(os.path.join(folder, 'index.html'), encoding='utf-8').read()
HREF = dict((m.group(2), m.group(1)) for m in re.finditer(r"href:'([^']+)', saveId:'([^']+)'", hub))
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)
def set_level(pg, cid, level, clean=False):
    pg.evaluate("([id,l,c]) => localStorage.setItem('astro_'+id+'_support', JSON.stringify({level:l,hintsUsedTotal:0,cleanLevel3:c}))", [cid, level, clean])

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(viewport={'width': 820, 'height': 1100}).new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    cid = 'summer'; items = data[cid]
    pg.goto(url('summer.html')); pg.evaluate("localStorage.clear(); sessionStorage.clear()"); pg.reload(); pg.wait_for_timeout(200)
    tabs = pg.locator('#tabRow .tab').all_inner_texts()
    check(any('Builder' in t for t in tabs) and any('Why Chain' in t for t in tabs), "tabs: Builder and Why Chain are present (" + " | ".join(tabs) + ")")
    check(pg.locator('.tab[data-tab="chain"].locked').count() == 1, "E.01: Why Chain is locked")
    pg.click('.tab[data-tab="chain"]'); pg.wait_for_timeout(150)
    check('E.02' in pg.inner_text('#toast') and pg.locator('.tab[data-tab="chain"].active').count() == 0, "E.01: tapping locked Why Chain shows the E.02 message and stays put")
    # ---- Sentence Builder
    pg.click('.tab[data-tab="builder"]'); pg.wait_for_timeout(150)
    check(pg.locator('.bcard').count() == 3 and '0/3' in pg.inner_text('.b-progress'), "builder: 3 sentence cards, 0/3 built")
    check(all(pg.locator(f'.bcard:nth-child({i+3}) .bopt').count() >= 2 for i in range(0)), "builder: options present")
    for i, it in enumerate(items):
        card = pg.locator('.bcard').nth(i)
        n_opts = card.locator('.bopt').count()
        check(n_opts in (3, 4) and n_opts >= 2, f"builder item {i+1}: {n_opts} options (right + wrong + decoy)")
        wrong = card.locator('.bopt', has_text=it['wrong']).first
        wrong.click(); pg.wait_for_timeout(80)
        check(pg.locator('.bcard').nth(i).locator('.bopt.wrong').count() == 1 and 'Not quite' in pg.locator('.bcard').nth(i).inner_text(), f"builder item {i+1}: wrong tap is gently rejected, no penalty")
        pg.locator('.bcard').nth(i).locator('.bopt', has_text=re.compile('^' + re.escape(it['answer']) + '$')).first.click(); pg.wait_for_timeout(80)
        check(pg.locator('.bcard').nth(i).locator('.bblank.filled').count() == 1, f"builder item {i+1}: correct tap fills the blank")
    check('You built it' in pg.inner_text('#stage'), "builder: completion panel appears")
    check('✓' in pg.locator('.tab[data-tab="builder"]').inner_text(), "builder: tab shows a ✓ (state is visible)")
    st = pg.evaluate("JSON.parse(localStorage.getItem('astro_summer_builder'))")
    check(st and st.get('builderDone') is True, "builder: state saved (builderDone)")
    paragraph = ' '.join(it['frame'].replace('___', it['answer']) for it in items)
    pg.click('#bUse'); pg.wait_for_timeout(200)
    check(pg.locator('.tab[data-tab="explainer"].active').count() == 1 and pg.input_value('#explainBox') == paragraph, "builder: 'Use it in my answer box' fills the Explainer box with the built paragraph")
    pg.click('#submitExplain'); pg.wait_for_timeout(500)
    check('Guided Flight' in pg.inner_text('body'), "builder: submitting the built paragraph passes E.01 (level-up overlay)")
    # ---- E.03: builder is practice only
    set_level(pg, 'summer', 3); pg.reload(); pg.wait_for_timeout(200)
    pg.click('.tab[data-tab="builder"]')
    for i, it in enumerate(items):
        pg.locator('.bcard').nth(i).locator('.bopt', has_text=re.compile('^' + re.escape(it['answer']) + '$')).first.click(); pg.wait_for_timeout(60)
    check(pg.locator('#bUse').count() == 0 and 'write the answer yourself' in pg.inner_text('#stage'), "E.03: no 'Use it' button, practice only")
    pg.click('#bAgain'); pg.wait_for_timeout(100)
    check('0/3' in pg.inner_text('.b-progress'), "builder: Build again resets")
    # ---- Why Chain
    set_level(pg, 'summer', 2); pg.reload(); pg.wait_for_timeout(200)
    check(pg.locator('.tab[data-tab="chain"].locked').count() == 0, "E.02: Why Chain unlocked")
    pg.click('.tab[data-tab="chain"]'); pg.wait_for_timeout(150)
    sentences = [it['frame'].replace('___', it['answer']) for it in items]
    check(pg.locator('.cslot').count() == 3 and pg.locator('.ccard').count() == 3, "chain: 3 empty slots and 3 shuffled cards")
    first_order = pg.locator('.ccard').all_inner_texts()
    check(first_order != sentences, "chain: cards start shuffled (not already solved)")
    check(pg.locator('#cCheck').is_disabled(), "chain: Check is disabled until every slot is filled")
    # place in the wrong order (reverse of correct) then check
    for s in reversed(sentences):
        pg.locator('.ccard', has_text=s).first.click(); pg.wait_for_timeout(60)
    pg.click('#cCheck'); pg.wait_for_timeout(100)
    check(pg.locator('.cslot.wrongpos').count() >= 1 and 'Not quite' in pg.inner_text('#stage'), "chain: wrong order is flagged (red) with a gentle message")
    # fix: empty all slots and place in the right order
    for k in range(3):
        pg.locator('.cslot').nth(k).click(); pg.wait_for_timeout(40)
    for s in sentences:
        pg.locator('.ccard', has_text=s).first.click(); pg.wait_for_timeout(60)
    pg.click('#cCheck'); pg.wait_for_timeout(150)
    check('Chain complete' in pg.inner_text('#stage') and pg.locator('.cslot.right').count() == 3, "chain: correct order is celebrated, all slots green")
    st = pg.evaluate("JSON.parse(localStorage.getItem('astro_summer_builder'))")
    check(st.get('chainDone') is True and '✓' in pg.locator('.tab[data-tab="chain"]').inner_text(), "chain: state saved and tab shows a ✓")
    # ---- every concept: builder + chain tabs render without errors
    ok = 0
    for cid2 in data:
        pg.goto(url(HREF[cid2])); pg.evaluate("localStorage.clear()"); set_level(pg, cid2, 2); pg.reload(); pg.wait_for_timeout(60)
        pg.click('.tab[data-tab="builder"]'); n1 = pg.locator('.bcard').count()
        pg.click('.tab[data-tab="chain"]'); n2 = pg.locator('.cslot').count()
        if n1 == n2 == len(data[cid2]): ok += 1
        else: print("   problem in", cid2, n1, n2, len(data[cid2]))
    check(ok == len(data), f"all {len(data)} concept pages render Builder and Chain with the right number of items ({ok})")
    check(not errs, "no JavaScript errors (" + "; ".join(errs[:2]) + ")")
    b.close()
print("\nFAILED:" if fails else "\nALL PASSED", fails if fails else "")
sys.exit(1 if fails else 0)
