// Regression tests for mark-point matching. Usage: node tools/test_matching.js project
const fs=require('fs'), path=require('path');
const dir=process.argv[2]||'project';
const eng=fs.readFileSync(path.join(dir,'engine-template.html'),'utf8');
const fnSrc=eng.match(/function normText[\s\S]*?function checkMarkPoints[\s\S]*?allFound[^\n]*\n\}/)[0];
const checkMarkPoints=new Function(fnSrc+'; return checkMarkPoints;')();
function load(f){const h=fs.readFileSync(path.join(dir,f),'utf8');
  const m=h.match(/const CONCEPT = \{[\s\S]*?\n\};/);
  return eval('('+m[0].replace('const CONCEPT = ','').replace(/;$/,'')+')');}
// [file, text, mark point id, expectFound]
const cases=[
 // false positives the old substring matcher allowed
 ['northpole.html','Since it was nice and twice as long','location',false],
 ['northpole.html','It is a very icy place with an ice cap','location',true],
 ['northpole.html','There was an iceberg near it','location',false],
 ['earth.html','People walk around the town','sphere',false],
 ['earth.html','Earth is shaped like a ball','sphere',true],
 ['earth.html','Earth is a football','sphere',false],
 ['earth.html','Earth is a planet that goes around the Sun','orbitsSun',true],
 ['earthaxis.html','It is a line on a page','imaginaryLine',false],
 ['earthaxis.html','It is an imaginary line','imaginaryLine',true],
 ['earthaxis.html','A line through Earth from pole to pole','imaginaryLine',true],
 ['compass.html','North is a direction people like','magneticNorth',false],
 ['compass.html','The needle points north','magneticNorth',true],
 ['compass.html','It points at magnetic north','usesMagnetism',false],
 ['compass.html','Earth acts like a giant magnet','usesMagnetism',true],
 ['compass.html','It uses Earth\u2019s magnetic field','usesMagnetism',true],
 ['day.html','Daytime is when it is warm','receivesLight',false],
 ['day.html','The side facing the Sun gets sunlight','receivesLight',true],
 ['day.html','The side facing the Sun','facingSun',true],
 ['day.html','Once in turn we go outside','rotationCause',false],
 ['day.html','Earth is spinning','rotationCause',true],
 ['earthrotation.html','It spins counter-clockwise','direction',true],
 ['earthrotation.html','It spins from west-to-east','direction',true],
 ['earthrotation.html','One day I will go','period',false],
 ['earthrotation.html','It takes 24 hours','period',true],
 ['hemisphere.html','Split by the equator','splitByEquator',true],
 ['hemisphere.html','The equator splits Earth in two','splitByEquator',true],
 ['hemisphere.html','The equator is hot','splitByEquator',false],
 ['latitude.html','The equator is 0\u00b0','equatorZero',true],
 ['latitude.html','It reaches 90\u00b0 at the poles','equatorZero',false],
 ['timezone.html','Different places have different times','rotationCause',false],
 ['timezone.html','Places face the Sun at different times','rotationCause',true],
 ['timezone.html','About 15\u00b0 per hour','longitude',true],
 ['shadow.html','The Sun is higher in the sky at noon','angle',true],
 ['shadow.html','The Sun is high in the sky so shadows are short','angle',true],
 ['earthspins.html','x','x',null],
];
let fail=0, n=0;
for(const [f,t,id,exp] of cases){
  if(exp===null) continue;
  const file=f==='earthspins.html'?'earth-spins.html':f;
  const C=load(file);
  const r=checkMarkPoints(t,C.markPoints).results.find(x=>x.id===id);
  n++;
  if(!r){console.log('MISSING mp',f,id);fail++;continue;}
  if(r.found!==exp){console.log('FAIL',f,id,JSON.stringify(t),'expected',exp,'got',r.found);fail++;}
}
// ---- A3 · Seasons: a model answer must pass EVERY mark point; a wrong answer must pass none ----
const A3 = {
 'earthorbit.html': ["Earth's orbit is its path around the Sun. One trip takes 365 days, and the Sun's gravity keeps it there.", "Earth is big and round and blue."],
 'tilt.html': ["Earth's axis is tilted by 23.5 degrees and it always points the same direction.", "Earth is round and spins."],
 'summer.html': ["A hemisphere is tilted toward the Sun, so it gets direct sunlight and longer days.", "Summer is when Earth is closer to the Sun."],
 'winter.html': ["The hemisphere is tilted away from the Sun, the light is spread out and the days are shorter.", "Winter is when Earth is far from the Sun."],
 'spring.html': ["Spring comes after winter, the days get longer and the hemisphere is tilting more toward the Sun.", "Spring is when flowers grow."],
 'autumn.html': ["Autumn comes after summer, the days get shorter and the hemisphere is tilting more away from the Sun.", "Autumn is when leaves fall."],
 'solstice.html': ["A solstice is when the hemisphere is tilted the most, giving the longest day or the shortest day. It happens twice a year.", "A solstice is a kind of star."],
 'equinox.html': ["At an equinox day and night are equal, and the Sun is directly over the equator. It happens twice a year.", "An equinox is a big storm."],
 'sunangle.html': ["A high Sun is more direct and concentrated. A low Sun is spread out over a larger area, so high is hotter.", "The Sun is big and yellow."],
 'daylength.html': ["Earth's tilt makes the days longer in summer and shorter in winter.", "Day is when it is light."],
};
for(const [f,[good,bad]] of Object.entries(A3)){
  const C=load(f);
  const g=checkMarkPoints(good,C.markPoints), b=checkMarkPoints(bad,C.markPoints);
  n++;
  if(!g.results.every(r=>r.found)){console.log('A3 FAIL model answer',f,g.results.filter(r=>!r.found).map(r=>r.id));fail++;}
  n++;
  if(b.results.some(r=>r.found)){console.log('A3 FAIL wrong answer passes',f,b.results.filter(r=>r.found).map(r=>r.id));fail++;}
  for(const q of C.examQuestions) for(const id of q.markPoints) if(!C.markPoints.some(m=>m.id===id)){console.log('A3 FAIL exam refs unknown mp',f,id);fail++;}
}
console.log(n-fail+'/'+n+' cases pass');
process.exit(fail?1:0);
