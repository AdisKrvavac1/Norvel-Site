"""Concept direction A ("Daylight") — Stripe-inspired light redesign of the Norvel home page.
Writes public/concept/index.html (noindex, unlinked). Run: python3 build/concept.py"""
import os
import re
import sys
import hashlib
from html import escape as e

sys.path.insert(0, os.path.dirname(__file__))
from data import SITE, HERO, PROBLEM, MODEL, SERVICES, PERSONAS, FAQS, CTA, PROJECTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")


def ver(rel):
    return hashlib.md5(open(os.path.join(PUB, rel), "rb").read()).hexdigest()[:8]


def hashed(rel):
    """Copy assets/concept/x.ext to x.<hash>.ext (the CDN ignores query strings) and return its URL."""
    import glob
    import shutil
    h = ver(rel)
    base, ext = os.path.splitext(rel)
    for old in glob.glob(os.path.join(PUB, f"{base}.*{ext}")):
        if not old.endswith(f".{h}{ext}"):
            os.remove(old)
    dst = f"{base}.{h}{ext}"
    if not os.path.exists(os.path.join(PUB, dst)):
        shutil.copy(os.path.join(PUB, rel), os.path.join(PUB, dst))
    return "/" + dst


def logo():
    s = open(os.path.join(PUB, "assets/img/norvel-logo-fog.svg")).read()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    s = re.sub(r"<defs>.*?</defs>", "", s, flags=re.S)
    return s.replace('class="cls-1"', 'fill="currentColor"').replace('id="Layer_1" data-name="Layer 1" ', 'class="logo" aria-label="Norvel Studio" role="img" ').strip()


ARROW = '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 7h8M7.5 3.5 11 7l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

WORK = ["hp-workforce-experience", "gyde-health", "playground"]


def work_cards():
    by = {p["slug"]: p for p in PROJECTS}
    out = []
    for i, s in enumerate(WORK):
        p = by[s]
        cls = "w-big" if i == 0 else "w-sm"
        out.append(f'''<a class="wcard {cls}" href="/projects/{s}/" data-rv>
  <div class="wimg"><img src="/assets/work/{s}/01-1400.webp" alt="{e(p["name"])} — {e(p["summary"])}" loading="lazy"></div>
  <div class="wmeta"><span class="tag">{e(p["category"])}</span><h3>{e(p["name"])}</h3><p>{e(p["card"])}</p><span class="more">View case study {ARROW}</span></div>
</a>''')
    return "".join(out)


def services_bento():
    (b_t, b_d, _), (w_t, w_d, _), (d_t, d_d, _) = SERVICES["items"]
    return f'''
  <div class="b c3" data-rv><h3>{e(b_t)}</h3><p>{e(b_d)}</p><div class="viz"><div class="marks" id="marks"></div></div></div>
  <div class="b c3" data-rv><h3>{e(w_t)}</h3><p>{e(w_d)}</p><div class="viz"><div class="frames" id="frames"></div></div></div>
  <div class="b c3" data-rv><h3>{e(d_t)}</h3><p>{e(d_d)}</p><div class="viz"><div class="dev"><div class="code" id="code"></div><div class="prev"><div class="mini"><i class="h"></i><i></i><i style="width:60%"></i><i class="g"></i></div><span class="pub" id="pub">Published</span></div></div></div></div>
  <div class="b c4" data-rv><h3>AI explores. Seniors decide.</h3><p>Ten directions in the time an agency books a kickoff — then one senior call.</p><div class="viz"><svg id="fan" viewBox="0 0 500 190" class="fan"></svg></div></div>
  <div class="b c4" data-rv><h3>Products we build</h3><p>Our own SaaS — Finovo, InvoicePro, NoWay! — built by the same senior team.</p><div class="viz"><div class="dash"><div class="chart"><small>Finovo · revenue</small><b id="rev">€48,210</b><svg id="ch" viewBox="0 0 260 110" preserveAspectRatio="none"></svg></div><div class="inv"><small>InvoicePro · latest</small><div id="rows"></div></div></div></div></div>'''


