/* Norvel — Concept A "Daylight": gradients, hero UI, bento micro-animations, tabs, reveal. */
(() => {
  const qs = new URLSearchParams(location.search), FIX = parseFloat(qs.get("t"));
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));

  /* nav */
  const nav = $("#nav");
  const onScroll = () => nav.classList.toggle("solid", scrollY > 20);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  $("#burger").addEventListener("click", () => nav.classList.toggle("open"));
  $$("#mnav a").forEach(a => a.addEventListener("click", () => nav.classList.remove("open")));

  /* moving mesh gradients (low-res canvas, upscaled = free blur) */
  const PAL = ["#9fd8ff", "#c8f03c", "#6ef2c9", "#d4c2ff", "#e9ff7a"];
  const grads = $$(".gcv").map(cv => ({ cv, cx: cv.getContext("2d"), vis: true }));
  const sizeG = g => { g.cv.width = Math.max(8, Math.ceil(g.cv.clientWidth / 6)); g.cv.height = Math.max(8, Math.ceil(g.cv.clientHeight / 6)); };
  grads.forEach(sizeG);
  const B = [[.15, .3, .7, 0], [.55, .2, .6, 1.3], [.85, .5, .65, 2.1], [.4, .8, .6, 3.2], [.95, .1, .5, 4.4]];
  function grad(g, t) {
    const { cv, cx } = g, w = cv.width, h = cv.height;
    cx.fillStyle = PAL[0]; cx.fillRect(0, 0, w, h);
    B.forEach(([x, y, r, ph], i) => {
      const X = w * (x + .12 * Math.sin(t * .35 + ph)), Y = h * (y + .18 * Math.cos(t * .28 + ph * 1.3)), R = w * r;
      const gr = cx.createRadialGradient(X, Y, 0, X, Y, R), c = PAL[(i + 1) % 5];
      gr.addColorStop(0, c); gr.addColorStop(1, c + "00"); cx.fillStyle = gr; cx.fillRect(0, 0, w, h);
    });
  }
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(es => es.forEach(en => { const g = grads.find(x => x.cv === en.target); if (g) g.vis = en.isIntersecting; }));
    grads.forEach(g => io.observe(g.cv));
  }

  /* hero UI (8 s loop) */
  const site = $("#site"), cur = $("#cur"), pg = $("#pg"), dep = $("#dep"), rings = $("#rings"), th = $("#th");
  const RV = [98, 100, 100, 100];
  rings.innerHTML = RV.map(() => `<div class="ring"><svg width="46" height="46"><circle cx="23" cy="23" r="19" fill="none" stroke="#e3e7ec" stroke-width="4"/><circle class="rr" cx="23" cy="23" r="19" fill="none" stroke="#0b0e13" stroke-width="4" stroke-linecap="round" stroke-dasharray="0 120"/></svg><b>0</b></div>`).join("");
  th.innerHTML = "<i></i>".repeat(12);
  const ringEls = [...rings.children], thEls = [...th.children];
  const PTS = [[40, 60], [300, 40], [120, 110], [260, 190], [200, 250]];
  function hero(t) {
    const k = t % 8;
    site.classList.toggle("on", k > 2.2 && k < 7.6);
    const p = PTS[Math.min(4, Math.floor(k / 1.6))]; cur.style.transform = `translate(${p[0]}px,${p[1]}px)`;
    const pr = clamp((k - 3) / 2); pg.style.width = pr * 100 + "%"; dep.classList.toggle("done", pr >= 1);
    ringEls.forEach((r, i) => {
      const v = Math.round(RV[i] * clamp((k - 4.6 - i * .15) / 1)), c = r.querySelector(".rr");
      c.setAttribute("stroke-dasharray", `${(v / 100 * 119.4).toFixed(1)} 120`); c.setAttribute("stroke", v >= 98 ? "#6f9112" : "#0b0e13");
      r.querySelector("b").textContent = v;
    });
    const lit = Math.floor(clamp((k - .4) * 8, 0, 12));
    thEls.forEach((el, i) => { el.className = k > 2 && k < 7.8 ? (i === 4 ? "pick" : "dim") : (i < lit ? "" : "dim"); });
  }

  /* bento */
  const SH = ['<circle cx="12" cy="12" r="10"/>', '<rect x="2" y="2" width="20" height="20" rx="5"/>', '<path d="M12 2l10 20H2z"/>', '<path d="M2 22V2l20 20z"/>',
    '<path d="M2 12a10 10 0 0120 0z"/><path d="M2 14h20v8H2z"/>', '<path d="M2 2h9v9H2zM13 13h9v9h-9z"/>',
    '<path d="M0 6.5 6.6 22H0zM15 13 8.6 0H15zM15 22H9.4L0 0h5.7z" transform="translate(4 1)"/>', '<circle cx="8" cy="12" r="6"/><circle cx="16" cy="12" r="6"/>'];
  const marks = $("#marks"); marks.innerHTML = SH.map(s => `<i><svg viewBox="0 0 24 24" fill="#0b0e13">${s}</svg></i>`).join("");
  const markEls = [...marks.children];
  const frames = $("#frames"); frames.innerHTML = [0, 1, 2].map(() => '<div class="frm"><i class="h"></i><i></i><i style="width:60%"></i><i class="g"></i><i style="width:40%"></i></div>').join("");
  const frmEls = [...frames.children];
  const CODE = ['<span class="k">const</span> hero = {', '  title: <span class="s">"Senior design."</span>,', '  cms: <span class="s">"case-studies"</span>,', '  motion: <span class="k">true</span>,', '};', '<span class="k">webflow</span>.publish(<span class="s">"prod"</span>)'];
  const code = $("#code"), pub = $("#pub"), fan = $("#fan"), ch = $("#ch"), rev = $("#rev");
  $("#rows").innerHTML = [["Acme Studio", "€2,400"], ["MM Mostar", "€860"], ["Lumen Labs", "€5,100"], ["North & Co", "€1,750"]]
    .map((r, i) => `<div class="row" style="animation-delay:${i * .35}s"><span>${r[0]}</span><span>${r[1]}<em>Paid</em></span></div>`).join("");
  const P = [90, 82, 86, 70, 74, 58, 62, 44, 40, 30, 26, 14];
  function bento(t) {
    const k = t % 6;
    markEls.forEach((el, i) => el.classList.toggle("sel", i === Math.floor(t / 1.2) % 8));
    frmEls.forEach((f, i) => { const ph = (t / 2 + i) % 3; f.style.transform = `translate(${ph * 48}px,${ph * 14}px) scale(${1 - ph * .06})`; f.style.zIndex = 3 - Math.floor(ph); f.style.opacity = 1 - ph * .25; });
    const n = Math.min(CODE.length, Math.floor(k * 1.6)); code.innerHTML = CODE.slice(0, n).join("<br>") + (k % 1 < .5 ? "▍" : ""); pub.style.opacity = n >= CODE.length ? 1 : 0;
    const cx = 70, cy = 95, rk = Math.min(1, k / 1.2), pick = k > 2.4;
    let s = `<rect x="${cx - 44}" y="${cy - 32}" width="88" height="64" rx="12" fill="#0b0e13"/><circle cx="${cx}" cy="${cy}" r="${11 + Math.sin(t * 3) * .6}" fill="#c8f03c"/>`;
    for (let j = 0; j < 10; j++) {
      const a = (-50 + j * 100 / 9) * Math.PI / 180, ex = cx + 44 + 260 * Math.cos(a) * rk, ey = cy + 120 * Math.sin(a) * rk, sel = j === 6;
      s += `<line x1="${cx + 44}" y1="${cy}" x2="${ex}" y2="${ey}" stroke="${pick && !sel ? "#e3e7ec" : "#6f9112"}" stroke-width="1.2" stroke-dasharray="3 5"/>`;
      s += `<rect x="${ex - 11}" y="${ey - 11}" width="22" height="22" rx="6" fill="${pick && sel ? "#c8f03c" : "#fff"}" stroke="${pick && !sel ? "#e3e7ec" : "#0b0e13"}" stroke-width="1.3"/>`;
      if (pick && sel) s += `<circle cx="${ex}" cy="${ey}" r="22" fill="none" stroke="#0b0e13" stroke-width="1.4"/><text x="${ex + 30}" y="${ey + 4}" font-size="11" font-weight="600" font-family="Inter,Arial" fill="#0b0e13">Senior pick</text>`;
    }
    fan.innerHTML = s;
    const m = Math.max(2, Math.floor(Math.min(1, k / 3) * P.length)), pts = P.slice(0, m).map((y, i) => `${i * 23.6},${y}`).join(" ");
    ch.innerHTML = `<defs><linearGradient id="cg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#c8f03c"/><stop offset="1" stop-color="#c8f03c" stop-opacity="0"/></linearGradient></defs><polygon points="0,110 ${pts} ${(m - 1) * 23.6},110" fill="url(#cg)" opacity=".7"/><polyline points="${pts}" fill="none" stroke="#0b0e13" stroke-width="2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>`;
    rev.textContent = "€" + Math.round(48210 * Math.min(1, .4 + k / 5)).toLocaleString("en");
  }

  /* persona tabs (auto-advance until the user clicks) */
  const tabs = $$(".ptab"), panes = $$(".ppane"); let tabI = 0, tabAuto = true, tabT = 0;
  const setTab = i => { tabI = i; tabs.forEach((b, j) => { b.classList.toggle("on", j === i); b.setAttribute("aria-selected", j === i); }); panes.forEach((p, j) => p.classList.toggle("on", j === i)); };
  tabs.forEach((b, i) => b.addEventListener("click", () => { tabAuto = false; setTab(i); }));

  /* reveal + counters */
  const rv = $$("[data-rv]");
  if ("IntersectionObserver" in window && !reduce && isNaN(FIX)) {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); count(en.target); } }), { threshold: .15 });
    rv.forEach(el => io.observe(el));
  } else rv.forEach(el => el.classList.add("in"));
  function count(el) {
    const b = el.querySelector("[data-count]"); if (!b) return;
    const to = +b.dataset.count, suf = b.dataset.suffix || "", t0 = performance.now();
    (function f(n) { const k = clamp((n - t0) / 1200); b.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))) + suf; if (k < 1) requestAnimationFrame(f); })(t0);
  }

  /* loop */
  let lastT = 0;
  function frame(t) {
    lastT = t;
    grads.forEach(g => { if (g.vis) grad(g, t); });
    hero(t); bento(t);
    if (tabAuto && t - tabT > 5) { tabT = t; setTab((tabI + 1) % tabs.length); }
  }
  addEventListener("resize", () => { grads.forEach(sizeG); grads.forEach(g => grad(g, lastT)); });
  if (!isNaN(FIX)) { $$(".row").forEach(r => (r.style.animation = "none")); tabAuto = false; frame(FIX); }
  else if (reduce) frame(5.8);
  else { const t0 = performance.now(); (function L(n) { frame((n - t0) / 1000); requestAnimationFrame(L); })(t0); }
})();
