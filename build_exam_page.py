"""Builds project/exam.html from tools/exam_template.html, copying the matcher from engine-template.html so the two can never drift.
Usage: python3 tools/build_exam_page.py project"""
import sys, os
folder = sys.argv[1] if len(sys.argv) > 1 else "project"
eng = open(os.path.join(folder, "engine-template.html"), encoding="utf-8").read()
matcher = eng[eng.index("function normText"):eng.index("function escapeHtml")].rstrip() + "\n"
tpl = open(os.path.join(os.path.dirname(__file__), "exam_template.html"), encoding="utf-8").read()
assert "/*__MATCHER__*/" in tpl
open(os.path.join(folder, "exam.html"), "w", encoding="utf-8").write(tpl.replace("/*__MATCHER__*/", matcher))
print("wrote exam.html")
