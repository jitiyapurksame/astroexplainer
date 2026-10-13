"""Template for generating a new module's concept files from engine-template.html.

How it works: every concept file = engine-template.html with ONLY the
`const CONCEPT = {...};` block swapped (plus the <title>). Engine code is never
edited per file. To add a module (e.g. A3), copy this, fill CONCEPTS, run it
from the project folder, then run validate_all.py.

Engine changes go the other way: edit engine-template.html first, then apply the
same old->new string replacement to every concept file (and re-validate all).
"""
START = "const CONCEPT = {"
END = "\n};\n\n/* ============================================================\n   ENGINE"

def esc_dq(s): return s.replace('\\', '\\\\').replace('"', '\\"')
def esc_sq(s): return s.replace('\\', '\\\\').replace("'", "\\'")

def build(template, c, subtitle):
    mps = ",\n    ".join(
        "{ id:'%s', label:'%s', terms:[%s] }" % (
            m["id"], esc_sq(m["label"]), ", ".join("'%s'" % esc_sq(t) for t in m["terms"]))
        for m in c["mark_points"])
    block = f"""const CONCEPT = {{
  id: '{c['id']}',
  icon: '{c['icon']}',
  title: '{esc_sq(c['title'])}',
  subtitle: '{esc_sq(subtitle)}',
  explain: {{
    prompt: "{esc_dq(c['prompt'])}",
    starters: [
      {", ".join('"%s"' % esc_dq(s) for s in c['starters'])}
    ],
    wordChoices: [{", ".join("'%s'" % esc_sq(w) for w in c['word_choices'])}]
  }},
  referenceImage: `{c['svg']}`,
  markPoints: [
    {mps}
  ],
  hintSequence: [
    {", ".join('"%s"' % esc_dq(h) for h in c['hints'])}
  ],
  examQuestions: [
    {{ prompt: "{esc_dq(c['exam_prompt'])}", marks: {c['exam_marks']}, markPoints: [{", ".join("'%s'" % esc_sq(m) for m in c['exam_mark_ids'])}] }}
  ],
}};"""
    s = template.index(START); e = template.index(END, s) + len("\n};")
    out = template[:s] + block + template[e:]
    return out.replace("<title>Concept · Astro Sketch Explainer</title>",
                       f"<title>{c['title']} · Astro Sketch Explainer</title>")

# CONCEPTS = [dict(id=..., icon=..., title=..., filename=..., prompt=..., starters=[...],
#   word_choices=[...], svg='<svg ...>', mark_points=[dict(id=,label=,terms=[])],
#   hints=[...3], exam_prompt=..., exam_marks=2, exam_mark_ids=[...]), ...]
# template = open("engine-template.html", encoding="utf-8").read()
# for c in CONCEPTS: open(c["filename"], "w", encoding="utf-8").write(build(template, c, "A3 · Seasons"))
