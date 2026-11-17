"""Lime line-art illustrations for the four Norvel principles (480x300 SVG)."""
import math

L = "#c8f03c"


def _svg(body, label):
    return (f'<svg class="p-art" viewBox="0 0 480 300" fill="none" stroke="{L}" stroke-width="1.25" '
            f'stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{label}">{body}</svg>')


def foundation():
    """AI is the foundation — stacked isometric layers, the base layer solid & glowing."""
    def plane(cy, w=150, h=62):
        cx = 240
        return f"{cx},{cy - h / 2} {cx + w},{cy} {cx},{cy + h / 2} {cx - w},{cy}"
    out = ['<defs><radialGradient id="pa1"><stop offset="0" stop-color="#c8f03c" stop-opacity=".35"/>'
           '<stop offset="1" stop-color="#c8f03c" stop-opacity="0"/></radialGradient></defs>',
           '<ellipse cx="240" cy="236" rx="190" ry="60" fill="url(#pa1)" stroke="none"/>']
    out.append(f'<polygon points="{plane(232)}" fill="{L}" fill-opacity=".14" stroke-width="1.6"/>')
    # grid on the base
    for k in range(1, 6):
        t = k / 6
        out.append(f'<line x1="{240 - 150 + 150 * t}" y1="{232 - 31 * t}" x2="{240 + 150 * t}" y2="{232 + 31 - 31 * t}" stroke-opacity=".45"/>')
        out.append(f'<line x1="{240 - 150 + 150 * t}" y1="{232 + 31 * t}" x2="{240 + 150 * t}" y2="{232 - 31 + 31 * t}" stroke-opacity=".45"/>')
    for i, cy in enumerate((182, 132, 82)):
        op = .85 - i * .2
        out.append(f'<g class="p-float" style="animation-delay:{i * .4}s"><polygon points="{plane(cy)}" stroke-opacity="{op}" stroke-dasharray="{"" if i == 0 else "4 5"}"/></g>')
    for x in (90, 240, 390):
        out.append(f'<line x1="{x}" y1="82" x2="{x}" y2="232" stroke-opacity=".25" stroke-dasharray="2 6"/>')
    out.append('<circle cx="240" cy="232" r="4" fill="#c8f03c" stroke="none"/>')
    return _svg("".join(out), "Stacked layers built on an AI foundation")


def explore():
    """Explore 10x — many branching paths fanning out, one highlighted."""
    out = []
    ox, oy = 40, 150
    n = 13
    for i in range(n):
        a = -46 + i * (92 / (n - 1))
        r = 380
        ex, ey = ox + r * math.cos(math.radians(a)), oy + r * math.sin(math.radians(a))
        mx, my = ox + 150 * math.cos(math.radians(a * .6)), oy + 150 * math.sin(math.radians(a * .6))
        hi = i == 9
        out.append(f'<path class="{"p-draw" if hi else ""}" d="M{ox},{oy} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}" '
                   f'stroke-opacity="{1 if hi else .28}" stroke-width="{2 if hi else 1}"/>')
        out.append(f'<circle cx="{ex - 18 * math.cos(math.radians(a)):.1f}" cy="{ey - 18 * math.sin(math.radians(a)):.1f}" r="{5 if hi else 2.5}" '
                   f'fill="{L if hi else "none"}" stroke-opacity="{1 if hi else .5}"/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="7" fill="{L}" stroke="none"/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="16" stroke-opacity=".5" class="p-pulse"/>')
    return _svg("".join(out), "One idea branching into many explored directions")


def loop():
    """Senior designers in the loop — an infinity loop with a fixed human node and a travelling AI dot."""
    d = "M240,150 C290,70 410,70 410,150 C410,230 290,230 240,150 C190,70 70,70 70,150 C70,230 190,230 240,150 Z"
    out = [f'<path d="{d}" stroke-opacity=".35"/>',
           f'<path d="{d}" stroke-dasharray="3 9" stroke-opacity=".6"/>',
           # human node (left loop)
           '<circle cx="70" cy="150" r="22" fill="#0b0e13" stroke-width="1.6"/>',
           '<circle cx="70" cy="143" r="6"/><path d="M58,163 Q70,151 82,163"/>',
           # AI node (right loop)
           '<rect x="388" y="128" width="44" height="44" rx="10" fill="#0b0e13" stroke-width="1.6"/>',
           '<path d="M400,150 h20 M410,140 v20" />',
           # travelling dot
           f'<circle r="6" fill="{L}" stroke="none"><animateMotion dur="7s" repeatCount="indefinite" path="{d}"/></circle>',
           '<text x="70" y="250" fill="#8a93a0" stroke="none" font-family="Inter,Arial" font-size="11" text-anchor="middle" letter-spacing="2">REVIEW</text>',
           '<text x="410" y="250" fill="#8a93a0" stroke="none" font-family="Inter,Arial" font-size="11" text-anchor="middle" letter-spacing="2">GENERATE</text>']
    return _svg("".join(out), "A loop between AI generation and human review")


