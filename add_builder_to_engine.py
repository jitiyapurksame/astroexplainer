"""Phase 4 engine change: 🧱 Sentence Builder + 🔗 Why Chain tabs (data in builder-data.js).
Applies the same exact old->new replacement to engine-template.html and every concept file (fails loudly if a block is missing).
Usage: python3 tools/add_builder_to_engine.py project"""
import sys, os, glob
folder = sys.argv[1] if len(sys.argv) > 1 else "project"

CSS = """  .b-progress{font-size:0.78rem; color:#B9C0EA; margin:0 0 12px;}
  .bcard,.cslot{display:flex; gap:12px; align-items:flex-start; background:var(--panel); border:2px solid var(--line);
    border-radius:16px; padding:12px 14px; margin-bottom:10px;}
  .bcard.done,.cslot.right{border-color:var(--teal); background:rgba(77,216,224,0.08);}
  .cslot.filled{border-color:var(--dusk);} .cslot.wrongpos{border-color:var(--danger); background:rgba(255,107,107,0.08);}
  .cslot.empty{border-style:dashed; color:#8A92C7; cursor:default;} .cslot.filled,.cslot.wrongpos,.cslot.right{cursor:pointer;}
  .bnum{flex:0 0 28px; height:28px; border-radius:50%; background:var(--panel-hi); border:1px solid var(--line);
    display:flex; align-items:center; justify-content:center; font-family:'Baloo 2'; font-weight:800; font-size:0.85rem; color:var(--sun-soft);}
  .bcard.done .bnum,.cslot.right .bnum{background:var(--teal); color:#08221f; border-color:var(--teal);}
  .bbody,.cbody{flex:1; min-width:0; font-size:0.95rem; line-height:1.5;}
  .bblank{display:inline-block; min-width:70px; border-bottom:3px dashed var(--sun-soft); text-align:center; padding:0 6px;}
  .bblank.filled{border-bottom:3px solid var(--teal); color:var(--teal); font-weight:800;}
  .bopts{display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;}
  .bopt{padding:9px 14px; border-radius:999px; border:2px solid var(--line); background:var(--panel-hi); font-size:0.85rem; font-weight:700; cursor:pointer;}
  .bopt:active{transform:scale(0.97);} .bopt.wrong{opacity:.4; text-decoration:line-through; cursor:default;}
  .bnote{font-size:0.78rem; color:var(--sun-soft); margin-top:8px;}
  .b-final{background:rgba(77,216,224,0.1); border:2px solid var(--teal); border-radius:16px; padding:14px; margin:12px 0;}
  .b-final p{margin:8px 0 0; line-height:1.55; font-size:0.9rem;}
  .c-tray{display:flex; flex-direction:column; gap:8px; margin:12px 0;}
  .ccard{background:var(--panel-hi); border:2px solid var(--sun-soft); border-radius:14px; padding:11px 14px; font-size:0.9rem; line-height:1.45; cursor:pointer;}
"""

