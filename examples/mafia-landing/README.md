# Mafia Landing Page — Process Walkthrough

This example shows the complete Diorama process from brief to finished page, featuring fully keyed transparent cutouts and rendered atmosphere plates to demonstrate live depth compositing.

---

## The Brief

> "Act as a Senior Graphic Designer and make an old school mafia type Landing Page for my website."

---

## Step 0 — Lock Art Direction

Before generating a single asset, we produced an **Art Bible** ([art-bible.md](./art-bible.md)) and confirmed it with the user. The Art Bible locks:

- **World**: Prohibition-era America, 1925-1933
- **Palette**: 6 named hex values (Midnight Navy, Smoky Charcoal, Burnished Brass, Aged Ivory, Blood Crimson, Fog Grey)
- **Lighting**: "Warm tungsten key light from screen-left, casting long dramatic shadows to the right. Deep vignette darkening all four edges."
- **Medium**: "Painterly digital illustration with visible brush strokes, reminiscent of noir movie posters from the 1940s."
- **Typography**: 3-tier locked system (Playfair Display 900 for Display, Libre Baskerville for Editorial, Courier Prime for Archival/Meta)
- **Voice**: Declassified DOJ surveillance dossier & syndicate ledger — zero generic SaaS CTAs or movie one-liner clichés
- **Motion**: "Slow, heavy, deliberate"

The lighting sentence and medium sentence are appended **verbatim** to every asset prompt.

---

## Step 1 — Decompose into Layers & Depth Typography

We wrote a **Component Manifest** ([manifest.md](./manifest.md)) breaking the scene into independent layers across depth planes:

| Layer | z-index | Type | Role |
|---|---|---|---|
| Background plate (foggy street) | 0 | Image (opaque) | Base environment |
| Directional Scrim | 5 | CSS gradient | Preserves stage-left text contrast over lights |
| Midground props (car, lamp) | 10 | Image (transparent) | Scene depth |
| **Back Masthead ("VITTORIO")** | 15 | DOM (Text) | Giant display watermark behind character |
| Hero character (The Boss) | 20 | Image (transparent) | Anchored stage-right, overlapping masthead |
| Foreground props (whiskey, bills) | 30 | Image (transparent) | Framing viewport edge |
| Smoke texture | 40 | Image (screen blend) | Atmospheric drift |
| Film grain texture | 41 | Image (overlay blend) | 35mm grain |
| Margin Spine Runner | 45 | DOM (Text) | Vertical surveillance log label |
| **Front UI & Copy Grid** | 50 | DOM (Interactive) | Asymmetric 12-col grid, docket stamps, CTAs |

Plus a motif set (bullet casings, playing cards, brass knuckles) and custom icon set.

---

## Step 2 — Generate + Key Each Layer

For each transparent layer, we:

1. **Wrote a structured prompt** with the Art Bible lock block appended (see [prompts/](./prompts/))
2. **Generated on green screen** (#00FF00) — not "transparent background"
3. **Ran chroma key**: `python scripts/chroma_key.py raw.png keyed.png`
4. **Verified alpha**: `python scripts/verify_alpha.py keyed.png`
5. If verification failed → adjusted `--similarity` or fell back to white/black matting

The background plate (z-index 0) skips the green screen — it's the base layer.

---

## Step 3 — Composite as Real HTML/CSS with Asymmetric Grid

The final page ([index.html](./index.html) + [styles.css](./styles.css)) composites layers as positioned DOM elements:

- **Asymmetric 12-Column Grid**: Text is anchored stage-left (cols 1–7) while the hero character is anchored stage-right (cols 8–12). No centered text collisions.
- **Depth-Interleaved Masthead**: "VITTORIO" sits at `z-index: 15` *behind* the hero cutout (`z-index: 20`), creating classic magazine/poster depth.
- **Directional Scrim**: Linear gradient mask at `z-index: 5` ensures crisp typographic contrast without muddy drop-shadows.
- **Tabular Syndicate Ledger**: Replaces generic bullet points with an authenticated covenant accounting table.
- Smoke texture uses `mix-blend-mode: screen` at 28% opacity.
- Film grain uses `mix-blend-mode: overlay` at 16% opacity.

### The ONE motion moment:
- **Layer entrance stagger** — layers fade in from back to front on page load
- Scroll parallax shifts layers at different rates (background slow, foreground fast)
- Smoke drifts via ambient animation (30s cycle, barely perceptible)
- All motion respects `prefers-reduced-motion`

---

## Step 4 — Automated Verification & Anti-Slop Audit

1. **Run the layout & copy linter**:
   ```bash
   python scripts/lint_anti_slop.py examples/mafia-landing/
   ```
   Ensures 0 centered text penalties, verifies depth interleaving, confirms directional scrims, and catches AI copywriting clichés.

2. **Check [references/anti-slop-checklist.md](../../references/anti-slop-checklist.md)**:
   - ✅ No centering disease — asymmetric 12-col editorial grid
   - ✅ No text colliding with character art
   - ✅ Depth-interleaved masthead behind character
   - ✅ Directional scrim protecting legibility
   - ✅ 3-tier typographic system (Playfair Display + Libre Baskerville + Courier Prime)
   - ✅ In-world artifact copy (dossier & covenants ledger)
   - ✅ All transparent assets verified with `verify_alpha.py`

**Final gut check**: Could this exact page come out of the same prompt for a different theme with only words swapped? **No** — the palette, typography, motifs, covenants table, character cutouts, and atmospheric scrims are all deeply authentic to this Prohibition-era brief.
