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


def problem_rows():
    return "".join(f'<div class="prow" data-rv><b>{e(n)}</b><span class="pl">{e(r)}</span><span class="pr">{e(l)}</span></div>'
                   for l, n, r in PROBLEM["rows"])


def page():
    tabs, panes = personas()
    css, js = ver("assets/concept/concept.css"), ver("assets/concept/concept.js")
    pjs = ver("assets/concept/process-flat.js")
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Norvel — Senior design, shipped at AI speed (concept A)</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/concept/concept.css?v={css}">
</head><body>
<header class="nav" id="nav"><div class="wrap navin">
  <a href="/concept/" class="brand">{logo()}</a>
  <nav aria-label="Main"><a href="/projects/">Work</a><a href="/services/">Services</a><a href="#products">Products</a><a href="/about/">About</a><a href="/insights/">Insights</a></nav>
  <a class="btn navcta" href="/contact/">Start a project {ARROW}</a>
  <button class="burger" id="burger" aria-label="Open menu"><span></span></button>
</div>
<div class="mnav" id="mnav"><a href="/projects/">Work</a><a href="/services/">Services</a><a href="#products">Products</a><a href="/about/">About</a><a href="/insights/">Insights</a><a class="btn" href="/contact/">Start a project {ARROW}</a></div>
</header>

<main>
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

<section class="sec" id="problem"><div class="wrap">
  <div class="head2"><div><div class="eyebrow">{e(PROBLEM["eyebrow"])}</div>
    <h2>{e(PROBLEM["title_a"])} <s>{e(PROBLEM["strike"])}</s> {e(PROBLEM["title_b"])}</h2></div>
    <p class="sub">{e(PROBLEM["lead"])}</p></div>
  <div class="procwrap" data-rv><div class="proc" data-theme="light"><div class="proc-stage"></div></div></div>
  <div class="prows">{problem_rows()}</div>
</div></section>

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

<section class="cta"><div class="grad grad-cta" aria-hidden="true"><canvas class="gcv" data-pal="a"></canvas></div>
  <div class="wrap ctain"><h2>{e(CTA["title"])}</h2><p>{e(CTA["copy"])}</p>
  <div class="ctas"><a class="btn" href="/contact/">{e(CTA["button"])} {ARROW}</a><a class="btn ghost" href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></div>
</section>
</main>

<footer class="foot"><div class="wrap">
  <div class="fcols"><div>{logo()}<p>{e(HERO["intro"])}</p></div>
    <div><h6>Studio</h6><a href="/about/">About</a><a href="/projects/">Work</a><a href="/testimonials/">Testimonials</a><a href="/insights/">Insights</a></div>
    <div><h6>Services</h6><a href="/services/">Brand &amp; Identity</a><a href="/services/">Web Design</a><a href="/services/">Webflow Development</a></div>
    <div><h6>Contact</h6><a href="mailto:{SITE["email"]}">{SITE["email"]}</a>{"".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SITE["socials"])}</div></div>
  <div class="fbot"><span>© 2026 Norvel Studio</span><span>Concept A — Daylight · not indexed</span></div>
</div></footer>
<script src="/assets/concept/concept.js?v={js}" defer></script>
<script src="/assets/concept/process-flat.js?v={pjs}" defer></script>
</body></html>'''


def main():
    os.makedirs(os.path.join(PUB, "concept"), exist_ok=True)
    open(os.path.join(PUB, "concept/index.html"), "w").write(page())
    print("Concept A written to public/concept/index.html")


if __name__ == "__main__":
    main()
