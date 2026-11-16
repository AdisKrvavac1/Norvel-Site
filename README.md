# Norvel Studio — website

Static site (HTML/CSS/JS, no framework) based on the Eclipsis layout from the Webflow project, rebuilt with Norvel branding.

## Structure
- `build/data.py` — **all site copy** (hero, sections, FAQ, projects). Edit here.
- `build/build.py` — generates every page into `public/`.
- `build/art.py` — generates placeholder project artwork (SVG) in the Norvel palette.
- `public/` — the deployable site (already built and committed).

## Edit & rebuild
```bash
python3 build/build.py          # regenerates public/
python3 -m http.server -d public 8080   # preview at http://localhost:8080
```
No dependencies beyond Python 3.

## Deploy on Render
1. Render → **New → Blueprint** → pick this repo (uses `render.yaml`), or **New → Static Site** with
   build command `python3 build/build.py` and publish directory `public`.
2. Add the custom domain `norvelstudio.com` in Render settings.
3. 404s are served from `public/404.html` automatically.

## Before going live
- Projects are **concept studies with placeholder artwork** — replace with real work in `build/data.py`
  and swap images in `public/assets/work/` (or point `cover`/`gallery` at your own files).
- Social links in `SITE["socials"]` point to the platform homepages — add your profile URLs.
- Brand: lime `#c8f03c`, fog `#eef1f4`, ink `#0b0e13`. Logos in `public/assets/img/`.
