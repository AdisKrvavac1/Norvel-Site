"""All site copy lives here. Edit text, then run: python3 build/build.py"""

SITE = {
    "name": "Norvel",
    "url": "https://norvelstudio.com",
    "email": "hello@norvelstudio.com",
    "tagline": "Design & technology studio",
    "description": "Norvel is an independent design & technology studio. Senior design judgment, AI-accelerated delivery — brand identity, web design and Webflow development.",
    "socials": [("LinkedIn", "https://www.linkedin.com/"), ("Instagram", "https://www.instagram.com/"), ("X", "https://x.com/")],
}

HERO = {
    "eyebrow": "AI-native design studio",
    "line1": "Senior design.",
    "line2": "Shipped at AI speed.",
    "sub": "We design and build brands and websites faster by combining senior creative judgment with AI-accelerated execution.",
    "intro": "Norvel is an independent design & technology studio. One senior team, from first sketch to a live Webflow site — no hand-offs, no bloat.",
}

PROBLEM = {
    "eyebrow": "The problem",
    "title_a": "The old agency model is",
    "strike": "broken",
    "title_b": "done.",
    "lead": "Traditional agencies are slow, expensive and buried in process. That model doesn’t survive in a world where AI exists.",
    "rows": [
        ("Months of meetings before a single pixel", "3", "Service pillars, one team"),
        ("Layers of account managers between you and the work", "5+", "Years of senior experience"),
        ("Strategy, design and build split across vendors", "1", "Point of contact, end to end"),
    ],
}

MODEL = {
    "eyebrow": "The Norvel model",
    "title": "AI-native by design",
    "lead": "Most studios bolt AI onto old workflows and call it innovation. We rebuilt the whole process around it — AI is the operating system, not an add-on.",
    "principles": [
        ("AI is the foundation, not a feature",
         "Every workflow, every decision and every layout is shaped by AI from the start — not patched on after the fact."),
        ("Explore 10× the creative space",
         "We prototype, test and iterate on more directions in a day than a traditional agency covers in a sprint."),
        ("Senior designers stay in the loop",
         "AI generates. People direct, review and own. The judgment that matters is never outsourced to a model."),
        ("Built for what’s next",
         "We don’t just use today’s tools — we keep evolving the process as the technology moves. The studio gets better every week."),
    ],
}

SERVICES = {
    "eyebrow": "Services",
    "title": "What we do best",
    "items": [
        ("Brand & Identity",
         "Identities that hold up everywhere — from a favicon to a billboard — built as systems, not one-off logos.",
         ["Logo & mark systems", "Visual language & guidelines", "Type, colour & motion principles", "Brand assets & templates"]),
        ("Web Design",
         "Websites designed around what your visitors need to understand, feel and do — then prototyped before a line of code.",
         ["UX structure & information architecture", "Responsive UI design", "Interactive prototypes", "Design systems for the web"]),
        ("Webflow Development",
         "Production-grade Webflow builds: fast, accessible, CMS-driven and easy for your team to run after launch.",
         ["Webflow & custom code", "CMS architecture", "GSAP & scroll interactions", "SEO, performance & analytics"]),
    ],
}

PERSONAS = {
    "eyebrow": "Pick the one that’s you",
    "title": "Who we work with",
    "lead": "Same playbook, three different shapes of client. Find yourself below.",
    "items": [
        ("I’m a marketing team", "The design & web team your marketing team doesn’t have.",
         "Landing pages, campaigns and site updates shipped in days, not quarters — without waiting on a dev backlog."),
        ("I’m a founder", "From idea to a brand and site that look funded.",
         "Positioning, identity and a launch-ready Webflow site, built by one senior team that moves at startup speed."),
        ("I’m a growing company", "A fractional creative team, on call.",
         "Rebrands, design systems and ongoing web work with a dedicated partner who already knows your brand."),
    ],
}

FAQS = {
    "eyebrow": "FAQ",
    "title": "Questions we often get",
    "aside": "Can’t find what you’re looking for? Write to us — we reply within one business day.",
    "items": [
        ("How fast can you start?",
         "Usually within one to two weeks. Smaller projects like a landing page can often start the same week."),
        ("What does “AI-native” mean for my project?",
         "AI speeds up research, exploration and production, so we can show you more directions earlier. Every decision, review and final output is still made by a senior designer."),
        ("Which tools do you work with?",
         "Figma for design, Adobe Creative Cloud for brand and illustration, Webflow for development, and GSAP for motion — plus AI tools across the whole process."),
        ("Do you only build in Webflow?",
         "Webflow is our default because it gives your team full control after launch. For special cases we also deliver custom-coded static sites."),
        ("Can you handle both branding and the website?",
         "Yes — that’s the point. Brand, web design and development are three equal pillars, handled by one team so nothing gets lost in hand-offs."),
        ("Where are you based?",
         "We’re a remote-first studio working with clients in the US and Europe, across time zones."),
    ],
}

