// Checks Sentence Builder / Why Chain data against every concept's real mark points, using the engine's own matcher.
// Usage: node tools/test_builder.js project
const fs=require('fs'), path=require('path'), vm=require('vm');
const dir=process.argv[2]||'project';
const eng=fs.readFileSync(path.join(dir,'engine-template.html'),'utf8');
const fnSrc=eng.slice(eng.indexOf('function normText'), eng.indexOf('function escapeHtml'));
const checkMarkPoints=new Function(fnSrc+'; return checkMarkPoints;')();
const B=new Function(fs.readFileSync(path.join(dir,'builder-data.js'),'utf8')+'; return ASTRO_BUILDER;')();
const hub=fs.readFileSync(path.join(dir,'index.html'),'utf8');
const MODULES=eval('('+hub.match(/const MODULES = (\[[\s\S]*?\n\]);/)[1]+')');
const fill=(f,a)=>f.replace('___',a);
let fail=0,n=0; const bad=m=>{console.log('FAIL',m);fail++;};
for(const m of MODULES) for(const c of m.concepts){ if(!c.href) continue;
  const h=fs.readFileSync(path.join(dir,c.href),'utf8'); const x=h.match(/const CONCEPT = \{[\s\S]*?\n\};/);
  const C=eval('('+x[0].replace('const CONCEPT = ','').replace(/;$/,'')+')');
  const items=B[C.id]; n++;
  if(!items){bad(C.id+': no builder items');continue;}
  const mpIds=C.markPoints.map(p=>p.id);
  if(JSON.stringify(items.map(i=>i.mp).sort())!==JSON.stringify(mpIds.slice().sort())) bad(C.id+': items must cover each mark point exactly once');
  for(const it of items){
    const mp=C.markPoints.find(p=>p.id===it.mp); if(!mp){bad(C.id+': unknown mp '+it.mp);continue;}
    if((it.frame.match(/___/g)||[]).length!==1) bad(C.id+'/'+it.mp+': frame needs exactly one ___');
    n++; if(!checkMarkPoints(fill(it.frame,it.answer),[mp]).allFound) bad(C.id+'/'+it.mp+': correct filler does NOT pass its mark point: "'+fill(it.frame,it.answer)+'"');
    n++; if(checkMarkPoints(fill(it.frame,it.wrong),[mp]).allFound) bad(C.id+'/'+it.mp+': WRONG filler passes its mark point: "'+fill(it.frame,it.wrong)+'"');
    if(it.answer===it.wrong) bad(C.id+'/'+it.mp+': answer equals wrong');
  }
  n++; const para=items.map(i=>fill(i.frame,i.answer)).join(' ');
  const r=checkMarkPoints(para,C.markPoints);
  if(!r.allFound) bad(C.id+': whole paragraph misses '+r.results.filter(q=>!q.found).map(q=>q.id)+' -> "'+para+'"');
}
for(const k of Object.keys(B)) if(!MODULES.some(m=>m.concepts.some(c=>c.saveId===k))) bad('builder data for unknown concept '+k);
console.log((n-fail)+'/'+n+' builder checks pass'); process.exit(fail?1:0);
