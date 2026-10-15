"""Phase 2: (1) swap the matcher in engine-template + every concept file,
(2) rewrite loose mark-point terms. Usage: python3 tighten_terms.py ../project
Idempotent-safe: fails loudly if an expected block is not found."""
import re, sys, glob, os
folder = sys.argv[1] if len(sys.argv) > 1 else "project"

OLD_MATCHER = """function checkMarkPoints(text, markPoints){
  const lower = (text||'').toLowerCase();
  const results = (markPoints||[]).map(mp => ({
    id: mp.id, label: mp.label,
    found: mp.terms.some(t => lower.includes(t.toLowerCase()))
  }));"""
NEW_MATCHER = """// Matching rules (Phase 2): text and terms are normalised (lowercase, curly quotes -> ', hyphens -> space).
// A term matches only where it STARTS a word (so 'ice' no longer matches 'nice'/'since', 'round' not 'around').
// A trailing $ on a term means the word must also END there ('ice$' matches 'ice' but not 'iceberg').
function normText(s){
  return (s||'').toLowerCase().replace(/[\\u2018\\u2019\\u02BC]/g, "'").replace(/[\\u2013\\u2014-]/g, ' ').replace(/\\s+/g, ' ').trim();
}
function hasTerm(text, rawTerm){
  let term = String(rawTerm||'');
  const whole = term.endsWith('$');
  if(whole) term = term.slice(0, -1);
  term = normText(term);
  if(!term) return false;
  let i = 0;
  while((i = text.indexOf(term, i)) !== -1){
    const before = i === 0 ? '' : text.charAt(i-1);
    const after = text.charAt(i + term.length);
    if(!/[a-z0-9]/.test(before) && (!whole || !/[a-z0-9]/.test(after))) return true;
    i++;
  }
  return false;
}
function checkMarkPoints(text, markPoints){
  const lower = normText(text);
  const results = (markPoints||[]).map(mp => ({
    id: mp.id, label: mp.label,
    found: mp.terms.some(t => hasTerm(lower, t))
  }));"""

SPIN = ['spin','rotat','earth turns','earth is turning','turns on','turns around','turning on','turning around']
FACE_SUN = ['facing the sun','faces the sun','face the sun','facing toward','facing towards','toward the sun','towards the sun','facing sunlight','pointing at the sun','pointed at the sun','points at the sun']
AWAY = ['facing away','faces away','face away','turned away','turns away','turning away','away from the sun','away from the light','back to the sun']

