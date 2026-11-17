"""Looping lime line-art for page heroes (480x360). Animations are CSS classes in style.css."""
L = "#c8f03c"
F = "#eef1f4"


def _svg(body, label):
    return (f'<svg class="ph-svg" viewBox="0 0 480 360" preserveAspectRatio="xMidYMid slice" fill="none" stroke="{L}" '
            f'stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{label}">'
            '<defs><pattern id="phg" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#eef1f4" '
            'stroke-opacity=".05" fill="none"/></pattern><radialGradient id="phl"><stop offset="0" stop-color="#c8f03c" '
            'stop-opacity=".2"/><stop offset="1" stop-color="#c8f03c" stop-opacity="0"/></radialGradient></defs>'
            f'{body}</svg>')


def about():
    """One studio: three orbiting rings (brand, web, webflow) around a single core."""
    o = []
    for i, (rx, ry, rot, dur) in enumerate([(150, 58, 0, 18), (150, 58, 60, 22), (150, 58, 120, 26)]):
        o.append(f'<g class="pa-spin" style="animation-duration:{dur}s;{"animation-direction:reverse;" if i == 1 else ""}">'
                 f'<ellipse cx="240" cy="180" rx="{rx}" ry="{ry}" transform="rotate({rot} 240 180)" stroke-opacity=".75"/>'
                 f'<circle cx="{240 + rx}" cy="180" r="5" fill="{L}" stroke="none" transform="rotate({rot} 240 180)"/></g>')
    o.append('<circle cx="240" cy="180" r="26" fill="#0b0e13" stroke-width="1.6"/>')
    o.append('<g transform="translate(227 166) scale(.054)" fill="#c8f03c" stroke="none">'
             '<polygon points="0 162.26 195.42 500.74 0 500.74"/><polygon points="463.94 341.1 267.01 0 463.94 0"/>'
             '<polygon points="463.94 500.74 288.95 500.74 0 .26 174.99 .26"/></g>')
    o.append('<circle cx="240" cy="180" r="40" class="pa-pulse" stroke-opacity=".5"/>')
    return _svg("".join(o), "Three disciplines orbiting one studio")


def work():
    """Selected work: a stack of browser frames cycling front to back."""
    o = []
    for i in range(3):
        o.append(f'<g class="pa-cycle" style="animation-delay:{-i * 2}s">'
                 '<rect x="110" y="96" width="260" height="168" rx="10" fill="#0b0e13" stroke-width="1.4"/>'
                 '<line x1="110" y1="120" x2="370" y2="120" stroke-opacity=".6"/>'
                 + "".join(f'<circle cx="{126 + k * 11}" cy="108" r="2.6"/>' for k in range(3)) +
                 f'<rect x="128" y="138" width="{[120, 90, 140][i]}" height="10" rx="3" fill="{L}" stroke="none"/>'
                 f'<rect x="128" y="156" width="{[70, 110, 60][i]}" height="10" rx="3" fill="{L}" fill-opacity=".4" stroke="none"/>'
                 '<rect x="128" y="180" width="70" height="66" rx="5" stroke-opacity=".7"/>'
                 '<rect x="206" y="180" width="70" height="66" rx="5" stroke-opacity=".7"/>'
                 '<rect x="284" y="180" width="70" height="66" rx="5" stroke-opacity=".7"/></g>')
    return _svg("".join(o), "Project frames cycling")


def services():
    """Three pillars: mark → wireframe → code, highlighted in turn."""
    o = []
    xs = [92, 240, 388]
    o.append('<path d="M92 180 H388" stroke-opacity=".3" stroke-dasharray="3 6"/>')
    o.append(f'<circle r="5" fill="{L}" stroke="none"><animateMotion dur="6s" repeatCount="indefinite" path="M92 180 H388 H92"/></circle>')
    for i, x in enumerate(xs):
        o.append(f'<g class="pa-hi" style="animation-delay:{i * 2}s"><rect x="{x - 56}" y="114" width="112" height="132" rx="12" fill="#0b0e13" stroke-width="1.4"/></g>')
    # icons
    o.append('<g transform="translate(74 158) scale(.08)" fill="none" stroke="#c8f03c" stroke-width="18">'
             '<polygon points="0 162.26 195.42 500.74 0 500.74"/><polygon points="463.94 341.1 267.01 0 463.94 0"/>'
             '<polygon points="463.94 500.74 288.95 500.74 0 .26 174.99 .26"/></g>')
    o.append('<rect x="212" y="152" width="56" height="12" rx="2"/><rect x="212" y="170" width="26" height="26" rx="2"/><rect x="242" y="170" width="26" height="26" rx="2"/>')
    o.append('<path d="M372 164 L360 180 L372 196 M404 164 L416 180 L404 196 M393 160 L383 200"/>')
    for x, t in zip(xs, ["BRAND", "WEB DESIGN", "WEBFLOW"]):
        o.append(f'<text x="{x}" y="232" text-anchor="middle" font-family="Inter,Arial" font-size="9" fill="#8a93a0" stroke="none" letter-spacing="2">{t}</text>')
    return _svg("".join(o), "Brand, web design and Webflow pillars")


