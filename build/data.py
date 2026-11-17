"""All site copy lives here. Edit text, then run: python3 build/build.py"""

SITE = {
    "name": "Norvel",
    "url": "https://norvelstudio.com",
    "email": "hello@norvelstudio.com",
    "tagline": "Design & technology studio",
    "description": "Norvel is an AI-native design studio for web design, Webflow development and brand identity — senior design judgment, shipped at AI speed for US and European teams.",
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
    "title_a": "Open for new projects",
    "title_b": "& partnerships",
    "copy": "Reach out with your idea — let’s build something remarkable.",
}

PROJECTS_PAGE = {
    "title": "Selected work",
    "lead": "Websites, Webflow builds and campaigns for venture firms, AI products and consumer brands.",
}

# Images live in public/assets/work/<slug>/01.jpg, 02.jpg ... (01 = cover).
# A walkthrough.mp4 in the same folder is shown automatically.
# "fallback" is placeholder artwork used only while a project has no images yet.
PROJECTS = [
    {
        "slug": "hp-workforce-experience",
        "name": "HP Workforce Experience",
        "summary": "Complete website design",
        "category": "Web Design",
        "url": "https://workforceexperience.hp.com/",
        "card": "A complete website for HP’s AI-driven digital employee experience platform — from homepage to platform, offerings, partners and resources.",
        "intro": "HP Workforce Experience Platform (WXP) helps IT teams prevent device and software issues, manage their fleets and improve employee experience across every OS and app. The brief: one website that explains a complex enterprise platform and serves IT leaders, partners and buyers alike.",
        "client": "HP",
        "role": "Website design — full site",
        "tools": "Figma",
        "approach": "We designed the complete site as a system: a light, airy hero with isometric product illustrations, real dashboard UI to show the product rather than describe it, and a strong light/dark section rhythm that keeps long enterprise pages easy to scan.",
        "steps": [("Structure", "Map platform, offerings, partners and resources into a clear, scalable architecture."),
                  ("Show the product", "Use real interface components and illustrations to make an abstract platform tangible."),
                  ("Systemise", "Build page templates and components that cover every section of the site.")],
        "result": "A cohesive enterprise website across platform, offerings, partners and resources — clear for IT teams, credible for buyers and built to grow with the product.",
        "fallback": "ui",
    },
    {
        "slug": "gyde-health",
        "name": "Gyde",
        "summary": "Website design & Webflow build",
        "category": "Web Design · Webflow",
        "url": "https://www.gydehealth.ai/",
        "card": "Brand-forward website for the first AI-native brokerage for insurance agencies — designed and built in Webflow.",
        "intro": "Gyde partners with Medicare and Employee Benefits agencies, bringing AI tools, back-office support and growth capital to ambitious agency owners. The website had to introduce a brand-new category and explain two products — the Gia assistant and GydeOS — to a very specific audience.",
        "client": "Gyde Health",
        "role": "Website design, Webflow development",
        "tools": "Figma, Webflow",
        "approach": "A confident red brand, an elegant serif for headlines and a large brand mark set the tone. Product sections show Gia as real conversations and GydeOS as tabbed interface views, so agency owners can see exactly how the product works.",
        "steps": [("Position", "Lead with a clear belief and the problem agencies face."),
                  ("Demonstrate", "Turn product features into conversations and interface previews."),
                  ("Build", "Develop the site in Webflow with scroll-based motion and a resources section.")],
        "result": "A launch-ready Webflow site that explains a new category in a single scroll — from belief and problem to product, impact, backers and partnership.",
        "fallback": "ui",
    },
    {
        "slug": "playground",
        "name": "Playground",
        "summary": "Website design & Webflow build",
        "category": "Web Design · Webflow",
        "url": "https://playground.com/",
        "card": "Marketing site for the AI design studio for everyone — playful, colourful and built in Webflow.",
        "intro": "Playground is an AI design tool used by millions of creators to make logos, stickers, T-shirts, posters and social graphics. The website needed to feel as fun as the work people make with it, while staying simple enough for first-time designers.",
        "client": "Playground",
        "role": "Website design, Webflow development",
        "tools": "Figma, Webflow",
        "approach": "A calm, minimal canvas lets the user-made artwork do the talking: stickers and merch float around a clean hero, gradient type adds energy, and interactive sections show templates and the prompt-to-design flow in action.",
        "steps": [("Canvas", "Keep the layout quiet so the colourful artwork stands out."),
                  ("Play", "Add floating artwork, gradient type and interactive carousels."),
                  ("Build", "Ship it in Webflow with smooth, performant interactions.")],
        "result": "A light, playful marketing site that makes AI design feel approachable — and shows what’s possible before anyone signs up.",
        "fallback": "poster",
    },
    {
        "slug": "lightspeed",
        "name": "Lightspeed",
        "summary": "Website design",
        "category": "Web Design",
        "url": "https://lsvp.com/",
        "card": "Website design for a multi-stage venture firm built around one idea: possibility grows the deeper you go.",
        "intro": "Lightspeed Venture Partners backs founders from seed to late stage and has been an early partner to many of today’s leading AI companies. The site had to express the firm’s philosophy of depth while giving founders, LPs and press a clear way into companies, team and stories.",
        "client": "Lightspeed Venture Partners",
        "role": "Website design",
        "tools": "Figma",
        "approach": "Soft gradients, layered imagery and oversized display type create a sense of depth as you scroll, while portfolio logos, founder spotlights and stories are organised into calm, scannable grids.",
        "steps": [("Narrative", "Translate the “deeper you go” philosophy into the scroll experience."),
                  ("Content", "Give portfolio, founders and stories a clear structure."),
                  ("Scale", "Design templates that hold a constant stream of new stories.")],
        "result": "A venture website that feels editorial rather than corporate — with room for portfolio, founder spotlights and an ever-growing newsfeed.",
        "fallback": "identity",
    },
    {
        "slug": "a16z",
        "name": "a16z",
        "summary": "Design collaboration",
        "category": "Design Collaboration",
        "url": "https://a16z.com/",
        "card": "Design collaboration with Andreessen Horowitz on a cinematic, video-led web experience.",
        "intro": "Andreessen Horowitz (a16z) is one of the most recognised venture firms in technology. We collaborated with the a16z team on design for its web presence — a bold, cinematic experience built around the message “It’s time to build”.",
        "client": "Andreessen Horowitz",
        "role": "Design collaboration",
        "tools": "Figma",
        "approach": "Full-screen video storytelling carries the page, with restrained interface elements and gold display type that let the footage set the mood.",
        "steps": [("Collaborate", "Work alongside the in-house team on direction and details."),
                  ("Frame", "Design a quiet interface layer around full-screen video."),
                  ("Refine", "Polish typography, motion and responsive behaviour.")],
        "result": "A cinematic, unmistakably a16z experience that puts the stories of builders front and centre.",
        "fallback": "orbit",
    },
    {
        "slug": "gtm10-awards",
        "name": "GTM10 Awards",
        "summary": "Billboards for the Nasdaq Tower, Times Square",
        "category": "Out-of-home · Billboards",
        "url": "",
        "card": "Billboard designs for the GTM10 Awards winners, shown on the Nasdaq Tower in Times Square.",
        "intro": "The GTM10 Awards, powered by Cello and Lightspeed, recognise the top go-to-market operators in software across marketing, sales, growth, customer success and partnerships. Winners are celebrated on the Nasdaq Tower billboard in Times Square.",
        "client": "GTM10 Awards (Cello & Lightspeed)",
        "role": "Billboard design",
        "tools": "Figma, Adobe Creative Cloud",
        "approach": "Designing for one of the most famous screens in the world means designing for distance and speed: bold type, high contrast and a layout that reads in seconds from street level.",
        "steps": [("Format", "Design to the Nasdaq Tower’s tall digital canvas."),
                  ("Legibility", "Keep names and titles readable from the street."),
                  ("Series", "Create a flexible template for every winner.")],
        "result": "A series of billboards that put GTM leaders on the Nasdaq Tower in Times Square.",
        "fallback": "pending",
    },
    {
        "slug": "lagunitas",
        "name": "Lagunitas",
        "summary": "Website design",
        "category": "Web Design",
        "url": "https://www.lagunitas.com/en-us/",
        "card": "A loud, irreverent website for the Petaluma brewery — beers, taproom and merch with plenty of attitude.",
        "intro": "Lagunitas Brewing Company is a Petaluma, California brewery known for its IPAs and its irreverent voice. The website brings together the beer line-up, the taproom, events and merch.",
        "client": "Lagunitas Brewing Company",
        "role": "Website design",
        "tools": "Figma",
        "approach": "Bold condensed type, torn-paper textures, brushed red accents and product-forward can photography give the site the same attitude as the brand.",
        "steps": [("Voice", "Let the brand’s humour lead the layout and copy."),
                  ("Product", "Make the cans the heroes of every section."),
                  ("Visit", "Give the taproom and events a clear path.")],
        "result": "A website that sounds and looks like Lagunitas — loud, fun and built around the beer.",
        "fallback": "poster",
    },
    {
        "slug": "hello-cake",
        "name": "Hello Cake",
        "summary": "E-commerce design",
        "category": "E-commerce",
        "url": "https://hellocake.com/",
        "card": "A bright, stigma-free online store for a fast-growing sexual wellness brand.",
        "intro": "Hello Cake is a sexual wellness brand on a mission to make the category easy, open and fun. The online store needed to feel friendly and approachable while making it simple to browse products and buy.",
        "client": "Hello Cake",
        "role": "E-commerce design",
        "tools": "Figma",
        "approach": "Bright product photography, a bold colour palette and clean product cards keep the experience playful and shoppable, with reviews and guarantees building trust along the way.",
        "steps": [("Tone", "Strike a friendly, stigma-free tone throughout."),
                  ("Shop", "Make browsing and adding to cart effortless."),
                  ("Trust", "Surface reviews, press and guarantees.")],
        "result": "A confident, product-first store that makes a sensitive category feel easy.",
        "fallback": "mobile",
    },
]


