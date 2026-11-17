/* Norvel Studio — interactions (no dependencies) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Nav: scrolled state + mobile menu */
  const nav = $(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("is-scrolled", window.scrollY > 10);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    const toggle = $(".nav-toggle", nav);
    toggle && toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    $$(".nav-menu a, .nav-cta", nav).forEach(a => a.addEventListener("click", () => {
      nav.classList.remove("is-open");
      document.body.style.overflow = "";
      toggle && toggle.setAttribute("aria-expanded", "false");
    }));
  }

  /* Active nav link for in-page sections */
  const sectionLinks = $$('.nav-menu a[href*="#"]');
  if (sectionLinks.length && "IntersectionObserver" in window) {
    const map = new Map();
    sectionLinks.forEach(a => {
      const id = a.getAttribute("href").split("#")[1];
      const el = id && document.getElementById(id);
      if (el) map.set(el, a);
    });
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          sectionLinks.forEach(l => l.classList.remove("is-active"));
          map.get(e.target).classList.add("is-active");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, el) => io.observe(el));
  }

  /* Split headings into words for scroll reveal */
  $$("[data-reveal]").forEach(el => {
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) frag.appendChild(document.createTextNode(part));
            else { const s = document.createElement("span"); s.className = "w"; s.textContent = part; frag.appendChild(s); }
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && !n.classList.contains("w")) walk(n);
      });
    };
    walk(el);
  });

  const revealEls = $$("[data-reveal]");
  const updateReveal = () => {
    const vh = window.innerHeight;
    revealEls.forEach(el => {
      const words = $$(".w", el);
      const r = el.getBoundingClientRect();
      // progress 0 when top hits 90% of viewport, 1 when it reaches 45%
      const p = Math.min(1, Math.max(0, (vh * 0.9 - r.top) / (vh * 0.45)));
      const n = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle("on", i < n));
    });
  };
  if (revealEls.length) {
    if (reduce) revealEls.forEach(el => $$(".w", el).forEach(w => w.classList.add("on")));
    else { updateReveal(); window.addEventListener("scroll", updateReveal, { passive: true }); window.addEventListener("resize", updateReveal); }
  }

  /* Fade-ups, strikes and stair dividers */
  const inView = $$("[data-fade], [data-anim], .strike-wrap");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -10% 0px" });
    inView.forEach(el => io.observe(el));
  } else inView.forEach(el => el.classList.add("is-in"));

  /* Hero custom cursor: lime dot + trailing ring (fine pointers only) */
  const hc = $(".hero-cursor");
  if (hc && !reduce && window.matchMedia("(pointer: fine) and (hover: hover) and (min-width: 1025px)").matches) {
    const heroEl = hc.parentElement, ring = $(".hc-ring", hc), dot = $(".hc-dot", hc);
    let x = 0, y = 0, rx = 0, ry = 0, on = false, raf = 0;
    const loop = () => {
      rx += (x - rx) * 0.16; ry += (y - ry) * 0.16;
      dot.style.transform = `translate(${x}px, ${y}px)`;
      ring.style.transform = `translate(${rx}px, ${ry}px)`;
      raf = on ? requestAnimationFrame(loop) : 0;
    };
    heroEl.addEventListener("pointermove", e => {
      const r = heroEl.getBoundingClientRect(); x = e.clientX - r.left; y = e.clientY - r.top;
      if (!on) { on = true; rx = x; ry = y; hc.classList.add("is-on"); raf = raf || requestAnimationFrame(loop); }
      hc.classList.toggle("is-link", !!e.target.closest("a, button"));
    });
    heroEl.addEventListener("pointerleave", () => { on = false; hc.classList.remove("is-on", "is-link"); });
    heroEl.addEventListener("pointerdown", () => { hc.classList.add("is-down"); });
    window.addEventListener("pointerup", () => hc.classList.remove("is-down"));
    heroEl.classList.add("has-cursor");
  }

  /* Marquee: duplicate items for a seamless loop */
  $$(".marquee-track").forEach(t => { t.innerHTML += t.innerHTML; $$(".marquee-item", t).slice(t.children.length / 2).forEach(i => i.setAttribute("aria-hidden", "true")); });

  /* Accordions (services + FAQ) */
  const accordion = (itemSel, btnSel, single) => {
    $$(itemSel).forEach(item => {
      const btn = $(btnSel, item);
      btn && btn.addEventListener("click", () => {
        const open = !item.classList.contains("is-open");
        if (single) $$(itemSel, item.parentElement).forEach(i => { i.classList.remove("is-open"); $(btnSel, i).setAttribute("aria-expanded", "false"); });
        item.classList.toggle("is-open", open);
        btn.setAttribute("aria-expanded", open);
      });
    });
  };
  accordion(".svc", ".svc-btn", true);
  accordion(".faq-item", ".faq-q", true);

  /* Sliders (principles + project gallery) */
  $$("[data-slider]").forEach(root => {
    const track = $("[data-track]", root);
    const items = [...track.children];
    const prev = $("[data-prev]", root), next = $("[data-next]", root), count = $("[data-count]", root);
    let i = 0;
    const perView = () => {
      if (!root.hasAttribute("data-multi")) return 1;
      const w = items[0].getBoundingClientRect().width;
      const n = Math.round(track.getBoundingClientRect().width / w);
      return Number.isFinite(n) && n > 0 ? n : 1;
    };
    const go = to => {
      const max = Math.max(0, items.length - perView());
      i = Math.min(max, Math.max(0, to));
      const gap = parseFloat(getComputedStyle(track).gap) || 0;
      const step = (items[0].getBoundingClientRect().width || 0) + gap;
      track.style.transform = `translateX(${-i * step}px)`;
      items.forEach((it, k) => it.classList.toggle("is-active", k === i));
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === max;
      if (count) count.textContent = `${String(i + 1).padStart(2, "0")} / ${String(items.length).padStart(2, "0")}`;
    };
    prev && prev.addEventListener("click", () => go(i - 1));
    next && next.addEventListener("click", () => go(i + 1));
    root.addEventListener("keydown", e => { if (e.key === "ArrowLeft") go(i - 1); if (e.key === "ArrowRight") go(i + 1); });
    let x0 = null;
    track.addEventListener("pointerdown", e => { x0 = e.clientX; });
    window.addEventListener("pointerup", e => { if (x0 === null) return; const dx = e.clientX - x0; if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1)); x0 = null; });
    window.addEventListener("resize", () => go(i));
    go(0);
  });

  /* Contact form: posts to an endpoint if configured, otherwise opens the email app */
  $$("[data-form]").forEach(form => {
    const status = $(".f-status", form);
    const say = (msg, cls) => { status.textContent = msg; status.className = "f-status " + (cls || ""); };
    form.addEventListener("submit", async ev => {
      ev.preventDefault();
      let ok = true;
      $$("[required]", form).forEach(f => {
        const bad = !f.value.trim() || (f.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.closest(".field").classList.toggle("is-invalid", bad);
        if (bad) ok = false;
      });
      if (!ok) return say("Please fill in the required fields.", "err");
      if (form._gotcha && form._gotcha.value) return;
      const data = new FormData(form);
      const services = data.getAll("services").join(", ");
      const endpoint = form.dataset.endpoint;
      if (endpoint) {
        say("Sending…");
        try {
          const r = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
          if (!r.ok) throw new Error();
          form.reset(); say("Thanks — we’ll be in touch within one business day.", "ok");
        } catch (_) { say("Something went wrong. Email us at " + form.dataset.email, "err"); }
        return;
      }
      const lines = [
        `Name: ${data.get("name")}`, `Email: ${data.get("email")}`, `Company: ${data.get("company") || "-"}`,
        `Services: ${services || "-"}`, `Budget: ${data.get("budget") || "-"}`, "", data.get("message")
      ];
      const subject = `New project inquiry — ${data.get("name")}`;
      window.location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
      say("Opening your email app…", "ok");
    });
    $$("input, textarea", form).forEach(f => f.addEventListener("input", () => f.closest(".field") && f.closest(".field").classList.remove("is-invalid")));
  });

  /* Hero dot field: dots part and glow lime around the pointer; tap sends a ripple */
  const canvas = $(".hero-dots");
  if (canvas && canvas.getContext) {
    const ctx = canvas.getContext("2d");
    const hero = canvas.parentElement;
    const GAP = 24, R = 210, PUSH = 26;
    let W = 0, H = 0, dpr = 1, dots = [], mx = -9999, my = -9999, ripples = [], running = false, visible = true, t0 = performance.now();
    const build = () => {
      const r = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      dots = [];
      const ox = (W % GAP) / 2, oy = (H % GAP) / 2;
      for (let y = oy; y < H; y += GAP) for (let x = ox; x < W; x += GAP) dots.push({ x, y, dx: 0, dy: 0, a: 0 });
    };
    const draw = now => {
      const t = (now - t0) / 1000;
      ctx.clearRect(0, 0, W, H);
      ripples = ripples.filter(rp => now - rp.t < 1600);
      for (const d of dots) {
        let tx = 0, ty = 0, glow = 0;
        const vx = d.x - mx, vy = d.y - my, dist = Math.hypot(vx, vy);
        if (dist < R) {
          const f = 1 - dist / R, k = f * f;
          tx += (vx / (dist || 1)) * PUSH * k; ty += (vy / (dist || 1)) * PUSH * k; glow = Math.max(glow, k);
        }
        for (const rp of ripples) {
          const age = (now - rp.t) / 1000, front = age * 520, dd = Math.hypot(d.x - rp.x, d.y - rp.y), band = Math.abs(dd - front);
          if (band < 60) { const k = (1 - band / 60) * (1 - age / 1.6); tx += ((d.x - rp.x) / (dd || 1)) * 14 * k; ty += ((d.y - rp.y) / (dd || 1)) * 14 * k; glow = Math.max(glow, k); }
        }
        if (!running) { /* static frame */ } else { ty += Math.sin(d.x * 0.012 + t * 0.9) * 1.6 + Math.cos(d.y * 0.015 + t * 0.6) * 1.2; }
        d.dx += (tx - d.dx) * 0.14; d.dy += (ty - d.dy) * 0.14; d.a += (glow - d.a) * 0.12;
        const a = d.a;
        ctx.beginPath();
        ctx.arc(d.x + d.dx, d.y + d.dy, 1.15 + a * 2.2, 0, 6.2832);
        ctx.fillStyle = a > 0.03 ? `rgba(200,240,60,${0.35 + a * 0.65})` : "rgba(238,241,244,0.24)";
        ctx.fill();
      }
      if (running) requestAnimationFrame(draw);
    };
    const start = () => { if (!running && visible) { running = true; requestAnimationFrame(draw); } };
    const stop = () => { running = false; };
    build();
    // Phones & tablets (touch / no hover, or <= 1024px): static dot grid only, no interaction or animation
    const staticGrid = () => reduce || window.matchMedia("(hover: none), (pointer: coarse), (max-width: 1024px)").matches;
    if (staticGrid()) { draw(performance.now()); }
    else {
      start();
      hero.addEventListener("pointermove", e => { const r = canvas.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; });
      hero.addEventListener("pointerleave", () => { mx = my = -9999; });
      hero.addEventListener("pointerdown", e => { const r = canvas.getBoundingClientRect(); ripples.push({ x: e.clientX - r.left, y: e.clientY - r.top, t: performance.now() }); });
      if ("IntersectionObserver" in window) new IntersectionObserver(([en]) => { visible = en.isIntersecting; visible ? start() : stop(); }).observe(canvas);
      document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    }
    let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { build(); if (staticGrid()) { stop(); draw(performance.now()); } }, 150); });
  }

  /* Contact: messages flying along a dashed route from edge to edge.
     Hover speeds them up, clicking sends an extra message, stations light up as planes pass. */
  const flight = $(".flight");
  if (flight) {
    const svg = $(".flight-svg", flight), NS = "http://www.w3.org/2000/svg";
    const mk = (tag, attrs, parent) => { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); parent && parent.appendChild(n); return n; };
    const ICONS = {
      mail: "M-9 -6 h18 v12 h-18 Z M-9 -6 L0 1 L9 -6",
      chat: "M-9 -7 h18 v11 h-9 l-5 4 v-4 h-4 Z",
      at: "M4 0 a4 4 0 1 1 -1.2 -2.9 M4 -3 v4.5 a2.5 2.5 0 0 0 5 0 V0 a9 9 0 1 0 -3.5 7.1",
      bolt: "M2 -9 L-5 1 h5 l-2 8 L5 -2 h-5 Z",
      check: "M-6 0 l4 4 l8 -9"
    };
    const STATIONS = [[0.14, "mail", "Brief"], [0.32, "chat", "Call"], [0.5, "bolt", "Plan"], [0.68, "at", "Kickoff"], [0.86, "check", "Launch"]];
    let W, H, path, len, nodes = [], planes = [], trail = [], sparks = [], boost = 1, target = 1, last = 0, running = false;
    const plane = ghost => { const g = mk("g", { class: "fl-plane" + (ghost ? " ghost" : "") }, svg); mk("path", { d: "M-13 -7 L13 0 L-13 7 L-7 0 Z" }, g); return g; };
    const build = () => {
      W = flight.clientWidth; H = flight.clientHeight;
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.innerHTML = "";
      const amp = H * 0.26, mid = H * 0.55, step = Math.max(260, W / 5);
      let d = `M -60 ${mid}`, x = -60, up = true;
      while (x < W + 60) { const nx = x + step; d += ` C ${x + step * .5} ${up ? mid - amp : mid + amp}, ${nx - step * .5} ${up ? mid - amp : mid + amp}, ${nx} ${mid}`; x = nx; up = !up; }
      path = mk("path", { d, class: "fl-path" }, svg); len = path.getTotalLength();
      sparks = Array.from({ length: Math.round(W / 60) }, () => mk("circle", { class: "fl-spark", cx: Math.random() * W, cy: Math.random() * H, r: Math.random() * 1.2 + .4, opacity: Math.random() * .4 + .1 }, svg));
      sparks.forEach(sp => sp._v = Math.random() * 6 + 4);
      const lenAtX = x => { let lo = 0, hi = len; for (let k = 0; k < 30; k++) { const m = (lo + hi) / 2; path.getPointAtLength(m).x < x ? (lo = m) : (hi = m); } return lo; };
      const list = W < 700 ? STATIONS.filter((_, i) => i % 2 === 0) : STATIONS;
      nodes = list.map(([f, ico, label], i) => {
        const at = lenAtX(W * (0.1 + 0.8 * (i / (list.length - 1))));
        const p = path.getPointAtLength(at), outer = mk("g", { transform: `translate(${p.x} ${p.y})` }, svg), g = mk("g", { class: "fl-node" }, outer);
        mk("circle", { class: "fl-halo", r: 20 }, g); mk("circle", { class: "fl-ring", r: 20 }, g); mk("path", { class: "fl-ico", d: ICONS[ico] }, g);
        const t = mk("text", { class: "fl-label", y: p.y < H / 2 ? 40 : -32 }, g); t.textContent = label;
        return { g, x: p.x, y: p.y, at, hitUntil: 0 };
      });
      trail = Array.from({ length: 14 }, (_, i) => mk("circle", { class: "fl-trail", r: 2.4 - i * .14, opacity: 0 }, svg));
      const old = planes; planes = [];
      const base = [{ s: 0, v: 150 }, { s: len * .38, v: 105, ghost: true }, { s: len * .7, v: 190 }];
      (old.length ? old.map(o => ({ s: o.s % len, v: o.v, ghost: o.ghost, extra: o.extra })) : base).forEach(p => planes.push({ ...p, g: plane(p.ghost) }));
      const hint = mk("text", { class: "fl-hint", x: W - 24, y: H - 14, "text-anchor": "end" }, svg); hint.textContent = "Click to send a message";
    };
    const frame = now => {
      const dt = Math.min(0.05, (now - (last || now)) / 1000); last = now;
      boost += (target - boost) * 0.06;
      planes.forEach((p, i) => {
        p.s += p.v * boost * dt;
        if (p.s > len) { if (p.extra) { p.g.remove(); p.dead = true; return; } p.s -= len; }
        const a = path.getPointAtLength(p.s), b = path.getPointAtLength(Math.min(len, p.s + 2));
        const ang = Math.atan2(b.y - a.y, b.x - a.x) * 57.2958;
        p.g.setAttribute("transform", `translate(${a.x} ${a.y}) rotate(${ang})`);
        if (i === 0) { p.hist = p.hist || []; p.hist.unshift([a.x, a.y]); p.hist.length = Math.min(p.hist.length, 42);
          trail.forEach((c, k) => { const h = p.hist[k * 3]; if (h) { c.setAttribute("cx", h[0]); c.setAttribute("cy", h[1]); c.setAttribute("opacity", (.6 - k * .04).toFixed(2)); } }); }
        nodes.forEach(n => { if (Math.abs(p.s - n.at) < 14 && now > n.hitUntil) { n.hitUntil = now + 900; n.g.classList.remove("hit"); void n.g.getBBox(); n.g.classList.add("hit"); } });
      });
      planes = planes.filter(p => !p.dead);
      nodes.forEach(n => { if (now > n.hitUntil) n.g.classList.remove("hit"); });
      sparks.forEach(sp => { let x = +sp.getAttribute("cx") + sp._v * boost * dt; if (x > W) x = 0; sp.setAttribute("cx", x.toFixed(1)); });
      if (running) requestAnimationFrame(frame);
    };
    const start = () => { if (!running) { running = true; last = 0; requestAnimationFrame(frame); } };
    const stop = () => { running = false; };
    build();
    if (reduce) { frame(performance.now()); }
    else {
      flight.addEventListener("pointerenter", () => (target = 2.4));
      flight.addEventListener("pointerleave", () => (target = 1));
      flight.addEventListener("pointermove", e => {
        const r = flight.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
        nodes.forEach(n => { const d = Math.hypot(n.x - x, n.y - y), k = Math.max(0, 1 - d / 160); n.g.style.transform = `translateY(${-k * 10}px)`; });
      });
      flight.addEventListener("click", () => { if (planes.length < 9) planes.push({ s: 0, v: 260 + Math.random() * 80, extra: true, g: plane(Math.random() > .5) }); });
      new IntersectionObserver(([en]) => (en.isIntersecting ? start() : stop())).observe(flight);
      document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    }
    let rt2; window.addEventListener("resize", () => { clearTimeout(rt2); rt2 = setTimeout(build, 200); });
  }

  /* Footer year */
  $$("[data-year]").forEach(el => (el.textContent = new Date().getFullYear()));
})();
