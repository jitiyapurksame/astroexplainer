"""Phase 3 hub change: per-module Exam Simulation bar (locked / ready / passed), E.04 badges after a pass, Mission Ready total pill.
Usage: python3 tools/add_exam_to_hub.py project"""
import sys, os
folder = sys.argv[1] if len(sys.argv) > 1 else "project"
path = os.path.join(folder, "index.html")
s = open(path, encoding="utf-8").read()

def rep(old, new):
    global s
    if s.count(old) != 1: sys.exit(f"hub: block not found exactly once: {old[:60]!r}")
    s = s.replace(old, new)

rep("  .footer-note{", """  .exam-bar{display:flex; align-items:center; gap:12px; margin-top:12px; padding:12px 14px; border-radius:16px;
    border:2px solid var(--line); background:var(--panel);}
  .exam-bar .ex-ic{font-size:1.5rem;}
  .exam-bar .ex-body{flex:1; min-width:0;}
  .exam-bar .ex-title{font-family:'Baloo 2'; font-weight:800; font-size:0.92rem;}
  .exam-bar .ex-sub{font-size:0.72rem; color:#B9C0EA; line-height:1.35;}
  .exam-bar .ex-prog{height:8px; background:var(--panel-hi); border-radius:999px; overflow:hidden; margin-top:6px; border:1px solid var(--line);}
  .exam-bar .ex-prog > div{height:100%; background:linear-gradient(90deg,var(--sun),var(--teal));}
  .exam-bar .ex-btn{flex:0 0 auto; text-decoration:none; background:var(--teal); color:#08221f; font-family:'Baloo 2'; font-weight:800;
    font-size:0.85rem; padding:9px 16px; border-radius:12px;}
  .exam-bar.soon{opacity:0.45;}
  .exam-bar.locked .ex-ic{opacity:0.7;}
  .exam-bar.ready{border-color:var(--teal); box-shadow:0 0 18px rgba(77,216,224,0.35); animation:examglow 2.4s ease-in-out infinite;}
  .exam-bar.passed{border-color:#FFD166; background:rgba(255,209,102,0.08);}
  .exam-bar.passed .ex-btn{background:var(--panel-hi); color:var(--cream); border:1px solid var(--line);}
  @keyframes examglow{ 50%{box-shadow:0 0 26px rgba(77,216,224,0.6);} }
  .footer-note{""")

rep("""    <div class="total-pill" id="readyTotal">🎯 0 exam-ready</div>""",
    """    <div class="total-pill" id="readyTotal">🎯 0 exam-ready</div>
    <div class="total-pill" id="missionTotal">🏅 0 Mission Ready</div>""")

rep("""function renderModules(){""", """function getExamRecord(key){
  try{ return JSON.parse(localStorage.getItem('astro_exam_' + key)); }catch(e){ return null; }
}

// Exam Simulation bar under each module: not built yet / locked (progress) / ready (glowing button) / passed (Mission Ready).
function buildExamBar(mod, builtCount, rec){
  const total = mod.concepts.length;
  const done = mod.concepts.filter(c=>{ const s = c.href && getSupportData(c.saveId); return s && s.cleanLevel3; }).length;
  const bar = document.createElement('div');
  if(builtCount < total){
    bar.className = 'exam-bar soon';
    bar.innerHTML = `<span class="ex-ic">🎯</span><div class="ex-body"><div class="ex-title">Exam Simulation</div><div class="ex-sub">Opens when all ${total} concepts in this module are built.</div></div>`;
  } else if(rec && rec.passed){
    bar.className = 'exam-bar passed';
    bar.innerHTML = `<span class="ex-ic">🏅</span><div class="ex-body"><div class="ex-title">Mission Ready · E.04</div><div class="ex-sub">Exam passed. Best score ${rec.bestPct}% · ${rec.attempts||1} attempt${(rec.attempts||1)===1?'':'s'}</div></div><a class="ex-btn" href="exam.html?m=${mod.key}">Retake</a>`;
  } else if(done === total){
    bar.className = 'exam-bar ready';
    bar.innerHTML = `<span class="ex-ic">🎯</span><div class="ex-body"><div class="ex-title">Exam Simulation is ready!</div><div class="ex-sub">All ${total} concepts mastered. Timed exam, no hints.${rec ? ` Best so far ${rec.bestPct}%.` : ''}</div></div><a class="ex-btn" href="exam.html?m=${mod.key}">Start</a>`;
  } else {
    bar.className = 'exam-bar locked';
    bar.innerHTML = `<span class="ex-ic">🔒</span><div class="ex-body"><div class="ex-title">Exam Simulation</div><div class="ex-sub">Unlocks when every concept has a clean E.03 pass (no hints): <strong>${done}/${total}</strong> so far.</div><div class="ex-prog"><div style="width:${Math.round(100*done/total)}%"></div></div></div>`;
  }
  return bar;
}

function renderModules(){""")

rep("let totalLive = 0, totalReady = 0;", "let totalLive = 0, totalReady = 0, totalMissions = 0;")
rep("    const row = section.querySelector('.card-row');\n", "    const row = section.querySelector('.card-row');\n    const examRec = getExamRecord(mod.key);\n    const passedExam = !!(examRec && examRec.passed && builtCount === mod.concepts.length);\n    if(passedExam) totalMissions++;\n")
rep("""${support ? `<div class="lvl-badge">${LEVELS[support.level].code}</div>` : ''}""", """${support ? `<div class="lvl-badge">${LEVELS[passedExam ? 4 : support.level].code}</div>` : ''}""")
rep("""<div class="status">${support ? LEVELS[support.level].label : 'Not started'}</div>""", """<div class="status">${support ? LEVELS[passedExam ? 4 : support.level].label : 'Not started'}</div>""")
rep("    root.appendChild(section);\n", "    section.appendChild(buildExamBar(mod, builtCount, examRec));\n    root.appendChild(section);\n")
rep("  document.getElementById('readyTotal').textContent = '🎯 ' + totalReady + ' exam-ready';",
    "  document.getElementById('readyTotal').textContent = '🎯 ' + totalReady + ' exam-ready';\n  document.getElementById('missionTotal').textContent = '🏅 ' + totalMissions + ' Mission Ready';")
open(path, "w", encoding="utf-8").write(s)
print("hub patched")
