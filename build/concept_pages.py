"""Concept A ("Daylight") — every page except Home. Called from concept.main()."""
import re
from html import escape as e
from urllib.parse import urlparse

from data import (SITE, PROJECTS, PROJECTS_PAGE, SERVICES, SERVICES_PAGE, SERVICE_PAGES, ABOUT_PAGE, MODEL,
                  TESTIMONIALS, TESTIMONIALS_PAGE, CONTACT_PAGE, FAQS, POSTS, AUTHOR)
from concept import ARROW, model_cards
import build as B

BYSLUG = {p["slug"]: p for p in PROJECTS}
PILLAR_SLUG = {"Brand & Identity": "brand-identity", "Web Design": "web-design", "Webflow Development": "webflow-development"}
CHECK = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="#c8f03c"/><path d="M4.6 8.2l2.2 2.2 4.6-4.8" fill="none" stroke="#0b0e13" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def img(src, alt, lazy=True, sizes="(max-width: 760px) 100vw, 1180px"):
    return B.pic(src, alt, sizes=sizes, lazy=lazy)


def frame(src, alt, url="", lazy=True, cls=""):
    host = urlparse(url).netloc.replace("www.", "") if url else "norvelstudio.com"
    return (f'<figure class="frame {cls}" data-rv><div class="fbar"><i></i><i></i><i></i><span>{e(host)}</span></div>'
            f'<div class="fimg">{img(src, alt, lazy)}</div></figure>')


def phero(eyebrow, title, lead, right="", crumbs=None, extra="", cls=""):
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb">' + " <span>/</span> ".join(
            f'<a href="{u}">{e(n)}</a>' if u else f'<span>{e(n)}</span>' for n, u in crumbs) + "</nav>"
    return f"""<section class="phero {cls}">
  <div class="grad grad-ph" aria-hidden="true"><canvas class="gcv"></canvas></div>
  <div class="wrap phgrid{' phgrid--r' if right else ''}">
    <div class="phcopy">{cr}<div class="eyebrow">{e(eyebrow)}</div><h1 class="ph1">{e(title)}</h1><p class="lead">{e(lead)}</p>{extra}</div>
    {f'<div class="phright">{right}</div>' if right else ''}
  </div>
</section>"""


def faq_list(items):
    return "".join(f'<details class="faq"{" open" if i == 0 else ""}><summary>{e(q)}<span class="pm"></span></summary><p>{e(a)}</p></details>'
                   for i, (q, a) in enumerate(items))


def faq_section(items, title="Questions we often get", aside=FAQS["aside"]):
    return f"""<section class="sec" id="faq"><div class="wrap fgrid">
  <div><div class="eyebrow">FAQ</div><h2>{e(title)}</h2><p class="sub">{e(aside)}</p></div>
  <div class="faqs">{faq_list(items)}</div>
</div></section>"""


