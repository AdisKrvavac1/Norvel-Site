"""Builds the static Norvel site into ./public.

Usage:  python3 build/build.py
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data import *          # noqa: F401,F403
from art import COMPS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUB = os.path.join(ROOT, "public")
e = html.escape

# ---------- logo (inline, recolourable) ----------
_logo_src = open(os.path.join(PUB, "assets/img/norvel-logo-fog.svg")).read()
_groups = re.findall(r"<g>(.*?)</g>\s*<g>(.*)</g>\s*</svg>", _logo_src, re.S)[0]
_mark_g = _groups[0].replace(' class="cls-1"', "")
_word_g = re.sub(r"\s+", " ", _groups[1].replace(' class="cls-1"', ""))
LOGO = ('<svg viewBox="0 0 1645.05 500.74" role="img" aria-label="Norvel Studio" fill="currentColor">'
        f'<g class="logo-mark">{_mark_g}</g><g>{_word_g}</g></svg>')

ARROW = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" stroke="currentColor" stroke-width="1.5"/></svg>'
ARROW_UR = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 13L13 3M5 3h8v8" stroke="currentColor" stroke-width="1.5"/></svg>'
ARROW_L = '<svg width="34" height="20" viewBox="0 0 34 20" fill="none" aria-hidden="true"><path d="M33 10H2M10 1L1 10l9 9" stroke="currentColor" stroke-width="1.5"/></svg>'
ARROW_R = '<svg width="34" height="20" viewBox="0 0 34 20" fill="none" aria-hidden="true"><path d="M1 10h31M24 1l9 9-9 9" stroke="currentColor" stroke-width="1.5"/></svg>'
PLUS = '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 0v14M0 7h14" stroke="currentColor" stroke-width="1.4"/></svg>'


def art(name, w, h, key):
    """Write an artwork SVG and return its URL."""
    fn = f"{key}.svg"
    path = os.path.join(PUB, "assets/work", fn)
    seed = sum(map(ord, key)) % 9 + 1
    with open(path, "w") as f:
        f.write(COMPS[name](w, h, seed))
    return f"/assets/work/{fn}"


def stairs(frm, to, rev=False):
    cls = "stairs stairs--rev" if rev else "stairs"
    return f'<div class="{cls}" data-anim aria-hidden="true" style="--from:{frm};--to:{to}"><span></span><span></span><span></span></div>'


def head(title, desc, path):
    full = f"{title} — {SITE['name']}" if title else f"{SITE['name']} — {SITE['tagline']}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE['url']}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE['url']}{path}">
<meta property="og:image" content="{SITE['url']}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0e13">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
"""


def nav(home=False):
    p = "" if home else "/"
    return f"""<header class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo" aria-label="Norvel — home">{LOGO}</a>
    <nav class="nav-menu" aria-label="Main">
      <a class="u-line" href="{p}#about">About</a>
      <a class="u-line" href="/projects/">Work<sup>({len(PROJECTS)})</sup></a>
      <a class="u-line" href="{p}#services">Services</a>
      <a class="u-line" href="{p}#model">Model</a>
    </nav>
    <a class="nav-cta" href="mailto:{SITE['email']}"><span class="dot"></span>Start a project {ARROW}</a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
  </div>
</header>
"""


def cta_section():
    return f"""<section class="section light cta" id="contact">
  <div class="container cta-grid">
    <h2 class="h2" data-reveal>{e(CTA['title'])}</h2>
    <div class="cta-copy" data-fade>
      <p>{e(CTA['copy'])}</p>
      <a class="btn" href="mailto:{SITE['email']}">{e(CTA['button'])}<span class="btn-ico">{ARROW_UR}</span></a>
    </div>
  </div>
</section>
"""


