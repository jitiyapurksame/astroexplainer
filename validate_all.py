"""Validate every .html in a folder: <script> brace balance + node --check.
Usage: python3 validate_all.py ../project
"""
import re, subprocess, sys, glob, os
folder = sys.argv[1] if len(sys.argv) > 1 else "."
ok_all = True
for path in sorted(glob.glob(os.path.join(folder, "*.html"))):
    html = open(path, encoding="utf-8").read()
    m = re.search(r"<script>(.*?)</script>", html, re.DOTALL)
    if not m:
        print(os.path.basename(path), "FAIL: no <script>"); ok_all = False; continue
    js = m.group(1)
    depth = 0; bad = False
    for ch in js:
        depth += (ch == '{') - (ch == '}')
        if depth < 0: bad = True; break
    if bad or depth != 0:
        print(os.path.basename(path), "FAIL: brace imbalance"); ok_all = False; continue
    open("/tmp/_check.js", "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", "/tmp/_check.js"], capture_output=True, text=True)
    if r.returncode:
        print(os.path.basename(path), "FAIL:", r.stderr); ok_all = False
    else:
        print(os.path.basename(path), "OK")

# ---- Term lint (Phase 2) -------------------------------------------------
# FAIL: purely alphabetic term shorter than 4 letters without a trailing $ (e.g. 'ice' -> use 'ice$').
# WARN: bare generic word that will match almost any answer, unless listed in ACCEPTED below.
GENERIC = {"line","lines","north","south","east","west","sun","light","away","turn","half","edge","face",
           "point","points","side","opposite","middle","round","ball","dark","warm","bright","top","bottom",
           "far","near","cold","hot","big","small","earth","planet","day","night"}
# (concept id, term) pairs reviewed and deliberately kept bare because the mark point IS that word.
ACCEPTED = {("earth","round"),("earth","planet"),("hemisphere","half"),("equator","middle"),
            ("sunrise","east"),("sunset","west"),("night","dark"),("northpole","cold"),
            ("globevsmap","round")}
lint_fail = False
for path in sorted(glob.glob(os.path.join(folder, "*.html"))):
    name = os.path.basename(path)
    if name in ("index.html", "engine-template.html", "exam.html"): continue
    html = open(path, encoding="utf-8").read()
    cid = re.search(r"const CONCEPT = \{\s*id:\s*'([^']+)'", html).group(1)
    for m in re.finditer(r"terms:\[([^\]]*)\]", html):
        for t in re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1)):
            t = t.replace("\\'", "'")
            bare = t.rstrip("$")
            if re.fullmatch(r"[a-z]+", t) and len(t) < 4:
                print(f"{name} LINT FAIL: term '{t}' is shorter than 4 letters - use '{t}$' (whole word) or a longer phrase")
                lint_fail = True
            elif bare in GENERIC and not t.endswith("$") and (cid, bare) not in ACCEPTED:
                print(f"{name} LINT WARN: bare generic term '{t}' - prefer a phrase")
print("term lint:", "FAIL" if lint_fail else "OK")

# ---- Phase 3: exam-data.js must be in sync with the concept files; exam.html must carry the engine's matcher ----
import shutil, tempfile, filecmp
exam_fail = False
if os.path.exists(os.path.join(folder, "exam-data.js")):
    tmp = tempfile.mkdtemp()
    shutil.copytree(folder, os.path.join(tmp, "p"))
    r = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_exam_data.js"), os.path.join(tmp, "p")], capture_output=True, text=True)
    if r.returncode or not filecmp.cmp(os.path.join(tmp, "p", "exam-data.js"), os.path.join(folder, "exam-data.js"), shallow=False):
        print("exam-data.js FAIL: out of date or invalid - run: node tools/build_exam_data.js", folder, r.stderr[-200:]); exam_fail = True
    else:
        print("exam-data.js OK (in sync)")
    eng = open(os.path.join(folder, "engine-template.html"), encoding="utf-8").read()
    matcher = eng[eng.index("function normText"):eng.index("function escapeHtml")].rstrip()
    if matcher not in open(os.path.join(folder, "exam.html"), encoding="utf-8").read():
        print("exam.html FAIL: matcher differs from engine-template.html - run: python3 tools/build_exam_page.py", folder); exam_fail = True
    else:
        print("exam.html matcher OK (identical to engine)")
# ---- Phase 4: Sentence Builder / Why Chain data must match every concept's real mark points ----
if os.path.exists(os.path.join(folder, "builder-data.js")):
    r = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_builder.js"), folder], capture_output=True, text=True)
    print("builder-data.js", "OK:" if r.returncode == 0 else "FAIL:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
    if r.returncode: print(r.stdout); exam_fail = True
lint_fail = lint_fail or exam_fail
sys.exit(0 if (ok_all and not lint_fail) else 1)
