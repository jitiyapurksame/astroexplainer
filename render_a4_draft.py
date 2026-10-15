import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from a4_content import CONCEPTS
out = ["""# A4 · Moon — Content Draft for Review

Status: **draft only, no files generated yet.** After your edits I will draw the 15 diagrams, generate the files from `tools/a4_content.py`, run the validator and tests, wire the hub, and hand over for the iPad checkpoint.

## Design choices applied to all 15 concepts
- **Hemisphere-neutral.** Phase descriptions never say "left side" or "right side" lit, because that flips between hemispheres. Waxing and waning are described as the lit part growing or shrinking.
- **Easy language, same rules as A3:** 3 starters, 4 word pills, exactly 3 required mark points, 3 escalating hints, 1 exam question, phrase-level terms (no bare generic words).
- **Pre-checked:** every concept has a model answer that passes all 3 mark points and a wrong answer that passes none (script `tools/check_a4_terms.py`, 15/15 clean, 0 lint problems).
- **Exact numbers he can remember:** 27 days (orbit), about 50 minutes later each day (moonrise), about 14 days (waxing/waning), 384,000 km and about a quarter of Earth's size (Earth-Moon System).

---
"""]
for i, c in enumerate(CONCEPTS, 1):
    out.append(f"## A4.{i} · {c['title']} {c['icon']} (`{c['id']}`)")
    out.append(f"**Prompt:** {c['prompt']}")
    out.append("**Starters:** " + " / ".join(f'"{s}"' for s in c['starters']))
    out.append("**Word pills:** " + " · ".join(c['word_choices']))
    out.append("")
    out.append("| Mark point | Terms |\n|---|---|")
    for m in c['mark_points']:
        out.append(f"| **{m['label']}** (`{m['id']}`) | " + ", ".join(m['terms']) + " |")
    out.append("")
    out.append("**Hints:** " + " ".join(f"{n}) {h}" for n, h in enumerate(c['hints'], 1)))
    out.append(f"**Exam question ({c['exam_marks']} marks):** \"{c['exam_prompt']}\" → " + ", ".join(f"`{x}`" for x in c['exam_mark_ids']))
    out.append(f"**Reference SVG idea:** {c['svg_idea']}")
    out.append("\n---\n")
out.append("""## Points I'd like you to decide before I build
1. **Moon Orbit "about a month".** The Moon takes 27.3 days to go around Earth but 29.5 days to go through its phases. I accept anything from 27 to 30 days or "a month", so he is not marked wrong for either number. OK?
2. **Moonrise "about 50 minutes later each day".** This is the hardest fact in the module and it is not in the exam question. Keep it as the third required point, or replace it with something simpler (e.g. "the Moon is in the sky at night")?
3. **Tides** only covers the Moon's gravity, the high-tide bulge and "two a day". I left out the Sun's effect and spring/neap tides to keep it easy. OK?
4. **Eclipse timing.** I accept just "full moon" (lunar) and "new moon" (solar) for the third point. Both are required, so he must remember the phase.
5. **Crater "no air or weather".** This is the explanation of why craters last. Is that too advanced, or fine for his level?
""")
open(sys.argv[1], 'w', encoding='utf-8').write("\n".join(out))
print("ok")
