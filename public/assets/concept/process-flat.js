/* Norvel — "Idea in, idea out". Flat line-art animation for The problem section.
   Old model: a crisp idea relays through six hand-offs, meetings pile up, it loses shape and colour,
   QA bounces it back. Norvel model: one senior team, AI explores ten directions at once,
   the senior picks one, it ships intact in two weeks.
   Markup: <div class="proc"><div class="proc-stage"></div></div>. ?procT=<s> freezes a frame. */
(() => {
  const T = 18;
  const INK = "#0b0e13", LIME = "#c8f03c", LIME2 = "#6f9112", G = "#8a93a0", LG = "#e3e7ec", RED = "#d6453d";
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const easeO = t => 1 - Math.pow(1 - clamp(t), 3);
  const easeIO = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  const lerp = (a, b, k) => a + (b - a) * k;
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, k) => { const A = hex(a), B = hex(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], clamp(k)))).join(",")})`; };
  const f1 = n => n.toFixed(1);
  const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

  const NAMES = ["Brief", "Account mgr", "Strategy", "Design", "Dev", "QA"];

  // ---- old-model timeline ----
  const WAIT = .56, MOVE = .36, BOUNCE = .9;
  const steps = [];
  steps.push({ k: "w", a: 0 });
  for (let i = 1; i <= 5; i++) { steps.push({ k: "m", a: i - 1, b: i }); steps.push({ k: "w", a: i, rej: i === 5 }); }
  steps.push({ k: "b", a: 5, b: 3 });
  steps.push({ k: "w", a: 3 });
  steps.push({ k: "m", a: 3, b: 4 }); steps.push({ k: "w", a: 4 });
  steps.push({ k: "m", a: 4, b: 5 }); steps.push({ k: "w", a: 5 });
  const OLD_START = .5;
  { let t = OLD_START, fid = 1, hand = 0;
    for (const s of steps) {
      s.t0 = t; s.d = s.k === "w" ? WAIT : s.k === "m" ? MOVE : BOUNCE; t += s.d; s.t1 = t;
      s.f0 = fid; if (s.k === "m") fid = Math.max(.3, fid - .11); if (s.k === "b") fid = Math.max(.3, fid - .14); s.f1 = fid;
      s.h0 = hand; if (s.k !== "w") hand++; s.h1 = hand;
    } }
  const OLD_END = steps[steps.length - 1].t1;
  const C0 = OLD_END + .35, C1 = C0 + 1.1, N0 = C1 + .1;
  // meetings booked at each wait (station → count added)
  const MEET = [1, 3, 2, 2, 1, 1, 0, 2, 1, 1, 0];

  function blob(cx, cy, r, amp, seed, t) {
    const n = 14, p = [];
    for (let i = 0; i < n; i++) {
      const a = i / n * Math.PI * 2;
      const no = Math.sin(seed * 12.9 + i * 1.7) * .6 + Math.sin(seed * 3.1 + i * 3.3) * .4 + Math.sin(t * 2.2 + i) * .25;
      const rr = r * (1 + amp * no);
      p.push([cx + rr * Math.cos(a), cy + rr * Math.sin(a)]);
    }
    let d = "";
    for (let i = 0; i < n; i++) {
      const c = p[i], nx = p[(i + 1) % n], m = [(c[0] + nx[0]) / 2, (c[1] + nx[1]) / 2];
      if (i === 0) { const pv = p[n - 1]; d += `M${f1((pv[0] + c[0]) / 2)} ${f1((pv[1] + c[1]) / 2)}`; }
      d += ` Q${f1(c[0])} ${f1(c[1])} ${f1(m[0])} ${f1(m[1])}`;
    }
    return d + "Z";
  }
  const text = (x, y, s, cls, extra = "") => `<text x="${f1(x)}" y="${f1(y)}" class="${cls}" ${extra}>${esc(s)}</text>`;

  function init(root) {
    const stage = root.querySelector(".proc-stage");
    let W, H, mobile, L, svg;

    function measure() {
      W = stage.clientWidth; H = stage.clientHeight; mobile = W < 700;
      const left = mobile ? 24 : Math.max(24, (W - 1280) / 2 + 24), right = W - left;
      L = { left, right };
      if (!mobile) {
        const ty = H * .5, sp = (right - left - 150) / 5;
        const cw = Math.min(150, sp * .74), ch = cw * .72;
        L.st = NAMES.map((_, i) => [left + 75 + sp * i, ty]);
        Object.assign(L, { cw, ch, ty, rulerY: H - 92, meterX: right - 220, meterW: 220, meterY: 58, capY: 58 });
        const span = right - left;
        L.sen = [left + span * .2, ty]; L.senW = Math.min(170, span * .14); L.senH = L.senW * .72;
        L.rayR = span * .3; L.rayA = [-42, 42]; L.rayFrom = [L.sen[0] + L.senW / 2, ty];
        L.liveW = Math.min(240, span * .2); L.liveH = L.liveW * .7; L.live = [right - L.liveW / 2 - 10, ty];
      } else {
        const top = Math.max(H * .3, 160), bot = H - 110, sp = (bot - top) / 5;
        const ch = Math.min(58, sp * .72), cw = ch * 2, x = W * .36;
        L.st = NAMES.map((_, i) => [x, top + sp * i]);
        Object.assign(L, { cw, ch, rulerY: 0, meterX: 24, meterW: W - 48, meterY: H - 44, capY: 34 });
        L.senW = 110; L.senH = 76; L.sen = [W / 2, 150 + L.senH / 2];
        L.rayR = Math.min(130, H * .2); L.rayA = [40, 140]; L.rayFrom = [W / 2, L.sen[1] + L.senH / 2];
        L.liveW = Math.min(250, W - 80); L.liveH = 130; L.live = [W / 2, H - 92 - L.liveH / 2];
      }
      L.rays = Array.from({ length: 10 }, (_, j) => {
        const a = (L.rayA[0] + (L.rayA[1] - L.rayA[0]) * j / 9) * Math.PI / 180;
        const sx = mobile ? 1.3 : 1, sy = mobile ? .85 : .62;
        return [L.rayFrom[0] + L.rayR * Math.cos(a) * sx, L.rayFrom[1] + L.rayR * Math.sin(a) * sy];
      });
      L.pick = mobile ? 4 : 5;
      stage.innerHTML = `<svg class="proc-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Animation: in the old agency model an idea loses shape across six hand-offs and twelve weeks; at Norvel one senior team explores ten directions with AI and ships the chosen one intact in two weeks."></svg>`;
      svg = stage.firstChild;
    }

    function oldState(t) {
      let s = steps[0];
      for (const x of steps) { if (t >= x.t0) s = x; }
      const k = seg(t, s.t0, s.t1);
      const st = L.st;
      let pos, at, fid = lerp(s.f0, s.f1, easeIO(k)), hand = s.h0 + (k >= 1 ? s.h1 - s.h0 : 0);
      if (t < OLD_START) { pos = st[0]; at = 0; }
      else if (s.k === "w") { pos = st[s.a]; at = s.a; }
      else if (s.k === "m") { const e = easeIO(k); pos = [lerp(st[s.a][0], st[s.b][0], e), lerp(st[s.a][1], st[s.b][1], e)]; at = e < .5 ? s.a : s.b; }
      else { const e = easeIO(k); pos = bounceAt(e); at = e < .5 ? s.a : s.b; }
      // meetings + reject
      const meet = [0, 0, 0, 0, 0, 0];
      let waits = 0, rej = 0, arc = 0, ghosts = [];
      steps.forEach(x => {
        if (x.k === "w") {
          const add = MEET[waits++] || 0;
          const shown = Math.floor(add * seg(t, x.t0 + .1, x.t1 - .1) + (t >= x.t1 ? .001 : 0));
          meet[x.a] += Math.min(add, t >= x.t1 ? add : shown);
          if (x.rej && t > x.t0 + .3) rej = easeO(seg(t, x.t0 + .3, x.t0 + .5));
          if (t >= x.t1) ghosts.push({ i: x.a, f: x.f1 });
        }
        if (x.k === "b") arc = t >= x.t0 ? seg(t, x.t0, x.t1) : 0;
      });
      const last = {}; ghosts.forEach(g => (last[g.i] = g)); ghosts = Object.values(last).filter(g => g.i !== at);
      const clockP = s.k === "w" ? k : 0;
      const prog = seg(t, OLD_START, OLD_END);
      return { pos, at, fid, hand, meet, rej, arc, ghosts, clockP, prog, wait: s.k === "w" && t >= OLD_START };
    }
    function bezPts() {
      const a = L.st[5], b = L.st[3];
      if (!mobile) { const up = L.ch * 1.9; return [a, [a[0], a[1] - up], [b[0], b[1] - up], b]; }
      const out = L.cw * .5 + 34; return [a, [a[0] - out * 1.6, a[1]], [b[0] - out * 1.6, b[1]], b];
    }
    function bounceAt(e) {
      const [p0, p1, p2, p3] = bezPts(), u = 1 - e;
      return [0, 1].map(i => u * u * u * p0[i] + 3 * u * u * e * p1[i] + 3 * u * e * e * p2[i] + e * e * e * p3[i]);
    }

    function card(x, y, name, meet, active, op, extraTop = "") {
      const { cw, ch } = L;
      let o = `<g opacity="${op.toFixed(3)}"><rect x="${f1(x - cw / 2)}" y="${f1(y - ch / 2)}" width="${f1(cw)}" height="${f1(ch)}" rx="${mobile ? 11 : 14}" fill="#fff" stroke="${INK}" stroke-width="${active ? 2 : 1.25}"/>`;
      const pw = [.34, .24, .38, .2, .3];
      const maxP = mobile ? 2 : 4;
      for (let k = 0; k < Math.min(meet, maxP); k++)
        o += `<rect x="${f1(x - cw / 2 + 12)}" y="${f1(y - ch / 2 + 11 + k * (mobile ? 9 : 10))}" width="${f1(cw * pw[k % 5])}" height="5" rx="2.5" fill="${active && k === Math.min(meet, maxP) - 1 ? INK : LG}"/>`;
      if (meet && !mobile) o += text(x + cw / 2 - 11, y - ch / 2 + 18, `${meet} mtg`, "pf-tiny", 'text-anchor="end"');
      if (name) o += mobile ? text(x + cw / 2 + 18, y + 4, name, active ? "pf-lbl pf-on" : "pf-lbl")
                            : text(x, y + ch / 2 + 26, name, active ? "pf-lbl pf-on" : "pf-lbl", 'text-anchor="middle"');
      return o + extraTop + "</g>";
    }

    function caption(phase, stats, accent, op) {
      const x = L.left, y = L.capY, big = mobile ? 34 : 44;
      let o = `<g opacity="${op.toFixed(3)}"><rect x="${x}" y="${y - 8}" width="7" height="7" fill="${accent ? LIME : INK}" stroke="${INK}" stroke-width="${accent ? 1 : 0}"/>`;
      o += text(x + 16, y, phase, "pf-lbl");
      let cx = x;
      stats.forEach(([v, l]) => {
        o += text(cx, y + 18 + big, v, "pf-num", `style="font-size:${big}px"`);
        o += text(cx, y + 40 + big, l, "pf-sm");
        cx += Math.max(mobile ? 58 : 76, l.length * 7 + 26);
      });
      return o + "</g>";
    }
    function meter(pct, op) {
      const { meterX: x, meterY: y, meterW: w } = L;
      const col = pct >= 99 ? LIME : pct > 55 ? LIME2 : "#b9c0c8";
      return `<g opacity="${op.toFixed(3)}">${text(x, y, "Original idea intact", "pf-lbl")}${text(x + w, y, Math.round(pct) + "%", "pf-lbl pf-on", 'text-anchor="end"')}` +
        `<rect x="${x}" y="${y + 12}" width="${w}" height="6" rx="3" fill="${LG}"/><rect x="${x}" y="${y + 12}" width="${f1(w * pct / 100)}" height="6" rx="3" fill="${col}"/></g>`;
    }
    function ruler(weeks, accent, op) {
      if (mobile) return "";
      const x0 = L.left, x1 = L.right, y = L.rulerY, n = 12;
      let o = `<g opacity="${op.toFixed(3)}"><line x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke="${LG}" stroke-width="6" stroke-linecap="round"/>`;
      if (weeks > 0) o += `<line x1="${x0}" y1="${y}" x2="${f1(x0 + (x1 - x0) * weeks / n)}" y2="${y}" stroke="${accent ? LIME : INK}" stroke-width="6" stroke-linecap="round"/>`;
      for (let i = 0; i <= n; i++) {
        const xx = x0 + (x1 - x0) * i / n;
        o += `<line x1="${f1(xx)}" y1="${y + 12}" x2="${f1(xx)}" y2="${y + 18}" stroke="#c3c9d0"/>`;
        if (i) o += text(xx - (x1 - x0) / n / 2, y + 34, "W" + i, weeks >= i - .5 ? "pf-tiny pf-on" : "pf-tiny", 'text-anchor="middle"');
      }
      return o + "</g>";
    }

    function frame(t) {
      const fadeAll = 1 - seg(t, T - .45, T);
      const fadeIn = easeO(seg(t, 0, .45));
      let o = "";
      const s = oldState(t);
      const cK = easeIO(seg(t, C0, C1));          // collapse progress
      const oldOp = fadeIn * (1 - seg(t, C0 + .6, C1));

      // ---------- OLD MODEL ----------
      if (t < C1 + .05) {
        // track
        const a = L.st[0], b = L.st[5];
        const tr = mobile ? `M${a[0]} ${a[1] - L.ch} L${b[0]} ${b[1] + L.ch}` : `M${L.left} ${a[1]} L${L.right} ${b[1]}`;
        o += `<path d="${tr}" stroke="${INK}" stroke-width="1.2" stroke-dasharray="4 7" fill="none" opacity="${(oldOp * (1 - cK)).toFixed(3)}"/>`;
        // bounce arc
        if (s.arc > 0) {
          const [p0, p1, p2, p3] = bezPts(), d = `M${p0[0]} ${p0[1]} C${p1[0]} ${p1[1]} ${p2[0]} ${p2[1]} ${p3[0]} ${p3[1]}`;
          const len = mobile ? 260 : 420, vis = clamp(s.arc * 1.15), bEnd = steps.find(x => x.k === "b").t1;
          o += `<g opacity="${(oldOp * (1 - cK) * (1 - seg(t, bEnd + .6, bEnd + 1.4))).toFixed(3)}"><path d="${d}" fill="none" stroke="${RED}" stroke-width="1.5" stroke-dasharray="${f1(len * vis)} ${len}"/>`;
          if (!mobile) o += text((p0[0] + p3[0]) / 2, p1[1] + L.ch * .22, "Back to design · +3 weeks", "pf-lbl pf-red", `text-anchor="middle" opacity="${seg(s.arc, .3, .6)}"`);
          o += "</g>";
        }
        // cards
        NAMES.forEach((n, i) => {
          const [x, y] = L.st[i];
          const cx = lerp(x, L.sen[0], cK), cy = lerp(y, L.sen[1], cK);
          let stamp = "";
          if (i === 5 && s.rej > 0) {
            const sc = lerp(1.6, 1, s.rej), w = mobile ? 72 : 84, h = mobile ? 26 : 30;
            stamp = `<g transform="translate(${f1(cx)} ${f1(cy)}) rotate(-12) scale(${sc.toFixed(3)})" opacity="${s.rej.toFixed(3)}"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="5" fill="#fff" stroke="${RED}" stroke-width="2"/>${text(0, 4, "Rejected", "pf-lbl pf-red pf-b", 'text-anchor="middle"')}</g>`;
          }
          o += card(cx, cy, cK > .05 ? "" : n, cK > .05 ? 0 : s.meet[i], i === s.at && t < C0, oldOp * (cK > 0 ? lerp(1, .35 + i * .1, cK) : 1), stamp);
        });
        // ghosts left behind
        s.ghosts.forEach(g => {
          const [x, y] = L.st[g.i];
          o += `<path d="${blob(x, y + (mobile ? 0 : 6), mobile ? 11 : 14, (1 - g.f) * .35, g.i + 1, 0)}" fill="none" stroke="#c3c9d0" stroke-width="1.2" opacity="${(oldOp * (1 - cK) * .9).toFixed(3)}"/>`;
        });
        // the idea
        const ideaOp = oldOp * (1 - seg(t, C0, C0 + .5));
        if (ideaOp > 0) {
          const [x, y] = s.pos, yy = y + (mobile ? 0 : 6), r = mobile ? 13 : 17;
          if (s.wait && s.clockP > 0) {
            const R = r + 11, a = s.clockP * Math.PI * 2, ex = x + R * Math.sin(a), ey = yy - R * Math.cos(a);
            o += `<circle cx="${f1(x)}" cy="${f1(yy)}" r="${R}" fill="none" stroke="${LG}" stroke-width="3" opacity="${ideaOp}"/>` +
                 `<path d="M${f1(x)} ${f1(yy - R)} A${R} ${R} 0 ${s.clockP > .5 ? 1 : 0} 1 ${f1(ex)} ${f1(ey)}" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round" opacity="${ideaOp}"/>`;
          }
          const amp = (1 - s.fid) * .42;
          o += `<path d="${blob(x, yy, r, amp, 7, t)}" fill="${mix(LIME, LG, (1 - s.fid) / .7)}" stroke="${INK}" stroke-width="1.5" stroke-linejoin="round" opacity="${ideaOp.toFixed(3)}"/>`;
        }
      }

      // ---------- NORVEL MODEL ----------
      const n = t - N0;
      if (t > C1 - .2) {
        const cardK = easeO(seg(n, -.1, .4));
        const [sx, sy] = L.sen, sw = L.senW * lerp(.85, 1, cardK), sh = L.senH * lerp(.85, 1, cardK);
        const rayK = L.rays.map((_, j) => easeO(seg(n, .8 + j * .025, 1.6 + j * .025)));
        const pickK = easeO(seg(n, 2.4, 2.8)), fadeK = seg(n, 2.4, 2.9);
        const shipK = easeIO(seg(n, 3.0, 3.6)), liveK = easeO(seg(n, 2.9, 3.35));
        // rays + variants
        L.rays.forEach(([ex, ey], j) => {
          const k = rayK[j]; if (k <= 0) return;
          const [fx, fy] = L.rayFrom, sel = j === L.pick;
          const col = sel ? LIME2 : mix(LIME2, LG, fadeK);
          o += `<line x1="${f1(fx)}" y1="${f1(fy)}" x2="${f1(lerp(fx, ex, k))}" y2="${f1(lerp(fy, ey, k))}" stroke="${col}" stroke-width="1.2" stroke-dasharray="3 5"/>`;
          const pop = easeO(seg(k, .85, 1));
          if (pop > 0) {
            const r = (mobile ? 11 : 13) * pop * (sel ? lerp(1, 1.25, pickK) : 1);
            const fill = sel ? mix("#ffffff", LIME, pickK) : "#fff", st = sel ? INK : mix(INK, LG, fadeK);
            o += `<path d="${blob(ex, ey, r, sel ? .16 * (1 - pickK) : .18, j + 3, 0)}" fill="${fill}" stroke="${st}" stroke-width="1.4" stroke-linejoin="round"/>`;
            if (sel && pickK > 0) {
              const R = mobile ? 24 : 28, c = 2 * Math.PI * R;
              o += `<circle cx="${f1(ex)}" cy="${f1(ey)}" r="${R}" fill="none" stroke="${INK}" stroke-width="1.5" stroke-dasharray="${f1(c * pickK)} ${f1(c)}" transform="rotate(-90 ${f1(ex)} ${f1(ey)})"/>`;
              const lx = mobile ? ex + R + 10 : ex, ly = mobile ? ey + 4 : ey - R - 12;
              o += text(lx, ly, "Senior picks", "pf-lbl pf-on", `${mobile ? "" : 'text-anchor="middle"'} opacity="${seg(n, 2.6, 2.9)}"`);
            }
          }
        });
        // ship line + live frame
        const [px, py] = L.rays[L.pick], [lx, ly] = L.live, lw = L.liveW, lh = L.liveH;
        const tx = mobile ? lx : lx - lw / 2, ty = mobile ? ly - lh / 2 : ly;
        if (liveK > 0) {
          const k = liveK, w = lw * lerp(.9, 1, k), h = lh * lerp(.9, 1, k), x = lx - w / 2, y = ly - h / 2;
          const barK = i => easeO(seg(n, 3.55 + i * .18, 3.9 + i * .18));
          o += `<g opacity="${k.toFixed(3)}"><rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" rx="14" fill="#fff" stroke="${INK}" stroke-width="1.6"/>` +
               `<line x1="${f1(x)}" y1="${f1(y + 24)}" x2="${f1(x + w)}" y2="${f1(y + 24)}" stroke="${INK}" stroke-width="1.2"/>` +
               [0, 1, 2].map(i => `<circle cx="${f1(x + 15 + i * 11)}" cy="${f1(y + 12)}" r="3" fill="none" stroke="${INK}"/>`).join("") +
               `<rect x="${f1(x + 18)}" y="${f1(y + 40)}" width="${f1(w * .5 * barK(0))}" height="12" rx="4" fill="${LIME}"/>` +
               `<rect x="${f1(x + 18)}" y="${f1(y + 62)}" width="${f1((w - 36) * .8 * barK(1))}" height="6" rx="3" fill="${LG}"/>` +
               `<rect x="${f1(x + 18)}" y="${f1(y + 74)}" width="${f1((w - 36) * .62 * barK(1))}" height="6" rx="3" fill="${LG}"/>` +
               `<rect x="${f1(x + 18)}" y="${f1(y + 90)}" width="${f1(w - 36)}" height="${f1(Math.max(0, h - 108))}" rx="8" fill="${LG}" opacity="${barK(2).toFixed(3)}"/></g>`;
          o += text(mobile ? lx : lx, ly + lh / 2 + 26, "Live", "pf-lbl pf-on", `text-anchor="middle" opacity="${k}"`);
        }
        if (shipK > 0) {
          const fx = mobile ? px : px + (mobile ? 0 : 28), fy = mobile ? py + 24 : py;
          o += `<line x1="${f1(fx)}" y1="${f1(fy)}" x2="${f1(lerp(fx, tx, shipK))}" y2="${f1(lerp(fy, ty, shipK))}" stroke="${INK}" stroke-width="1.5"/>`;
          const bx = lerp(px, tx, shipK), by = lerp(py, ty, shipK), r = (mobile ? 14 : 16) * (1 - seg(n, 3.45, 3.6));
          if (r > .5) o += `<path d="${blob(bx, by, r, 0, 1, 0)}" fill="${LIME}" stroke="${INK}" stroke-width="1.4"/>`;
        }
        // check badge + pulse
        const chk = easeO(seg(n, 4.2, 4.5));
        if (chk > 0) {
          const cx = lx + lw / 2, cy = ly - lh / 2, r = 17 * chk;
          const pk = ((n - 4.5) % 1.6) / 1.6;
          if (n > 4.5) o += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(17 + pk * 22)}" fill="none" stroke="${LIME2}" stroke-width="1.4" opacity="${(1 - pk).toFixed(3)}"/>`;
          o += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="${LIME}" stroke="${INK}" stroke-width="1.5"/>`;
          if (chk > .6) o += `<path d="M${f1(cx - 7)} ${f1(cy)} l5 5 l9 -10" fill="none" stroke="${INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`;
        }
        // senior card (drawn last so rays come out of it)
        const scOp = seg(t, C1 - .2, C1 + .1);
        o += `<g opacity="${scOp.toFixed(3)}"><rect x="${f1(sx - sw / 2)}" y="${f1(sy - sh / 2)}" width="${f1(sw)}" height="${f1(sh)}" rx="16" fill="${INK}"/>`;
        o += text(sx - sw / 2 + 14, sy - sh / 2 + 22, "AI × senior", "pf-tiny pf-mute");
        const ideaK = easeO(seg(n, .2, .6)), breath = 1 + Math.sin(t * 3) * .04;
        o += `<path d="${blob(sx, sy + 4, (mobile ? 15 : 18) * ideaK * breath, 0, 1, 0)}" fill="${LIME}"/>`;
        o += "</g>" + (mobile ? text(sx + sw / 2 + 14, sy + 4, "Senior team", "pf-lbl pf-on", `opacity="${scOp}"`) : text(sx, sy + sh / 2 + 26, "Senior team", "pf-lbl pf-on", `text-anchor="middle" opacity="${scOp}"`));
      }

      // ---------- HUD ----------
      const isN = t >= C0 + .6;
      const capOp = fadeIn * (isN ? seg(t, C0 + .6, C0 + 1) : 1 - seg(t, C0 + .2, C0 + .6));
      if (!isN) {
        const weeks = s.prog > 0 ? 1 + Math.floor(s.prog * 11.99) : 1;
        const meets = s.meet.reduce((a, b) => a + b, 0);
        o += caption("The old agency model", [[weeks, weeks === 1 ? "week" : "weeks"], [s.hand, "hand-offs"], [meets, "meetings"]], false, capOp);
      } else {
        const dirs = Math.round(10 * easeO(seg(n, .8, 1.7)));
        const wk = n > 3.6 ? 2 : 1;
        o += caption("The Norvel model", [[wk, wk === 1 ? "week" : "weeks"], [1, "senior team"], [dirs + "×", "directions explored"]], true, capOp);
      }
      const pct = !isN ? s.fid * 100 * (1 - cK) + 100 * cK * 0 : 100;
      const meterOp = fadeIn * (isN ? seg(t, C1, C1 + .4) : 1 - seg(t, C0 + .2, C0 + .6));
      o += meter(isN ? 100 : s.fid * 100, meterOp);
      if (!isN) o += ruler(s.prog > 0 ? 1 + s.prog * 11 : .3, false, fadeIn * (1 - seg(t, C0 + .2, C0 + .6)));
      else { const wk = lerp(0, 1, easeIO(seg(n, 0, 1.6))) + easeIO(seg(n, 3, 3.6)); o += ruler(wk, true, seg(t, C1, C1 + .4)); }

      svg.innerHTML = `<g opacity="${fadeAll.toFixed(3)}">${o}</g>`;
    }

    measure();
    const fixed = parseFloat(new URLSearchParams(location.search).get("procT"));
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!isNaN(fixed)) { frame(fixed); return; }
    if (reduce) { frame(N0 + 5); return; }
    let t0 = performance.now(), running = false, paused = 0;
    const loop = now => { if (!running) return; frame(((now - t0) / 1000) % T); requestAnimationFrame(loop); };
    const start = () => { if (!running) { running = true; t0 = performance.now() - paused * 1000; requestAnimationFrame(loop); } };
    const stop = () => { if (running) { running = false; paused = ((performance.now() - t0) / 1000) % T; } };
    new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop()), { threshold: .15 }).observe(root);
    let rt, lastW = W;
    window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (stage.clientWidth !== lastW) { lastW = stage.clientWidth; measure(); } }, 200); });
  }

  document.querySelectorAll(".proc").forEach(init);
})();
