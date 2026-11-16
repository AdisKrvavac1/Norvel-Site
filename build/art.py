"""Generates placeholder artwork (SVG) in the Norvel palette.

These are stand-ins for real project imagery. Replace the files in
public/assets/work/ with real images (same file names, or update data.py).
"""
import math
import random

INK, INK2, INK3 = "#0b0e13", "#11151c", "#1a2029"
LIME, FOG, SLATE = "#c8f03c", "#eef1f4", "#8a93a0"

MARK = ('<polygon points="0 162.26 195.42 500.74 0 500.74"/>'
        '<polygon points="463.94 341.1 267.01 0 463.94 0"/>'
        '<polygon points="463.94 500.74 288.95 500.74 0 .26 174.99 .26"/>')


def svg(w, h, body, bg=INK2):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def mark(x, y, size, fill):
    s = size / 500.74
    return f'<g transform="translate({x} {y}) scale({s})" fill="{fill}">{MARK}</g>'


def grid_lines(w, h, step, color, op=0.08):
    out = []
    for x in range(0, w + 1, step):
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{color}" stroke-opacity="{op}"/>')
    for y in range(0, h + 1, step):
        out.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{color}" stroke-opacity="{op}"/>')
    return "".join(out)


def glow(cx, cy, r, color=LIME, op=0.35, gid="g"):
    return (f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>')


# ---------- compositions ----------

def comp_identity(w, h, seed=1, bg=INK2, fg=LIME):
    """Big brand mark on a grid — identity cover."""
    size = min(w, h) * 0.46
    body = grid_lines(w, h, 60, FOG, 0.05) + glow(w / 2, h / 2, size, fg, 0.18, f"gi{seed}")
    body += mark(w / 2 - size * 0.4633, h / 2 - size / 2, size, fg)
    body += f'<text x="40" y="{h - 40}" font-family="Inter,Arial" font-size="18" fill="{SLATE}" letter-spacing="3">IDENTITY SYSTEM</text>'
    body += f'<text x="{w - 40}" y="{h - 40}" text-anchor="end" font-family="Inter,Arial" font-size="18" fill="{SLATE}">0{seed}</text>'
    return svg(w, h, body, bg)


def comp_ui(w, h, seed=2, bg=INK2):
    """Browser / website wireframe."""
    pad = w * 0.09
    bw, bh = w - pad * 2, h - pad * 1.6
    x, y = pad, pad * 0.9
    b = glow(w * 0.75, h * 0.2, w * 0.5, LIME, 0.12, f"gu{seed}")
    b += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="{INK}" stroke="{INK3}"/>'
    b += "".join(f'<circle cx="{x + 26 + i * 18}" cy="{y + 22}" r="5" fill="{INK3}"/>' for i in range(3))
    b += f'<line x1="{x}" y1="{y + 44}" x2="{x + bw}" y2="{y + 44}" stroke="{INK3}"/>'
    ix, iy = x + 40, y + 90
    b += f'<rect x="{ix}" y="{iy}" width="{bw * 0.5}" height="{bh * 0.09}" rx="4" fill="{FOG}"/>'
    b += f'<rect x="{ix}" y="{iy + bh * 0.13}" width="{bw * 0.34}" height="{bh * 0.09}" rx="4" fill="{FOG}" fill-opacity=".35"/>'
    b += f'<rect x="{ix}" y="{iy + bh * 0.3}" width="{bw * 0.42}" height="8" rx="4" fill="{SLATE}" fill-opacity=".5"/>'
    b += f'<rect x="{ix}" y="{iy + bh * 0.3 + 18}" width="{bw * 0.3}" height="8" rx="4" fill="{SLATE}" fill-opacity=".5"/>'
    b += f'<rect x="{ix}" y="{iy + bh * 0.44}" width="140" height="40" rx="20" fill="{LIME}"/>'
    cw = (bw - 80 - 32) / 3
    for i in range(3):
        b += f'<rect x="{ix + i * (cw + 16)}" y="{y + bh * 0.68}" width="{cw}" height="{bh * 0.24}" rx="6" fill="{INK2}" stroke="{INK3}"/>'
    b += mark(x + bw - 40 - bh * 0.28, iy, bh * 0.3, LIME)
    return svg(w, h, b, bg)


def comp_system(w, h, seed=3, bg=INK2):
    """Design-system tokens: swatches + type scale."""
    rnd = random.Random(seed)
    b = grid_lines(w, h, 40, FOG, 0.04)
    sw = [LIME, FOG, SLATE, INK3, INK]
    s = w * 0.12
    for i, c in enumerate(sw):
        b += f'<rect x="{w * 0.08 + i * (s + 14)}" y="{h * 0.14}" width="{s}" height="{s}" rx="8" fill="{c}" stroke="{INK3}"/>'
    sizes = [96, 64, 40, 24]
    yy = h * 0.5
    for sz in sizes:
        b += f'<text x="{w * 0.08}" y="{yy}" font-family="Inter,Arial" font-size="{sz}" fill="{FOG}" letter-spacing="-2">Aa</text>'
        b += f'<line x1="{w * 0.3}" y1="{yy - sz * 0.3}" x2="{w * 0.92}" y2="{yy - sz * 0.3}" stroke="{SLATE}" stroke-opacity=".35"/>'
        b += f'<text x="{w * 0.92}" y="{yy - sz * 0.3 - 8}" text-anchor="end" font-family="Inter,Arial" font-size="14" fill="{SLATE}">{sz}px</text>'
        yy += sz * 0.9 + 10
    for i in range(6):
        on = rnd.random() > 0.4
        b += f'<rect x="{w * 0.62 + (i % 3) * 64}" y="{h * 0.14 + (i // 3) * 40}" width="52" height="26" rx="13" fill="{LIME if on else INK3}"/>'
        b += f'<circle cx="{w * 0.62 + (i % 3) * 64 + (39 if on else 13)}" cy="{h * 0.14 + (i // 3) * 40 + 13}" r="9" fill="{INK if on else SLATE}"/>'
    return svg(w, h, b, bg)


def comp_editorial(w, h, seed=4, bg=FOG):
    """Editorial layout on fog."""
    b = f'<rect x="{w * 0.07}" y="{h * 0.1}" width="{w * 0.4}" height="{h * 0.8}" fill="{INK}"/>'
    b += glow(w * 0.27, h * 0.55, w * 0.25, LIME, 0.45, f"ge{seed}")
    b += mark(w * 0.16, h * 0.32, h * 0.34, LIME)
    b += f'<text x="{w * 0.53}" y="{h * 0.25}" font-family="Inter,Arial" font-size="{h * 0.09}" fill="{INK}" letter-spacing="-3">Field</text>'
    b += f'<text x="{w * 0.53}" y="{h * 0.35}" font-family="Inter,Arial" font-size="{h * 0.09}" fill="{INK}" letter-spacing="-3">Notes</text>'
    for i in range(9):
        lw = w * (0.38 if i % 4 != 3 else 0.22)
        b += f'<rect x="{w * 0.53}" y="{h * 0.46 + i * 22}" width="{lw}" height="7" rx="3" fill="{INK}" fill-opacity=".22"/>'
    b += f'<rect x="{w * 0.53}" y="{h * 0.84}" width="{w * 0.12}" height="4" fill="{INK}"/>'
    return svg(w, h, b, bg)


def comp_pattern(w, h, seed=5, bg=INK):
    """Repeating mark pattern with one highlight."""
    rnd = random.Random(seed)
    cell = 120
    b = ""
    hl = (rnd.randint(1, max(1, w // cell - 2)), rnd.randint(1, max(1, h // cell - 2)))
    for gx in range(-1, w // cell + 1):
        for gy in range(-1, h // cell + 1):
            c = LIME if (gx, gy) == hl else INK3
            b += mark(gx * cell + 24, gy * cell + 16, cell * 0.72, c)
    b += glow(hl[0] * cell + 60, hl[1] * cell + 60, 260, LIME, 0.2, f"gp{seed}")
    return svg(w, h, b, bg)


def comp_orbit(w, h, seed=6, bg=INK2):
    """Concentric motion arcs — motion design."""
    cx, cy = w * 0.5, h * 0.52
    b = glow(cx, cy, min(w, h) * 0.5, LIME, 0.16, f"go{seed}")
    for i in range(1, 9):
        r = i * min(w, h) * 0.055
        dash = 2 * math.pi * r
        b += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LIME if i in (3, 7) else FOG}" '
              f'stroke-opacity="{0.9 if i in (3, 7) else 0.12}" stroke-width="{2 if i in (3, 7) else 1}" '
              f'stroke-dasharray="{dash * 0.62} {dash}" transform="rotate({i * 37} {cx} {cy})"/>')
    b += f'<circle cx="{cx}" cy="{cy}" r="10" fill="{LIME}"/>'
    return svg(w, h, b, bg)


def comp_poster(w, h, seed=7, bg=LIME):
    """Lime poster with large type."""
    b = f'<text x="{w * 0.07}" y="{h * 0.3}" font-family="Inter,Arial" font-size="{w * 0.2}" fill="{INK}" letter-spacing="-8">Form</text>'
    b += f'<text x="{w * 0.07}" y="{h * 0.5}" font-family="Inter,Arial" font-size="{w * 0.2}" fill="{INK}" letter-spacing="-8">&amp; flow</text>'
    b += mark(w * 0.68, h * 0.66, h * 0.26, INK)
    b += f'<text x="{w * 0.07}" y="{h * 0.92}" font-family="Inter,Arial" font-size="18" fill="{INK}" letter-spacing="3">NORVEL — CONCEPT {seed:02d}</text>'
    return svg(w, h, b, bg)


def comp_mobile(w, h, seed=8, bg=INK2):
    """Two phone screens."""
    b = glow(w * 0.5, h * 0.5, w * 0.45, LIME, 0.12, f"gm{seed}")
    pw, ph = h * 0.42, h * 0.8
    for k, off in enumerate((-0.55, 0.55)):
        x = w / 2 + off * pw - pw / 2
        y = h * 0.1 + (k * 30)
        b += f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="34" fill="{INK}" stroke="{INK3}" stroke-width="2"/>'
        b += f'<rect x="{x + pw * 0.36}" y="{y + 14}" width="{pw * 0.28}" height="10" rx="5" fill="{INK3}"/>'
        b += f'<rect x="{x + 22}" y="{y + 60}" width="{pw * 0.6}" height="22" rx="4" fill="{FOG}"/>'
        b += f'<rect x="{x + 22}" y="{y + 92}" width="{pw * 0.4}" height="22" rx="4" fill="{FOG}" fill-opacity=".35"/>'
        b += f'<rect x="{x + 22}" y="{y + 140}" width="{pw - 44}" height="{ph * 0.32}" rx="14" fill="{LIME if k == 0 else INK3}"/>'
        if k == 0:
            b += mark(x + pw / 2 - ph * 0.09, y + 140 + ph * 0.06, ph * 0.2, INK)
        for i in range(3):
            b += f'<rect x="{x + 22}" y="{y + 160 + ph * 0.32 + i * 34}" width="{pw - 44}" height="22" rx="6" fill="{INK2}"/>'
    return svg(w, h, b, bg)


COMPS = {
    "identity": comp_identity, "ui": comp_ui, "system": comp_system, "editorial": comp_editorial,
    "pattern": comp_pattern, "orbit": comp_orbit, "poster": comp_poster, "mobile": comp_mobile,
}


def comp_pending(w, h, seed=9, bg=INK2):
    """Neutral placeholder while real project visuals are pending."""
    b = grid_lines(w, h, 80, FOG, 0.05) + glow(w / 2, h / 2, w * 0.4, LIME, 0.10, f"gx{seed}")
    b += mark(w / 2 - h * 0.09, h * 0.36, h * 0.2, INK3)
    b += f'<text x="{w / 2}" y="{h * 0.72}" text-anchor="middle" font-family="Inter,Arial" font-size="{h * 0.035}" fill="{SLATE}" letter-spacing="4">VISUALS COMING SOON</text>'
    return svg(w, h, b, bg)


COMPS["pending"] = comp_pending