def steps(items, title, eyebrow="Process", sub=""):
    li = "".join(f'<li data-rv><span class="sn">{i + 1:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(items))
    return f"""<section class="sec"><div class="wrap">
  <div class="eyebrow">{e(eyebrow)}</div><h2>{e(title)}</h2>{f'<p class="sub">{e(sub)}</p>' if sub else ''}
  <ol class="steps" style="--n:{len(items)}">{li}</ol>
</div></section>"""


def project_card(p, big=False):
    cover = B.project_images(p)[0]
    return f"""<a class="pjcard{' pj-big' if big else ''}" href="/projects/{p['slug']}/" data-cat="{e(p['category'].lower())}" data-rv>
  <div class="pjimg">{img(cover, p['name'] + ' — ' + p['summary'], sizes='(max-width: 760px) 100vw, 600px')}</div>
  <div class="pjmeta"><span class="tag">{e(p['category'])}</span><h3>{e(p['name'])}</h3><p>{e(p['card'])}</p><span class="more">View case study {ARROW}</span></div>
</a>"""


# ------------------------------------------------------------------ pages
def page_projects():
    cats = ["All", "Web Design", "Webflow", "E-commerce", "Collaboration", "Out-of-home"]
    chips = "".join(f'<button class="fchip{" on" if i == 0 else ""}" data-f="{"" if c == "All" else c.lower()}">{e(c)}</button>' for i, c in enumerate(cats))
    cards = "".join(project_card(p) for p in PROJECTS)
    right = f'<div class="mk2 statcard"><b>{len(PROJECTS)}</b><span>case studies across venture, AI, enterprise and consumer brands</span><div class="logos2">' + "".join(f'<i>{e(p["client"])}</i>' for p in PROJECTS[:6]) + "</div></div>"
    body = phero("Work", PROJECTS_PAGE["title"], PROJECTS_PAGE["lead"], right) + f"""
<section class="sec pt0"><div class="wrap">
  <div class="filters" role="toolbar" aria-label="Filter projects">{chips}</div>
  <div class="pjgrid" id="pjgrid">{cards}</div>
</div></section>"""
    return body


def page_project(i, p):
    imgs = B.project_images(p)
    video = B.project_video(p)
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    live = f'<a class="btn" href="{p["url"]}" target="_blank" rel="noopener">Visit live site {ARROW}</a>' if p.get("url") else ""
    facts = "".join(f'<div><dt>{a}</dt><dd>{e(b)}</dd></div>' for a, b in (("Client", p["client"]), ("Role", p["role"]), ("Tools", p["tools"]), ("Category", p["category"])))
    right = f'<div class="mk2 facts"><dl>{facts}</dl>{live}</div>'
    shots = imgs[1:]
    media = ""
    if video:
        media += f'<figure class="frame" data-rv><div class="fbar"><i></i><i></i><i></i><span>{e(urlparse(p.get("url", "")).netloc.replace("www.", "") or "norvelstudio.com")}</span></div><div class="fimg"><video src="{video}" poster="{imgs[0]}" autoplay muted loop playsinline preload="metadata" aria-label="{e(p["name"])} walkthrough"></video></div></figure>'
    first = "".join(frame(s, f'{p["name"]} — screen {k + 2}', p.get("url", "")) for k, s in enumerate(shots[:1]))
    rest = "".join(frame(s, f'{p["name"]} — screen {k + 3}', p.get("url", "")) for k, s in enumerate(shots[1:]))
    stp = "".join(f'<div class="scard" data-rv><span class="sn">{k + 1:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>' for k, (a, b) in enumerate(p["steps"]))
    body = phero(p["category"], p["name"], p["card"], right, crumbs=[("Work", "/projects/"), (p["name"], "")], cls="phero--case") + f"""
<section class="cover"><div class="wrap">{frame(imgs[0], p['name'] + ' — ' + p['summary'] + ' by Norvel', p.get('url', ''), lazy=False, cls='frame--hero')}</div></section>
<section class="sec"><div class="wrap split">
  <div><div class="eyebrow">Overview</div><h2>{e(p['summary'])}</h2></div>
  <p class="big">{e(p['intro'])}</p>
</div>
<div class="wrap media">{media}{first}</div></section>
<section class="sec soft"><div class="wrap">
  <div class="head2"><div><div class="eyebrow">Approach</div><h2>Behind the design</h2></div><p class="sub">{e(p['approach'])}</p></div>
  <div class="sgrid">{stp}</div>
</div></section>
{f'<section class="sec"><div class="wrap media">{rest}</div></section>' if rest else ''}
<section class="sec{' pt0' if rest else ''}"><div class="wrap">
  <div class="result" data-rv><div class="eyebrow lime">The result</div><p>{e(p['result'])}</p></div>
  <a class="nextp" href="/projects/{nxt['slug']}/" data-rv>
    <div><span class="eyebrow">Next project</span><h3>{e(nxt['name'])}</h3><p>{e(nxt['summary'])}</p><span class="more">View case study {ARROW}</span></div>
    <div class="npimg">{img(B.project_images(nxt)[0], nxt['name'], sizes='600px')}</div>
  </a>
</div></section>"""
    return body


def page_services():
    pillars = []
    for k, (t, d, items) in enumerate(SERVICES["items"]):
        slug = PILLAR_SLUG[t]
        sp = next(x for x in SERVICE_PAGES if x["slug"] == slug)
        cover = B.project_images(BYSLUG[sp["cover"]])[0]
        li = "".join(f"<li>{CHECK}<span>{e(x)}</span></li>" for x in items)
        pillars.append(f"""<article class="pillar{' rev' if k % 2 else ''}" data-rv>
  <div class="plcopy"><span class="sn">0{k + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p><ul class="checks">{li}</ul><a class="btn ghost dark" href="/services/{slug}/">Explore {e(t)} {ARROW}</a></div>
  <div class="plviz"><div class="pgr pgr-a"></div><div class="plframe">{frame(cover, t + ' — ' + BYSLUG[sp['cover']]['name'], BYSLUG[sp['cover']].get('url', ''))}</div></div>
</article>""")
    eng = "".join(f"""<div class="eng{' hl' if k == 1 else ''}" data-rv><h3>{e(a)}</h3><p>{e(b)}</p><ul class="checks">{''.join(f'<li>{CHECK}<span>{e(x)}</span></li>' for x in c)}</ul><a class="btn{'' if k == 1 else ' ghost dark'}" href="/contact/">Start a {e(a.lower())} {ARROW}</a></div>"""
                  for k, (a, b, c) in enumerate(SERVICES_PAGE["engagements"]))
    body = phero(SERVICES_PAGE["eyebrow"], SERVICES_PAGE["title"], SERVICES_PAGE["lead"]) + f"""
<section class="sec pt0"><div class="wrap pillars">{''.join(pillars)}</div></section>
<section class="sec soft"><div class="wrap">
  <div class="eyebrow">Engagement</div><h2>{e(SERVICES_PAGE['engage_title'])}</h2>
  <div class="engs">{eng}</div>
</div></section>
{steps(ABOUT_PAGE['process'], ABOUT_PAGE['process_title'])}
{faq_section(FAQS['items'])}"""
    return body


def page_service(sp):
    cover = BYSLUG[sp["cover"]]
    right = frame(B.project_images(cover)[0], f'{sp["pillar"]} — {cover["name"]}', cover.get("url", ""), lazy=False)
    ctas = f'<div class="ctas"><a class="btn" href="/contact/">Start a project {ARROW}</a><a class="btn ghost" href="/projects/">See our work ›</a></div>'
    dl = "".join(f'<div class="dcard" data-rv><span class="dico">{k + 1:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>' for k, (a, b) in enumerate(sp["deliverables"]))
    work = "".join(project_card(BYSLUG[s]) for s in sp["work"])
    body = phero(sp["pillar"], sp["title"], sp["lead"], right, crumbs=[("Services", "/services/"), (sp["pillar"], "")], extra=ctas, cls="phero--svc") + f"""
<section class="sec"><div class="wrap split">
  <div><div class="eyebrow">Why it matters</div><h2>{e(sp['pillar'])}, done properly.</h2></div>
  <p class="big">{e(sp['intro'])}</p>
</div></section>
<section class="sec soft"><div class="wrap">
  <div class="eyebrow">What you get</div><h2>Deliverables</h2>
  <div class="dgrid2">{dl}</div>
</div></section>
{steps(sp['process'], 'How the project runs')}
<section class="sec soft"><div class="wrap">
  <div class="head2"><div><div class="eyebrow">Related work</div><h2>{e(sp['pillar'])} in practice</h2></div><a class="btn ghost dark" href="/projects/">All work {ARROW}</a></div>
  <div class="pjgrid pj3">{work}</div>
</div></section>
{faq_section(sp['faqs'], f"{sp['pillar']} FAQ")}"""
    return body


def page_about():
    A = ABOUT_PAGE
    right = """<div class="mk2 aboutcard">
  <div class="arow"><b>3</b><span>service pillars, one team</span></div>
  <div class="arow"><b>8</b><span>flagship case studies</span></div>
  <div class="arow"><b>10×</b><span>directions explored per project</span></div>
  <div class="arow"><b>1</b><span>senior point of contact</span></div>
</div>"""
    story = "".join(f'<p data-rv>{e(x)}</p>' for x in A["story"])
    body = phero(A["eyebrow"], A["title"], A["lead"], right) + f"""
<section class="sec"><div class="wrap split">
  <div><div class="eyebrow">Our story</div><h2>{e(A['story_title'])}</h2></div>
  <div class="story">{story}</div>
</div></section>
<section class="sec dark"><div class="wrap">
  <div class="head2"><div><div class="eyebrow lime">{e(MODEL['eyebrow'])}</div><h2>{e(MODEL['title'])}</h2></div><p class="sub">{e(MODEL['lead'])}</p></div>
  <div class="mgrid">{model_cards()}</div>
</div></section>
{steps(A['process'], A['process_title'])}"""
    return body


def page_testimonials():
    T = TESTIMONIALS_PAGE
    cards = "".join(f"""<figure class="quote{' qbig' if k == 0 else ''}" data-rv>
  {'<span class="sample">Sample</span>' if t.get('sample') else ''}
  <svg class="qmark" viewBox="0 0 32 24" aria-hidden="true"><path d="M0 24V14C0 6 4 1 12 0l1 4c-4 1-6 4-6 8h6v12zm19 0V14c0-8 4-13 12-14l1 4c-4 1-6 4-6 8h6v12z" fill="#c8f03c"/></svg>
  <blockquote>{e(t['quote'])}</blockquote>
  <figcaption><span class="av2">{e(t['name'][:1])}</span><div><b>{e(t['name'])}</b><small>{e(t['role'])}</small></div></figcaption>
</figure>""" for k, t in enumerate(TESTIMONIALS))
    cards += f'<a class="quote qnext" href="/contact/" data-rv><h3>Your project could be next.</h3><p>Tell us what you’re working on — we reply within one business day.</p><span class="more">Start a project {ARROW}</span></a>'
    body = phero(T["eyebrow"], T["title"], T["lead"]) + f'<section class="sec pt0"><div class="wrap qgrid">{cards}</div></section>'
    return body


def page_contact():
    C = CONTACT_PAGE
    chips = "".join(f'<label class="ck"><input type="checkbox" name="services" value="{e(x)}"><span>{e(x)}</span></label>' for x in C["services"])
    budgets = "".join(f'<label class="ck"><input type="radio" name="budget" value="{e(x)}"><span>{e(x)}</span></label>' for x in C["budgets"])
    details = "".join(f'<div class="dt"><small>{e(a)}</small>{f"<a href=mailto:{b}>{b}</a>" if "@" in b else f"<b>{e(b)}</b>"}</div>' for a, b in C["details"])
    action = C["form_endpoint"] or f"mailto:{SITE['email']}"
    body = f"""<section class="phero contact">
  <div class="grad grad-ph" aria-hidden="true"><canvas class="gcv"></canvas></div>
  <div class="wrap cgrid">
    <div class="phcopy"><div class="eyebrow">{e(C['eyebrow'])}</div><h1 class="ph1">{e(C['title'])}</h1><p class="lead">{e(C['lead'])}</p>
      <div class="dts">{details}</div>
      <ol class="nexts"><li><b>1</b>We read your brief and reply within a day.</li><li><b>2</b>A short call to understand goals and timeline.</li><li><b>3</b>A rough plan and estimate, usually within the week.</li></ol>
    </div>
    <form class="cform" action="{action}" method="post" data-cform data-email="{SITE['email']}" data-endpoint="{e(C['form_endpoint'])}" novalidate>
      <div class="frow"><label class="fld"><span>Name *</span><input name="name" required autocomplete="name" placeholder="Your name"></label>
        <label class="fld"><span>Email *</span><input name="email" type="email" required autocomplete="email" placeholder="you@company.com"></label></div>
      <label class="fld"><span>Company</span><input name="company" autocomplete="organization" placeholder="Company or project name"></label>
      <fieldset class="fld"><legend>What do you need?</legend><div class="cks">{chips}</div></fieldset>
      <fieldset class="fld"><legend>Budget</legend><div class="cks">{budgets}</div></fieldset>
      <label class="fld"><span>Tell us about the project *</span><textarea name="message" rows="5" required placeholder="Goals, timeline, links — anything that helps."></textarea></label>
      <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
      <div class="ffoot"><button class="btn" type="submit">Send message {ARROW}</button><p class="fstat" role="status" aria-live="polite"></p></div>
    </form>
  </div>
</section>
{faq_section(FAQS['items'][:4])}"""
    return body


def post_art(q):
    return f'<div class="postart" aria-hidden="true"><div class="pgr pgr-c"></div><div class="mk pa-card"><h6>{e(q["category"])}</h6><p>{e(q["read"])}</p><div class="pa-l"><i></i><i></i><i style="width:60%"></i></div></div></div>'


def page_insights():
    cards = "".join(f"""<a class="post{' post-big' if k == 0 else ''}" href="/insights/{q['slug']}/" data-rv>
  {post_art(q)}
  <div class="postmeta"><div class="pm2"><span class="tag">{e(q['category'])}</span><span>{e(q['date'])} · {e(q['read'])}</span></div><h3>{e(q['title'])}</h3><p>{e(q['excerpt'])}</p><span class="more">Read article {ARROW}</span></div>
</a>""" for k, q in enumerate(POSTS))
    body = phero("Insights", "Notes on design, Webflow and AI-native studios", "Practical guides from the work we do every day — written for marketing teams and founders choosing how to build.") + f'<section class="sec pt0"><div class="wrap">{cards}</div></section>'
    return body


def page_post(q):
    toc = "".join(f'<a href="#{re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")}">{e(v)}</a>' for k, v in q["body"] if k == "h2")
    body = f"""<article>
<section class="phero phero--post">
  <div class="grad grad-ph" aria-hidden="true"><canvas class="gcv"></canvas></div>
  <div class="wrap narrow">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/insights/">Insights</a> <span>/</span> <span>{e(q['category'])}</span></nav>
    <div class="pm2"><span class="tag">{e(q['category'])}</span><span>{e(q['date'])} · {e(q['read'])}</span></div>
    <h1 class="ph1">{e(q['title'])}</h1><p class="lead">{e(q['excerpt'])}</p>
    <div class="author"><span class="av2">{e(AUTHOR['name'][:1])}</span><div><b>{e(AUTHOR['name'])}</b><small>{e(AUTHOR['role'])}</small></div></div>
  </div>
</section>
<section class="sec pt0"><div class="wrap postgrid">
  <aside class="toc"><small>On this page</small>{toc}</aside>
  <div class="prose">{B.render_body(q['body'])}</div>
</div></section>
</article>"""
    return body


def build_all(out, shell):
    n = 0
    out("projects/index.html", shell("Selected work | Norvel", PROJECTS_PAGE["lead"], page_projects(), "projects")); n += 1
    for i, p in enumerate(PROJECTS):
        out(f"projects/{p['slug']}/index.html", shell(f"{p['name']} — {p['summary']} | Norvel", p["card"], page_project(i, p), "projects")); n += 1
    out("services/index.html", shell("Services | Norvel", SERVICES_PAGE["lead"], page_services(), "services")); n += 1
    for sp in SERVICE_PAGES:
        out(f"services/{sp['slug']}/index.html", shell(sp["seo_title"], sp["description"], page_service(sp), "services")); n += 1
    out("about/index.html", shell("About | Norvel", ABOUT_PAGE["lead"], page_about(), "about")); n += 1
    out("testimonials/index.html", shell("Testimonials | Norvel", TESTIMONIALS_PAGE["lead"], page_testimonials(), "testimonials")); n += 1
    out("contact/index.html", shell("Contact | Norvel", CONTACT_PAGE["lead"], page_contact(), "contact", with_cta=False)); n += 1
    out("insights/index.html", shell("Insights | Norvel", "Notes on design, Webflow and AI-native studios.", page_insights(), "insights")); n += 1
    for q in POSTS:
        out(f"insights/{q['slug']}/index.html", shell(q["seo_title"], q["description"], page_post(q), "insights")); n += 1
    return n
