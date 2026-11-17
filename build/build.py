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
LOGO_MARK = f'<svg viewBox="0 0 463.94 500.74" fill="currentColor" aria-hidden="true">{_mark_g}</svg>'
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


import json

SEO_HOME_TITLE = "Norvel — Web Design, Webflow Development & Branding Studio"
ORG_ID = SITE["url"] + "/#organization"


def org_node():
    return {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": "Norvel Studio",
        "alternateName": "Norvel",
        "url": SITE["url"] + "/",
        "logo": {"@type": "ImageObject", "url": SITE["url"] + "/assets/img/norvel-logo-lime.svg"},
        "image": SITE["url"] + "/assets/img/og.png",
        "email": SITE["email"],
        "description": SITE["description"],
        "slogan": "Senior design. Shipped at AI speed.",
        "areaServed": ["United States", "Europe"],
        "knowsAbout": ["Web design", "Webflow development", "Brand identity", "UX/UI design",
                       "Design systems", "Motion design", "AI-assisted design"],
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": SITE["email"],
                         "url": SITE["url"] + "/contact/", "availableLanguage": ["English", "Bosnian"]},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Design & development services",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}}
                                                for t, d, _ in SERVICES["items"]]},
    }


def jsonld(path, title, desc, extra, crumbs):
    url = SITE["url"] + path
    graph = [
        org_node(),
        {"@type": "WebSite", "@id": SITE["url"] + "/#website", "url": SITE["url"] + "/", "name": "Norvel Studio",
         "publisher": {"@id": ORG_ID}, "inLanguage": "en"},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": SITE["url"] + "/#website"}, "about": {"@id": ORG_ID}, "inLanguage": "en"},
    ]
    if crumbs:
        items = [("Home", "/")] + crumbs
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + u} for i, (n, u) in enumerate(items)]})
    graph += extra
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{data.replace("</", "<\\/")}</script>'


def faq_ld(items, path):
    return {"@type": "FAQPage", "@id": SITE["url"] + path + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def project_ld(p):
    url = f"{SITE['url']}/projects/{p['slug']}/"
    node = {"@type": "CreativeWork", "@id": url + "#work", "name": f"{p['name']} — {p['summary']}",
            "url": url, "description": p["card"], "creator": {"@id": ORG_ID},
            "about": {"@type": "Organization", "name": p["client"]},
            "genre": p["category"], "image": [SITE["url"] + i for i in project_images(p) if i.startswith("/")]}
    if p.get("url"):
        node["sameAs"] = p["url"]
    return node


# ---------- responsive images (WebP + JPG fallback) ----------
try:
    from PIL import Image as _PIL       # only needed locally to (re)generate image variants
except ImportError:
    _PIL = None
WIDTHS = (800, 1400, 2000)
_MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "images.json")
_MANIFEST = json.load(open(_MANIFEST_PATH)) if os.path.exists(_MANIFEST_PATH) else {}


def responsive(src):
    """Create WebP variants for a /assets/work/... jpg. Returns (webp_srcset, jpg_srcset, w, h)."""
    path = os.path.join(PUB, src.lstrip("/"))
    if not src.endswith(".jpg") or not os.path.exists(path):
        return None
    if _PIL is None:                      # e.g. on Render: use committed variants + manifest
        if src not in _MANIFEST:
            return None
        W, H = _MANIFEST[src]
        ws = [w for w in WIDTHS if w <= W]
        return (", ".join([f"{src[:-4]}-{w}.webp {w}w" for w in ws] + [f"{src[:-4]}.webp {W}w"]),
                ", ".join([f"{src[:-4]}-{w}.jpg {w}w" for w in ws] + [f"{src} {W}w"]), W, H)
    im = _PIL.open(path).convert("RGB")
    W, H = im.size
    _MANIFEST[src] = [W, H]
    base = path[:-4]
    webp, jpg = [], []
    for w in WIDTHS:
        if w > W:
            continue
        h = round(H * w / W)
        wp, jp = f"{base}-{w}.webp", f"{base}-{w}.jpg"
        if not os.path.exists(wp):
            im.resize((w, h), _PIL.LANCZOS).save(wp, "WEBP", quality=80, method=6)
        if not os.path.exists(jp):
            im.resize((w, h), _PIL.LANCZOS).save(jp, quality=82, optimize=True, progressive=True)
        webp.append(f"{src[:-4]}-{w}.webp {w}w"); jpg.append(f"{src[:-4]}-{w}.jpg {w}w")
    full_wp = base + ".webp"
    if not os.path.exists(full_wp):
        im.save(full_wp, "WEBP", quality=80, method=6)
    webp.append(f"{src[:-4]}.webp {W}w"); jpg.append(f"{src} {W}w")
    return ", ".join(webp), ", ".join(jpg), W, H


def pic(src, alt, sizes="100vw", lazy=True, cls=""):
    r = responsive(src)
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    if not r:
        return f'<img src="{src}" alt="{e(alt)}"{load}{c}>'
    webp, jpg, W, H = r
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="{src}" srcset="{jpg}" sizes="{sizes}" alt="{e(alt)}" width="{W}" height="{H}"{load}{c}></picture>')