T = {
 'compass': {
  'needlePoints': ['needle','points to','pointing','points toward','points towards','points north','points at','arrow'],
  'magneticNorth': ['magnetic north','points north','pointing north','points to north','points to the north','toward north','towards north','toward the north','towards the north','shows north','show north','north pole','north direction'],
  'usesMagnetism': ['magnetism','magnetic field','magnetic force','magnetic pull','magnetic needle','is magnetic','magnet$','magnets$','attracted by','attracts'],
 },
 'day': {
  'facingSun': FACE_SUN + ['turned toward the sun','turned towards the sun'],
  'receivesLight': ['sunlight','sun\'s light','light from the sun','sun shines','sun is shining','shining on','lit up','lit by','gets light','receives light','gets sunlight','daylight','bright light','bright side','brightly lit'],
  'rotationCause': SPIN,
 },
 'earthspins': {
  'rotation': SPIN,
  'axis': ['axis'],
  'sunlight': FACE_SUN + ['sunlight','light from the sun','toward the light','towards the light','facing the light','faces the light','sun shines','lit by','lit up'],
  'facingAway': AWAY + ['opposite side','other side','dark side','night side','not facing the sun','not facing'],
 },
 'earth': {
  'planet': ['planet'],
  'sphere': ['sphere','spherical','round','ball$','globe'],
  'orbitsSun': ['orbit','around the sun','revolv','circles the sun','circling the sun'],
 },
 'earthaxis': {
  'imaginaryLine': ['imaginary','invisible','not a real','not real','pretend','line through','line from','line running','line that goes','line that runs','line between'],
  'poles': ['north pole','south pole','poles$','pole to pole'],
  'spinsAround': SPIN,
 },
 'earthrotation': {
  'axis': ['axis'],
  'direction': ['west to east','west to the east','counterclockwise','counter clockwise','anticlockwise','anti clockwise','eastward','towards the east','toward the east','to the east'],
  'period': ['24 hour','24hr','24 hrs','24h','a full day','a whole day','once a day','once every day','once per day','one full day','one whole day','1 day','takes a day','takes one day','one day to','twenty four hour'],
 },
 'equator': {
  'middleLine': ['middle','center','centre','around the middle','around the globe','around the earth','around earth'],
  'dividesHemispheres': ['northern','southern','two halves','2 halves','hemisphere','north and south','top and bottom','splits earth','splits the earth','divides earth','divides the earth','separates earth','separates the earth'],
  'equalDistance': ['halfway','half way','equal distance','equally far','same distance','equidistant','midway','between the poles'],
 },
 'globevsmap': {
  'globeIsSphere': ['round','sphere','spherical','3d','three dimensional','curved','ball$'],
  'mapIsFlattened': ['flatten','map is flat','maps are flat','is flat','are flat','stretch','squash','2d','two dimensional','flat paper','on paper'],
  'distortion': ['distort','inaccurate','not accurate','less accurate','wrong shape','wrong size','warp','misleading'],
 },
 'hemisphere': {
  'halfOfEarth': ['half'],
  'splitByEquator': ['equator splits','equator divides','equator separates','equator cuts','split by the equator','split by equator','splits at the equator','divided by the equator','divided by equator','divided at the equator','separated by the equator','separated by equator','cut by the equator'],
  'namedHalves': ['northern hemisphere','southern hemisphere','northern and southern','north and south','north half','south half','northern half','southern half'],
 },
 'latitude': {
  'horizontalLines': ['horizontal','side to side','east west','east to west','west to east','left to right','sideways','parallel','run across','runs across','go across','goes across','runs around','go around'],
  'measuresNorthSouth': ['north or south','north south','north and south','how far north','how far south','distance from equator','distance from the equator','distance north','distance south','north of','south of'],
  'equatorZero': ['equator is zero','equator is 0','equator is at zero','equator is at 0','equator at 0','0 degrees','zero degrees','0°','zero at the equator','starts at the equator','start at the equator','begins at the equator'],
 },
 'longitude': {
  'verticalLines': ['vertical','up and down','pole to pole','top to bottom','north to south'],
  'measuresEastWest': ['east or west','east west','east and west','how far east','how far west','distance east','distance west','east of','west of','distance from the prime meridian','distance from prime meridian','from the prime meridian'],
  'meetAtPoles': ['meet at the pole','meet at both pole','meet at each pole','meet at the north','meet at the south','meet at north','meet at south','join at the pole','come together at the pole','converge','touch at the pole','meet at the top','meet at the bottom'],
 },
 'midnight': {
  'facingAway': AWAY + ['most directly away','directly away','opposite the sun','points away from the sun','farthest from the sun','furthest from the sun'],
  'middle': ['middle of the night','middle of night','deepest night','darkest','halfway through the night','half way through the night','center of the night','centre of the night','midpoint of the night'],
 },
 'night': {
  'facingAway': AWAY + ['opposite side','other side','not facing'],
  'noDirectLight': ['dark','no light','no sunlight','no direct','not lit','isn\'t lit','doesn\'t get any light','doesn\'t get light','does not get any light','does not get light','doesn\'t receive','does not receive','cannot reach','can\'t reach','block','shadow'],
  'rotationCause': SPIN,
 },
 'noon': None,
 'shadow': {
  'opposite': ['opposite the sun','opposite to the sun','opposite direction','away from the sun','on the opposite side'],
  'angle': ['angle','how high','higher in the sky','lower in the sky','height of the sun','sun is higher','sun is lower','sun is high','sun is low','high in the sky','low in the sky','position of the sun'],
  'changes': ['rotat','earth spins','earth is spinning','earth turns','changes through the day','changes throughout the day','throughout the day','over the day','during the day','sun moves'],
 },
 'northpole': {
  'axisTop': ['top of the axis','top of earth\'s axis','top end of','end of the axis','end of earth\'s axis','axis at the top','axis through the north','axis goes through','axis passes','axis points to','axis comes out','axis meets','axis ends','axis exits','where the axis','where earth\'s axis'],
  'northernmost': ['furthest north','farthest north','northernmost','most northern','top of the world'],
  'location': ['arctic','icy$','ice$','ice cap','ice caps','frozen','freezing','snow','polar bear','cold'],
 },
 'southpole': {
  'axisBottom': ['bottom of the axis','bottom of earth\'s axis','bottom end of','end of the axis','end of earth\'s axis','axis at the bottom','axis through the south','axis goes through','axis passes','axis points to','axis comes out','axis meets','axis ends','axis exits','where the axis','where earth\'s axis'],
  'southernmost': ['furthest south','farthest south','southernmost','most southern','bottom of the world'],
  'oppositeNorth': ['opposite the north','opposite to the north','opposite of the north','opposite from the north','opposite end','other end','opposite side','across from the north','farthest from the north','furthest from the north','opposite north','opposite to north'],
 },
 'sunrise': {
  'rotation': SPIN,
  'terminator': ['terminator','boundary','line between','edge of the light','edge of the dark','edge of day','edge of night','border','dividing line','day night line','where day meets night','line that separates'],
  'direction': ['east','into the light','into the day','into the sunlight','toward the sun','towards the sun','toward the light','towards the light','into the sun','from night into day'],
 },
 'sunset': {
  'rotation': SPIN,
  'terminator': ['terminator','boundary','line between','edge of the light','edge of the dark','edge of day','edge of night','border','dividing line','day night line','where day meets night','line that separates'],
  'direction': ['west','away from the sun','away from the light','into the dark','into the night','out of the light','out of the sun','out of the sunlight','from day into night'],
 },
 'timezone': {
  'rotationCause': ['face the sun at','facing the sun at','faces the sun at','sun at different','sun at a different','sun shines on different','sun reaches','sun hits','not facing the sun at the same','not all face','not every place','not every part','one side','depends where','depends on where','depends on location','depends on the location','at different times because','at different times as','at different times since'],
  'longitude': ['longitude','15 degree','15°','degrees of longitude'],
  'eastAhead': ['further east','farther east','east is ahead','east are ahead','east ahead','ahead in time','east is later','east first','sees the sun first','more east','eastern'],
 },
}

