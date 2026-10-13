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
sys.exit(0 if ok_all else 1)