def project_images(p):
    """Real images in public/assets/work/<slug>/, or a generated fallback."""
    d = os.path.join(PUB, "assets/work", p["slug"])
    imgs = sorted(f for f in os.listdir(d) if re.fullmatch(r"\d+\.(jpg|png)", f)) if os.path.isdir(d) else []
    if imgs:
        return [f"/assets/work/{p['slug']}/{f}" for f in imgs]
    return [art(p["fallback"], 1600, 1000, f"{p['slug']}-placeholder")]


def project_video(p):
    f = os.path.join(PUB, "assets/work", p["slug"], "walkthrough.mp4")
    return f"/assets/work/{p['slug']}/walkthrough.mp4" if os.path.exists(f) else ""


def stairs(frm, to, rev=False):
    cls = "stairs stairs--rev" if rev else "stairs"
    return f'<div class="{cls}" data-anim aria-hidden="true" style="--from:{frm};--to:{to}"><span></span><span></span><span></span></div>'


def _ver(rel):
    import hashlib
    return hashlib.md5(open(os.path.join(PUB, rel), "rb").read()).hexdigest()[:8]


def head(title, desc, path, ld=None, crumbs=None, og_type="website", og_image=None):
    full = title or SEO_HOME_TITLE
    desc = desc if len(desc) <= 158 else desc[:155].rsplit(" ", 1)[0] + "…"
    ld_html = jsonld(path, title or full, desc, ld or [], crumbs)
    og_img = og_image or f"{SITE['url']}/assets/img/og.png"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE['url']}{path}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE['url']}{path}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Norvel — Senior design. Shipped at AI speed.">
