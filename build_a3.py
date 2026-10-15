"""Generate A3 · Seasons concept files. Run from the package root:  python3 tools/build_a3.py project
Reuses build() from new_concept_example.py and the SVGs from a3_svgs.py."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from new_concept_example import build
from a3_svgs import SVGS

folder = sys.argv[1] if len(sys.argv) > 1 else "project"

def C(id, icon, title, prompt, starters, pills, mps, hints, exam_prompt, exam_ids):
    return dict(id=id, icon=icon, title=title, filename=id + ".html", prompt=prompt, starters=starters,
                word_choices=pills, svg=SVGS[id], mark_points=[dict(id=a, label=b, terms=c) for a, b, c in mps],
                hints=hints, exam_prompt=exam_prompt, exam_marks=len(exam_ids), exam_mark_ids=exam_ids)

CONCEPTS = [
 C('earthorbit','🛰️','Earth Orbit',
   "In your own words: what is Earth's orbit, and how long does one trip around the Sun take?",
   ["Earth's orbit is the path ...", "Earth travels around the ... and one trip takes ...", "Earth stays on its path because ..."],
   ['orbit','one year','gravity','Sun'],
   [('orbitPath','Path around the Sun',['orbit','around the sun','revolv','circles the sun','circling the sun','path around']),
    ('period','Takes one year',['365','one year','a full year','1 year','12 months','twelve months','takes a year','once a year','once per year','every year']),
    ('gravity',"Held in by the Sun's gravity",['gravity','gravitational','pull of the sun','sun pulls',"sun's pull",'pulled by the sun','pulls earth'])],
   ["You said Earth moves. What is it moving around, and what do we call that path?",
    "Good. How long does one full trip around the Sun take?",
    "Last piece: what pull from the Sun keeps Earth on its path instead of flying away?"],
   "Describe Earth's orbit and how long it takes.", ['orbitPath','period']),

 C('tilt','📐','Tilt',
   "In your own words: what does it mean that Earth is tilted, and does the tilt change as Earth goes around the Sun?",
   ["Earth's axis is tilted by about ...", "Instead of standing straight up, Earth ...", "As Earth orbits, the tilt always points ..."],
   ['tilted','23.5°','same direction','axis'],
   [('tilted','Axis is tilted',['tilt','leans','leaning','slanted','not straight up','not upright','angled']),
    ('amount','About 23.5°',['23.5','23 degrees','23°','23 and a half','about 23','twenty three']),
    ('fixedDirection','Always points the same direction',['same direction','same way','always points','keeps pointing','stays tilted','stays pointing','stays pointed','always tilted','same tilt','never changes','north star','polaris','fixed direction'])],
   ["Earth is not standing straight up. What is leaning, and by how many degrees?",
    "Good. Now picture Earth going around the Sun. Does the tilt flip around, or point the same way?",
    "Try this: 'The tilt always points the same direction in space (toward the North Star).'"],
   "Describe Earth's tilt.", ['tilted','amount','fixedDirection']),

 C('summer','☀️','Summer',
   "In your own words: why does a hemisphere have summer? Is it because Earth is closer to the Sun?",
   ["Summer happens when a hemisphere is ...", "In summer, sunlight hits the ground more ...", "It isn't about distance, it's about ..."],
   ['tilted toward','direct sunlight','longer days','hemisphere'],
   [('tiltedToward','Tilted toward the Sun',['tilted toward','tilted towards','tilts toward','tilts towards','tilting toward','leans toward','leaning toward','pointing toward the sun','pointed toward the sun']),
    ('directSunlight','More direct sunlight',['direct sunlight','direct rays','more direct','directly overhead','higher in the sky','sun is higher','sun is high','high in the sky','more concentrated','steeper angle','hits more directly','strikes more directly']),
    ('longerDays','Longer days',['longer days','longer daylight','more daylight','more hours of daylight','days are longer','longer day','long days','more hours of sun','more hours of light'])],
   ["Forget distance for a moment. Which way is that hemisphere leaning: toward the Sun or away?",
    "Good. How does the Sun's light reach the ground: straight on, or at a slant?",
    "One more effect: what happens to the number of daylight hours?"],
   "Explain why a hemisphere has summer.", ['tiltedToward','directSunlight','longerDays']),

 C('winter','❄️','Winter',
   "In your own words: why does a hemisphere have winter, even though Earth is not farther from the Sun?",
   ["Winter happens when a hemisphere is ...", "In winter, sunlight hits the ground at a ...", "The days in winter are ..."],
   ['tilted away','slanted rays','shorter days','hemisphere'],
   [('tiltedAway','Tilted away from the Sun',['tilted away','tilts away','tilting away','leans away','leaning away','pointing away from the sun','pointed away from the sun']),
    ('indirectSunlight','Less direct, spread-out sunlight',['indirect','less direct','slanted','at a slant','at an angle','lower in the sky','sun is lower','sun is low','low in the sky','spread out','less concentrated','shallow angle','weaker']),
    ('shorterDays','Shorter days',['shorter days','shorter daylight','less daylight','fewer hours of daylight','days are shorter','shorter day','short days','fewer hours of sun','fewer hours of light'])],
   ["Which way is that hemisphere leaning now: toward the Sun or away?",
    "Good. How does the Sun's light reach the ground: straight on, or at a slant and spread out?",
    "One more effect: what happens to the number of daylight hours?"],
   "Explain why a hemisphere has winter.", ['tiltedAway','indirectSunlight','shorterDays']),

 C('spring','🌸','Spring',
   "In your own words: what is spring, and what is changing about the Sun and the days as it arrives?",
   ["Spring comes after ... and before ...", "During spring the days get ...", "The hemisphere is tilting more ... the Sun, so ..."],
   ['after winter','longer days','tilting toward','before summer'],
   [('transition','Between winter and summer',['between winter and summer','after winter','before summer','follows winter','comes after winter','transition','winter into summer','changing from winter','moving from winter']),
    ('daysLengthen','Days getting longer',['days get longer','days are getting longer','days getting longer','longer days','daylight increases','more daylight','day length increases','days grow longer','days lengthen','gradually longer']),
    ('tiltChange','Tilting more toward the Sun',['tilting toward','tilting more toward','tilting towards','tilts more toward','tilted more toward','more tilted toward','leaning more toward','starting to tilt toward','beginning to tilt toward','starts to tilt toward','turning toward the sun','tilt toward the sun','tilt towards the sun'])],
   ["Which two seasons does spring sit between?",
    "Good. What is happening to the length of the days?",
    "Last piece: which way is the hemisphere tilting, toward the Sun or away?"],
   "Describe what is happening to the days and the tilt during spring.", ['daysLengthen','tiltChange']),

 C('autumn','🍂','Autumn',
   "In your own words: what is autumn (fall), and what is changing about the Sun and the days as it arrives?",
   ["Autumn comes after ... and before ...", "During autumn the days get ...", "The hemisphere is tilting more ... the Sun, so ..."],
   ['after summer','shorter days','tilting away','before winter'],
   [('transition','Between summer and winter',['between summer and winter','after summer','before winter','follows summer','comes after summer','summer into winter','changing from summer','moving from summer']),
    ('daysShorten','Days getting shorter',['days get shorter','days are getting shorter','days getting shorter','shorter days','daylight decreases','less daylight','day length decreases','days grow shorter','days shorten']),
    ('tiltChange','Tilting more away from the Sun',['tilting away','tilting more away','tilts more away','tilted more away','more tilted away','leaning more away','starting to tilt away','beginning to tilt away','starts to tilt away','turning away from the sun','tilt away from the sun'])],
   ["Which two seasons does autumn sit between?",
    "Good. What is happening to the length of the days?",
    "Last piece: which way is the hemisphere tilting, toward the Sun or away?"],
   "Describe what is happening to the days and the tilt during autumn.", ['daysShorten','tiltChange']),

 C('solstice','📅','Solstice',
   "In your own words: what is a solstice, and how many happen each year?",
   ["A solstice is when a hemisphere is ...", "On a solstice the day is either the ... or the ...", "There are ... solstices a year, in ... and ..."],
   ['most tilted','longest day','shortest day','twice a year'],
   [('maxTilt','Tilted the most toward or away',['most tilted','maximum tilt','fully tilted','tilted the most','tilted most toward','tilted most away','tilted furthest','tilted farthest','tilted as far','furthest toward','farthest toward','greatest tilt','extreme tilt']),
    ('longestShortest','Longest or shortest day',['longest day','shortest day','longest and shortest','longest daylight','shortest daylight','longest night','shortest night']),
    ('twoPerYear','Two a year (June and December)',['two a year','twice a year','twice each year','twice per year','two solstices','two times','summer solstice','winter solstice','june','december'])],
   ["Think about the tilt. At a solstice, how far toward or away from the Sun is the hemisphere tilted?",
    "Good, the maximum. What does that do to the length of the day?",
    "Last piece: how many solstices are there in a year, and roughly when?"],
   "Explain what happens to Earth's tilt and the length of the day at a solstice.", ['maxTilt','longestShortest']),

 C('equinox','⚖️','Equinox',
   "In your own words: what is an equinox, and what is special about day and night?",
   ["At an equinox, day and night are ...", "At an equinox the Sun is directly over the ...", "There are ... equinoxes a year, in ... and ..."],
   ['equal','12 hours','over the equator','twice a year'],
   [('equalDayNight','Day and night about equal',['equal day and night','equal length','equal hours','equal amounts','equal daylight','same length','about 12 hours','12 hours of day','12 hours of daylight','12 hours of night','day and night are equal','day and night are the same','same amount of day and night','equally long','12 hours each']),
    ('sunOverEquator','Sun directly over the equator',['over the equator','above the equator','overhead at the equator','shining on the equator','shines on the equator','hits the equator','strikes the equator','straight down on the equator','directly on the equator','on the equator']),
    ('twoPerYear','Two a year (March and September)',['two a year','twice a year','twice each year','twice per year','two equinoxes','two times','spring equinox','autumn equinox','fall equinox','vernal','march','september'])],
   ["The word 'equi' means equal. What is equal about day and night?",
    "Good. Where on Earth is the Sun shining straight down at an equinox? (Hint: the line around the middle.)",
    "Last piece: how many equinoxes are there in a year, and roughly when?"],
   "Describe day and night at an equinox and where the Sun is shining straight down.", ['equalDayNight','sunOverEquator']),

 C('sunangle','📏','Sun Angle',
   "In your own words: what is the Sun's angle in the sky, and how does it change how hot the ground gets?",
   ["When the Sun is high in the sky, its rays ...", "When the Sun is low, the same sunlight is ...", "That is why a high Sun makes it ..."],
   ['high angle','concentrated','spread out','hotter'],
   [('highDirect','High Sun: more direct and concentrated',['high angle','higher angle','steep angle','sun is higher','sun is high','high in the sky','overhead','directly overhead','straight down','more direct','hits directly','strikes directly','perpendicular','right angle','90 degrees','90°','concentrated','focused','smaller area']),
    ('lowSpread','Low Sun: spread over a larger area',['spread out','spread over','spreads out','larger area','bigger area','wider area','more spread','less concentrated','less intense','shallow angle','low angle','low in the sky','sun is low']),
    ('heatEffect','High is hotter, low is cooler',['hotter','warmer','cooler','colder','more heat','less heat','more energy','less energy','heats more','heats less','heats up more','more intense'])],
   ["Picture a torch shining straight down on a table, then at a slant. Which spot is brighter?",
    "Good. So what happens to the same sunlight when the Sun is low in the sky?",
    "Last piece: what does that do to the temperature of the ground?"],
   "Explain how the Sun's angle affects the temperature of the ground.", ['highDirect','heatEffect']),

 C('daylength','⏱️','Day Length',
   "In your own words: why does the number of daylight hours change through the year?",
   ["Daylight hours change because Earth is ...", "In summer the days are ... and in winter they are ...", "Earth's ... is what makes this happen."],
   ['tilt','longer in summer','shorter in winter','daylight hours'],
   [('tiltCause',"Caused by Earth's tilt",['tilt','tilted','tilts','leans','leaning']),
    ('longSummer','Longer in summer',['longer in summer','longer in the summer','longest in summer','summer days are longer','longer summer days','long in summer','longer days in summer','more daylight in summer','more hours in summer','summer has longer','summer is longer']),
    ('shortWinter','Shorter in winter',['shorter in winter','shorter in the winter','shortest in winter','winter days are shorter','shorter winter days','short in winter','shorter days in winter','less daylight in winter','fewer hours in winter','winter has shorter','winter is shorter'])],
   ["What feature of Earth (the one that gives us seasons) changes the daylight hours?",
    "Good. In which season are the days long?",
    "Last piece: and in which season are the days short?"],
   "Explain why day length changes during the year.", ['tiltCause','longSummer','shortWinter']),
]

template = open(os.path.join(folder, "engine-template.html"), encoding="utf-8").read()
for c in CONCEPTS:
    out = build(template, c, "A3 · Seasons")
    open(os.path.join(folder, c["filename"]), "w", encoding="utf-8").write(out)
    print("wrote", c["filename"])

# wire the hub: add href to each A3 placeholder
idx_path = os.path.join(folder, "index.html")
idx = open(idx_path, encoding="utf-8").read()
for c in CONCEPTS:
    import re
    pat = re.compile(r"(\{icon:'[^']*', name:'[^']*', )(saveId:'%s'\})" % re.escape(c["id"]))
    idx, n = pat.subn(lambda m: m.group(1) + "href:'%s', " % c["filename"] + m.group(2), idx)
    if n != 1: sys.exit(f"hub: {c['id']} matched {n} times")
open(idx_path, "w", encoding="utf-8").write(idx)
print("hub wired")