# ---------------------------------------------------------------- inner pages

ABOUT_PAGE = {
    "eyebrow": "About Norvel",
    "title": "A studio built for how work gets done now",
    "lead": "Norvel is an independent design & technology studio. We bring brand, web design and Webflow development under one senior team — and run the whole process on AI, so you get more thinking, faster, without losing the craft.",
    "story_title": "Why Norvel exists",
    "story": [
        "Great brands and websites still need taste, judgment and care. What they no longer need is months of meetings, layers of account managers and three vendors who never talk to each other.",
        "So we built a studio around a simple idea: keep the senior people close to the work, and let AI handle the heavy lifting. The result is a tighter loop between your idea and a finished, live product.",
    ],
    "process_title": "How we work",
    "process": [
        ("Discover", "We learn your business, your audience and what success looks like — usually in a single focused workshop."),
        ("Explore", "AI-assisted research and rapid exploration put many directions on the table in days, not weeks."),
        ("Design", "A senior designer takes the strongest direction and turns it into a precise, considered system."),
        ("Build", "We build in Webflow with clean structure, motion and a CMS your team can actually use."),
        ("Launch & grow", "We ship, measure and keep improving — as a one-off project or an ongoing partner."),
    ],
}

SERVICES_PAGE = {
    "eyebrow": "Services",
    "title": "Three pillars, one team",
    "lead": "Brand, web design and Webflow development are equal parts of what we do. Take one, or let us handle all three end to end.",
    "engage_title": "Ways to work with us",
    "engagements": [
        ("Project", "A defined scope with a clear timeline — a new identity, a website or a launch.", ["Fixed scope & timeline", "Weekly check-ins", "Full handover at launch"]),
        ("Retainer", "A set number of design and development hours every month, for teams that ship continuously.", ["Priority turnaround", "Monthly planning", "Pause or scale anytime"]),
        ("Fractional team", "A senior creative and Webflow team on call, embedded in your workflow.", ["Dedicated lead", "Works in your tools", "Strategy + execution"]),
    ],
}

