"""Phase 3 engine change: E.04 Mission Ready ladder rung + exam banner on every concept page, and the exam-data.js include.
Applies the same exact old->new replacement to engine-template.html and every concept file (fails loudly if a block is missing).
Usage: python3 tools/add_exam_to_engine.py project"""
import sys, os, glob
folder = sys.argv[1] if len(sys.argv) > 1 else "project"

R = []
R.append(("</div>\n\n<script>\n/* ====", "</div>\n\n<script src=\"exam-data.js\"></script>\n<script>\n/* ===="))
R.append(("function setSupport(s){ localStorage.setItem(SUPPORT_KEY, JSON.stringify(s)); }\n",
"""function setSupport(s){ localStorage.setItem(SUPPORT_KEY, JSON.stringify(s)); }

// Phase 3: module exam status for this concept (exam-data.js lists the modules). E.04 Mission Ready = module exam passed.
function getExamInfo(){
  try{
    if(typeof ASTRO_MODULES === 'undefined') return null;
    for(const key in ASTRO_MODULES){
      const m = ASTRO_MODULES[key];
      if(!m.concepts.some(c=>c.id === CONCEPT.id)) continue;
      let rec = null; try{ rec = JSON.parse(localStorage.getItem('astro_exam_' + key)); }catch(e){}
      let done = 0;
      m.concepts.forEach(c=>{ try{ const s = JSON.parse(localStorage.getItem('astro_' + c.id + '_support')); if(s && s.cleanLevel3) done++; }catch(e){} });
      return { key, title:m.title, total:m.concepts.length, done, complete:!!m.complete, passed:!!(rec && rec.passed), bestPct: rec ? rec.bestPct : null };
    }
  }catch(e){}
  return null;
}
"""))
R.append(("""function renderLadder(){
  const support = getSupport();
  const ladder = document.getElementById('ladder');
  ladder.innerHTML = [1,2,3,4].map(n=>{
    const cls = n === support.level ? 'current' : (n < support.level ? 'past' : '');
    return `<div class="rung ${cls}"><span class="code">${LEVELS[n].code}</span><span class="lbl">${LEVELS[n].label}</span></div>`;
  }).join('');
}
""", """function renderLadder(){
  const support = getSupport();
  const info = getExamInfo();
  const lvl = (info && info.passed) ? 4 : support.level;   // passing the module exam lights up E.04 on every concept in the module
  const ladder = document.getElementById('ladder');
  ladder.innerHTML = [1,2,3,4].map(n=>{
    const cls = n === lvl ? 'current' : (n < lvl ? 'past' : '');
    return `<div class="rung ${cls}"><span class="code">${LEVELS[n].code}</span><span class="lbl">${LEVELS[n].label}</span></div>`;
  }).join('');
  renderMissionBanner();
}

function renderMissionBanner(){
  const info = getExamInfo();
  const ladder = document.getElementById('ladder');
  let mb = document.getElementById('missionBanner');
  if(!mb){ mb = document.createElement('div'); mb.id = 'missionBanner'; ladder.parentNode.insertBefore(mb, ladder.nextSibling); }
  if(!info || !info.complete){ mb.innerHTML = ''; mb.style.display = 'none'; return; }
  mb.style.display = '';
  const base = 'border-radius:14px; padding:10px 14px; margin:-6px 0 16px; font-size:0.8rem; line-height:1.45; border:1px solid var(--line); background:var(--panel-hi);';
  const link = txt => `<a href="exam.html?m=${info.key}" style="color:var(--teal); font-weight:800; text-decoration:none; white-space:nowrap;">${txt} →</a>`;
  const title = escapeHtml(info.title);
  if(info.passed){
    mb.setAttribute('style', base + 'border-color:var(--teal);');
    mb.innerHTML = `🎯 <strong>Mission Ready!</strong> You passed the ${title} exam (best ${info.bestPct}%). ${link('Retake exam')}`;
  } else if(info.done === info.total){
    mb.setAttribute('style', base + 'border-color:var(--teal); box-shadow:0 0 14px rgba(77,216,224,0.3);');
    mb.innerHTML = `🎯 <strong>Exam Simulation is ready!</strong> All ${info.total} concepts mastered. ${link('Start the exam')}`;
  } else {
    mb.setAttribute('style', base);
    mb.innerHTML = `🎯 ${title} exam: <strong>${info.done}/${info.total}</strong> concepts mastered. Get a clean E.03 pass (no hints) on each one to unlock it.`;
  }
}
"""))

files = sorted(glob.glob(os.path.join(folder, "*.html")))
for path in files:
    name = os.path.basename(path)
    if name in ("index.html", "exam.html"): continue
    s = open(path, encoding="utf-8").read()
    for old, new in R:
        if s.count(old) != 1: sys.exit(f"{name}: block not found exactly once: {old[:50]!r}")
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)
print("patched", len([f for f in files if os.path.basename(f) not in ("index.html","exam.html")]), "files")