ICONS = [
    '<path d="M4 18h16M6 18V9l6-4 6 4v9" />',
    '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3"/>',
    '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    '<path d="M4 14l5 5L20 6"/><path d="M14 4h6v6"/>',
]


def model_cards():
    return "".join(
        f'<div class="mcard" data-rv><span class="mico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[i]}</svg></span>'
        f'<span class="mnum">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(MODEL["principles"]))


def personas():
    tabs = "".join(f'<button class="ptab{" on" if i == 0 else ""}" data-i="{i}" role="tab" aria-selected="{"true" if i == 0 else "false"}">{e(a)}</button>'
                   for i, (a, _, _) in enumerate(PERSONAS["items"]))
    panes = "".join(f'<div class="ppane{" on" if i == 0 else ""}" role="tabpanel"><h3>{e(b)}</h3><p>{e(c)}</p><a class="btn" href="/contact/">Start a project {ARROW}</a></div>'
                    for i, (_, b, c) in enumerate(PERSONAS["items"]))
    return tabs, panes


def faqs():
    return "".join(f'<details class="faq"{" open" if i == 0 else ""}><summary>{e(q)}<span class="pm"></span></summary><p>{e(a)}</p></details>'
                   for i, (q, a) in enumerate(FAQS["items"]))



PLUS = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'

PCARDS = [
    ("pa", "Two weeks from brief to live. Not twelve.", "Speed",
     "A traditional agency spends the first month on kickoffs, decks and approvals. We go from brief to a live, production Webflow site in about two weeks — because the people designing are the people building."),
    ("pb", "One senior team. Zero hand-offs.", "Team",
     "Every hand-off between an account manager, a strategist, a designer and a developer loses context. At Norvel, the senior team you meet is the team doing the work, from first sketch to launch."),
    ("pc", "10× the directions, explored before the kickoff call.", "AI-native",
     "AI lets us prototype ten directions in the time an agency books a kickoff. Senior designers review them and pick the one worth building — the judgment is never outsourced to a model."),
    ("pd", "Fewer status calls. More shipping.", "Process",
     "Status meetings don’t move a project. We replace them with short weekly reviews of real, working pages you can click through."),
    ("pe", "Your idea, intact.", "Quality",
     "Ideas get diluted when they pass through six people. With one team end to end, what you approve on day one is what goes live."),
]

SCENES = {
    "pa": """<div class="sc" data-w="760" data-h="380">
  <div class="pgr pgr-a"></div>
  <div class="mk gantt"><div class="mkbar"><i></i><i></i><i></i><span>agency-project · timeline</span></div>
    <div class="gw"><span></span>""" + "".join(f"<em>W{i}</em>" for i in range(1, 13)) + """</div>
    <div class="grows" id="grows"></div></div>
  <div class="mk sprint" id="sprint"><h6>Norvel sprint</h6><p>Brief → live</p><div class="sbar"><i id="sbi"></i></div><div class="srow"><span>W1</span><span>W2</span><b class="chipok" id="sok">Shipped ✓</b></div></div>
  <div class="phone"><div class="pscr" id="pscr"><i class="p1"></i><i class="p2"></i><i class="p3"></i><i class="p4"></i><i class="p5"></i>
    <div class="toast" id="toast"><b>✓</b>Live · week 2</div></div></div>
</div>""",
    "pb": """<div class="sc" data-w="360" data-h="440">
  <div class="pgr pgr-b"></div>
  <div class="mk team"><h6>Your project team</h6><div id="troles"></div><div class="trow tnew" id="tnew"><span class="av lime">N</span><div><b>Norvel senior team</b><small>Strategy · design · build</small></div><em class="dl">Direct line</em></div></div>
  <div class="mk hand"><h6>Hand-offs per project</h6>
    <div class="hb"><span>Agency</span><div class="ht"><i id="hba"></i></div><b id="hna">0</b></div>
    <div class="hb"><span>Norvel</span><div class="ht"><i id="hbn" class="lime"></i></div><b>0</b></div></div>
</div>""",
    "pc": """<div class="sc" data-w="360" data-h="250">
  <div class="pgr pgr-c"></div>
  <div class="mk dirs"><div class="dhead"><h6>AI explorations</h6><span id="dcount">0 / 12</span></div><div class="dgrid" id="dgrid"></div></div>
</div>""",
    "pd": """<div class="sc" data-w="360" data-h="250">
  <div class="pgr pgr-d"></div>
  <div class="mk cal"><div class="chead"><span></span><em>Mon</em><em>Tue</em><em>Wed</em><em>Thu</em><em>Fri</em></div><div class="cbody" id="cbody"></div></div>
</div>""",
    "pe": """<div class="sc" data-w="360" data-h="250">
  <div class="pgr pgr-e"></div>
  <div class="mk intact">
    <div class="irow"><svg viewBox="-24 -24 48 48" class="iblob"><path id="ibA" fill="#e3e7ec" stroke="#0b0e13" stroke-width="1.4"/></svg><div class="im"><div class="il"><span>Agency · 6 hand-offs</span><b id="ipA">100%</b></div><div class="it"><i id="ibarA"></i></div><div class="idots" id="idots"></div></div></div>
    <div class="irow"><svg viewBox="-24 -24 48 48" class="iblob"><circle r="17" fill="#c8f03c" stroke="#0b0e13" stroke-width="1.4"/></svg><div class="im"><div class="il"><span>Norvel · 1 team</span><b>100%</b></div><div class="it"><i class="lime" style="width:100%"></i></div><div class="idots"><i class="on"></i></div></div></div>
  </div>
</div>""",
}


def problem_cards():
    out = []
    for i, (k, title, eb, body) in enumerate(PCARDS):
        size = "pc-lg" if i == 0 else ("pc-tall" if i == 1 else "pc-sm")
        out.append(f'<article class="pcard {size}" data-rv data-eb="{e(eb)}" data-body="{e(body)}">'
                   f'<header><h3>{e(title)}</h3><button class="pplus" aria-label="More about: {e(title)}">{PLUS}</button></header>'
                   f'<div class="pviz2" aria-hidden="true">{SCENES[k]}</div></article>')
    return "".join(out)


def problem_rows():
    return "".join(f'<div class="prow" data-rv><b>{e(n)}</b><span class="pl">{e(r)}</span><span class="pr">{e(l)}</span></div>'
                   for l, n, r in PROBLEM["rows"])


NAVL = [("Work", "/projects/", "projects"), ("Services", "/services/", "services"), ("About", "/about/", "about"),
        ("Testimonials", "/testimonials/", "testimonials"), ("Insights", "/insights/", "insights")]


def cta():
    return f"""<section class="cta"><div class="grad grad-cta" aria-hidden="true"><canvas class="gcv"></canvas></div>
  <div class="wrap ctain"><h2>{e(CTA["title"])}</h2><p>{e(CTA["copy"])}</p>
  <div class="ctas"><a class="btn" href="/contact/">{e(CTA["button"])} {ARROW}</a><a class="btn ghost" href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></div>
</section>"""


LIVE = {"on": False}


def shell(title, desc, body, active="", with_cta=True):
    css, js = hashed("assets/concept/concept.css"), hashed("assets/concept/concept.js")
    links = "".join(f'<a href="{u}"{" aria-current=page" if k == active else ""}>{n}</a>' for n, u, k in NAVL)
    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav" id="nav"><div class="wrap navin">
  <a href="/" class="brand" aria-label="Norvel home">{logo()}</a>
  <nav aria-label="Main">{links}</nav>
  <a class="btn navcta" href="/contact/">Start a project {ARROW}</a>
  <button class="burger" id="burger" aria-label="Open menu"><span></span></button>
</div>
<div class="mnav" id="mnav">{links}<a class="btn" href="/contact/">Start a project {ARROW}</a></div>
</header>
<main id="main">
{body}
{cta() if with_cta else ""}
</main>
<footer class="foot"><div class="wrap">
  <div class="fcols"><div>{logo()}<p>{e(HERO["intro"])}</p></div>
    <div><h6>Studio</h6><a href="/about/">About</a><a href="/projects/">Work</a><a href="/testimonials/">Testimonials</a><a href="/insights/">Insights</a></div>
    <div><h6>Services</h6><a href="/services/brand-identity/">Brand &amp; Identity</a><a href="/services/web-design/">Web Design</a><a href="/services/webflow-development/">Webflow Development</a></div>
    <div><h6>Contact</h6><a href="/contact/">Start a project</a><a href="mailto:{SITE["email"]}">{SITE["email"]}</a>{"".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SITE["socials"])}</div></div>
  <div class="fbot"><span>© 2026 Norvel Studio</span><span>Designed &amp; built by Norvel</span></div>