CTA = {
    "title": "Let’s build what’s next",
    "copy": "Whether you need a new identity, a full website or a Webflow team on call — tell us what you’re working on and we’ll come back with a plan.",
    "button": "Start a project",
}

FOOTER = {
    "title_a": "Available for new projects",
    "title_b": "& partnerships",
    "copy": "Reach out with your idea — let’s build something remarkable.",
}

PROJECTS_PAGE = {
    "title": "Selected work",
    "lead": "Concept studies and studio work — a look at how we think about brands, interfaces and the systems behind them.",
}

# NOTE: these are studio concept studies (placeholders). Replace with real case studies.
PROJECTS = [
    {
        "slug": "halden",
        "name": "Halden",
        "summary": "Brand identity for an architecture practice",
        "date": "Concept · 2026",
        "card": "A quiet, structural identity for a studio that designs in concrete and light — a system of marks, grids and restrained type.",
        "intro": "Halden is a concept identity for a small architecture practice. The brief: a brand that feels as considered as the buildings — precise, calm and built on a clear structural logic.",
        "client": "Concept study",
        "role": "Brand strategy, identity design",
        "tools": "Figma, Illustrator, AI-assisted exploration",
        "cover": "identity",
        "gallery": ["pattern", "poster", "system"],
        "wide": "editorial",
        "approach": "We explored more than forty mark directions in the first two days, then narrowed down to a mark built from the same diagonal geometry as the practice’s floor plans.",
        "steps": [("Discover", "Define what the practice stands for and how it should feel."),
                  ("Explore", "Generate and test dozens of directions across marks, grids and type."),
                  ("Refine", "Turn the chosen direction into a flexible, documented system.")],
        "result": "A compact identity system — mark, type, colour and layout rules — that scales from a business card to site hoardings.",
    },
    {
        "slug": "kinetic",
        "name": "Kinetic",
        "summary": "Webflow site for a SaaS launch",
        "date": "Concept · 2026",
        "card": "A launch site that explains a complex product in one scroll — built in Webflow with a CMS the marketing team runs on its own.",
        "intro": "Kinetic is a concept launch site for a B2B SaaS product. The goal was a site that tells the product story in one scroll and that the marketing team can update without a developer.",
        "client": "Concept study",
        "role": "Web design, Webflow development",
        "tools": "Figma, Webflow, GSAP",
        "cover": "ui",
        "gallery": ["mobile", "system", "orbit"],
        "wide": "ui",
        "approach": "We started from the questions a buyer asks in their first minute on the page and designed every section to answer exactly one of them.",
        "steps": [("Map", "Structure the story around the buyer’s first questions."),
                  ("Prototype", "Validate the flow with an interactive prototype before building."),
                  ("Build", "Ship a fast, CMS-driven Webflow site with scroll-based motion.")],
        "result": "A lean, fast launch site with reusable components and a CMS for releases and customer stories.",
    },
    {
        "slug": "ferro",
        "name": "Ferro",
        "summary": "Design system for a fintech dashboard",
        "date": "Concept · 2026",
        "card": "Tokens, components and patterns for a data-heavy dashboard — designed so product teams can ship new screens without starting from scratch.",
        "intro": "Ferro is a concept design system for a fintech dashboard. Dense data, many states, and several teams designing in parallel — the system had to keep all of it consistent.",
        "client": "Concept study",
        "role": "Design system, UI design",
        "tools": "Figma variables, tokens, documentation",
        "cover": "system",
        "gallery": ["ui", "mobile", "pattern"],
        "wide": "system",
        "approach": "We built the system bottom-up: tokens first, then primitives, then the handful of patterns that cover most real screens.",
        "steps": [("Audit", "Inventory existing screens and find the repeated patterns."),
                  ("Define", "Set tokens for colour, type, spacing and motion."),
                  ("Document", "Ship components with usage guidelines and examples.")],
        "result": "A token-based system with documented components that cuts the time to design a new screen dramatically.",
    },
    {
        "slug": "atlas",
        "name": "Atlas",
        "summary": "Editorial site for a travel journal",
        "date": "Concept · 2026",
        "card": "An editorial reading experience with generous type, a flexible story template and motion that never gets in the way of the words.",
        "intro": "Atlas is a concept editorial site for an independent travel journal. Long reads, big imagery and a team of writers who publish every week.",
        "client": "Concept study",
        "role": "Art direction, web design",
        "tools": "Figma, Webflow CMS",
        "cover": "editorial",
        "gallery": ["poster", "orbit", "identity"],
        "wide": "pattern",
        "approach": "Typography led every decision — we designed the reading experience first and let the layout grow around it.",
        "steps": [("Read", "Study how the audience reads: on the go, on mobile, in long sessions."),
                  ("Compose", "Design a story template with flexible image and quote blocks."),
                  ("Publish", "Connect it to a CMS so editors can publish without help.")],
        "result": "A calm, fast editorial site where every story gets a bespoke feel from one flexible template.",
    },
]