JS = r"""// ---------- Phase 4: Sentence Builder + Why Chain (generic scaffolds; sentences live in builder-data.js) ----------
function builderItems(){ return (typeof ASTRO_BUILDER !== 'undefined' && ASTRO_BUILDER[CONCEPT.id]) ? ASTRO_BUILDER[CONCEPT.id] : null; }
function getBuilderState(){ try{ return JSON.parse(localStorage.getItem('astro_' + CONCEPT.id + '_builder')) || {}; }catch(e){ return {}; } }
function setBuilderState(patch){ const s = Object.assign(getBuilderState(), patch); localStorage.setItem('astro_' + CONCEPT.id + '_builder', JSON.stringify(s)); }
function shuffleArr(a){ a = a.slice(); for(let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
function fillFrame(frame, answer){ return frame.replace('___', answer); }
function sentenceHtml(frame, answer, filled){
  const parts = frame.split('___');
  return escapeHtml(parts[0]) + (filled ? `<span class="bblank filled">${escapeHtml(answer)}</span>` : '<span class="bblank">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>') + escapeHtml(parts[1] || '');
}
function builderDecoyPool(){
  const pool = [];
  try{
    let ids = null;
    if(typeof ASTRO_MODULES !== 'undefined'){
      for(const k in ASTRO_MODULES){ const m = ASTRO_MODULES[k]; if(m.concepts.some(c=>c.id === CONCEPT.id)){ ids = m.concepts.map(c=>c.id); break; } }
    }
    if(!ids) ids = Object.keys(ASTRO_BUILDER);
    ids.forEach(id=>{ if(id !== CONCEPT.id && ASTRO_BUILDER[id]) ASTRO_BUILDER[id].forEach(it=>pool.push(it.answer)); });
  }catch(e){}
  return pool;
}
// Each blank gets 3 choices: the right words, the authored wrong words, and one decoy borrowed from another concept in the module
// (only used if it would NOT pass this mark point when dropped into the sentence).
function newBuilderRun(){
  const data = builderItems(); if(!data) return null;
  const pool = builderDecoyPool();
  return data.map(it=>{
    const mp = (CONCEPT.markPoints || []).find(m=>m.id === it.mp);
    const wrongs = [it.wrong];
    const extra = shuffleArr(pool).find(a => a !== it.answer && a !== it.wrong && mp && !checkMarkPoints(fillFrame(it.frame, a), [mp]).allFound);
    if(extra) wrongs.push(extra);
    return { frame:it.frame, answer:it.answer, options:shuffleArr([it.answer].concat(wrongs)), done:false, tried:[] };
  });
}
let builderRun = null;

function renderBuilder(){
  const stage = document.getElementById('stage');
  const support = getSupport();
  if(!builderRun) builderRun = newBuilderRun();
  if(!builderRun){ stage.innerHTML = '<div class="locked-note">The Sentence Builder is not available for this concept.</div>'; return; }
  const doneCount = builderRun.filter(x=>x.done).length;
  const allDone = doneCount === builderRun.length;
  stage.innerHTML = `
    <p class="prompt">🧱 <strong>Sentence Builder</strong> — build your explanation one sentence at a time. Tap the words that fit the gap.</p>
    <div class="b-progress">${doneCount}/${builderRun.length} sentences built</div>
    ${builderRun.map((it, i)=>`
      <div class="bcard ${it.done ? 'done' : ''}">
        <div class="bnum">${it.done ? '✓' : i + 1}</div>
        <div class="bbody">
          <div class="bsent">${sentenceHtml(it.frame, it.answer, it.done)}</div>
          ${it.done ? '' : `<div class="bopts">${it.options.map(o=>`<div class="bopt ${it.tried.includes(o) ? 'wrong' : ''}" data-i="${i}" data-o="${encodeURIComponent(o)}">${escapeHtml(o)}</div>`).join('')}</div>
          ${it.tried.length ? '<div class="bnote">Not quite, try another one.</div>' : ''}`}
        </div>
      </div>`).join('')}
    ${allDone ? `
      <div class="b-final"><strong>✅ You built it!</strong><p>${escapeHtml(builderRun.map(x=>fillFrame(x.frame, x.answer)).join(' '))}</p></div>
      ${support.level < 3 ? '<button class="primary-btn" id="bUse">✍️ Use it in my answer box</button>' : '<div class="locked-note" style="margin-top:10px">At E.03 · Solo Flight you write the answer yourself. This is just practice, nice work!</div>'}
      <div class="stuck-link" id="bAgain">🔁 Build again</div>` : ''}
  `;
  stage.querySelectorAll('.bopt').forEach(el=>{
    el.onclick = ()=>{
      const i = +el.dataset.i, o = decodeURIComponent(el.dataset.o), it = builderRun[i];
      if(it.done || it.tried.includes(o)) return;
      if(o === it.answer){
        it.done = true;
        if(builderRun.every(x=>x.done)){ setBuilderState({ builderDone:true }); renderTabs(); showToast('🧱 Builder complete!'); }
      } else it.tried.push(o);
      renderBuilder();
    };
  });
  const use = document.getElementById('bUse');
  if(use) use.onclick = ()=>{
    sessionStorage.setItem('astro_builderdraft_' + CONCEPT.id, builderRun.map(x=>fillFrame(x.frame, x.answer)).join(' '));
    activeTab = 'explainer'; renderTabs(); renderStage();
  };
  const again = document.getElementById('bAgain');
  if(again) again.onclick = ()=>{ builderRun = newBuilderRun(); renderBuilder(); };
}

let chainRun = null;
function newChainRun(){
  const data = builderItems(); if(!data) return null;
  let order, tries = 0;
  do { order = shuffleArr(data.map((_, i)=>i)); tries++; } while(order.every((v, i)=>v === i) && tries < 20);
  return { order, slots:new Array(data.length).fill(null), checked:false, solved:false };
}
function renderChain(){
  const stage = document.getElementById('stage');
  const data = builderItems();
  if(!data){ stage.innerHTML = '<div class="locked-note">The Why Chain is not available for this concept.</div>'; return; }
  if(!chainRun) chainRun = newChainRun();
  const r = chainRun;
  const sentence = i => fillFrame(data[i].frame, data[i].answer);
  const placed = new Set(r.slots.filter(x=>x !== null));
  const tray = r.order.filter(i=>!placed.has(i));
  const full = r.slots.every(x=>x !== null);
  stage.innerHTML = `
    <p class="prompt">🔗 <strong>Why Chain</strong> — put the sentences in the order that makes the best explanation, so each one leads to the next.</p>
    <div class="b-progress">Tip: start with the main idea or the cause, and finish with the result.</div>
    ${r.slots.map((v, k)=>{
      const cls = v === null ? 'empty' : (r.checked ? (v === k ? 'right' : 'wrongpos') : 'filled');
      return `<div class="cslot ${cls}" data-k="${k}"><div class="bnum">${v !== null && r.checked && v === k ? '✓' : k + 1}</div><div class="cbody">${v === null ? 'Tap a sentence below to put it here' : escapeHtml(sentence(v))}</div></div>`;
    }).join('')}
    ${tray.length ? `<div class="c-tray">${tray.map(i=>`<div class="ccard" data-i="${i}">${escapeHtml(sentence(i))}</div>`).join('')}</div>` : ''}
    ${r.solved ? `<div class="b-final"><strong>🔗 Chain complete!</strong><p>That is a clear explanation: each sentence leads to the next.</p></div><div class="stuck-link" id="cAgain">🔁 Try again with a new shuffle</div>`
      : `<button class="primary-btn" id="cCheck" ${full ? '' : 'disabled style="opacity:.5"'}>Check my chain</button>
         ${r.checked ? '<div class="bnote">Not quite. Green ones are in the right place. Tap a red one to move it.</div>' : ''}`}
  `;
  stage.querySelectorAll('.ccard').forEach(el=>{
    el.onclick = ()=>{ if(r.solved) return; const k = r.slots.indexOf(null); if(k < 0) return; r.slots[k] = +el.dataset.i; r.checked = false; renderChain(); };
  });
  stage.querySelectorAll('.cslot').forEach(el=>{
    el.onclick = ()=>{ if(r.solved) return; const k = +el.dataset.k; if(r.slots[k] === null) return; r.slots[k] = null; r.checked = false; renderChain(); };
  });
  const chk = document.getElementById('cCheck');
  if(chk) chk.onclick = ()=>{
    if(!full) return;
    r.checked = true;
    if(r.slots.every((v, k)=>v === k)){ r.solved = true; setBuilderState({ chainDone:true }); renderTabs(); showToast('🔗 Chain complete!'); }
    renderChain();
  };
  const again = document.getElementById('cAgain');
  if(again) again.onclick = ()=>{ chainRun = newChainRun(); renderChain(); };
}

"""