def footer():
    socials = "".join(f'<a class="u-line" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SITE["socials"])
    return f"""<footer class="footer">
  <div class="footer-glow" aria-hidden="true"></div>
  <div class="container">
    <div class="footer-top">
      <h2 class="h2">{e(FOOTER['title_a'])}<br>{e(FOOTER['title_b'])}</h2>
      <p>{e(FOOTER['copy'])}</p>
      <a class="footer-mail u-line" href="mailto:{SITE['email']}">{SITE['email']}</a>
    </div>
    <div class="footer-brand">
      <a href="/" class="footer-logo" aria-label="Norvel — home">{LOGO}</a>
      <nav class="footer-links" aria-label="Footer">
        <a href="/projects/">Work</a><a href="/#services">Services</a><a href="/#model">Model</a>{socials}
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Norvel Studio. All rights reserved.</span>
      <span>Designed &amp; built by Norvel</span>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def write(rel, content):
    path = os.path.join(PUB, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


# ---------- pages ----------

def page_home():
    covers = {p["slug"]: art(p["cover"], 1200, 900, f"{p['slug']}-cover") for p in PROJECTS}
    marquee_keys = ["identity", "ui", "poster", "system", "orbit", "mobile", "editorial", "pattern"]
    marquee = "".join(
        f'<div class="marquee-item"><img src="{art(k, 800, 600, "marquee-" + k)}" alt="" loading="lazy" width="800" height="600"></div>'
        for k in marquee_keys)
    socials = "".join(f'<a class="u-line" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SITE["socials"])
    about_img = art("pattern", 800, 600, "about")

    rows = "".join(
        f'<div class="about-row" data-fade><p>{e(a)}</p><span class="stat">{e(b)}</span><small>{e(c)}</small></div>'
        for a, b, c in PROBLEM["rows"])

    work = "".join(f"""
      <a class="work-item" href="/projects/{p['slug']}/" data-fade>
        <div class="work-meta"><span>{e(p['date'])}</span><span>{e(p['name'])} — {e(p['summary'])}</span><span>View case</span></div>
        <div class="work-media"><img src="{covers[p['slug']]}" alt="{e(p['name'])} — {e(p['summary'])}" loading="lazy" width="1200" height="900"><span class="view">View project</span></div>
      </a>""" for p in PROJECTS[:3])

    svcs = "".join(f"""
      <div class="svc{' is-open' if i == 0 else ''}">
        <button class="svc-btn" aria-expanded="{'true' if i == 0 else 'false'}">
          <span class="svc-num">0{i + 1}</span><span class="svc-title">{e(t)}</span><span class="svc-plus">{PLUS}</span>
        </button>
        <div class="svc-panel"><div><div class="svc-panel-inner"><p>{e(d)}</p><ul>{''.join(f'<li>{e(x)}</li>' for x in items)}</ul></div></div></div>
      </div>""" for i, (t, d, items) in enumerate(SERVICES["items"]))

    slides = "".join(f"""
          <article class="slide">
            <div><span class="slide-num">0{i + 1} — PRINCIPLE</span><h3>{e(t)}</h3></div>
            <p>{e(d)}</p>
          </article>""" for i, (t, d) in enumerate(MODEL["principles"]))

    personas = "".join(f"""
      <a class="persona" href="mailto:{SITE['email']}?subject={e(t)}" data-fade>
        <div class="persona-top"><span>0{i + 1}</span><span>{i + 1} of {len(PERSONAS['items'])}</span></div>
        <h3>{e(h)}</h3>
        <p>{e(d)}</p>
        <span class="link-arrow">That’s me {ARROW}</span>
      </a>""" for i, (t, h, d) in enumerate(PERSONAS["items"]))

    faqs = "".join(f"""
          <div class="faq-item">
            <button class="faq-q" aria-expanded="false">{e(q)}<span class="faq-ico" aria-hidden="true"></span></button>
            <div class="faq-a"><div><p>{e(a)}</p></div></div>
          </div>""" for q, a in FAQS["items"])

    body = f"""{nav(home=True)}
<main id="main">
  <section class="hero">
    <div class="container">
      <div class="hero-head">
        <div class="hero-glow" aria-hidden="true"></div>
        <span class="eyebrow">{e(HERO['eyebrow'])}</span>
        <h1 class="h1 hero-title"><span class="line">{e(HERO['line1'])}</span><span class="line"><span class="glow-word">{e(HERO['line2'])}</span></span></h1>
        <p class="hero-sub">{e(HERO['sub'])}</p>
        <div class="hero-actions">
          <a class="btn" href="mailto:{SITE['email']}">Talk to Norvel<span class="btn-ico">{ARROW_UR}</span></a>
          <a class="link-arrow u-line" href="#model">How we work {ARROW}</a>
        </div>
      </div>
    </div>
    <div class="marquee" aria-label="Selected visuals"><div class="marquee-track">{marquee}</div></div>
    <div class="container hero-foot">
      <p>{e(HERO['intro'])}</p>
      <div class="socials">{socials}</div>
    </div>
  </section>

  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light" id="about" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">{e(PROBLEM['eyebrow'])}</span>
          <h2 class="h2 strike-wrap">{e(PROBLEM['title_a'])} <span class="strike">{e(PROBLEM['strike'])}</span> {e(PROBLEM['title_b'])}</h2></div>
        <p data-fade>{e(PROBLEM['lead'])}</p>
      </div>
      <div class="about-body">
        <div class="about-visual" data-fade><img src="{about_img}" alt="" loading="lazy" width="800" height="600"></div>
        <div class="about-rows">{rows}</div>
      </div>
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}

  <section class="section" id="work" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">Selected work</span><h2 class="h2" data-reveal>Work that tells a story</h2></div>
        <p data-fade>A selection of studio concept studies — how we take an idea from first question to a finished system.</p>
      </div>
      <div class="work-list">{work}</div>
      <div class="work-all"><a class="btn" href="/projects/">View all work<span class="btn-ico">{ARROW_UR}</span></a></div>
    </div>
  </section>

  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light" id="services" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">{e(SERVICES['eyebrow'])}</span><h2 class="h2" data-reveal>{e(SERVICES['title'])}</h2></div></div>
      <div class="svc-list">{svcs}</div>
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}

  <section class="section" id="model" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">{e(MODEL['eyebrow'])}</span><h2 class="h2" data-reveal>{e(MODEL['title'])}</h2></div>
        <p data-fade>{e(MODEL['lead'])}</p>
      </div>
      <div class="slider" data-slider tabindex="0" aria-label="Norvel principles">
        <div class="slider-viewport"><div class="slider-track" data-track>{slides}
        </div></div>
        <div class="slider-ctrl">
          <span class="slider-count" data-count></span>
          <div class="slider-arrows"><button data-prev aria-label="Previous">{ARROW_L}</button><button data-next aria-label="Next">{ARROW_R}</button></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="clients" style="padding-top:0">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">{e(PERSONAS['eyebrow'])}</span><h2 class="h2" data-reveal>{e(PERSONAS['title'])}</h2></div>
        <p data-fade>{e(PERSONAS['lead'])}</p>
      </div>
      <div class="personas">{personas}</div>
    </div>
  </section>

  <section class="section" id="faq" style="padding-top:0">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">{e(FAQS['eyebrow'])}</span><h2 class="h2" data-reveal>{e(FAQS['title'])}</h2></div></div>
      <div class="faq-body">
        <div class="faq-aside" data-fade><p>{e(FAQS['aside'])}</p><a class="link-arrow u-line" href="mailto:{SITE['email']}">{SITE['email']} {ARROW}</a></div>
        <div class="faq-list">{faqs}
        </div>
      </div>
    </div>
  </section>

  {stairs('var(--ink)', 'var(--fog)')}
  {cta_section().replace('class="section light cta"', 'class="section light cta" style="padding-top:calc(var(--section) - 96px)"')}
  {stairs('var(--fog)', 'var(--ink)', rev=True)}
