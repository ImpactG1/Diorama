---
name: diorama
description: >-
  Use whenever a user asks for a themed landing page, hero section, or UI that should feel
  illustrated, cinematic, or hand-designed rather than templated — e.g. "act as a senior
  graphic designer and build a 1920s mafia landing page," a strong theme/world/character brief,
  or a complaint about "AI slop," generic gradients, stock icon sets, or cookie-cutter card
  layouts. Builds the page from a set of individually generated, art-directed, TRUE-transparency
  image components (environment plates, character cutouts, prop/bullet motifs, texture overlays,
  custom icon sets) that get composited and animated in real HTML/CSS — instead of one flat AI
  hero image or a default component-kit layout. Do not use for plain data UIs, dashboards, or
  forms with no visual theme.
---

# Diorama — Layer-Composited Anti-Slop UI

You are pairing as both art director and frontend engineer. The failure mode this skill exists to prevent: asking an image model for "a mafia landing page" and pasting the single flat image it returns into a `<div>`, or asking a coding agent for "a mafia landing page" and getting the same terracotta-cream SaaS-card template as every other brief. Neither is a real UI.

**This skill's method**: lock one visual identity → decompose the scene into independent transparent layers → generate each layer against that lock → verify real alpha transparency in code (never trust the model's claim) → composite and animate the layers as actual DOM/CSS → run the anti-slop checklist.

The result is editable, responsive, accessible, and specific to the brief.

Read `references/anti-slop-checklist.md` in this folder before starting — it contains the concrete tells to check every output against before calling it done.

---

## Step 0 — Lock the art direction before generating anything

Every asset generated later must share one identity, or the composite will look like a stock-photo collage instead of one illustrated world. Produce a short **Art Bible** and confirm it with the user in one message before spending any generation calls:

- **World & era specifics** — research real reference details for the brief's subject (e.g. "old-school mafia" → Prohibition-era America, tommy guns, fedora silhouettes, brass and smoke, not a generic "gangster" clip-art read).
- **Palette** — 4–6 named hex values with usage notes, not "dark and moody."
- **Lighting rule** — one sentence, reused **verbatim** in every asset prompt. This is the single highest-leverage lock. Example: *"Warm tungsten key light from screen-left, deep vignette, fine film grain."* Without a shared lighting rule, independently generated assets never read as one scene.
- **Render medium** — one consistent style, e.g. "gouache illustration with visible brush texture" vs. "flat vector" vs. "grainy photobash." Never mix mediums across layers.
- **Typography system** — 3-tier locked font stack: (1) Display face with strong era/theme personality, (2) Editorial/body face for long-form legibility, (3) Technical/archival face (mono or small-caps) for dates, docket stamps, and metadata. Never default to generic unstyled system fonts or Inter.
- **Voice & copywriting persona** — define the in-world artifact (e.g. "classified 1928 Bureau dossier" or "bootleg speakeasy ledger"). Ban marketing fluff, generic AI tricolons ("Power. Loyalty. Respect."), and fake profundity ("Every empire starts with a single deal").
- **Motion personality** — 2–3 words (e.g. "slow, heavy, deliberate" vs. "snappy, playful") that govern Step 4's animation choices.

See `examples/mafia-landing/art-bible.md` for a complete example.

## Step 1 — Decompose the scene into a component manifest

Do not ask for "a hero image." Write out a manifest of independent layers, each with a name, a role, its z-index, and whether it needs a transparent background. Notice that typography is decomposed across depth planes rather than slapped on top as a flat sticker:

| Layer | Role | Transparent? | z-index |
|---|---|---|---|
| Background plate | Environment, no characters | No (base) | 0 |
| Midground props | Supporting objects (vehicles, furniture) | Yes | 10 |
| **Back typography (Masthead)** | Giant display title / watermark behind character | DOM (text) | 15 |
| Hero character cutout | The focal figure | Yes | 20 |
| Foreground props | Frame-edge objects, bottom of viewport | Yes | 30 |
| Texture overlay | Grain / smoke / light-leak (CSS blend layer) | Yes | 40 |
| **Front typography & UI** | Lede, docket stamps, ledger items, interactive CTAs | DOM (interactive) | 50 |
| Custom icon set | Nav icons, button glyphs, in the SAME render medium | Yes | — |
| Prop/motif set | Bullet casings, playing cards — for `<li>` markers, dividers | Yes | — |