</div></footer>
<script src="{js}" defer></script>
</body></html>"""
    if LIVE["on"]:
        return html
    # preview: keep every internal link inside /concept/
    return re.sub(r'href="/(?!concept/|assets/)([^"]*)"', r'href="/concept/\1"', html)


def home():
    tabs, panes = personas()
    body = f"""
<section class="hero">
  <div class="grad" aria-hidden="true"><canvas class="gcv" data-pal="a"></canvas></div>
  <div class="wrap hgrid">
    <div class="hcopy">
      <a class="chip" href="/services/"><b>New</b>AI-native design sprints — live in 2 weeks {ARROW}</a>
      <h1>{e(HERO["line1"])}<br>{e(HERO["line2"])}</h1>
      <p class="lead">{e(HERO["sub"])}</p>
      <div class="ctas"><a class="btn" href="/contact/">{e(CTA["button"])} {ARROW}</a><a class="btn ghost" href="/projects/">See our work ›</a></div>
    </div>
    <div class="stage" aria-hidden="true">
      <div class="card browser"><div class="bar"><i></i><i></i><i></i><span>yourbrand.com</span></div>
        <div class="site" id="site"><div class="blk s1"></div><div class="blk s2"></div><div class="blk s3"></div><div class="blk s4"></div><div class="s5"><div class="blk"></div><div class="blk"></div></div><div class="blk s6"></div>
          <div class="cursor" id="cur"><svg width="18" height="18" viewBox="0 0 18 18"><path d="M2 1l13 7-6 1.6L6.4 16z" fill="#0b0e13" stroke="#fff" stroke-width="1.2"/></svg><em>Senior designer</em></div></div></div>
      <div class="card deploy" id="dep"><h6>Publishing to Webflow</h6><p>Week 2 · production</p><div class="prog"><i id="pg"></i></div><span class="ok"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M3 7.5l2.6 2.6L11 4" fill="none" stroke="#0b0e13" stroke-width="2" stroke-linecap="round"/></svg></span></div>
      <div class="card lh"><h6>Lighthouse</h6><p>Performance · A11y · SEO · Best practices</p><div class="rings" id="rings"></div></div>
      <div class="card ai"><h6>AI explored 12 directions</h6><p>Senior team picked one</p><div class="thumbs" id="th"></div></div>
    </div>
  </div>
  <div class="wrap logos" aria-label="Selected clients"><span>Trusted by teams at</span><b>HP</b><b>a16z</b><b>Lightspeed</b><b>Lagunitas</b><b>Gyde</b><b>Playground</b><b>Hello Cake</b></div>
