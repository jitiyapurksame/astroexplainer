"""Generate A4 · Moon concept files. Run from the package root:  python3 tools/build_a4.py project
Content lives in a4_content.py, diagrams in a4_svgs.py."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
from new_concept_example import build
from a4_content import CONCEPTS
from a4_svgs import SVGS

folder = sys.argv[1] if len(sys.argv) > 1 else "project"
template = open(os.path.join(folder, "engine-template.html"), encoding="utf-8").read()
cases = {}
for c in CONCEPTS:
    c = dict(c, svg=SVGS[c['id']])
    open(os.path.join(folder, c["filename"]), "w", encoding="utf-8").write(build(template, c, "A4 · Moon"))
    cases[c["filename"]] = [c["model"], c["wrong"]]
    print("wrote", c["filename"])
json.dump(cases, open(os.path.join(os.path.dirname(__file__), "a4_cases.json"), "w"), indent=1)

idx_path = os.path.join(folder, "index.html")
idx = open(idx_path, encoding="utf-8").read()
for c in CONCEPTS:
    pat = re.compile(r"(\{icon:'[^']*', name:'[^']*', )(saveId:'%s'\})" % re.escape(c["id"]))
    idx, n = pat.subn(lambda m: m.group(1) + "href:'%s', " % c["filename"] + m.group(2), idx)
    if n != 1: sys.exit(f"hub: {c['id']} matched {n} times")
open(idx_path, "w", encoding="utf-8").write(idx)
print("hub wired")
