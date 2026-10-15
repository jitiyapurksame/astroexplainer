"""Reference SVGs for A3 · Seasons (memory-jog diagrams, viewBox 0 0 200 140)."""
import math
F = 'font-family="Nunito, sans-serif"'
CREAM, MUTED, SUN, CYAN, EARTH, LAND, NIGHT, EDGE = '#F5F0E6', '#8A92C7', '#FFD166', '#4DD8E0', '#2F8FC4', '#3F9B57', '#14102A', '#3A2E5C'

def txt(x, y, s, size=9, fill=MUTED, weight=700, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" {F} font-weight="{weight}">{s}</text>'

DEFS = f'''<defs>
    <marker id="ray" markerUnits="userSpaceOnUse" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{SUN}"/></marker>
    <marker id="arr" markerUnits="userSpaceOnUse" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{CYAN}"/></marker>
  </defs>'''

def sun(cx, cy, r=12, label=True):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>'
    if label: s += txt(cx, cy + r + 11, 'SUN', 8, SUN)
    return s

def earth(cx, cy, r, tilt=0, cap=False, cid='ec', axis=True, night=False):
    land = (f'<ellipse cx="{cx-r*0.3}" cy="{cy-r*0.35}" rx="{r*0.33}" ry="{r*0.2}" fill="{LAND}"/>'
            f'<ellipse cx="{cx+r*0.35}" cy="{cy+r*0.25}" rx="{r*0.28}" ry="{r*0.18}" fill="{LAND}"/>'
            f'<ellipse cx="{cx-r*0.1}" cy="{cy+r*0.6}" rx="{r*0.18}" ry="{r*0.12}" fill="{LAND}"/>')
    s = f'<g transform="rotate({tilt} {cx} {cy})"><clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{EARTH}"/><g clip-path="url(#{cid})">{land}'
    if cap: s += f'<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{r}" fill="{SUN}" opacity="0.38"/>'
    s += '</g>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="2"/>'
    if axis: s += f'<line x1="{cx}" y1="{cy-r-13}" x2="{cx}" y2="{cy+r+13}" stroke="{CYAN}" stroke-width="2" stroke-dasharray="4,3" stroke-linecap="round"/>'
    s += '</g>'
    return s

def wrap(body, extra=''):
    return f'<svg viewBox="0 0 200 140" xmlns="http://www.w3.org/2000/svg">\n  {DEFS}\n  {body}\n</svg>'

def rays_to_earth(cx, cy, r, ys, x0=46):
    out = ''
    for y in ys:
        hit = cx - math.sqrt(max(r*r - (y-cy)**2, 0)) - 3
        out += f'<line x1="{x0}" y1="{y}" x2="{hit:.1f}" y2="{y}" stroke="{SUN}" stroke-width="2" stroke-linecap="round" marker-end="url(#ray)"/>'
    return out

def svg_orbit():
    b = '<ellipse cx="100" cy="66" rx="72" ry="42" fill="none" stroke="#8A92C7" stroke-width="1.5" stroke-dasharray="4,4"/>'
    b += sun(100, 66, 12)
    b += earth(160, 90, 9, 0, axis=False, cid='e1')
    b += f'<path d="M136,104 Q112,114 88,106" fill="none" stroke="{CYAN}" stroke-width="2" marker-end="url(#arr)"/>'
    b += txt(100, 14, 'EARTH\'S ORBIT', 10, CREAM, 800) + txt(100, 128, '1 trip around the Sun = 1 year (365 days)', 8.5, MUTED)
    b += txt(172, 72, 'EARTH', 8, CREAM, 800, 'middle')
    return wrap(b)

def svg_tilt():
    b = f'<line x1="100" y1="18" x2="100" y2="124" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="3,3"/>'
    b += earth(100, 72, 34, 23.5, cid='e1')
    b += f'<path d="M100,30 A42,42 0 0,1 117,33.5" fill="none" stroke="{SUN}" stroke-width="2"/>'
    b += txt(128, 36, '23.5°', 11, SUN, 800, 'start')
    b += txt(100, 12, 'EARTH IS TILTED', 10, CREAM, 800) + txt(100, 134, 'the tilt always points the same way', 8.5, MUTED)
    return wrap(b)

def svg_season(tilt, title, caption, label, who):
    cx, cy, r = 140, 78, 30
    b = sun(22, 78, 12)
    b += rays_to_earth(cx, cy, r, [58, 70, 82, 94], 42)
    b += earth(cx, cy, r, tilt, cap=True, cid='e1')
    b += txt(100, 12, title, 9.5, CREAM, 800) + txt(100, 132, caption, 8.5, MUTED)
    b += txt(who[0], who[1], label, 8.5, SUN, 800)
    return wrap(b)

def svg_transition(prev, cur, nxt, line1, line2, arrow_up):
    boxes = [(12, prev, False), (75, cur, True), (138, nxt, False)]
    b = ''
    for x, name, hi in boxes:
        fill = '#FF5DA2' if hi else '#251642'
        tcol = '#0A0718' if hi else CREAM
        b += f'<rect x="{x}" y="22" width="50" height="26" rx="8" fill="{fill}" stroke="{EDGE}" stroke-width="1.5"/>'
        b += txt(x + 25, 39, name, 9, tcol, 800)
    b += f'<path d="M63,35 L74,35" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr)"/><path d="M126,35 L137,35" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr)"/>'
    b += txt(100, 13, 'BETWEEN ' + prev.upper() + ' AND ' + nxt.upper(), 8.5, MUTED, 700)
    b += earth(56, 88, 18, -23.5 if arrow_up else 23.5, cid='e1')
    b += sun(18, 96, 8, False) if False else ''
    b += f'<text x="150" y="82" text-anchor="middle" font-size="9" fill="{CREAM}" {F} font-weight="700">{line1}</text>'
    b += f'<text x="150" y="98" text-anchor="middle" font-size="9" fill="{CREAM}" {F} font-weight="700">{line2}</text>'
    b += txt(150, 116, '▲ more daylight' if arrow_up else '▼ less daylight', 9, SUN, 800)
    b += txt(56, 133, 'tilting toward the Sun' if arrow_up else 'tilting away from the Sun', 7.5, MUTED)
    return wrap(b)

def svg_solstice():
    b = '<ellipse cx="100" cy="68" rx="76" ry="40" fill="none" stroke="#8A92C7" stroke-width="1.5" stroke-dasharray="4,4"/>'
    b += sun(100, 68, 11)
    b += earth(26, 68, 13, 23.5, cid='e1')
    b += earth(174, 68, 13, 23.5, cid='e2')
    b += txt(38, 100, 'tilted most', 7.5, CREAM, 800) + txt(38, 110, 'TOWARD Sun', 7.5, CREAM, 800) + txt(38, 124, 'longest day', 8, SUN, 800)
    b += txt(160, 100, 'tilted most', 7.5, CREAM, 800) + txt(160, 110, 'AWAY from Sun', 7.5, CREAM, 800) + txt(160, 124, 'shortest day', 8, SUN, 800)
    b += txt(100, 13, 'SOLSTICE: 2 a year', 10, CREAM, 800)
    return wrap(b)

def svg_equinox():
    cx, cy, r = 118, 70, 38
    b = sun(20, 70, 12)
    for y in (40, 55, 70, 85, 100):
        hit = cx - math.sqrt(r*r - (y-cy)**2) - 3
        w = 3 if y == 70 else 1.5
        b += f'<line x1="40" y1="{y}" x2="{hit:.1f}" y2="{y}" stroke="{SUN}" stroke-width="{w}" stroke-linecap="round" marker-end="url(#ray)"/>'
    b += f'<clipPath id="e1"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><circle cx="{cx}" cy="{cy}" r="{r}" fill="{EARTH}"/>'
    b += f'<g clip-path="url(#e1)"><ellipse cx="{cx-14}" cy="{cy-18}" rx="12" ry="8" fill="{LAND}"/><ellipse cx="{cx-10}" cy="{cy+20}" rx="9" ry="6" fill="{LAND}"/><rect x="{cx}" y="{cy-r}" width="{r}" height="{2*r}" fill="{NIGHT}" opacity="0.85"/></g>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="2"/>'
    b += f'<line x1="{cx}" y1="{cy-r-12}" x2="{cx}" y2="{cy+r+12}" stroke="{CYAN}" stroke-width="2" stroke-dasharray="4,3"/>'
    b += txt(cx - 20, cy + 3, 'DAY', 9, CREAM, 800) + txt(cx + 20, cy + 3, 'NIGHT', 9, MUTED, 800)
    b += txt(100, 12, 'EQUINOX', 10, CREAM, 800)
    b += txt(100, 134, 'Sun over the equator: day = night', 8.5, MUTED)
    b += txt(66, 28, 'rays hit the equator', 8, SUN, 800)
    return wrap(b)

def svg_sunangle():
    b = txt(100, 12, 'THE SUN\'S ANGLE', 10, CREAM, 800)
    # left: high sun, vertical rays
    b += f'<circle cx="48" cy="26" r="7" fill="{SUN}"/>'
    for x in (33, 48, 63):
        b += f'<line x1="{x}" y1="38" x2="{x}" y2="92" stroke="{SUN}" stroke-width="2" stroke-linecap="round" marker-end="url(#ray)"/>'
    b += f'<line x1="10" y1="96" x2="90" y2="96" stroke="{MUTED}" stroke-width="2"/><line x1="33" y1="96" x2="63" y2="96" stroke="#FF5DA2" stroke-width="5" stroke-linecap="round"/>'
    b += txt(50, 112, 'HIGH Sun', 9, CREAM, 800) + txt(52, 124, 'concentrated = hotter', 7.5, SUN, 800)
    # right: low sun, slanted rays (30 deg), same ray spacing perpendicular
    ang = math.radians(40); d = (math.cos(ang), math.sin(ang)); p = (-math.sin(ang), math.cos(ang))
    b += f'<circle cx="112" cy="34" r="7" fill="{SUN}"/>'
    for i in range(3):
        sx = 118 + i*15*p[0]; sy = 40 + i*15*p[1]
        t = (96 - sy) / d[1]
        ex = sx + t*d[0]
        b += f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex-4*d[0]:.1f}" y2="{96-4*d[1]:.1f}" stroke="{SUN}" stroke-width="2" stroke-linecap="round" marker-end="url(#ray)"/>'
        if i == 0: e0 = ex
        if i == 2: e2 = ex
    b += f'<line x1="106" y1="96" x2="196" y2="96" stroke="{MUTED}" stroke-width="2"/><line x1="{e0:.1f}" y1="96" x2="{e2:.1f}" y2="96" stroke="#FF5DA2" stroke-width="5" stroke-linecap="round" opacity="0.8"/>'
    b += txt(150, 112, 'LOW Sun', 9, CREAM, 800) + txt(150, 124, 'spread out = cooler', 7.5, SUN, 800)
    return wrap(b)

def svg_daylength():
    pts = []
    for i in range(0, 25):
        x = 24 + i*6.5
        y = 66 - 30*math.sin(2*math.pi*i/24 - math.pi/2*0)   # peak at i=6 (summer), trough at i=18 (winter)
        pts.append((x, y))
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    b = txt(100, 12, 'DAYLIGHT THROUGH THE YEAR', 9.5, CREAM, 800)
    b += f'<line x1="24" y1="20" x2="24" y2="112" stroke="{MUTED}" stroke-width="1.5"/><line x1="24" y1="112" x2="184" y2="112" stroke="{MUTED}" stroke-width="1.5"/>'
    b += f'<line x1="24" y1="66" x2="184" y2="66" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="4,3"/>'
    b += f'<path d="{d}" fill="none" stroke="{SUN}" stroke-width="3" stroke-linecap="round"/>'
    b += txt(63, 28, 'longest day (summer)', 8, SUN, 800) + txt(141, 108, 'shortest (winter)', 8, SUN, 800)
    b += txt(186, 57, 'near equator: ~12 h', 7.5, CYAN, 700, 'end')
    b += txt(104, 130, 'months of the year →', 8, MUTED)
    return wrap(b)

SVGS = {
 'earthorbit': svg_orbit(),
 'tilt': svg_tilt(),
 'summer': svg_season(-23.5, 'SUMMER: tilted TOWARD the Sun', 'tilt, not distance, makes the seasons', 'this half: SUMMER', (150, 24)),
 'winter': svg_season(23.5, 'WINTER: tilted AWAY from the Sun', 'tilt, not distance, makes the seasons', 'this half: WINTER', (150, 24)),
 'spring': svg_transition('Winter', 'SPRING', 'Summer', 'days get longer', 'and warmer', True),
 'autumn': svg_transition('Summer', 'AUTUMN', 'Winter', 'days get shorter', 'and cooler', False),
 'solstice': svg_solstice(),
 'equinox': svg_equinox(),
 'sunangle': svg_sunangle(),
 'daylength': svg_daylength(),
}