</section>

<section class="sec pbsec" id="problem"><div class="wrap">
  <div class="eyebrow">{e(PROBLEM["eyebrow"])}</div>
  <h2 class="lead2">{e(PROBLEM["title_a"])} <s>{e(PROBLEM["strike"])}</s> {e(PROBLEM["title_b"])} <span>{e(PROBLEM["lead"])}</span></h2>
  <div class="pgrid">{problem_cards()}</div>
</div></section>
<div class="pmodal" id="pmodal" hidden><div class="pmbox" role="dialog" aria-modal="true" aria-labelledby="pmt"><button class="pmx" id="pmx" aria-label="Close">×</button><div class="eyebrow" id="pme"></div><h3 id="pmt"></h3><p id="pmp"></p><a class="btn" href="/contact/">Start a project {ARROW}</a></div></div>

<section class="sec soft" id="work"><div class="wrap">
  <div class="head2"><div><div class="eyebrow">Selected work</div><h2>Websites for teams building what’s next.</h2></div>
    <a class="btn ghost dark" href="/projects/">All {len(PROJECTS)} case studies {ARROW}</a></div>
  <div class="wgrid">{work_cards()}</div>
</div></section>

<section class="sec" id="services"><div class="wrap">
  <div class="eyebrow">{e(SERVICES["eyebrow"])}</div>
  <h2>One senior team. Everything a modern brand needs.</h2>
  <p class="sub">Brand, website and build under one roof — with AI doing the heavy lifting and seniors making every call that matters.</p>
  <div class="bento" id="products">{services_bento()}</div>