</main>
"""
    write("index.html", head("", SITE["description"], "/") + body + footer())


def page_projects():
    cards = "".join(f"""
      <a class="proj-card" href="/projects/{p['slug']}/" data-fade>
        <div class="work-media"><img src="/assets/work/{p['slug']}-cover.svg" alt="{e(p['name'])} — {e(p['summary'])}" loading="lazy" width="1200" height="900"><span class="view">View project</span></div>
        <h3>{e(p['name'])}<span>{e(p['summary'])}</span></h3>
        <p>{e(p['card'])}</p>
      </a>""" for p in PROJECTS)
    body = f"""{nav()}
<main id="main">
  <section class="page-hero">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">Work</span><h1 class="h1">{e(PROJECTS_PAGE['title'])}</h1></div>
        <p class="muted" data-fade>{e(PROJECTS_PAGE['lead'])}</p>
      </div>
      <div class="proj-grid"><span class="proj-label">Projects ({len(PROJECTS)})</span>{cards}
      </div>
    </div>
  </section>
  {stairs('var(--ink)', 'var(--fog)')}
  {cta_section().replace('class="section light cta"', 'class="section light cta" style="padding-top:calc(var(--section) - 96px)"')}
  {stairs('var(--fog)', 'var(--ink)', rev=True)}