<meta property="og:site_name" content="Norvel Studio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_img}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0e13">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v={_ver('assets/css/style.css')}">
{ld_html}
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
"""


def nav(active=""):
    links = [("about", "About", "/about/"), ("projects", f"Projects<sup>({len(PROJECTS)})</sup>", "/projects/"),
             ("services", "Services", "/services/"), ("testimonials", "Testimonials", "/testimonials/")]
    items = "".join(f'<a class="u-line{" is-active" if k == active else ""}" href="{u}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, t, u in links)
    return f"""<header class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo" aria-label="Norvel — home">{LOGO}</a>
    <nav class="nav-menu" aria-label="Main">{items}</nav>
    <a class="nav-cta{" is-active" if active == "contact" else ""}" href="/contact/"><span class="dot"></span>Contact {ARROW}</a>
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
      <a class="btn" href="/contact/">{e(CTA['button'])}<span class="btn-ico">{ARROW_UR}</span></a>
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
        <a href="/about/">About</a><a href="/projects/">Projects</a><a href="/services/">Services</a><a href="/testimonials/">Testimonials</a><a href="/insights/">Insights</a><a href="/contact/">Contact</a>{socials}
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Norvel Studio. All rights reserved.</span>
      <span>Designed &amp; built by Norvel</span>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js?v={_ver('assets/js/main.js')}" defer></script>
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
    covers = {p["slug"]: project_images(p)[0] for p in PROJECTS}
    marquee_keys = ["identity", "ui", "poster", "system", "orbit", "mobile", "editorial", "pattern"]
    marquee = "".join(
        f'<div class="marquee-item">{pic(covers[p["slug"]], p["name"] + " — " + p["summary"], "300px")}</div>'
        for p in PROJECTS)
    socials = "".join(f'<a class="u-line" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SITE["socials"])
    about_img = art("pattern", 800, 600, "about")

    rows = "".join(
        f'<div class="about-row" data-fade><p>{e(a)}</p><span class="stat">{e(b)}</span><small>{e(c)}</small></div>'
        for a, b, c in PROBLEM["rows"])

    work = "".join(f"""
      <article class="case" data-fade>
        <a class="case-media" href="/projects/{p['slug']}/" aria-label="{e(p['name'])} case study">
          {pic(covers[p['slug']], p['name'] + " — " + p['summary'] + " by Norvel")}
          <span class="view">View case study</span>
        </a>
        <div class="container case-meta">
          <span class="case-num">0{n + 1}</span>
          <div><h3>{e(p['name'])}</h3><p>{e(p['summary'])}</p></div>
          <span class="case-cat">{e(p['category'])}</span>
          <a class="link-arrow u-line" href="/projects/{p['slug']}/">View case study {ARROW}</a>
        </div>
      </article>""" for n, p in enumerate(PROJECTS[:3]))

    svcs = "".join(f"""
      <div class="svc{' is-open' if i == 0 else ''}">
        <button class="svc-btn" aria-expanded="{'true' if i == 0 else 'false'}">
          <span class="svc-num">0{i + 1}</span><span class="svc-title">{e(t)}</span><span class="svc-plus">{PLUS}</span>
        </button>
        <div class="svc-panel"><div><div class="svc-panel-inner"><p>{e(d)}<br><a class="link-arrow u-line" style="margin-top:1rem;color:var(--ink)" href="/services/{['brand-identity', 'web-design', 'webflow-development'][i]}/">Learn more {ARROW}</a></p><ul>{''.join(f'<li>{e(x)}</li>' for x in items)}</ul></div></div></div>
      </div>""" for i, (t, d, items) in enumerate(SERVICES["items"]))

    slides = "".join(f"""
          <article class="slide">
            <div><span class="slide-num">0{i + 1} — PRINCIPLE</span><h3>{e(t)}</h3></div>
            <p>{e(d)}</p>
          </article>""" for i, (t, d) in enumerate(MODEL["principles"]))

    personas = "".join(f"""
      <a class="persona" href="/contact/" data-fade>
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

    body = f"""{nav()}
<main id="main">
  <section class="hero">
    <div class="container">
      <div class="hero-head">
        <div class="hero-glow" aria-hidden="true"></div>
        <span class="eyebrow">{e(HERO['eyebrow'])}</span>
        <h1 class="h1 hero-title"><span class="line">{e(HERO['line1'])}</span><span class="line"><span class="glow-word">{e(HERO['line2'])}</span></span></h1>
        <p class="hero-sub">{e(HERO['sub'])}</p>
        <div class="hero-actions">
          <a class="btn" href="/contact/">Talk to Norvel<span class="btn-ico">{ARROW_UR}</span></a>
          <a class="link-arrow u-line" href="/about/#process">How we work {ARROW}</a>
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
      <div class="work-all"><a class="btn" href="/about/">More about Norvel<span class="btn-ico">{ARROW_UR}</span></a></div>
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}

  <section class="section" id="work" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">Selected work</span><h2 class="h2" data-reveal>Work that tells a story</h2></div>
        <p data-fade>Websites, Webflow builds and campaigns for venture firms, AI products and consumer brands.</p>
      </div>
    </div>
    <div class="case-list">{work}</div>
    <div class="container work-all"><a class="btn" href="/projects/">View all {len(PROJECTS)} projects<span class="btn-ico">{ARROW_UR}</span></a></div>
  </section>

  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light" id="services" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">{e(SERVICES['eyebrow'])}</span><h2 class="h2" data-reveal>{e(SERVICES['title'])}</h2></div></div>
      <div class="svc-list">{svcs}</div>
      <div class="work-all"><a class="btn" href="/services/">Explore services<span class="btn-ico">{ARROW_UR}</span></a></div>
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
    write("index.html", head("", SITE["description"], "/", ld=[faq_ld(FAQS["items"], "/")]) + body + footer())


def page_projects():
    cards = "".join(f"""
      <article class="case" data-fade>
        <a class="case-media" href="/projects/{p['slug']}/" aria-label="{e(p['name'])} case study">
          {pic(project_images(p)[0], p['name'] + " — " + p['summary'] + " by Norvel", lazy=n > 0)}
          <span class="view">View case study</span>
        </a>
        <div class="container case-meta">
          <span class="case-num">{n + 1:02d}</span>
          <div><h3>{e(p['name'])}</h3><p>{e(p['card'])}</p></div>
          <span class="case-cat">{e(p['category'])}</span>
          <a class="link-arrow u-line" href="/projects/{p['slug']}/">View case study {ARROW}</a>
        </div>
      </article>""" for n, p in enumerate(PROJECTS))
    body = f"""{nav()}
<main id="main">
  <section class="page-hero">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">Work</span><h1 class="h1">{e(PROJECTS_PAGE['title'])}</h1></div>
        <p class="muted" data-fade>{e(PROJECTS_PAGE['lead'])}</p>
      </div>
    </div>
    <div class="case-list case-list--page">{cards}
    </div>
  </section>
  {stairs('var(--ink)', 'var(--fog)')}
  {cta_section().replace('class="section light cta"', 'class="section light cta" style="padding-top:calc(var(--section) - 96px)"')}
  {stairs('var(--fog)', 'var(--ink)', rev=True)}
</main>
"""
    body = body.replace(nav(), nav("projects"), 1)
    write("projects/index.html", head("Work — Website Design & Webflow Case Studies | Norvel",
              "Case studies by Norvel: website design and Webflow builds for HP, Lightspeed, a16z, Gyde, Playground, Lagunitas, Hello Cake and the GTM10 Awards.",
              "/projects/", crumbs=[("Work", "/projects/")],
              ld=[{"@type": "ItemList", "@id": SITE["url"] + "/projects/#list", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": f"{SITE['url']}/projects/{q['slug']}/", "name": q["name"]} for i, q in enumerate(PROJECTS)]}]) + body + footer())


def page_project(i, p):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    imgs = project_images(p)
    video = project_video(p)
    shots = [f'<figure class="pd-shot" data-fade>{pic(g, p["name"] + " website — screen " + str(k + 2))}</figure>'
             for k, g in enumerate(imgs[1:])]
    if video:
        shots.insert(0, f'<figure class="pd-shot pd-shot--video" data-fade><video src="{video}" poster="{imgs[0]}" autoplay muted loop playsinline preload="metadata" aria-label="{e(p["name"])} walkthrough"></video></figure>')
    first, rest = "".join(shots[:1]), "".join(shots[1:])
    live = f'<a class="link-arrow u-line pd-live" href="{p["url"]}" target="_blank" rel="noopener">Visit live site {ARROW_UR}</a>' if p.get("url") else ""
    steps = "".join(f"<li><span><strong>{e(a)}:</strong> {e(b)}</span></li>" for a, b in p["steps"])
    body = f"""{nav()}
<main id="main">
  <section class="pd-hero">
    <div class="container">
      <span class="eyebrow">{e(p['summary'])}</span>
      <h1 class="h1" style="margin-top:1.5rem">{e(p['name'])}</h1>
    </div>
    <figure class="pd-hero-media" data-fade>{pic(imgs[0], p['name'] + " — " + p['summary'] + " by Norvel", lazy=False)}</figure>
    <div class="container">
      <div class="pd-top">
        <p class="pd-intro">{e(p['intro'])}</p>
        <div>
          <dl class="pd-facts">
            <div><dt>Client</dt><dd>{e(p['client'])}</dd></div>
            <div><dt>Role</dt><dd>{e(p['role'])}</dd></div>
            <div><dt>Tools</dt><dd>{e(p['tools'])}</dd></div>
            <div><dt>Category</dt><dd>{e(p['category'])}</dd></div>
          </dl>
          {live}
        </div>
      </div>
    </div>
    <div class="pd-shots">{first}</div>
    <div class="container">
      <div class="pd-text">
        <h2 data-reveal>Behind the design</h2>
        <div data-fade><p>{e(p['approach'])}</p><ol>{steps}</ol></div>
      </div>
    </div>
    <div class="pd-shots">{rest}</div>
    <div class="container">
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
    body = body.replace(nav(), nav("projects"), 1)
    write(f"projects/{p['slug']}/index.html", head(f"{p['name']} — {p['summary']} | Norvel Case Study",
              f"{p['summary']} for {p['client']} by Norvel. {p['card']}",
              f"/projects/{p['slug']}/", ld=[project_ld(p)], og_type="article",
              crumbs=[("Work", "/projects/"), (p["name"], f"/projects/{p['slug']}/")],
              og_image=SITE["url"] + imgs[0] if imgs[0].startswith("/assets/work/") and imgs[0].endswith(".jpg") else None) + body + footer())


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
    write("404.html", head("Page not found | Norvel", SITE["description"], "/404").replace('content="index, follow, max-image-preview:large"', 'content="noindex"') + body + footer())


def extras():
    mark_g = _mark_g
    write("assets/img/favicon.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -40 584 580"><rect x="-60" y="-40" width="584" height="580" rx="110" fill="#0b0e13"/><g fill="#c8f03c">{mark_g}</g></svg>')
    import datetime
    today = datetime.date.today().isoformat()
    urls = (["/", "/about/", "/projects/", "/services/", "/testimonials/", "/contact/", "/insights/"]
            + [f"/services/{x['slug']}/" for x in SERVICE_PAGES] + [f"/projects/{p['slug']}/" for p in PROJECTS]
            + [f"/insights/{x['slug']}/" for x in POSTS])
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE['url']}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "PerplexityBot", "Google-Extended", "Applebot", "Applebot-Extended"]
    write("robots.txt", "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
          + f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    proj = "\n".join(f"- [{p['name']} — {p['summary']}]({SITE['url']}/projects/{p['slug']}/): {p['card']}" for p in PROJECTS)
    svc = "\n".join(f"- **{t}**: {d} Includes: {', '.join(x)}." for t, d, x in SERVICES["items"])
    faq = "\n".join(f"- **{q}** {a}" for q, a in FAQS["items"])
    write("llms.txt", f"""# Norvel Studio

> {SITE['description']}

Norvel is an independent, AI-native design and technology studio (norvelstudio.com). One senior team handles brand identity, website design and Webflow development end to end, using AI to explore and ship faster while senior designers own every decision. Clients are primarily in the United States and Europe. Contact: {SITE['email']}.

## Services
{svc}

Ways to work together: fixed-scope projects, monthly retainers, or a fractional design & Webflow team.

## Selected work
{proj}

## FAQ
{faq}

## Service pages
""" + "\n".join(f"- [{x['pillar']}]({SITE['url']}/services/{x['slug']}/): {x['description']}" for x in SERVICE_PAGES) + f"""

## Insights
""" + "\n".join(f"- [{x['title']}]({SITE['url']}/insights/{x['slug']}/): {x['description']}" for x in POSTS) + f"""

## Pages
- [Home]({SITE['url']}/)
- [About]({SITE['url']}/about/)
- [Work]({SITE['url']}/projects/)
- [Services]({SITE['url']}/services/)
- [Insights]({SITE['url']}/insights/)
- [Contact]({SITE['url']}/contact/)
""")


# ---------- shared section builders for inner pages ----------

def page_hero(eyebrow, title, lead):
    return f"""<section class="page-hero">
    <div class="container">
      <div class="sec-head" style="padding-bottom:clamp(3rem,6vw,5rem)">
        <div><span class="eyebrow">{e(eyebrow)}</span><h1 class="h1" style="margin-top:1.5rem">{e(title)}</h1></div>
        <p class="muted" data-fade>{e(lead)}</p>
      </div>
    </div>
  </section>"""


def end_cta():
    return (stairs('var(--ink)', 'var(--fog)')
            + cta_section().replace('class="section light cta"', 'class="section light cta" style="padding-top:calc(var(--section) - 96px)"')
            + stairs('var(--fog)', 'var(--ink)', rev=True))


def model_slider():
    slides = "".join(f"""
          <article class="slide">
            <div><span class="slide-num">0{i + 1} — PRINCIPLE</span><h3>{e(t)}</h3></div>
            <p>{e(d)}</p>
          </article>""" for i, (t, d) in enumerate(MODEL["principles"]))
    return f"""<div class="slider" data-slider tabindex="0" aria-label="Norvel principles">
        <div class="slider-viewport"><div class="slider-track" data-track>{slides}
        </div></div>
        <div class="slider-ctrl">
          <span class="slider-count" data-count></span>
          <div class="slider-arrows"><button data-prev aria-label="Previous">{ARROW_L}</button><button data-next aria-label="Next">{ARROW_R}</button></div>
        </div>
      </div>"""


def personas_grid():
    return '<div class="personas">' + "".join(f"""
      <a class="persona" href="/contact/" data-fade>
        <div class="persona-top"><span>0{i + 1}</span><span>{i + 1} of {len(PERSONAS['items'])}</span></div>
        <h3>{e(h)}</h3>
        <p>{e(d)}</p>
        <span class="link-arrow">That’s me {ARROW}</span>
      </a>""" for i, (t, h, d) in enumerate(PERSONAS["items"])) + "</div>"


def faq_block(items):
    faqs = "".join(f"""
          <div class="faq-item">
            <button class="faq-q" aria-expanded="false">{e(q)}<span class="faq-ico" aria-hidden="true"></span></button>
            <div class="faq-a"><div><p>{e(a)}</p></div></div>
          </div>""" for q, a in items)
    return f"""<section class="section" id="faq">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">{e(FAQS['eyebrow'])}</span><h2 class="h2" data-reveal>{e(FAQS['title'])}</h2></div></div>
      <div class="faq-body">
        <div class="faq-aside" data-fade><p>{e(FAQS['aside'])}</p><a class="link-arrow u-line" href="/contact/">Get in touch {ARROW}</a></div>
        <div class="faq-list">{faqs}
        </div>
      </div>
    </div>
  </section>"""


def testimonial_card(t, big=False):
    tag = '<span class="t-sample">Sample</span>' if t.get("sample") else ""
    return f"""<figure class="t-card{' t-card--big' if big else ''}" data-fade>
        <div class="t-top"><span class="t-mark">{LOGO_MARK}</span>{tag}</div>
        <blockquote>“{e(t['quote'])}”</blockquote>
        <figcaption><strong>{e(t['name'])}</strong><span>{e(t['role'])}</span></figcaption>
      </figure>"""


# ---------- inner pages ----------

def page_about():
    A = ABOUT_PAGE
    rows = "".join(
        f'<div class="about-row" data-fade><p>{e(a)}</p><span class="stat">{e(b)}</span><small>{e(c)}</small></div>'
        for a, b, c in PROBLEM["rows"])
    steps = "".join(f"""
        <li class="step" data-fade><span class="step-num">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>"""
        for i, (t, d) in enumerate(A["process"]))
    story = "".join(f"<p>{e(x)}</p>" for x in A["story"])
    body = f"""{nav("about")}
<main id="main">
  {page_hero(A['eyebrow'], A['title'], A['lead'])}
  <section class="container"><div class="pd-wide" data-fade><img src="{art('pattern', 1600, 700, 'about-wide')}" alt="" width="1600" height="700"></div></section>

  <section class="section">
    <div class="container story">
      <h2 class="h2" data-reveal>{e(A['story_title'])}</h2>
      <div class="story-copy" data-fade>{story}</div>
    </div>
  </section>

  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">{e(PROBLEM['eyebrow'])}</span>
          <h2 class="h2 strike-wrap">{e(PROBLEM['title_a'])} <span class="strike">{e(PROBLEM['strike'])}</span> {e(PROBLEM['title_b'])}</h2></div>
        <p data-fade>{e(PROBLEM['lead'])}</p>
      </div>
      <div class="about-body">
        <div class="about-visual" data-fade><img src="/assets/work/about.svg" alt="" loading="lazy" width="800" height="600"></div>
        <div class="about-rows">{rows}</div>
      </div>
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}

  <section class="section" id="model" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">{e(MODEL['eyebrow'])}</span><h2 class="h2" data-reveal>{e(MODEL['title'])}</h2></div>
        <p data-fade>{e(MODEL['lead'])}</p>
      </div>
      {model_slider()}
    </div>
  </section>

  <section class="section" id="process" style="padding-top:0">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">Process</span><h2 class="h2" data-reveal>{e(A['process_title'])}</h2></div></div>
      <ol class="steps">{steps}
      </ol>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="sec-head">
        <div><span class="eyebrow">{e(PERSONAS['eyebrow'])}</span><h2 class="h2" data-reveal>{e(PERSONAS['title'])}</h2></div>
        <p data-fade>{e(PERSONAS['lead'])}</p>
      </div>
      {personas_grid()}
    </div>
  </section>
  {end_cta()}
</main>
"""
    write("about/index.html", head("About Norvel — AI-Native Design & Webflow Studio",
              "Norvel is an independent, AI-native design and technology studio: brand, web design and Webflow development handled by one senior team.",
              "/about/", crumbs=[("About", "/about/")]) + body + footer())


def page_services():
    S = SERVICES_PAGE
    pillars = "".join(f"""
      <article class="pillar" id="{['brand', 'web-design', 'webflow'][i]}">
        <div class="pillar-head" data-fade><span class="svc-num" style="padding:0">0{i + 1}</span><h2 class="h2">{e(t)}</h2></div>
        <div class="pillar-media" data-fade><img src="{art(['identity', 'ui', 'mobile'][i], 1200, 900, 'service-' + str(i))}" alt="" loading="lazy" width="1200" height="900"></div>
        <div class="pillar-copy" data-fade>
          <p>{e(d)}</p>
          <span class="eyebrow" style="margin-top:2rem">Deliverables</span>
          <ul class="ticks">{''.join(f'<li>{e(x)}</li>' for x in items)}</ul>
          <a class="btn" href="/services/{['brand-identity', 'web-design', 'webflow-development'][i]}/" style="margin-top:2rem">Explore {e(t)}<span class="btn-ico">{ARROW_UR}</span></a>
        </div>
      </article>""" for i, (t, d, items) in enumerate(SERVICES["items"]))
    engage = "".join(f"""
        <div class="engage" data-fade>
          <span class="persona-top"><span>0{i + 1}</span><span>Engagement</span></span>
          <h3>{e(t)}</h3><p>{e(d)}</p>
          <ul class="ticks">{''.join(f'<li>{e(x)}</li>' for x in items)}</ul>
        </div>""" for i, (t, d, items) in enumerate(S["engagements"]))
    body = f"""{nav("services")}
<main id="main">
  {page_hero(S['eyebrow'], S['title'], S['lead'])}
  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light pillars" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">{pillars}
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}
  <section class="section" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">Engagements</span><h2 class="h2" data-reveal>{e(S['engage_title'])}</h2></div></div>
      <div class="personas">{engage}</div>
    </div>
  </section>
  {faq_block(FAQS['items'])}
  {end_cta()}
</main>
"""
    write("services/index.html", head("Web Design, Webflow Development & Brand Identity Services | Norvel",
              "Website design, Webflow development and brand identity from one senior studio. Projects, retainers or a fractional design & Webflow team.",
              "/services/", crumbs=[("Services", "/services/")],
              ld=[faq_ld(FAQS["items"], "/services/")] + [{"@type": "Service", "@id": f"{SITE['url']}/services/#{k}", "name": t,
                  "description": d, "provider": {"@id": ORG_ID}, "areaServed": ["United States", "Europe"],
                  "serviceType": t, "offers": {"@type": "Offer", "url": SITE["url"] + "/contact/"}}
                  for k, (t, d, _) in zip(["brand", "web-design", "webflow"], SERVICES["items"])]) + body + footer())


def page_testimonials():
    T = TESTIMONIALS_PAGE
    slides = "".join(f'<div class="t-slide">{testimonial_card(t, big=True)}</div>' for t in TESTIMONIALS)
    grid = "".join(testimonial_card(t) for t in TESTIMONIALS)
    body = f"""{nav("testimonials")}
<main id="main">
  {page_hero(T['eyebrow'], T['title'], T['lead'])}
  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="slider" data-slider tabindex="0" aria-label="Testimonials">
        <div class="slider-viewport"><div class="slider-track" data-track>{slides}</div></div>
        <div class="slider-ctrl"><span class="slider-count" data-count></span>
          <div class="slider-arrows"><button data-prev aria-label="Previous">{ARROW_L}</button><button data-next aria-label="Next">{ARROW_R}</button></div></div>
      </div>
    </div>
  </section>
  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head"><div><span class="eyebrow">All feedback</span><h2 class="h2" data-reveal>In their words</h2></div>
        <p data-fade>Worked with us? We’d love to hear from you — every review helps another team find the right partner.</p></div>
      <div class="t-grid">{grid}</div>
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}
  <section class="section" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head"><div><span class="eyebrow">{e(PERSONAS['eyebrow'])}</span><h2 class="h2" data-reveal>{e(PERSONAS['title'])}</h2></div><p data-fade>{e(PERSONAS['lead'])}</p></div>
      {personas_grid()}
    </div>
  </section>
  {end_cta()}
</main>
"""
    write("testimonials/index.html", head("Client Testimonials | Norvel", T["lead"], "/testimonials/", crumbs=[("Testimonials", "/testimonials/")]) + body + footer())


def page_contact():
    C = CONTACT_PAGE
    chips = "".join(f'<label class="chip"><input type="checkbox" name="services" value="{e(x)}"><span>{e(x)}</span></label>' for x in C["services"])
    budgets = "".join(f'<label class="chip"><input type="radio" name="budget" value="{e(x)}"><span>{e(x)}</span></label>' for x in C["budgets"])
    details = "".join(f'<div><dt>{e(a)}</dt><dd>{f"<a class=u-line href=mailto:{b}>{b}</a>" if "@" in b else e(b)}</dd></div>' for a, b in C["details"])
    socials = "".join(f'<a class="u-line" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SITE["socials"])
    action = C["form_endpoint"] or f"mailto:{SITE['email']}"
    body = f"""{nav("contact")}
<main id="main">
  <section class="page-hero">
    <div class="container contact-grid">
      <div class="contact-aside">
        <span class="eyebrow">{e(C['eyebrow'])}</span>
        <h1 class="h1" style="margin-top:1.5rem">{e(C['title'])}</h1>
        <p class="muted" style="margin-top:2rem;max-width:420px;line-height:1.5">{e(C['lead'])}</p>
        <dl class="pd-facts">{details}</dl>
        <div class="socials" style="margin-top:2.5rem">{socials}</div>
      </div>
      <form class="contact-form" action="{action}" method="post" data-form data-email="{SITE['email']}" data-endpoint="{e(C['form_endpoint'])}" novalidate>
        <div class="f-row">
          <label class="field"><span>Name *</span><input name="name" required autocomplete="name" placeholder="Your name"></label>
          <label class="field"><span>Email *</span><input name="email" type="email" required autocomplete="email" placeholder="you@company.com"></label>
        </div>
        <label class="field"><span>Company</span><input name="company" autocomplete="organization" placeholder="Company or project name"></label>
        <fieldset class="field"><legend>What do you need?</legend><div class="chips">{chips}</div></fieldset>
        <fieldset class="field"><legend>Budget</legend><div class="chips">{budgets}</div></fieldset>
        <label class="field"><span>Tell us about the project *</span><textarea name="message" rows="5" required placeholder="Goals, timeline, links — anything that helps."></textarea></label>
        <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="sr-only" aria-hidden="true">
        <div class="f-foot">
          <button class="btn" type="submit">Send message<span class="btn-ico">{ARROW_UR}</span></button>
          <p class="f-status" role="status" aria-live="polite"></p>
        </div>
      </form>
    </div>
  </section>
  {faq_block(FAQS['items'][:4])}
</main>
"""
    write("contact/index.html", head("Contact Norvel — Start a Web Design or Webflow Project",
              "Tell us about your website, Webflow or branding project. Norvel replies within one business day with next steps.",
              "/contact/", crumbs=[("Contact", "/contact/")], ld=[faq_ld(FAQS["items"][:4], "/contact/")]) + body + footer())


# ---------- service landing pages ----------
def md_inline(t):
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a class="u-line lime" href="\2">\1</a>', t)
    return t


def related_cards(slugs):
    ps = [q for q in PROJECTS if q["slug"] in slugs]
    return "".join(f"""
      <a class="rel-card" href="/projects/{q['slug']}/" data-fade>
        <div class="rel-media">{pic(project_images(q)[0], q['name'] + ' — ' + q['summary'], '(max-width: 991px) 100vw, 33vw')}</div>
        <h3>{e(q['name'])}</h3><p>{e(q['summary'])}</p>
      </a>""" for q in ps)


def page_service(sp):
    cover_p = next(q for q in PROJECTS if q["slug"] == sp["cover"])
    cover = project_images(cover_p)[0]
    deliver = "".join(f'<div class="dl-item" data-fade><span class="svc-num" style="padding:0">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                      for i, (t, d) in enumerate(sp["deliverables"]))
    steps = "".join(f"""
        <li class="step" data-fade><span class="step-num">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>"""
                    for i, (t, d) in enumerate(sp["process"]))
    others = "".join(f'<a class="link-arrow u-line" href="/services/{o["slug"]}/">{e(o["pillar"])} {ARROW}</a>'
                     for o in SERVICE_PAGES if o["slug"] != sp["slug"])
    path = f"/services/{sp['slug']}/"
    ld = [{"@type": "Service", "@id": SITE["url"] + path + "#service", "name": sp["pillar"], "serviceType": sp["pillar"],
           "description": sp["description"], "provider": {"@id": ORG_ID}, "areaServed": ["United States", "Europe"],
           "url": SITE["url"] + path,
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": sp["pillar"], "itemListElement": [
               {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in sp["deliverables"]]}},
          faq_ld(sp["faqs"], path)]
    body = f"""{nav("services")}
<main id="main">
  <section class="page-hero">
    <div class="container">
      <div class="sec-head" style="padding-bottom:clamp(2.5rem,5vw,4rem)">
        <div><span class="eyebrow">Services · {e(sp['pillar'])}</span><h1 class="h1" style="margin-top:1.5rem">{e(sp['title'])}</h1></div>
        <div class="sec-aside" data-fade><p class="muted">{e(sp['lead'])}</p>
          <a class="btn" href="/contact/" style="margin-top:1.75rem">Start a project<span class="btn-ico">{ARROW_UR}</span></a></div>
      </div>
    </div>
    <figure class="pd-hero-media" data-fade>{pic(cover, cover_p['name'] + ' — ' + cover_p['summary'] + ' by Norvel', lazy=False)}</figure>
  </section>

  <section class="section">
    <div class="container story">
      <h2 class="h2" data-reveal>Why {e(sp['pillar'])} with Norvel</h2>
      <div class="story-copy" data-fade><p>{e(sp['intro'])}</p></div>
    </div>
  </section>

  {stairs('var(--ink)', 'var(--fog)')}
  <section class="section light" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">What you get</span><h2 class="h2" data-reveal>Deliverables</h2></div></div>
      <div class="dl-grid">{deliver}</div>
    </div>
  </section>
  {stairs('var(--fog)', 'var(--ink)', rev=True)}

  <section class="section" style="padding-top:calc(var(--section) - 96px)">
    <div class="container">
      <div class="sec-head sec-head--solo"><div><span class="eyebrow">Process</span><h2 class="h2" data-reveal>How we work</h2></div></div>
      <ol class="steps steps--4">{steps}
      </ol>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="sec-head"><div><span class="eyebrow">Related work</span><h2 class="h2" data-reveal>{e(sp['pillar'])} in practice</h2></div>
        <p data-fade><a class="link-arrow u-line" href="/projects/">All projects {ARROW}</a></p></div>
      <div class="rel-grid">{related_cards(sp['work'])}</div>
    </div>
  </section>

  {faq_block(sp['faqs'])}

  <section class="section" style="padding-top:0">
    <div class="container other-svcs"><span class="eyebrow">Other services</span><div>{others}</div></div>
  </section>
  {end_cta()}
</main>
"""
    write(path.strip("/") + "/index.html",
          head(sp["seo_title"], sp["description"], path, ld=ld,
               crumbs=[("Services", "/services/"), (sp["pillar"], path)]) + body + footer())


# ---------- insights ----------
def render_body(blocks):
    out = []
    for kind, val in blocks:
        if kind == "p":
            out.append(f"<p>{md_inline(val)}</p>")
        elif kind == "h2":
            out.append(f'<h2 id="{re.sub(r"[^a-z0-9]+", "-", val.lower()).strip("-")}">{e(val)}</h2>')
        elif kind in ("ul", "ol"):
            out.append(f"<{kind}>" + "".join(f"<li>{md_inline(x)}</li>" for x in val) + f"</{kind}>")
    return "\n".join(out)


def page_insights():
    cards = "".join(f"""
      <a class="post-card" href="/insights/{q['slug']}/" data-fade>
        <div class="post-meta"><span>{e(q['category'])}</span><span>{e(q['read'])}</span></div>
        <h2>{e(q['title'])}</h2><p>{e(q['excerpt'])}</p>
        <span class="link-arrow lime">Read article {ARROW}</span>
      </a>""" for q in POSTS)
    ld = [{"@type": "Blog", "@id": SITE["url"] + "/insights/#blog", "name": "Norvel Insights", "publisher": {"@id": ORG_ID},
           "blogPost": [{"@type": "BlogPosting", "headline": q["title"], "url": f"{SITE['url']}/insights/{q['slug']}/",
                         "datePublished": q["date"]} for q in POSTS]}]
    body = f"""{nav()}
<main id="main">
  {page_hero("Insights", "Notes on design, Webflow and building for the web", "Practical thinking from the studio — how we approach websites, brands and Webflow builds for SaaS, AI and B2B teams.")}
  <section class="section" style="padding-top:0"><div class="container post-list">{cards}</div></section>
  {end_cta()}
</main>
"""
    write("insights/index.html", head("Insights — Web Design & Webflow Articles | Norvel",
          "Articles from Norvel on website design, Webflow development, branding and building marketing sites for SaaS, AI and B2B companies.",
          "/insights/", ld=ld, crumbs=[("Insights", "/insights/")]) + body + footer())


def page_post(q):
    import datetime
    path = f"/insights/{q['slug']}/"
    nice = datetime.date.fromisoformat(q["date"]).strftime("%B %-d, %Y")
    ld = [{"@type": "BlogPosting", "@id": SITE["url"] + path + "#article", "headline": q["title"], "description": q["description"],
           "datePublished": q["date"], "dateModified": q["date"], "url": SITE["url"] + path, "mainEntityOfPage": SITE["url"] + path,
           "author": {"@type": "Person", "name": AUTHOR["name"], "jobTitle": AUTHOR["role"], "worksFor": {"@id": ORG_ID}},
           "publisher": {"@id": ORG_ID}, "image": SITE["url"] + "/assets/img/og.png", "articleSection": q["category"],
           "inLanguage": "en"}]
    body = f"""{nav()}
<main id="main">
  <article class="post">
    <header class="container post-head">
      <a class="link-arrow u-line" href="/insights/">← Insights</a>
      <span class="eyebrow" style="margin-top:2rem">{e(q['category'])}</span>
      <h1 class="h2" style="margin-top:1.25rem">{e(q['title'])}</h1>
      <div class="post-byline"><span>By {e(AUTHOR['name'])}</span><span>{nice}</span><span>{e(q['read'])}</span></div>
    </header>
    <div class="container"><div class="post-body">{render_body(q['body'])}</div></div>
  </article>
  {end_cta()}
</main>
"""
    write(path.strip("/") + "/index.html", head(q["seo_title"], q["description"], path, ld=ld, og_type="article",
          crumbs=[("Insights", "/insights/"), (q["title"], path)]) + body + footer())


if __name__ == "__main__":
    os.makedirs(os.path.join(PUB, "assets/work"), exist_ok=True)
    page_home()
    page_projects()
    for i, p in enumerate(PROJECTS):
        page_project(i, p)
    page_about()
    page_services()
    page_testimonials()
    page_contact()
    for sp in SERVICE_PAGES:
        page_service(sp)
    page_insights()
    for q in POSTS:
        page_post(q)
    page_404()
    extras()
    if _PIL is not None:
        json.dump(_MANIFEST, open(_MANIFEST_PATH, "w"), indent=1, sort_keys=True)
    print("Built:", sum(len(f) for _, _, f in os.walk(PUB)), "files in", PUB)