</div></section>

<section class="sec dark" id="model"><div class="wrap">
  <div class="head2"><div><div class="eyebrow lime">{e(MODEL["eyebrow"])}</div><h2>{e(MODEL["title"])}</h2></div><p class="sub">{e(MODEL["lead"])}</p></div>
  <div class="mgrid">{model_cards()}</div>
</div></section>

<section class="sec" id="who"><div class="wrap">
  <div class="eyebrow">{e(PERSONAS["eyebrow"])}</div><h2>{e(PERSONAS["title"])}</h2>
  <div class="persona" data-rv><div class="ptabs" role="tablist">{tabs}</div><div class="ppanes">{panes}<div class="pviz" aria-hidden="true"><canvas class="gcv" data-pal="a"></canvas></div></div></div>
</div></section>

<section class="sec stats-sec"><div class="wrap"><div class="stats">
  <div data-rv><b data-count="8">8</b><span>flagship case studies</span></div>
  <div data-rv><b data-count="2" data-suffix=" wks">2 wks</b><span>to first live release</span></div>
  <div data-rv><b data-count="10" data-suffix="×">10×</b><span>directions explored</span></div>
  <div data-rv><b data-count="1">1</b><span>senior team, end to end</span></div>
</div></div></section>

<section class="sec" id="faq"><div class="wrap fgrid">
  <div><div class="eyebrow">{e(FAQS["eyebrow"])}</div><h2>{e(FAQS["title"])}</h2><p class="sub">{e(FAQS["aside"])}</p></div>
  <div class="faqs">{faqs()}</div>
</div></section>

"""
    return body


def merge_head(rel, html):
    """Live mode: keep the SEO head (canonical, OG, JSON-LD, robots) the classic build wrote for this URL."""
    old_path = os.path.join(PUB, rel)
    if not os.path.exists(old_path):
        return html
    old = open(old_path).read()
    oh = old[old.index("<head>") + 6:old.index("</head>")]
    oh = re.sub(r'<link[^>]+(style\.css|fonts\.googleapis\.com/css2|fonts\.googleapis\.com"|fonts\.gstatic\.com)[^>]*>\n?', "", oh)
    oh = oh.replace('content="#0b0e13"', 'content="#ffffff"')
    nh = html[html.index("<head>") + 6:html.index("</head>")]
    keep = "\n".join(l for l in nh.splitlines() if "fonts.g" in l or "assets/concept" in l)
    return html[:html.index("<head>") + 6] + oh + keep + "\n" + html[html.index("</head>"):]


def out(rel, html):
    if LIVE["on"]:
        html = merge_head(rel, html)
        path = os.path.join(PUB, rel)
    else:
        path = os.path.join(PUB, "concept", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(html)


def page_404():
    return f"""<section class="phero nf"><div class="grad grad-ph" aria-hidden="true"><canvas class="gcv"></canvas></div>
  <div class="wrap phgrid"><div class="phcopy"><div class="eyebrow">Error 404</div><h1 class="ph1">This page took a different direction.</h1>
  <p class="lead">The page you’re looking for doesn’t exist or has moved. Let’s get you back on track.</p>
  <div class="ctas"><a class="btn" href="/">Back to home {ARROW}</a><a class="btn ghost" href="/projects/">See our work ›</a></div></div></div></section>"""


def main(live=False):
    LIVE["on"] = live
    out("index.html", shell("Norvel — Senior design, shipped at AI speed", SITE["description"], home()))
    import concept_pages
    n = concept_pages.build_all(out, shell)
    out("404.html", shell("Page not found | Norvel", SITE["description"], page_404(), with_cta=False))
    print("Daylight design written:", n + 2, "pages", "(live)" if live else "under public/concept/")


if __name__ == "__main__":
    main()
