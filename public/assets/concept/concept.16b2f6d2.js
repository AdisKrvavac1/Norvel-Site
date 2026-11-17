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


  /* ===== The problem — card scenes ===== */
  const scs = $$(".sc");
  const fitScenes = () => scs.forEach(sc => {
    const vw = sc.parentElement.clientWidth, dw = +sc.dataset.w;
    sc.style.width = dw + "px"; sc.style.height = sc.dataset.h + "px";
    sc.style.transform = `scale(${Math.max(.62, Math.min(1.25, vw / dw)).toFixed(3)})`;
  });
  fitScenes(); addEventListener("resize", fitScenes);
  const GR = [["Brief", 0, 1.5], ["Account mgr", 1, 2], ["Strategy", 2.5, 2.5], ["Design", 4.5, 3], ["Dev", 7, 3.2], ["QA", 9.5, 1.3], ["Revisions", 10.2, 1.8, "rev"]];
  const grows = $("#grows");
  grows.innerHTML = GR.map(r => `<div class="grow"><span>${r[0]}</span><div class="gtrack"><i class="${r[3] || ""}"></i></div></div>`).join("");
  const gbars = $$("#grows i");
  const sbi = $("#sbi"), sok = $("#sok"), pscr = $("#pscr"), toast = $("#toast");
  const ROLES = [["AM", "Account manager", "Kickoff"], ["ST", "Strategist", "Brief v2"], ["DS", "Designer", "Hand-off"], ["DV", "Developer", "Hand-off"], ["QA", "QA", "Back to design"]];
  $("#troles").innerHTML = ROLES.map(r => `<div class="trow"><span class="av">${r[0]}</span><div><b>${r[1]}</b><small>Agency team</small></div><em>${r[2]}</em></div>`).join("");
  const trows = $$("#troles .trow"), tnew = $("#tnew"), hba = $("#hba"), hna = $("#hna"), hbn = $("#hbn");
  const dgrid = $("#dgrid"), DC = ["#c8f03c", "#9fd8ff", "#6ef2c9", "#d4c2ff", "#ffd36e", "#0b0e13"];
  dgrid.innerHTML = Array.from({ length: 12 }, (_, i) => `<i style="--c:${DC[i % 6]}"></i>`).join("");
  const tiles = [...dgrid.children], dcount = $("#dcount");
  const cbody = $("#cbody");
  const OLD = [[0, .02, .2, "Kickoff"], [0, .5, .18, "Status call"], [1, .1, .22, "Brief review"], [1, .62, .18, "Sync"], [2, .02, .18, "Status call"], [2, .3, .26, "Stakeholder deck"], [2, .7, .2, "Approval"],
    [3, .12, .2, "Sync"], [3, .45, .22, "Feedback round"], [4, .05, .18, "Status call"], [4, .38, .2, "Re-brief"], [4, .7, .2, "Approval"]];
  const NEW = [[2, .3, .22, "Weekly review", "new"], [4, .55, .22, "Shipped ✓", "ship"]];
  cbody.innerHTML = ["9:00", "11:00", "13:00", "15:00"].map((h, i) => `<span class="tl" style="grid-column:1;grid-row:${i + 1}">${h}</span>`).join("") +
    OLD.map(o => `<div class="cev old" style="left:calc(30px + (100% - 30px) * ${o[0]} / 5 + 2px);width:calc((100% - 30px) / 5 - 4px);top:${o[1] * 100}%;height:${o[2] * 100}%">${o[3]}</div>`).join("") +
    NEW.map(o => `<div class="cev ${o[4]}" style="left:calc(30px + (100% - 30px) * ${o[0]} / 5 + 2px);width:calc((100% - 30px) / 5 - 4px);top:${o[1] * 100}%;height:${o[2] * 100}%">${o[3]}</div>`).join("");
  cbody.style.gridTemplateRows = "repeat(4,1fr)";
  const cold = $$("#cbody .cev.old"), cnew = $$("#cbody .cev.new, #cbody .cev.ship");
  const ibA = $("#ibA"), ipA = $("#ipA"), ibarA = $("#ibarA"), idots = $("#idots");
  idots.innerHTML = "<i></i>".repeat(6); const dots = [...idots.children];
  function blobD(r, amp, t) {
    const n = 14, p = [];
    for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, no = Math.sin(7 * 12.9 + i * 1.7) * .6 + Math.sin(7 * 3.1 + i * 3.3) * .4 + Math.sin(t * 2.2 + i) * .25; const rr = r * (1 + amp * no); p.push([rr * Math.cos(a), rr * Math.sin(a)]); }
    let d = ""; for (let i = 0; i < n; i++) { const c = p[i], nx = p[(i + 1) % n], m = [(c[0] + nx[0]) / 2, (c[1] + nx[1]) / 2]; if (!i) { const pv = p[n - 1]; d += `M${((pv[0] + c[0]) / 2).toFixed(1)} ${((pv[1] + c[1]) / 2).toFixed(1)}`; } d += ` Q${c[0].toFixed(1)} ${c[1].toFixed(1)} ${m[0].toFixed(1)} ${m[1].toFixed(1)}`; }
    return d + "Z";
  }
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  function problem(t) {
    // A
    let k = t % 10, out = k > 9.4;
    gbars.forEach((b, i) => { const r = GR[i], p = out ? 0 : seg(k, .3 + i * .75, 1.05 + i * .75); b.style.left = r[1] / 12 * 100 + "%"; b.style.width = r[2] / 12 * 100 * p + "%"; b.classList.toggle("lead", p > 0 && p < 1); });
    sbi.style.width = (out ? 0 : seg(k, .8, 3) * 100) + "%"; sok.classList.toggle("on", !out && k > 3.1);
    pscr.classList.toggle("on", !out && k > 1.8); toast.classList.toggle("on", !out && k > 3.2);
    // B
    k = t % 10; out = k > 9.5;
    trows.forEach((r, i) => { const vis = !out && k > .2 + i * .3; r.style.opacity = vis ? "" : 0; r.style.transform = vis ? "" : "translateY(8px)"; r.classList.toggle("off", !out && k > 4 + i * .12); });
    tnew.classList.toggle("on", !out && k > 4.8);
    const h = out ? 0 : Math.round(6 * seg(k, .5, 3.5)); hna.textContent = h; hba.style.width = h / 6 * 100 + "%"; hbn.style.width = (out ? 0 : 3 * seg(k, 4.8, 5.3)) + "%";
    // C
    k = t % 8; out = k > 7.6;
    const g = out ? 0 : Math.min(12, Math.floor(seg(k, .3, 2.5) * 12.99)); dcount.textContent = g + " / 12";
    tiles.forEach((el, i) => { el.className = out ? "" : (k > 3.6 ? (i === 6 ? "gen pick" : "gen dim") : (i < g ? "gen" : "")); });
    // D
    k = t % 8; out = k > 7.6;
    cold.forEach((el, i) => { const a = !out && k > .2 + i * .14 && k < 3.6 + i * .04; el.style.opacity = a ? 1 : 0; el.style.transform = a ? "" : "scale(.94)"; });
    cnew.forEach((el, i) => { const a = !out && k > 4.3 + i * .7; el.style.opacity = a ? 1 : 0; el.style.transform = a ? "" : "translateY(6px)"; });
    // E
    k = t % 8; out = k > 7.6;
    const hn = out ? 0 : Math.min(6, Math.floor(seg(k, .3, 3.6) * 6.99)), f = 1 - .115 * hn;
    dots.forEach((d, i) => d.classList.toggle("on", i < hn));
    ipA.textContent = Math.round(f * 100) + "%"; ibarA.style.width = f * 100 + "%";
    ibA.setAttribute("d", blobD(17, (1 - f) * .45, t)); ibA.setAttribute("fill", hn ? "#e3e7ec" : "#c8f03c");
  }
  /* modal */
  const pm = $("#pmodal");
  $$(".pplus").forEach(b => b.addEventListener("click", () => {
    const c = b.closest(".pcard"); $("#pme").textContent = c.dataset.eb; $("#pmt").textContent = c.querySelector("h3").textContent; $("#pmp").textContent = c.dataset.body;
    pm.hidden = false; requestAnimationFrame(() => pm.classList.add("on"));
  }));
  const closeM = () => { pm.classList.remove("on"); setTimeout(() => (pm.hidden = true), 250); };
  $("#pmx").addEventListener("click", closeM); pm.addEventListener("click", e => { if (e.target === pm) closeM(); });
  addEventListener("keydown", e => { if (e.key === "Escape" && !pm.hidden) closeM(); });

  /* loop */
  let lastT = 0;
  function frame(t) {
    lastT = t;
    grads.forEach(g => { if (g.vis) grad(g, t); });
    hero(t); bento(t); problem(t);
    if (tabAuto && t - tabT > 5) { tabT = t; setTab((tabI + 1) % tabs.length); }
  }
  addEventListener("resize", () => { grads.forEach(sizeG); grads.forEach(g => grad(g, lastT)); });
  if (!isNaN(FIX)) { $$(".row").forEach(r => (r.style.animation = "none")); tabAuto = false; frame(FIX); }
  else if (reduce) frame(5.8);
  else { const t0 = performance.now(); (function L(n) { frame((n - t0) / 1000); requestAnimationFrame(L); })(t0); }
})();