</main>
"""
    write("projects/index.html", head("Work", PROJECTS_PAGE["lead"], "/projects/") + body + footer())


def page_project(i, p):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    gallery = "".join(
        f'<div class="gallery-item"><img src="{art(g, 800, 1000, p["slug"] + "-g" + str(k))}" alt="{e(p["name"])} visual {k + 1}" loading="lazy" width="800" height="1000"></div>'
        for k, g in enumerate(p["gallery"] + [p["cover"]]))
    wide = art(p["wide"], 1600, 700, p["slug"] + "-wide")
    steps = "".join(f"<li><span><strong>{e(a)}:</strong> {e(b)}</span></li>" for a, b in p["steps"])
    body = f"""{nav()}
<main id="main">
  <section class="pd-hero">
    <div class="container">
      <span class="eyebrow">{e(p['summary'])}</span>
      <h1 class="h1" style="margin-top:1.5rem">{e(p['name'])}</h1>
      <div class="pd-top">
        <div>
          <p class="pd-intro">{e(p['intro'])}</p>
          <dl class="pd-facts">
            <div><dt>Client</dt><dd>{e(p['client'])}</dd></div>
            <div><dt>Role</dt><dd>{e(p['role'])}</dd></div>
            <div><dt>Tools</dt><dd>{e(p['tools'])}</dd></div>
          </dl>
          <span class="pd-tag">{e(p['date'])}</span>
        </div>
        <div class="pd-cover" data-fade><img src="/assets/work/{p['slug']}-cover.svg" alt="{e(p['name'])} cover" width="1200" height="900"></div>
      </div>

      <div class="gallery" data-slider data-multi tabindex="0" aria-label="Project gallery">
        <span class="eyebrow">Visual journey</span>
        <div style="overflow:hidden;margin-top:1.5rem"><div class="gallery-track" data-track>{gallery}</div></div>
        <div class="slider-ctrl"><span class="slider-count" data-count></span>
          <div class="slider-arrows"><button data-prev aria-label="Previous">{ARROW_L}</button><button data-next aria-label="Next">{ARROW_R}</button></div></div>
      </div>

      <div class="pd-text">
        <h2 data-reveal>Behind the design</h2>
        <div data-fade><p>{e(p['approach'])}</p><ol>{steps}</ol></div>
      </div>
      <div class="pd-wide" data-fade><img src="{wide}" alt="{e(p['name'])} wide visual" loading="lazy" width="1600" height="700"></div>
      <div class="pd-text">
        <h2 data-reveal>The result</h2>
        <p data-fade>{e(p['result'])}</p>
      </div>

      <div class="pd-next">
        <div><span class="eyebrow">Next project</span><br><br><a class="h2" href="/projects/{nxt['slug']}/">{e(nxt['name'])}</a></div>
        <a class="link-arrow u-line" href="/projects/">All work {ARROW}</a>
      </div>
    </div>
  </section>
  {stairs('var(--ink)', 'var(--fog)')}
  {cta_section().replace('class="section light cta"', 'class="section light cta" style="padding-top:calc(var(--section) - 96px)"')}
  {stairs('var(--fog)', 'var(--ink)', rev=True)}
</main>
"""
    write(f"projects/{p['slug']}/index.html", head(p["name"], p["intro"], f"/projects/{p['slug']}/") + body + footer())


def page_404():
    body = f"""{nav()}
<main id="main" class="nf">
  <div>
    <span class="eyebrow">Error</span>
    <h1 class="h1"><span class="lime">4</span>0<span class="lime">4</span></h1>
    <p>This page took a different direction. Let’s get you back on track.</p>
    <a class="btn" href="/">Back to home<span class="btn-ico">{ARROW_UR}</span></a>
  </div>
</main>
"""
    write("404.html", head("Page not found", SITE["description"], "/404") + body + footer())


def extras():
    mark_g = _mark_g
    write("assets/img/favicon.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -40 584 580"><rect x="-60" y="-40" width="584" height="580" rx="110" fill="#0b0e13"/><g fill="#c8f03c">{mark_g}</g></svg>')
    write("assets/img/og.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#0b0e13"/>'
          f'<g transform="translate(120 245) scale(0.42)" fill="#eef1f4"><g fill="#c8f03c">{mark_g}</g>{_word_g}</g></svg>')
    urls = ["/", "/projects/"] + [f"/projects/{p['slug']}/" for p in PROJECTS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE['url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")


if __name__ == "__main__":
    os.makedirs(os.path.join(PUB, "assets/work"), exist_ok=True)
    page_home()
    page_projects()
    for i, p in enumerate(PROJECTS):
        page_project(i, p)
    page_404()
    extras()
    print("Built:", sum(len(f) for _, _, f in os.walk(PUB)), "files in", PUB)
