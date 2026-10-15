"""Pre-build check of A4 content: lint rules + model-answer / wrong-answer test using a Python port of the engine matcher."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from a4_content import CONCEPTS
GENERIC = {"line","lines","north","south","east","west","sun","light","away","turn","half","edge","face","point","points","side","opposite","middle","round","ball","dark","warm","bright","top","bottom","far","near","cold","hot","big","small","earth","planet","day","night"}
def norm(s): return re.sub(r"\s+"," ",re.sub(r"[\u2013\u2014-]"," ",re.sub(r"[\u2018\u2019\u02bc]","'",(s or "").lower()))).strip()
def has(text, raw):
    whole = raw.endswith('$'); t = norm(raw[:-1] if whole else raw)
    if not t: return False
    i = 0
    while True:
        i = text.find(t, i)
        if i < 0: return False
        b = text[i-1] if i else ''; a = text[i+len(t)] if i+len(t) < len(text) else ''
        if not re.match(r"[a-z0-9]", b) and (not whole or not re.match(r"[a-z0-9]", a)): return True
        i += 1
bad = 0
for c in CONCEPTS:
    ids = [m['id'] for m in c['mark_points']]
    for m in c['mark_points']:
        for t in m['terms']:
            if re.fullmatch(r"[a-z]+", t) and len(t) < 4: print(c['id'], "LINT FAIL short term", t); bad += 1
            if t.rstrip('$') in GENERIC and not t.endswith('$'): print(c['id'], "LINT WARN generic", t)
    mod = norm(c['model']); wr = norm(c['wrong'])
    miss = [m['id'] for m in c['mark_points'] if not any(has(mod, t) for t in m['terms'])]
    hit = [m['id'] for m in c['mark_points'] if any(has(wr, t) for t in m['terms'])]
    if miss: print(c['id'], "MODEL ANSWER misses", miss); bad += 1
    if hit: print(c['id'], "WRONG ANSWER passes", hit); bad += 1
    for e in c['exam_mark_ids']:
        if e not in ids: print(c['id'], "exam refs unknown", e); bad += 1
    if len(c['hints']) != 3 or len(c['starters']) != 3 or len(c['word_choices']) != 4 or len(ids) != 3: print(c['id'], "COUNT problem"); bad += 1
print(len(CONCEPTS), "concepts;", "problems:", bad)