The prop/icon layer and typographic depth separation are the highest-leverage steps: swapping default bullets and default icon libraries for theme-consistent motifs, and interleaving typography behind the hero figure, immediately breaks the "AI-generated billboard" feel.

See `examples/mafia-landing/manifest.md` for a complete example.

## Step 2 — Write structured prompts using the prompt patterns

For each layer in the manifest, write a generation prompt using the templates in `references/prompt-patterns.md`. Every prompt MUST end with the **Art Bible Lock Block** — the lighting rule, render medium, and palette pasted verbatim.

Key rules:
- For transparent layers: request the subject on a **flat, solid, saturated pure green background (#00FF00)** — NOT "transparent background" (models paint a checkerboard, not real alpha).
- One character per generation call — multiple characters produce inconsistent poses.
- Specify exact prop counts and grid layouts for motif sets.
- The background plate is the only layer that doesn't use green screen.

See `examples/mafia-landing/prompts/` for complete prompt examples for each layer type.

## Step 3 — Generate each component, then verify real transparency

Current image models cannot output a real alpha channel. Asking for "transparent background" produces a painted-on checkerboard. **Never trust model output directly.** Always derive real transparency programmatically:

### Primary method: Green-screen chroma key

1. Generate each transparent layer with the Art Bible lock block + green screen backing.
2. Run through the chroma key script:
   ```
   python scripts/chroma_key.py input.png output.png --key-color #00FF00 --similarity 0.22 --blend 0.08
   ```
3. Verify the result has real transparent pixels:
   ```
   python scripts/verify_alpha.py output.png
   ```
4. If verification passes → asset is ready for compositing.
5. If verification fails → adjust `--similarity` (raise if fringing, lower if subject eaten) and re-run.

### Fallback method: White/black difference matting

If the model won't hold a clean flat green (subject bleeds into backing, or model interprets "green background" as grass):

1. Generate the same subject on **pure white (#FFFFFF)** background.
2. Re-generate (or image-edit the first result) on **pure black (#000000)** background, keeping pixels aligned.
3. Derive alpha from the two renders:
   ```
   python scripts/chroma_key.py --fallback --white-input white.png --black-input black.png output.png
   ```
4. Verify with `verify_alpha.py`.

### Batch workflow

For a full scene with 6+ layers, batch the generation-key-verify cycle rather than hand-rolling each asset:
- Apply the same Art Bible lock block to every prompt.
- Run the same keying parameters across the whole set.
- Verify all assets at once: `python scripts/verify_alpha.py assets/`

**On Windows**: Use the Python scripts (`chroma_key.py`, `verify_alpha.py`). They require only Pillow (`pip install Pillow`).
**On Linux/macOS**: The Python scripts work everywhere. Alternatively, `scripts/chroma_key.sh` uses ffmpeg + ImageMagick for faster processing on large images.

## Step 4 — Composite as real HTML/CSS, not as one flat image

Reference `references/composition-patterns.md` and `references/spatial-layouts.md` for all code patterns. The essential rules:

- **Ban "Centering Disease"**: Never default to centering all text over the center of the viewport (`align-items: center; text-align: center`). Choose an intentional **Spatial Composition Archetype**:
  - *Asymmetric Rule-of-Thirds Split*: Character anchored to stage-right (cols 7–12), text locked to stage-left (cols 1–6).
  - *Cinematic Masthead*: Giant display title interleaved behind character (z-index 15), interactive elements at bottom corners.
  - *Peripheral Frame*: Diorama center is unobstructed; metadata, tickers, and CTAs flank the margins.
- **Interleave typography in depth**: Place the giant masthead/watermark title at `z-index: 15` *behind* the hero character cutout (`z-index: 20`). Place actionable content (lede, CTAs, archival stamps) at `z-index: 50` *in front*.
- **Directional Atmospheric Scrims**: Do NOT use fuzzy amateur `text-shadow` blurs. Use directional gradient masks (`linear-gradient(to right, ...)`), tactile backing cards, or targeted backdrop filters behind text zones to guarantee contrast over painted art.
- **Text is ALWAYS in real DOM nodes** — never baked into a generated image. This is non-negotiable for accessibility, localization, and SEO.
- **Depth comes from parallax**: a small differential transform per layer on scroll or pointer-move, background slowest, foreground fastest. Apply this ONCE as the page's one orchestrated motion moment.
- **Use the custom motif set** for list markers (`list-style-image`), button icons, and dividers — never default bullets or stock icon libraries on a themed page.
- **Texture overlays** use `mix-blend-mode` (overlay, screen, multiply, or soft-light depending on texture type) — see the blend mode table in `references/composition-patterns.md`.
- **Respect `prefers-reduced-motion`** — disable parallax and ambient animations.
- **Responsive**: layered scenes break first on mobile. Re-stack asymmetric layouts into a vertical editorial sequence, hide non-essential props, and disable parallax on touch screens.

See `examples/mafia-landing/index.html` and `examples/mafia-landing/styles.css` for a complete implementation.

## Step 5 — Animate deliberately, not generically

Reference `references/animation-playbook.md` for all motion patterns. The core principle:

**ONE orchestrated motion moment per scene.** Choose one:
- Layer entrance stagger (layers reveal back-to-front)
- Scroll parallax (layers shift at different speeds)
- Pointer parallax (layers follow cursor)
- Ambient drift (one texture layer drifts slowly)

Never combine two moment types on the same scene. Never add separate hover effects on every element. Scattered small effects with no single highlight is the #1 AI-slop motion tell.

Match easing to the Art Bible's motion personality:
- "Slow, heavy, deliberate" → `cubic-bezier(0.16, 1, 0.3, 1)`
- "Snappy, precise" → `cubic-bezier(0.33, 1, 0.68, 1)`
- "Dramatic, theatrical" → `cubic-bezier(0.7, 0, 0.3, 1)`

## Step 6 — Run the anti-slop checklist & automated layout linter

1. Run the automated code linter to catch centering reflexes, missing scrims, and generic copy:
   ```
   python scripts/lint_anti_slop.py index.html styles.css
   ```
2. Walk the finished page against `references/anti-slop-checklist.md` and flag any match.
3. Apply one round of **"remove one accessory"**: find the single most attention-grabbing element, make sure everything else is quiet around it, and cut anything decorative that isn't doing a job for this specific brief.

**Final gut check**: Could this exact page have come out of the same prompt for a completely different theme, with only the words swapped? If yes, the design leaned on defaults — go back to Step 0 and tighten the Art Bible.

---

## Using this in Antigravity / Gemini CLI

Place this folder at `.agents/skills/diorama/` (workspace-scoped) or `~/.gemini/config/skills/diorama/` (global). The `SKILL.md` file will be discovered automatically. You don't need to invoke it by name — a themed-page brief should trigger it — but you can force it explicitly with "use the diorama skill."

## Bundled resources

### Scripts
- `scripts/chroma_key.py` — Cross-platform Python chroma key (requires Pillow). Supports green-screen keying and white/black difference matting fallback.
- `scripts/verify_alpha.py` — Batch alpha verification for generated assets. Run before compositing.
- `scripts/lint_anti_slop.py` — Static layout and typography linter for HTML/CSS to catch AI-slop design reflexes.
- `scripts/chroma_key.sh` — Bash/ffmpeg/ImageMagick alternative for Linux/macOS environments.

### References (progressive disclosure — the agent reads these only when needed)
- `references/prompt-patterns.md` — Structured prompt templates for each layer type (background, character, props, textures, icons).
- `references/spatial-layouts.md` — 12-column grid archetypes, asymmetric alignment rules, and depth-interleaved typography.
- `references/composition-patterns.md` — HTML/CSS code patterns for scene containers, parallax, blend modes, atmospheric scrims, custom motifs.
- `references/animation-playbook.md` — Motion design patterns: entrance stagger, ambient drift, scroll reveals, easing reference.
- `references/anti-slop-checklist.md` — Concrete tells to check every output against before calling it done.

### Examples
- `examples/mafia-landing/` — Complete reference implementation with Art Bible, manifest, prompts, HTML, and CSS. See its `README.md` for a step-by-step walkthrough.