def testimonials():
    """Speech bubbles appearing in turn, with typing dots."""
    o = []
    bubbles = [(70, 70, 230, 70, "l"), (180, 160, 230, 70, "r"), (70, 250, 200, 56, "l")]
    for i, (x, y, w, h, side) in enumerate(bubbles):
        tail = (f'M{x + 26},{y + h} l-8,16 l22,-16' if side == "l" else f'M{x + w - 26},{y + h} l8,16 l-22,-16')
        o.append(f'<g class="pa-pop" style="animation-delay:{i * 1.2}s"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#0b0e13" stroke-width="1.4"/>'
                 f'<path d="{tail}" fill="#0b0e13"/>')
        if i < 2:
            o.append(f'<text x="{x + 18}" y="{y + 40}" font-family="Georgia,serif" font-size="34" fill="#c8f03c" stroke="none">“</text>'
                     f'<rect x="{x + 52}" y="{y + 22}" width="{w - 80}" height="7" rx="3" fill="{F}" fill-opacity=".35" stroke="none"/>'
                     f'<rect x="{x + 52}" y="{y + 38}" width="{w - 120}" height="7" rx="3" fill="{F}" fill-opacity=".2" stroke="none"/>')
        else:
            for k in range(3):
                o.append(f'<circle class="pa-dot" style="animation-delay:{k * .2}s" cx="{x + 30 + k * 16}" cy="{y + h / 2}" r="4" fill="{L}" stroke="none"/>')
        o.append('</g>')
    return _svg("".join(o), "Client messages appearing")


def insights():
    """Notes: a document whose lines write themselves, with a blinking caret."""
    o = ['<rect x="130" y="56" width="220" height="250" rx="12" fill="#0b0e13" stroke-width="1.4"/>',
         '<path d="M310 56 v30 h40" stroke-opacity=".5"/>',
         f'<rect x="154" y="86" width="120" height="12" rx="3" fill="{L}" stroke="none"/>']
    lines = [(150, 170), (170, 150), (190, 162), (210, 120), (234, 166), (254, 140), (274, 96)]
    for i, (y, w) in enumerate(lines):
        o.append(f'<line class="pa-write" style="animation-delay:{i * .45}s" x1="154" y1="{y}" x2="{154 + w}" y2="{y}" stroke-width="5" stroke-opacity=".55"/>')
    o.append(f'<rect class="pa-caret" x="256" y="266" width="2" height="16" fill="{L}" stroke="none"/>')
    o.append('<g class="pa-float"><circle cx="372" cy="98" r="22" fill="#0b0e13" stroke-width="1.4"/>'
             '<path d="M364 104 q8 -22 16 0 M366 110 h12"/></g>')
    return _svg("".join(o), "A document writing itself")


def contact():
    """Contact: a paper plane looping along a dashed path toward an inbox."""
    path = "M60 270 C140 120 260 300 330 170 S420 90 430 120"
    o = [f'<path d="{path}" stroke-opacity=".4" stroke-dasharray="4 7"/>',
         '<rect x="392" y="96" width="70" height="52" rx="8" fill="#0b0e13" stroke-width="1.4"/>',
         '<path d="M392 104 L427 128 L462 104" />',
         f'<g><path d="M-14 -8 L14 0 L-14 8 L-8 0 Z" fill="{L}" stroke="none"/>'
         f'<animateMotion dur="5s" repeatCount="indefinite" rotate="auto" path="{path}"/></g>',
         '<circle cx="427" cy="122" r="44" class="pa-pulse" stroke-opacity=".45"/>']
    return _svg("".join(o), "A message flying to an inbox")


PAGE_ARTS = {"about": about(), "work": work(), "services": services(), "testimonials": testimonials(),
             "insights": insights(), "contact": contact()}