LABEL = r'''(?:'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")'''

def js_list(items):
    seen, out = set(), []
    for t in items:
        if t in seen: continue
        seen.add(t); out.append("'" + t.replace("\\", "\\\\").replace("'", "\\'") + "'")
    return "[" + ", ".join(out) + "]"

def patch(path, fn):
    s = open(path, encoding="utf-8").read()
    s2 = fn(s)
    if s2 != s: open(path, "w", encoding="utf-8").write(s2)

def swap_matcher(s, path):
    if OLD_MATCHER not in s:
        sys.exit(f"{os.path.basename(path)}: old matcher block NOT FOUND")
    return s.replace(OLD_MATCHER, NEW_MATCHER)

files = sorted(glob.glob(os.path.join(folder, "*.html")))
for path in files:
    name = os.path.basename(path)
    if name == "index.html": continue
    s = open(path, encoding="utf-8").read()
    s = swap_matcher(s, path)
    if name != "engine-template.html":
        cid = re.search(r"^\s*id:\s*'([^']+)'", s[s.index("const CONCEPT"):], re.M).group(1)
        if cid not in T: sys.exit(f"{name}: concept id {cid} has no term table")
        if T[cid] is None:   # reviewed, terms already specific: matcher swap only
            open(path, "w", encoding="utf-8").write(s); print("patched (matcher only)", name); continue
        for mp, terms in T[cid].items():
            pat = re.compile(r"(id:'" + re.escape(mp) + r"',\s*label:" + LABEL + r",\s*terms:)\[[^\]]*\]")
            s, n = pat.subn(lambda m: m.group(1) + js_list(terms), s)
            if n != 1: sys.exit(f"{name}: mark point {mp} matched {n} times")
        # every markPoint in the file must have been covered
        ids = re.findall(r"id:'([^']+)',\s*label:" + LABEL + r",\s*terms:", s)
        missing = [i for i in ids if i not in T[cid]]
        if missing: sys.exit(f"{name}: uncovered mark points {missing}")
    open(path, "w", encoding="utf-8").write(s)
    print("patched", name)
