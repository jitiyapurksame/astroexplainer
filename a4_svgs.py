"""Reference SVGs for A4 · Moon (memory-jog diagrams, viewBox 0 0 200 140). Reuses helpers from a3_svgs."""
import math
from a3_svgs import txt, wrap, sun, earth, CREAM, MUTED, SUN, CYAN, EARTH, LAND, NIGHT, EDGE

MOON_LIT, MOON_DARK = '#EDE7D3', '#2A2F4A'
PINK = '#FF5DA2'

def moon(cx, cy, r, f=1.0, flip=False):
    """Moon disc with a lit fraction f (0..1). Lit side is on the right unless flip=True."""
    s = f'<g transform="translate({2*cx} 0) scale(-1 1)">' if flip else '<g>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{MOON_DARK}"/>'
    if f >= 0.995:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{MOON_LIT}"/>'
    elif f > 0.005:
        t = r * (1 - 2*f); rx = abs(t)
        if rx < 0.05:
            s += f'<path d="M{cx},{cy-r} A{r},{r} 0 0 1 {cx},{cy+r} Z" fill="{MOON_LIT}"/>'
        else:
            sweep = 0 if t > 0 else 1
            s += f'<path d="M{cx},{cy-r} A{r},{r} 0 0 1 {cx},{cy+r} A{rx:.2f},{r} 0 0 {sweep} {cx},{cy-r} Z" fill="{MOON_LIT}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="1.5"/></g>'
    return s