R = []
R.append(('<script src="exam-data.js"></script>\n<script>', '<script src="exam-data.js"></script>\n<script src="builder-data.js"></script>\n<script>'))
R.append(("  .tab-row{display:flex; gap:8px; margin:0 0 16px;}", "  .tab-row{display:flex; gap:6px; margin:0 0 16px;}"))
R.append(("  .tab{flex:1; text-align:center; padding:10px 6px; border-radius:12px; border:2px solid var(--line);\n    background:var(--panel); font-size:0.76rem;",
          "  .tab{flex:1; text-align:center; padding:10px 4px; border-radius:12px; border:2px solid var(--line);\n    background:var(--panel); font-size:0.7rem;"))
R.append(("  .exam-label{display:inline-block;", CSS + "  .exam-label{display:inline-block;"))
R.append(("  const cardUnlocked = !!support.cleanLevel3;\n  const tabRow = document.getElementById('tabRow');",
          "  const cardUnlocked = !!support.cleanLevel3;\n  const hasBuilder = !!builderItems();\n  const chainUnlocked = support.level >= 2;\n  const bs = getBuilderState();\n  const tabRow = document.getElementById('tabRow');"))
R.append(("""    <div class="tab ${activeTab==='explainer'?'active':''}" data-tab="explainer">🚀 Explainer Lab</div>\n""",
          """    <div class="tab ${activeTab==='explainer'?'active':''}" data-tab="explainer">🚀 Explainer Lab</div>
    ${hasBuilder ? `<div class="tab ${activeTab==='builder'?'active':''}" data-tab="builder">🧱 Builder${bs.builderDone ? ' ✓' : ''}</div>
    <div class="tab ${activeTab==='chain'?'active':''} ${chainUnlocked?'':'locked'}" data-tab="chain">${chainUnlocked ? '🔗 Why Chain' : '🔒 Why Chain'}${bs.chainDone ? ' ✓' : ''}</div>` : ''}\n"""))
R.append(("      if(tab === 'examiner' && !examinerUnlocked){",
          "      if(tab === 'chain' && !chainUnlocked){\n        showToast('Reach E.02 · Guided Flight to unlock the Why Chain');\n        return;\n      }\n      if(tab === 'examiner' && !examinerUnlocked){"))
R.append(("function renderStage(){\n  if(activeTab === 'examiner') renderExaminerMode();",
          JS + "function renderStage(){\n  if(activeTab === 'builder') renderBuilder();\n  else if(activeTab === 'chain') renderChain();\n  else if(activeTab === 'examiner') renderExaminerMode();"))
R.append(("  if(prevLevelText){\n    const prevLink = document.getElementById('prevAnswerLink');",
          "  const builderDraft = sessionStorage.getItem('astro_builderdraft_' + CONCEPT.id);\n  sessionStorage.removeItem('astro_builderdraft_' + CONCEPT.id);\n  if(builderDraft && support.level < 3) document.getElementById('explainBox').value = builderDraft;\n\n  if(prevLevelText){\n    const prevLink = document.getElementById('prevAnswerLink');"))

for path in sorted(glob.glob(os.path.join(folder, "*.html"))):
    name = os.path.basename(path)
    if name in ("index.html", "exam.html"): continue
    s = open(path, encoding="utf-8").read()
    for old, new in R:
        if s.count(old) != 1: sys.exit(f"{name}: block not found exactly once: {old[:60]!r}")
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)
print("patched")