def next_():
    """Built for what's next — ascending steps and an expanding trajectory."""
    out = []
    pts = []
    for i in range(6):
        x, y = 60 + i * 66, 250 - i * 34
        pts.append((x, y))
        out.append(f'<rect x="{x}" y="{y}" width="56" height="{280 - y}" stroke-opacity="{.25 + i * .12:.2f}" fill="{L}" fill-opacity="{.02 + i * .025:.3f}"/>')
    path = "M" + " L".join(f"{x + 28},{y - 14}" for x, y in pts)
    out.append(f'<path class="p-draw" d="{path} L452,40" stroke-width="2"/>')
    out.append('<path d="M436,38 L454,38 L454,56" stroke-width="2"/>')
    for x, y in pts:
        out.append(f'<circle cx="{x + 28}" cy="{y - 14}" r="3.5" fill="#0b0e13" stroke-width="1.6"/>')
    for r in (18, 34, 52):
        out.append(f'<circle cx="452" cy="40" r="{r}" stroke-opacity="{.5 - r / 140:.2f}" class="p-pulse" style="animation-delay:{r / 30:.1f}s"/>')
    return _svg("".join(out), "Steps rising towards what comes next")


ARTS = [foundation(), explore(), loop(), next_()]


def post_webflow_vs_wordpress():
    """Two browser windows side by side: a tidy component-based layout vs a plugin-stacked one."""
    def win(x, y, w, h, op):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#0b0e13" stroke-opacity="{op}"/>'
                f'<line x1="{x}" y1="{y + 26}" x2="{x + w}" y2="{y + 26}" stroke-opacity="{op * .6:.2f}"/>'
                + "".join(f'<circle cx="{x + 16 + i * 12}" cy="{y + 13}" r="3" stroke-opacity="{op}"/>' for i in range(3)))
    o = ['<defs><pattern id="pg" width="24" height="24" patternUnits="userSpaceOnUse">'
         '<path d="M24 0H0V24" stroke="#eef1f4" stroke-opacity=".05" fill="none"/></pattern>'
         '<radialGradient id="pgl"><stop offset="0" stop-color="#c8f03c" stop-opacity=".22"/><stop offset="1" stop-color="#c8f03c" stop-opacity="0"/></radialGradient></defs>',
         '<rect width="480" height="300" fill="#11151c" stroke="none"/>',
         '<rect width="480" height="300" fill="url(#pg)" stroke="none"/>',
         '<circle cx="150" cy="150" r="190" fill="url(#pgl)" stroke="none"/>']
    # left: Webflow-like — clean component blocks, lime
    x, y = 46, 58
    o.append(win(x, y, 176, 184, 1))
    o.append(f'<rect x="{x + 16}" y="{y + 42}" width="96" height="12" rx="3" fill="{L}" stroke="none"/>')
    o.append(f'<rect x="{x + 16}" y="{y + 62}" width="64" height="12" rx="3" fill="{L}" fill-opacity=".45" stroke="none"/>')
    o.append(f'<rect x="{x + 16}" y="{y + 86}" width="44" height="14" rx="7" fill="{L}" stroke="none"/>')
    for i in range(3):
        o.append(f'<rect class="p-float" style="animation-delay:{i * .3}s" x="{x + 16 + i * 50}" y="{y + 116}" width="42" height="52" rx="5" stroke-opacity=".9"/>')
    # right: WordPress-like — plugin pieces stacked, dashed, outlined
    x2, y2 = 258, 58
    o.append(win(x2, y2, 176, 184, .55))
    pieces = [(16, 42, 70, 22), (92, 42, 68, 22), (16, 70, 50, 30), (72, 70, 88, 30), (16, 106, 144, 22), (16, 134, 60, 34), (82, 134, 78, 34)]
    for i, (px, py, pw, ph) in enumerate(pieces):
        o.append(f'<rect x="{x2 + px}" y="{y2 + py}" width="{pw}" height="{ph}" rx="3" stroke-opacity=".5" stroke-dasharray="3 4"/>')
        o.append(f'<circle cx="{x2 + px + pw - 6}" cy="{y2 + py + 6}" r="2" fill="#eef1f4" fill-opacity=".4" stroke="none"/>')
    # vs
    o.append('<circle cx="240" cy="150" r="17" fill="#0b0e13" stroke-width="1.4"/>')
    o.append('<text x="240" y="154.5" text-anchor="middle" font-family="Inter,Arial" font-size="12" fill="#c8f03c" stroke="none" letter-spacing="1">VS</text>')
    o.append('<text x="134" y="270" text-anchor="middle" font-family="Inter,Arial" font-size="10" fill="#8a93a0" stroke="none" letter-spacing="2.5">COMPONENTS</text>')
    o.append('<text x="346" y="270" text-anchor="middle" font-family="Inter,Arial" font-size="10" fill="#8a93a0" stroke="none" letter-spacing="2.5">PLUGINS</text>')
    return (f'<svg class="post-art-svg" viewBox="0 0 480 300" preserveAspectRatio="xMidYMid slice" fill="none" stroke="{L}" '
            f'stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" role="img" '
            f'aria-label="Webflow components compared with WordPress plugins">{"".join(o)}</svg>')


POST_ARTS = {"webflow-vs-wordpress-b2b-marketing-site": post_webflow_vs_wordpress()}