TESTIMONIALS_PAGE = {
    "eyebrow": "Testimonials",
    "title": "What clients say",
    "lead": "Feedback from the people we work with. We’re a new studio — this page grows with every project we ship.",
}

# SAMPLE CONTENT — replace with real client quotes before launch.
# While "sample" is True, a visible "Sample" label is shown on the card.
TESTIMONIALS = [
    {"quote": "Clear communication, thoughtful design and a result beyond what we expected. It felt like having an in-house team.", "name": "Client name", "role": "Founder, Company", "sample": True},
    {"quote": "They explored more directions in a week than our last agency did in a month — and the final identity is exactly us.", "name": "Client name", "role": "Marketing Lead, Company", "sample": True},
    {"quote": "Our Webflow site is fast, easy to update and finally looks like the product we’re building.", "name": "Client name", "role": "Head of Growth, Company", "sample": True},
    {"quote": "Brand, website and launch handled by one team. No hand-offs, no surprises, just steady progress.", "name": "Client name", "role": "CEO, Company", "sample": True},
]

CONTACT_PAGE = {
    "eyebrow": "Contact",
    "title": "Let’s talk about your project",
    "lead": "Tell us what you’re working on. We reply within one business day with next steps — usually a short call and a rough plan.",
    # Paste a Formspree / Web3Forms endpoint here to receive submissions directly.
    # Left empty, the form opens the visitor's email app with everything pre-filled.
    "form_endpoint": "",
    "services": ["Brand & Identity", "Web Design", "Webflow Development", "Not sure yet"],
    "budgets": ["Under $5k", "$5k – $15k", "$15k – $40k", "$40k+"],
    "details": [("Email", "hello@norvelstudio.com"), ("Response time", "Within one business day"), ("Location", "Remote-first · US & Europe")],
}

