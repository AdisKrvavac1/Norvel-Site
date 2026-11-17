/* Norvel — "Why the old agency model is done" process animation.
   Isometric SVG scene, driven by a 16s looping timeline.
   Old model: brief crawls through 6 hand-offs, meetings pile up, QA bounces it back.
   Norvel model: one platform, AI explores many directions, senior picks one, it ships.
   Markup: <section class="proc" data-theme="light|lime"><div class="proc-stage"></div></section> */
(() => {
  const NS = "http://www.w3.org/2000/svg";
  const T = 16;                         // loop length (s)
  const C30 = Math.cos(Math.PI / 6), S30 = 0.5;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const ease = t => 1 - Math.pow(1 - clamp(t), 3);
  const easeIO = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const lerp = (a, b, k) => a + (b - a) * k;
  const mk = (tag, attrs = {}, parent) => { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); parent && parent.appendChild(n); return n; };

  const OLD = ["Brief", "Account mgr", "Strategy", "Design", "Dev", "QA"];

  function init(root) {
    const stage = root.querySelector(".proc-stage");
    const css = getComputedStyle(root);
    const col = k => css.getPropertyValue("--p-" + k).trim();
    let svg, S = 46, mobile, els = {}, layout, ox = 0, oy = 0;

    const iso = (x, y, z = 0) => [ox + (x - y) * C30 * S, oy + (x + y) * S30 * S - z * S];
    const pts = a => a.map(p => p.map(v => v.toFixed(1)).join(",")).join(" ");

    // An isometric box made of 3 polygons; update() redraws it.
    function box(parent, cls) {
      const g = mk("g", { class: cls || "" }, parent);
      const l = mk("polygon", { fill: col("left"), stroke: col("line"), "stroke-width": 1.2, "stroke-linejoin": "round" }, g);
      const r = mk("polygon", { fill: col("right"), stroke: col("line"), "stroke-width": 1.2, "stroke-linejoin": "round" }, g);
      const t = mk("polygon", { fill: col("top"), stroke: col("line"), "stroke-width": 1.2, "stroke-linejoin": "round" }, g);
      return {
        g, l, r, t,
        set(x, y, w, d, h, z = 0, fills) {
          h = Math.max(0.001, h);
          const A = iso(x, y, z + h), B = iso(x + w, y, z + h), C = iso(x + w, y + d, z + h), D = iso(x, y + d, z + h);
          const B0 = iso(x + w, y, z), C0 = iso(x + w, y + d, z), D0 = iso(x, y + d, z);
          t.setAttribute("points", pts([A, B, C, D]));
          r.setAttribute("points", pts([B, C, C0, B0]));
          l.setAttribute("points", pts([D, C, C0, D0]));
          if (fills) { t.setAttribute("fill", fills[0]); l.setAttribute("fill", fills[1]); r.setAttribute("fill", fills[2]); }
        }
      };
    }

    function build() {
      const W = stage.clientWidth, H = stage.clientHeight;
      mobile = W < 720;
      // station grid positions (iso units)
      // desktop: +x / -y staircase reads as a horizontal line; mobile: +x / +y reads vertical
      layout = mobile
        ? [[0, 0], [3.6, 0], [3.6, 3.6], [7.2, 3.6], [7.2, 7.2], [10.8, 7.2]]
        : [[0, 0], [3.8, 0], [3.8, -3.8], [7.6, -3.8], [7.6, -7.6], [11.4, -7.6]];
      // fit: compute bbox of scene at S=1
      S = 1; ox = 0; oy = 0;
      const ptsAll = [];
      layout.forEach(([x, y]) => { for (const [a, b, z] of [[x, y, 0], [x + 1.8, y, 0], [x, y + 1.8, 0], [x + 1.8, y + 1.8, 0], [x, y, 4.2], [x + 1.8, y + 1.8, 4.2]]) ptsAll.push(iso(a, b, z)); });
      const xs = ptsAll.map(p => p[0]), ys = ptsAll.map(p => p[1]);
      const bw = Math.max(...xs) - Math.min(...xs), bh = Math.max(...ys) - Math.min(...ys);
      const padTop = mobile ? H * 0.22 : H * 0.10, padBot = mobile ? H * 0.03 : H * 0.20, padX = mobile ? W * 0.07 : W * 0.08;
      const availW = W - padX * 2, availH = H - padTop - padBot;
      S = Math.min(availW / bw, availH / bh);
      ox = 0; oy = 0;
      const xs2 = ptsAll.map(p => p[0] * S), ys2 = ptsAll.map(p => p[1] * S);
      ox = padX + (availW - (Math.max(...xs2) - Math.min(...xs2))) / 2 - Math.min(...xs2);
      oy = padTop + (availH - (Math.max(...ys2) - Math.min(...ys2))) / 2 - Math.min(...ys2) + (mobile ? 0 : H * 0.04);

      stage.innerHTML = "";
      svg = mk("svg", { viewBox: `0 0 ${W} ${H}`, class: "proc-svg", role: "img", "aria-label": "Animation comparing the old agency process with the Norvel process" }, stage);
      const gGround = mk("g", {}, svg), gScene = mk("g", {}, svg), gFx = mk("g", {}, svg);
      els = { gGround, gScene, gFx, st: [], meet: [], label: [] };

      // ground route (dashed) between stations
      const c = ([x, y]) => iso(x + .9, y + .9, 0);
      let d = `M ${c(layout[0]).join(" ")}`;
      for (let i = 1; i < layout.length; i++) d += ` L ${c(layout[i]).join(" ")}`;
      els.route = mk("path", { d, fill: "none", stroke: col("line"), "stroke-width": 1.2, "stroke-dasharray": "4 6", "stroke-opacity": .55 }, gGround);
      els.routeLen = els.route.getTotalLength();
      // back-route arc for the QA bounce
      const q = c(layout[5]), ds = c(layout[3]);
      els.back = mk("path", { d: `M ${q.join(" ")} Q ${(q[0] + ds[0]) / 2} ${Math.min(q[1], ds[1]) - S * 3.2} ${ds.join(" ")}`, fill: "none", stroke: col("accent2"), "stroke-width": 1.6, "stroke-dasharray": "3 5", opacity: 0 }, gGround);

      // stations
      layout.forEach(([x, y], i) => {
        const b = box(gScene, "st");
        const meets = [0, 1, 2].map(() => box(gScene, "meet"));
        const lab = mk("text", { class: "proc-lbl", "text-anchor": "middle" }, gFx); lab.textContent = OLD[i];
        const clock = mk("g", {}, gFx);
        mk("circle", { r: S * .42, fill: col("bg"), stroke: col("line"), "stroke-width": 1.2 }, clock);
        const arc = mk("circle", { r: S * .42, fill: "none", stroke: col("accent2"), "stroke-width": 3, "stroke-dasharray": `0 999`, transform: "rotate(-90)" }, clock);
        mk("path", { d: `M0 0 V${-S * .26} M0 0 H${S * .18}`, stroke: col("line"), "stroke-width": 1.4, "stroke-linecap": "round" }, clock);
        els.st.push({ b, meets, lab, clock, arc, x, y });
      });

      // packet (the client's brief)
      els.packet = box(gScene, "pk");
      els.x = mk("g", { opacity: 0 }, gFx);
      mk("circle", { r: S * .36, fill: col("bg"), stroke: col("line"), "stroke-width": 1.4 }, els.x);
      mk("path", { d: `M${-S * .14} ${-S * .14} L${S * .14} ${S * .14} M${S * .14} ${-S * .14} L${-S * .14} ${S * .14}`, stroke: col("line"), "stroke-width": 2, "stroke-linecap": "round" }, els.x);

      // Norvel scene (center of layout)
      // Norvel scene centre: the iso point that projects to a chosen spot in the frame
      const X0 = mobile ? W * 0.5 : W * 0.56, Y0 = mobile ? H * 0.66 : H * 0.53;
      const a = (X0 - ox) / (C30 * S), b2 = (Y0 - oy) / (S30 * S);
      const cx = (a + b2) / 2, cy = (b2 - a) / 2;
      els.center = [cx, cy];
      els.plat = box(gScene, "plat");
      els.tiles = Array.from({ length: 9 }, () => box(gScene, "tile"));
      els.core = box(gScene, "core");
      els.senior = box(gScene, "senior");
      els.live = box(gScene, "live");
      els.beams = mk("g", {}, gGround);
      els.tileBeams = els.tiles.map(() => mk("line", { stroke: col("accent2"), "stroke-width": 1.2, "stroke-dasharray": "2 4", opacity: 0 }, els.beams));
      els.pickBeam = mk("line", { stroke: col("line"), "stroke-width": 1.6, opacity: 0 }, els.beams);
      els.shipBeam = mk("line", { stroke: col("line"), "stroke-width": 1.6, "stroke-dasharray": "5 5", opacity: 0 }, els.beams);
      els.check = mk("g", { opacity: 0 }, gFx);
      mk("circle", { r: S * .5, fill: col("accent"), stroke: col("line"), "stroke-width": 1.4 }, els.check);
      mk("path", { d: `M${-S * .2} 0 l${S * .14} ${S * .14} l${S * .28} ${-S * .3}`, fill: "none", stroke: col("check"), "stroke-width": 2.2, "stroke-linecap": "round", "stroke-linejoin": "round" }, els.check);
      els.nLabels = ["AI explores", "Senior picks", "Live"].map(t => { const n = mk("text", { class: "proc-lbl proc-lbl--n", "text-anchor": "middle", opacity: 0 }, gFx); n.textContent = t; return n; });
      els.pulse = mk("circle", { fill: "none", stroke: col("accent2"), "stroke-width": 1.4, opacity: 0 }, gFx);
    }

    // packet path along the old route; returns [x,y] iso-ground position for progress s (station index float)
    const stPos = i => { const [x, y] = layout[i]; return [x + .55, y + .55]; };

    // timeline of the old journey: list of [type, from, to, dur]
    const steps = [];
    (() => {
      const wait = 0.62, move = 0.42;
      steps.push(["w", 0, 0, wait]);
      for (let i = 1; i <= 5; i++) { steps.push(["m", i - 1, i, move]); steps.push(["w", i, i, i === 5 ? wait * 1.1 : wait]); }
      steps.push(["b", 5, 3, 0.8]);              // bounced back from QA to Design
      steps.push(["w", 3, 3, wait]);
      steps.push(["m", 3, 4, move]); steps.push(["w", 4, 4, wait * .7]);
      steps.push(["m", 4, 5, move]); steps.push(["w", 5, 5, wait]);
    })();
    const OLD_START = 0.9, OLD_DUR = steps.reduce((a, s) => a + s[3], 0), OLD_END = OLD_START + OLD_DUR;
    const COLLAPSE = [OLD_END + 0.2, OLD_END + 1.4], N0 = OLD_END + 1.5;

    function frame(t) {
      const fills = { st: [col("top"), col("left"), col("right")], meet: [col("top"), col("left"), col("right")],
        pk: [col("ink-top"), col("ink-left"), col("ink-right")], acc: [col("accent"), col("accent-l"), col("accent-r")] };
      // ---------- OLD MODEL ----------
      const rise = i => easeIO(seg(t, 0.05 + i * 0.1, 0.55 + i * 0.1));
      const col0 = easeIO(seg(t, COLLAPSE[0], COLLAPSE[1]));      // 0 → 1 collapse
      const fadeLoop = 1 - seg(t, T - 0.5, T);
      // find packet state
      let tt = t - OLD_START, pos = stPos(0), waitAt = -1, waitK = 0, visits = new Array(6).fill(0), bounced = false, bounceK = 0;
      if (tt >= 0) {
        for (const [ty, a, b, du] of steps) {
          if (tt <= du) {
            const k = tt / du;
            if (ty === "w") { pos = stPos(a); waitAt = a; waitK = k; visits[a]++; }
            else if (ty === "m") { const p = stPos(a), q = stPos(b), e = easeIO(k); pos = [lerp(p[0], q[0], e), lerp(p[1], q[1], e)]; }
            else { const p = stPos(a), q = stPos(b), e = easeIO(k); pos = [lerp(p[0], q[0], e), lerp(p[1], q[1], e)]; bounced = true; bounceK = k; }
            break;
          }
          if (ty === "w") visits[a]++;
          if (ty === "b") bounced = true;
          tt -= du;
          pos = stPos(b);
        }
        if (t > OLD_END) { pos = stPos(5); }
      }
      els.st.forEach((s, i) => {
        const h = 1.25 * rise(i) * (1 - col0);
        const [cx, cy] = els.center;
        const x = lerp(s.x, cx - .9, col0), y = lerp(s.y, cy - .9, col0);
        s.b.set(x, y, 1.8, 1.8, h, 0, fills.st);
        s.b.g.setAttribute("opacity", (1 - col0 * .9) * fadeLoop);
        // meetings pile on top: one slab per visit (max 3)
        const n = Math.min(3, visits[i]);
        s.meets.forEach((m, k) => {
          const on = k < n ? 1 : 0;
          m.set(x + .35, y + .35, 1.1, 1.1, .16 * on, h + k * .2 * on, fills.meet);
          m.g.setAttribute("opacity", on * (1 - col0) * fadeLoop);
        });
        const top = iso(x + .9, y + .9, h + .9 + n * .2);
        s.lab.setAttribute("x", top[0]); s.lab.setAttribute("y", top[1] - S * .55);
        s.lab.setAttribute("opacity", rise(i) * (1 - col0) * fadeLoop * (mobile ? (waitAt === i || (waitAt < 0 && i === 0 && t < OLD_START) ? 1 : 0) : 1));
        s.lab.setAttribute("x", clamp(+s.lab.getAttribute("x"), 44, stage.clientWidth - 44));
        // clock while waiting
        const showClock = waitAt === i && t < OLD_END + .1;
        s.clock.setAttribute("transform", `translate(${top[0] + S * 1.05} ${top[1] - S * .2})`);
        s.clock.setAttribute("opacity", showClock ? 1 : 0);
        s.arc.setAttribute("stroke-dasharray", `${(2 * Math.PI * S * .42 * waitK).toFixed(1)} 999`);
      });
      // packet
      const pkOn = t >= OLD_START - .2 && t < COLLAPSE[1];
      const [px, py] = pos;
      const hop = waitAt >= 0 ? 0 : .5;
      const baseH = waitAt >= 0 ? 1.25 * (1 - col0) : 0.15;
      els.packet.set(lerp(px, els.center[0] - .35, col0), lerp(py, els.center[1] - .35, col0), .7, .7, .7, baseH + hop + (bounced && bounceK > 0 && bounceK < 1 ? Math.sin(bounceK * Math.PI) * 2 : 0), fills.pk);
      els.packet.g.setAttribute("opacity", pkOn ? (1 - col0) : 0);
      // QA bounce: × + back arc
      const xOn = bounced && t < OLD_END ? 1 : 0;
      const q = iso(layout[5][0] + .9, layout[5][1] + .9, 1.25 + 2.4);
      els.x.setAttribute("transform", `translate(${q[0]} ${q[1]})`);
      els.x.setAttribute("opacity", xOn * (bounceK < 1 ? 1 : .6) * (1 - col0));
      els.back.setAttribute("opacity", xOn * .9 * (1 - col0));
      els.route.setAttribute("stroke-opacity", (.55 * (1 - col0)).toFixed(2));

      // ---------- NORVEL MODEL ----------
      const [cx, cy] = els.center;
      const n1 = easeIO(seg(t, N0, N0 + .6));                 // platform rises
      const nOut = fadeLoop;
      const PW = mobile ? 5.0 : 4.6;
      els.plat.set(cx - PW / 2, cy - PW / 2, PW, PW, .5 * n1, 0, fills.st);
      els.plat.g.setAttribute("opacity", n1 * nOut);
      const coreK = easeIO(seg(t, N0 + .4, N0 + .9));
      const breathe = 1 + Math.sin(t * 5) * .06 * coreK;
      const cs = (mobile ? 1.6 : 1.35) * breathe;
      els.core.set(cx - cs / 2, cy - cs / 2, cs, cs, (mobile ? 1.6 : 1.4) * coreK, .5, fills.acc);
      els.core.g.setAttribute("opacity", coreK * nOut);
      // tiles fan out around the core (AI explores many directions)
      const R = mobile ? 3.5 : 3.6, tile = mobile ? .95 : .85, pick = 2;
      const pickT = N0 + 2.5, shipT = N0 + 3.3;
      els.tiles.forEach((b, k) => {
        const a = (k / els.tiles.length) * Math.PI * 2 - Math.PI / 4;
        const kk = easeIO(seg(t, N0 + .9 + k * .09, N0 + 1.5 + k * .09));
        const tx = cx + Math.cos(a) * R * kk - tile / 2, ty = cy + Math.sin(a) * R * kk - tile / 2;
        const picked = k === pick && t > pickT;
        const fade = k !== pick && t > pickT ? 1 - seg(t, pickT, pickT + .4) * .75 : 1;
        b.set(tx, ty, tile, tile, (picked ? .9 : .45) * kk, .5 * (1 - kk) + 0, picked ? fills.acc : fills.meet);
        b.g.setAttribute("opacity", kk * fade * nOut);
        const p1 = iso(cx, cy, 1.1), p2 = iso(tx + tile / 2, ty + tile / 2, .45);
        const ln = els.tileBeams[k];
        ln.setAttribute("x1", p1[0]); ln.setAttribute("y1", p1[1]); ln.setAttribute("x2", p2[0]); ln.setAttribute("y2", p2[1]);
        ln.setAttribute("opacity", kk * .8 * fade * nOut);
        if (k === pick) els.pickXY = [tx, ty];
      });
      // senior + live blocks
      const sK = easeIO(seg(t, N0 + 1.9, N0 + 2.4));
      const sx = mobile ? cx - 1.2 : cx - R - 2.2, sy = mobile ? cy + R + .2 : cy - .6, lx = mobile ? cx + R + .1 : cx + R + 1, ly = mobile ? cy - 1.5 : cy - .7;
      els.senior.set(sx, sy, 1.2, 1.2, 1.5 * sK, 0, fills.pk);
      els.senior.g.setAttribute("opacity", sK * nOut);
      const lK = easeIO(seg(t, N0 + 3.0, N0 + 3.5));
      els.live.set(lx, ly, 1.4, 1.4, 1.1 * lK, 0, fills.st);
      els.live.g.setAttribute("opacity", lK * nOut);
      if (els.pickXY) {
        const sp = iso(sx + .6, sy + .6, 1.5), pp = iso(els.pickXY[0] + tile / 2, els.pickXY[1] + tile / 2, .9);
        const pk = seg(t, pickT - .3, pickT);
        els.pickBeam.setAttribute("x1", sp[0]); els.pickBeam.setAttribute("y1", sp[1]);
        els.pickBeam.setAttribute("x2", lerp(sp[0], pp[0], pk)); els.pickBeam.setAttribute("y2", lerp(sp[1], pp[1], pk));
        els.pickBeam.setAttribute("opacity", pk * nOut);
        const lp = iso(lx + .7, ly + .7, 1.1), sh = easeIO(seg(t, shipT, shipT + .7));
        els.shipBeam.setAttribute("x1", pp[0]); els.shipBeam.setAttribute("y1", pp[1]);
        els.shipBeam.setAttribute("x2", lerp(pp[0], lp[0], sh)); els.shipBeam.setAttribute("y2", lerp(pp[1], lp[1], sh));
        els.shipBeam.setAttribute("opacity", (sh > 0 ? 1 : 0) * nOut);
        const ck = easeIO(seg(t, shipT + .6, shipT + .9));
        els.check.setAttribute("transform", `translate(${lp[0]} ${lp[1] - S * 1.1}) scale(${ck})`);
        els.check.setAttribute("opacity", ck * nOut);
        // pulse from Live
        const pu = seg(t, shipT + .8, shipT + 1.8);
        els.pulse.setAttribute("cx", lp[0]); els.pulse.setAttribute("cy", lp[1] - S * 1.1);
        els.pulse.setAttribute("r", (S * .5 + pu * S * 1.6).toFixed(1));
        els.pulse.setAttribute("opacity", (pu > 0 && pu < 1 ? (1 - pu) * .8 : 0) * nOut);
        // labels
        const L = [[iso(cx, cy, 2.6), coreK], [iso(sx + .6, sy + .6, 2.7), sK], [iso(lx + .7, ly + .7, 2.9), lK]];
        const Wd = stage.clientWidth; L.forEach(([p, k], i) => { els.nLabels[i].setAttribute("x", clamp(p[0], 52, Wd - 52)); els.nLabels[i].setAttribute("y", p[1]); els.nLabels[i].setAttribute("opacity", k * nOut); });
      }

      // ---------- captions ----------
      const oldPhase = t < COLLAPSE[0] + .3;
      const weeks = oldPhase ? Math.max(1, Math.round(12 * clamp((t - OLD_START) / OLD_DUR))) : Math.max(1, Math.round(2 * clamp((t - N0 - .6) / 3.4)));
      const handoffs = oldPhase ? Math.min(6, 1 + Math.floor(clamp((t - OLD_START) / (OLD_DUR * .55)) * 5)) : 1;
      root.classList.toggle("is-new", !oldPhase);
      if (root._weeks !== weeks) { root._weeks = weeks; cap.weeks.textContent = weeks; }
      cap.weeksUnit.textContent = weeks === 1 ? "week" : "weeks";
      cap.hand.textContent = oldPhase ? handoffs : 1;
      cap.handUnit.textContent = oldPhase ? (handoffs === 1 ? "hand-off" : "hand-offs") : "senior team";
      cap.loops.textContent = oldPhase ? (bounced || t > OLD_END ? 1 : 0) : "10×";
      cap.loopsUnit.textContent = oldPhase ? "revision loops" : "directions explored";
      cap.phase.textContent = oldPhase ? "The old agency model" : "The Norvel model";
      root.style.setProperty("--p-strike", easeIO(seg(t, COLLAPSE[0] - .2, COLLAPSE[0] + .5)).toFixed(3));
      root.style.setProperty("--p-cap", (seg(t, 0, .6) * fadeLoop).toFixed(3));
    }

    // caption DOM
    const capEl = document.createElement("div");
    capEl.className = "proc-cap";
    capEl.innerHTML = `<span class="proc-phase"></span>
      <div class="proc-stats">
        <div><b data-w>1</b><span data-wu>week</span></div>
        <div><b data-h>1</b><span data-hu>hand-off</span></div>
        <div><b data-l>0</b><span data-lu>revision loops</span></div>
      </div>`;
    root.appendChild(capEl);
    const cap = { phase: capEl.querySelector(".proc-phase"), weeks: capEl.querySelector("[data-w]"), weeksUnit: capEl.querySelector("[data-wu]"),
      hand: capEl.querySelector("[data-h]"), handUnit: capEl.querySelector("[data-hu]"), loops: capEl.querySelector("[data-l]"), loopsUnit: capEl.querySelector("[data-lu]") };

    build();
    const fixed = parseFloat(new URLSearchParams(location.search).get("procT"));
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!isNaN(fixed)) { frame(fixed); return; }
    if (reduce) { frame(N0 + 4); return; }
    let t0 = performance.now(), running = false, paused = 0;
    const loop = now => { if (!running) return; frame(((now - t0) / 1000) % T); requestAnimationFrame(loop); };
    const start = () => { if (!running) { running = true; t0 = performance.now() - paused * 1000; requestAnimationFrame(loop); } };
    const stop = () => { if (running) { running = false; paused = ((performance.now() - t0) / 1000) % T; } };
    new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop()), { threshold: .15 }).observe(root);
    let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { build(); }, 200); });
  }

  document.querySelectorAll(".proc").forEach(init);
})();