def arrow(x1, y1, x2, y2, col=CYAN, w=1.8):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" marker-end="url(#arr)"/>'

def title(t): return txt(100, 12, t, 10, CREAM, 800)

def svg_fullmoon():
    b = title('FULL MOON')
    b += sun(22, 66, 11) + moon(176, 66, 14, 0.5, flip=True) + earth(100, 66, 13, 0, axis=False, cid='e1')
    b += f'<path d="M100,53 A13,13 0 0 0 100,79 Z" fill="{SUN}" opacity="0.3"/>'
    b += txt(100, 92, 'EARTH', 8, CREAM, 800) + txt(176, 92, 'MOON', 8, CREAM, 800)
    b += f'<line x1="38" y1="66" x2="84" y2="66" stroke="{SUN}" stroke-width="1.5" stroke-dasharray="3,3"/>'
    b += moon(44, 118, 10, 1.0) + txt(60, 121, 'we see the whole face', 8, SUN, 800, 'start')
    b += txt(100, 38, 'Earth in the middle', 8.5, MUTED)
    return wrap(b)

def svg_newmoon():
    b = title('NEW MOON')
    b += sun(22, 66, 11) + moon(100, 66, 14, 0.5, flip=True) + earth(176, 66, 13, 0, axis=False, cid='e1')
    b += txt(100, 92, 'MOON', 8, CREAM, 800) + txt(176, 92, 'EARTH', 8, CREAM, 800)
    b += txt(100, 36, 'Moon in the middle', 8.5, MUTED) + txt(100, 106, 'lit side faces away from Earth', 8, SUN, 800)
    b += moon(50, 124, 9, 0.0) + txt(64, 127, 'we cannot see it', 8, SUN, 800, 'start')
    return wrap(b)

def svg_crescent():
    b = title('CRESCENT MOON')
    b += moon(100, 70, 36, 0.18)
    b += txt(100, 124, 'a thin sliver is lit', 9, SUN, 800)
    b += txt(100, 136, 'seen near the Sun: after sunset or before sunrise', 7, MUTED)
    return wrap(b)

def svg_quarter():
    b = title('QUARTER MOON')
    b += sun(16, 78, 8, False) + earth(62, 78, 11, 0, axis=False, cid='e1')
    b += f'<circle cx="62" cy="78" r="40" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3,3"/>'
    b += f'<path d="M102,78 A40,40 0 0 0 62,38" fill="none" stroke="{CYAN}" stroke-width="2.5"/>'
    b += moon(62, 38, 7, 0.5, flip=True)
    b += txt(62, 134, 'a quarter of the orbit', 7.5, CYAN, 800)
    b += moon(158, 70, 26, 0.5) + txt(158, 112, 'half the face is lit', 7.5, SUN, 800)
    b += txt(158, 124, 'first or last quarter', 7, MUTED)
    return wrap(b)

def svg_gibbous():
    b = title('GIBBOUS MOON')
    b += moon(100, 52, 30, 0.8)
    b += txt(100, 96, 'more than half is lit', 9, SUN, 800)
    b += moon(38, 114, 9, 0.5) + moon(100, 114, 9, 0.8) + moon(162, 114, 9, 1.0)
    b += txt(38, 133, 'Quarter', 7.5, MUTED) + txt(100, 133, 'GIBBOUS', 7.5, CREAM, 800) + txt(162, 133, 'Full', 7.5, MUTED)
    return wrap(b)

def strip(fs, flip, t, caption, label):
    b = title(t)
    for i, f in enumerate(fs):
        x = 24 + i*38
        b += moon(x, 58, 15, f, flip)
    names = ['New','','','','Full'] if not flip else ['Full','','','','New']
    for i, n in enumerate(names):
        if n: b += txt(24 + i*38, 88, n + ' Moon', 7.5, MUTED)
    b += arrow(30, 104, 170, 104, SUN, 2.2)
    b += txt(100, 122, caption, 9.5, SUN, 800) + txt(100, 135, label, 8, MUTED)
    return wrap(b)

def svg_waxing(): return strip([0.0, 0.25, 0.5, 0.75, 1.0], False, 'WAXING MOON', 'lit part getting bigger', 'about 2 weeks (14 days)')
def svg_waning(): return strip([1.0, 0.75, 0.5, 0.25, 0.0], True, 'WANING MOON', 'lit part getting smaller', 'about 2 weeks (14 days)')

def svg_moonorbit():
    b = title('THE MOON\'S ORBIT')
    b += f'<circle cx="100" cy="66" r="40" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4,4"/>'
    b += earth(100, 66, 12, 0, axis=False, cid='e1')
    for (mx, my, ang) in [(140, 66, 0), (100, 26, 90), (60, 66, 180)]:
        dx, dy = 100 - mx, 66 - my; L = math.hypot(dx, dy)
        px, py = mx + dx/L*6.5, my + dy/L*6.5
        b += f'<circle cx="{mx}" cy="{my}" r="8" fill="{MOON_LIT}" stroke="{EDGE}" stroke-width="1.5"/><circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{PINK}"/>'
    b += txt(100, 86, 'EARTH', 8, CREAM, 800)
    b += txt(100, 124, 'one trip = about a month (27 days)', 8.5, SUN, 800)
    b += txt(100, 136, 'the pink dot side always faces Earth', 7.5, MUTED)
    return wrap(b)

def horizon(title_t, ex, cx, label_l, label_r, up):
    b = title(title_t)
    b += f'<clipPath id="hz"><rect x="0" y="0" width="200" height="100"/></clipPath>'
    b += f'<g clip-path="url(#hz)">{moon(cx, 100 - (4 if up else -4), 20, 1.0)}</g>'
    b += f'<rect x="0" y="100" width="200" height="40" fill="#1E2A1F"/><line x1="0" y1="100" x2="200" y2="100" stroke="{LAND}" stroke-width="2"/>'
    b += txt(14, 116, 'W', 11, CREAM, 800) + txt(186, 116, 'E', 11, CREAM, 800)
    return b

def svg_moonrise():
    b = horizon('MOONRISE', 0, 150, 'W', 'E', True)
    b += arrow(150, 66, 150, 40, SUN, 2.4) + txt(150, 32, 'comes up', 9, SUN, 800)
    b += txt(60, 70, 'Earth spins,', 8.5, CYAN, 800) + txt(60, 82, 'so the Moon rises', 8.5, CYAN, 800)
    b += txt(100, 134, 'rises in the east', 8.5, MUTED)
    return wrap(b)

def svg_moonset():
    b = horizon('MOONSET', 0, 50, 'W', 'E', False)
    b += arrow(50, 40, 50, 66, SUN, 2.4) + txt(50, 32, 'goes down', 9, SUN, 800)
    b += txt(100, 134, 'sets in the west', 8.5, MUTED)
    b += txt(140, 70, 'Earth spins,', 8.5, CYAN, 800) + txt(140, 82, 'so the Moon sets', 8.5, CYAN, 800)
    return wrap(b)

def svg_lunareclipse():
    b = title('LUNAR ECLIPSE')
    b += sun(20, 68, 11)
    b += f'<polygon points="108,56 200,62 200,74 108,80" fill="#0A0718" opacity="0.7"/>'
    b += earth(100, 68, 14, 0, axis=False, cid='e1')
    b += f'<circle cx="170" cy="68" r="11" fill="#8B3A3A" stroke="{EDGE}" stroke-width="1.5"/>'
    b += txt(100, 96, 'EARTH', 8, CREAM, 800) + txt(170, 92, 'MOON', 8, CREAM, 800)
    b += txt(100, 114, 'Earth is in the middle', 8.5, MUTED)
    b += txt(100, 128, "Earth's shadow falls on the Moon", 8.5, SUN, 800)
    return wrap(b)

def svg_solareclipse():
    b = title('SOLAR ECLIPSE')
    b += sun(24, 68, 14)
    b += f'<polygon points="106,64 168,67 168,69 106,72" fill="#0A0718" opacity="0.8"/>'
    b += f'<circle cx="100" cy="68" r="6" fill="{MOON_LIT}" stroke="{EDGE}" stroke-width="1.5"/>'
    b += earth(176, 68, 14, 0, axis=False, cid='e1')
    b += txt(100, 88, 'MOON', 8, CREAM, 800) + txt(176, 94, 'EARTH', 8, CREAM, 800)
    b += txt(100, 114, 'Moon is in the middle', 8.5, MUTED)
    b += txt(100, 128, "Moon's shadow falls on Earth", 8.5, SUN, 800)
    return wrap(b)

def svg_tides():
    b = title('TIDES')
    b += f'<ellipse cx="86" cy="72" rx="48" ry="34" fill="#1F6FA8" opacity="0.8"/>'
    b += earth(86, 72, 30, 0, axis=False, cid='e1')
    b += f'<circle cx="176" cy="72" r="10" fill="{MOON_LIT}" stroke="{EDGE}" stroke-width="1.5"/>' + txt(176, 56, 'MOON', 8, CREAM, 800)
    b += arrow(160, 72, 140, 72, SUN, 2.2) + txt(152, 88, 'gravity pull', 7.5, SUN, 800)
    b += txt(20, 44, 'HIGH', 8, CYAN, 800) + txt(20, 54, 'tide', 8, CYAN, 800)
    b += txt(140, 44, 'HIGH', 8, CYAN, 800) + txt(140, 54, 'tide', 8, CYAN, 800)
    b += txt(86, 122, "the Moon's gravity pulls the ocean", 8.5, MUTED) + txt(86, 134, '2 high tides + 2 low tides a day', 8.5, SUN, 800)
    return wrap(b)

def svg_earthmoon():
    b = title('EARTH-MOON SYSTEM')
    b += earth(46, 66, 24, 0, axis=False, cid='e1')
    b += f'<circle cx="168" cy="66" r="6.5" fill="{MOON_LIT}" stroke="{EDGE}" stroke-width="1.5"/>'
    b += f'<line x1="74" y1="66" x2="156" y2="66" stroke="{CYAN}" stroke-width="1.8" stroke-dasharray="4,3"/>'
    b += txt(114, 60, '384,000 km', 9.5, SUN, 800)
    b += txt(46, 102, 'EARTH', 8, CREAM, 800) + txt(168, 90, 'MOON', 8, CREAM, 800)
    b += txt(100, 118, 'Moon is about 1/4 the size of Earth', 8.5, MUTED)
    b += txt(100, 132, 'it orbits Earth (distance not to scale)', 7.5, MUTED)
    return wrap(b)

def svg_crater():
    b = title('MOON CRATER')
    b += f'<path d="M0,96 L78,96 Q86,94 92,102 Q114,126 136,102 Q142,94 150,96 L200,96 L200,140 L0,140 Z" fill="#5A6088"/>'
    b += f'<path d="M0,96 L78,96 Q86,94 92,102 Q114,126 136,102 Q142,94 150,96 L200,96" fill="none" stroke="{CREAM}" stroke-width="2" stroke-linejoin="round"/>'
    b += f'<line x1="32" y1="30" x2="76" y2="72" stroke="#FFB347" stroke-width="3" stroke-linecap="round" stroke-dasharray="2,5"/>'
    b += f'<circle cx="82" cy="78" r="7" fill="#A0805A" stroke="{EDGE}" stroke-width="1.5"/>'
    b += txt(40, 24, 'space rock', 8, CREAM, 800) + txt(114, 90, 'IMPACT!', 8.5, SUN, 800)
    b += txt(114, 126, 'bowl-shaped hole', 8.5, CREAM, 800)
    b += txt(100, 136, 'many are billions of years old', 7.5, MUTED)
    return wrap(b)

SVGS = {
 'fullmoon': svg_fullmoon(), 'newmoon': svg_newmoon(), 'crescent': svg_crescent(), 'quarter': svg_quarter(),
 'gibbous': svg_gibbous(), 'waxing': svg_waxing(), 'waning': svg_waning(), 'moonorbit': svg_moonorbit(),
 'moonrise': svg_moonrise(), 'moonset': svg_moonset(), 'lunareclipse': svg_lunareclipse(),
 'solareclipse': svg_solareclipse(), 'tides': svg_tides(), 'earthmoonsystem': svg_earthmoon(), 'mooncrater': svg_crater(),
}