# ---------------------------------------------------------------- service landing pages
SERVICE_PAGES = [
    {
        "slug": "webflow-development",
        "pillar": "Webflow Development",
        "title": "Webflow development studio for fast, scalable marketing sites",
        "seo_title": "Webflow Development Agency — Custom Webflow Sites & CMS | Norvel",
        "description": "Norvel builds production-grade Webflow websites: custom code, CMS architecture, GSAP interactions, SEO and performance — handed over so your team can run it.",
        "lead": "We build Webflow sites that are fast, accessible and easy for your marketing team to run — from a single launch page to a full CMS-driven website.",
        "intro": "Webflow gives marketing teams something most websites never do: the freedom to publish without waiting on developers. We make sure that freedom doesn’t come at the cost of quality. Every build is structured with a clean class system, a CMS that matches how your team actually publishes, and the custom code and motion that make a site feel considered.",
        "cover": "gyde-health",
        "deliverables": [
            ("Webflow build", "Pixel-accurate development from Figma, responsive across every breakpoint."),
            ("CMS architecture", "Collections, references and templates designed around your content model."),
            ("Interactions & motion", "Webflow interactions and GSAP / ScrollTrigger where native tools stop."),
            ("Custom code & integrations", "Forms, analytics, HubSpot, Memberstack, APIs and anything in between."),
            ("SEO & performance", "Semantic markup, metadata, structured data, image optimisation and Core Web Vitals."),
            ("Handover & training", "A documented style guide and a walkthrough so your team owns the site."),
        ],
        "process": [
            ("Audit & plan", "We review the design, content and integrations, then map the CMS and page templates."),
            ("Build", "Components first, then pages — reviewed in a staging link you can click through every week."),
            ("QA & launch", "Cross-browser and device testing, redirects, SEO checks, then a calm launch day."),
            ("Support", "Optional retainer for new pages, experiments and ongoing improvements."),
        ],
        "work": ["gyde-health", "playground"],
        "faqs": [
            ("Can you build in Webflow from our existing Figma designs?", "Yes. We regularly develop sites from designs made by in-house teams or other studios, and flag anything that needs adapting for Webflow early."),
            ("Can we migrate from WordPress to Webflow?", "Yes — we migrate content into the Webflow CMS, rebuild templates, and set up 301 redirects so existing search rankings are preserved."),
            ("Will our team be able to edit the site?", "That’s the point. We structure the CMS and components so marketers can publish pages and posts without breaking the design, and we train your team at handover."),
            ("Do you offer ongoing Webflow support?", "Yes, through a monthly retainer with a set number of hours for new pages, landing pages and improvements."),
        ],
    },
    {
        "slug": "web-design",
        "pillar": "Web Design",
        "title": "Website design that makes complex products easy to understand",
        "seo_title": "Website Design Agency for SaaS, AI & B2B Companies | Norvel",
        "description": "Strategic website design for SaaS, AI and B2B companies: information architecture, UX, UI design and interactive prototypes — by a senior, AI-native studio.",
        "lead": "We design websites around what your visitors need to understand, feel and do — then prototype everything before a line of code is written.",
        "intro": "Most websites fail for the same reason: they describe the company instead of answering the visitor’s questions. We start from those questions, structure the site around them, and design every section to move someone one step closer to a demo, a sign-up or a conversation. AI lets us explore far more directions early, so the final design is chosen — not settled for.",
        "cover": "hp-workforce-experience",
        "deliverables": [
            ("Information architecture", "Sitemap, page structure and user flows built around real buyer questions."),
            ("UX & wireframes", "Low-fidelity layouts to agree on structure and messaging before visuals."),
            ("UI design", "High-fidelity, responsive designs for desktop, tablet and mobile."),
            ("Interactive prototypes", "Clickable Figma prototypes for stakeholder reviews and user testing."),
            ("Web design system", "Tokens, components and page templates that keep the site consistent as it grows."),
            ("Developer handover", "Specs, assets and motion notes — or we build it ourselves in Webflow."),
        ],
        "process": [
            ("Discover", "A focused workshop on your audience, positioning, competitors and goals."),
            ("Structure", "Sitemap, page outlines and wireframes for the key templates."),
            ("Design", "Visual direction, then full UI design of every page and state."),
            ("Prototype & refine", "Clickable prototype, feedback rounds and final polish before build."),
        ],
        "work": ["hp-workforce-experience", "lightspeed", "lagunitas"],
        "faqs": [
            ("How long does a website design project take?", "A focused marketing site usually takes 4–8 weeks from kickoff to final designs, depending on the number of templates and review cycles."),
            ("Do you also write the copy?", "We shape the messaging and page structure with you and write UX copy; for long-form copy we work with your team or a copywriter."),
            ("Can you redesign our site without hurting SEO?", "Yes. We keep URL structures where possible, plan redirects where not, and carry over metadata and structured data."),
            ("Do you design only for Webflow?", "No — our designs work on any platform. Webflow is simply our default when we build the site too."),
        ],
    },
    {
        "slug": "brand-identity",
        "pillar": "Brand & Identity",
        "title": "Brand identity systems built to work everywhere",
        "seo_title": "Brand Identity Design Studio — Logos & Visual Systems | Norvel",
        "description": "Brand identity design by Norvel: logo and mark systems, visual language, typography, colour, motion principles and brand guidelines built as a flexible system.",
        "lead": "Identities that hold up everywhere — from a favicon to a billboard — designed as systems, not one-off logos.",
        "intro": "A logo is only the entry point. What makes a brand recognisable is a consistent system of type, colour, layout, imagery and motion that anyone on your team can apply. We design that system with you, test it across real touchpoints — website, product, social, out-of-home — and document it so it stays consistent long after launch.",
        "cover": "lagunitas",
        "deliverables": [
            ("Brand strategy", "Positioning, personality and the core message the identity should carry."),
            ("Logo & mark system", "Primary logo, symbol, lockups and responsive variations."),
            ("Visual language", "Typography, colour palette, grids, imagery and graphic elements."),
            ("Motion principles", "How the brand moves on screen — transitions, logo animation, pacing."),
            ("Brand guidelines", "A clear, practical guide your team and partners can actually use."),
            ("Launch assets", "Social templates, presentation decks, signage and campaign assets."),
        ],
        "process": [
            ("Discover", "Interviews and a workshop to define what the brand stands for."),
            ("Explore", "AI-assisted exploration of many directions across marks, type and colour."),
            ("Refine", "One direction developed into a complete, tested identity system."),
            ("Roll out", "Guidelines, templates and launch assets across every touchpoint."),
        ],
        "work": ["lagunitas", "hello-cake", "a16z"],
        "faqs": [
            ("How many logo concepts will we see?", "We explore widely internally, then present two to three strong directions with rationale, applied to real touchpoints."),
            ("Can you refresh our existing brand instead of starting over?", "Yes. Often an evolution — sharper type, a clearer system, better guidelines — is the right move."),
            ("What files do we receive?", "Logo files in all formats (SVG, PNG, PDF), colour and type specs, guidelines, and editable templates."),
            ("Can you design the website as well?", "Yes — brand, web design and Webflow development are handled by one team, so the identity carries straight into the site."),
        ],
    },
]

