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

  /* Hero glow follows the pointer */
  const hero = $(".hero-head"), glow = $(".hero-glow");
  if (hero && glow && !reduce && window.matchMedia("(pointer: fine)").matches) {
    hero.addEventListener("pointermove", e => {
      const r = hero.getBoundingClientRect();
      glow.style.left = `${e.clientX - r.left}px`;
      glow.style.top = `${e.clientY - r.top}px`;
    });
    hero.addEventListener("pointerleave", () => { glow.style.left = "50%"; glow.style.top = "55%"; });
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
      return Math.max(1, Math.round(track.getBoundingClientRect().width / w));
    };
    const go = to => {
      const max = Math.max(0, items.length - perView());
      i = Math.min(max, Math.max(0, to));
      const gap = parseFloat(getComputedStyle(track).gap) || 0;
      const step = items[0].getBoundingClientRect().width + gap;
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

  /* Footer year */
  $$("[data-year]").forEach(el => (el.textContent = new Date().getFullYear()));
})();