# ---------------------------------------------------------------- insights / blog
AUTHOR = {"name": "Adis Krvavac", "role": "Founder, Norvel Studio"}

POSTS = [
    {
        "slug": "webflow-vs-wordpress-b2b-marketing-site",
        "title": "Webflow vs WordPress for B2B marketing sites: how to choose",
        "seo_title": "Webflow vs WordPress for B2B Marketing Sites (2026 Guide) | Norvel",
        "description": "Webflow or WordPress for your B2B website? A practical comparison of editing, performance, security, SEO, flexibility and cost of ownership — and when each is the right call.",
        "date": "2026-11-17",
        "read": "7 min read",
        "category": "Webflow",
        "excerpt": "Both platforms can run a great B2B website. The right choice depends less on features and more on who will own the site day to day.",
        "body": [
            ("p", "Every B2B team rebuilding its website eventually asks the same question: Webflow or WordPress? Both can power a fast, beautiful, search-friendly marketing site. But they make very different trade-offs — and the right choice depends less on feature lists than on who will run the site after launch."),
            ("p", "Here is how we think about it after building and redesigning marketing sites for SaaS, AI and enterprise companies."),
            ("h2", "The short answer"),
            ("ul", [
                "Choose **Webflow** if your marketing team wants to publish and iterate on pages without developers, and your site is primarily a marketing site: pages, landing pages, a blog, case studies.",
                "Choose **WordPress** if you need deep custom functionality, a very large content library with complex workflows, heavy e-commerce, or a specific plugin ecosystem your business depends on.",
            ]),
            ("h2", "1. Editing and day-to-day ownership"),
            ("p", "This is the biggest difference. In Webflow, marketers edit content directly on the page and can build new pages from approved components. Design stays consistent because the building blocks are locked to the design system."),
            ("p", "WordPress editing depends heavily on how the site was built. A well-structured block theme can be pleasant to use; a theme stacked with page-builder plugins often isn’t. In practice, many WordPress sites end up needing a developer for changes that Webflow users make themselves."),
            ("h2", "2. Performance"),
            ("p", "Webflow serves sites from a global CDN with hosting included, and outputs relatively clean markup. Fast performance is the default; you mainly need to watch image sizes, third-party scripts and heavy animations."),
            ("p", "WordPress can be extremely fast, but performance is something you have to engineer: hosting choice, caching, plugin discipline and theme quality all matter. The gap between a well-built and a poorly-built WordPress site is large."),
            ("h2", "3. Security and maintenance"),
            ("p", "Webflow is a hosted platform: there are no core, theme or plugin updates to run, and no server to patch. That removes a whole category of maintenance work and risk."),
            ("p", "WordPress is self-managed (unless you choose managed hosting). Core, themes and plugins need regular updates, and outdated plugins are a common source of vulnerabilities. It’s manageable — but it is ongoing work someone must own."),
            ("h2", "4. SEO"),
            ("p", "Both platforms can rank equally well. Rankings come from content, structure and site quality, not from the CMS logo. Webflow gives you control over metadata, URLs, redirects, sitemaps and custom code for structured data out of the box. WordPress achieves the same through plugins such as Yoast or Rank Math, which add convenience but also another dependency."),
            ("h2", "5. Flexibility and custom functionality"),
            ("p", "WordPress wins on raw extensibility. With custom post types, PHP and tens of thousands of plugins, it can become almost anything — membership platforms, complex directories, large stores."),
            ("p", "Webflow is deliberately more focused. Custom code, integrations and tools like Memberstack, HubSpot or Zapier cover most marketing needs, but if your website is really a web application, a custom stack or WordPress may be the better foundation."),
            ("h2", "6. Cost of ownership"),
            ("p", "Compare total cost, not just licences. Webflow has a predictable subscription that includes hosting. WordPress software is free, but hosting, premium plugins, maintenance and developer time add up. For most marketing sites, the cost that matters most is how often your team has to wait for a developer."),
            ("h2", "How we decide with clients"),
            ("p", "We ask four questions:"),
            ("ol", [
                "Who will update the site every week — marketers or developers?",
                "Is this a marketing site, or a product with marketing pages attached?",
                "Which integrations are non-negotiable?",
                "How much content are you migrating, and how is it structured?",
            ]),
            ("p", "For most SaaS, AI and B2B marketing sites we work on, the answers point to Webflow: it lets marketing teams move faster, keeps the design consistent, and removes maintenance overhead. When the answers point elsewhere, we say so."),
            ("p", "Planning a rebuild or a migration? [Tell us about your project](/contact/) — we’ll give you an honest recommendation, whichever platform it points to."),
        ],
    },
]
