# Mafia Landing Page — Process Walkthrough

This example shows the complete Diorama process from brief to finished page. It uses placeholder elements instead of actual generated images to demonstrate the structure without large binary files.

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
- **Motion**: "Slow, heavy, deliberate"

The lighting sentence and medium sentence are appended **verbatim** to every asset prompt.

---

## Step 1 — Decompose into Layers

We wrote a **Component Manifest** ([manifest.md](./manifest.md)) breaking the scene into independent layers:

| Layer | z-index | Transparent? |
|---|---|---|
| Background plate (foggy street) | 0 | No |
| Midground props (car, lamp) | 10 | Yes |
| Hero character (The Boss) | 20 | Yes |
| Foreground props (whiskey, revolver) | 30 | Yes |
| Smoke texture | 40 | Yes |
| Film grain texture | 41 | Yes |

Plus a motif set (bullet casings, playing cards, etc.) and custom icon set.

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

## Step 3 — Composite as Real HTML/CSS

The final page ([index.html](./index.html) + [styles.css](./styles.css)) composites layers as positioned DOM elements:

- Each layer is `position: absolute` with `z-index` from the manifest
- The content text is a real DOM node at z-index 50 — never baked into an image
- Smoke texture uses `mix-blend-mode: screen` at 30% opacity
- Film grain uses `mix-blend-mode: overlay` at 15% opacity
- Custom bullet casings replace default `<li>` markers
- Ace of Spades motif replaces `<hr>` dividers
- Custom icons in the nav, not default icon libraries

### The ONE motion moment:
- **Layer entrance stagger** — layers fade in from back to front on page load
- Scroll parallax shifts layers at different rates (background slow, foreground fast)
- Smoke drifts via ambient animation (30s cycle, barely perceptible)
- All motion respects `prefers-reduced-motion`

---

## Step 4 — Anti-Slop Checklist

Run the finished page against [references/anti-slop-checklist.md](../../references/anti-slop-checklist.md):

- ✅ No identical rounded cards with generic shadows
- ✅ No numbered markers on non-sequential content
- ✅ No warm cream + terracotta default palette
- ✅ No default Inter/system-ui font — uses Playfair Display + Libre Baskerville
- ✅ No one flat hero image — scene is decomposed into 6 layers
- ✅ No default icon library — custom generated icons
- ✅ No default `<ul>` bullets — bullet-casing motifs
- ✅ No scattered hover effects — one orchestrated parallax moment
- ✅ Motion respects `prefers-reduced-motion`
- ✅ Text is in real DOM, not baked into images
- ✅ All transparent assets verified with `verify_alpha.py`

**Final gut check**: Could this exact page come out of the same prompt for a different theme with only words swapped? **No** — the palette, typography, motifs, character cutouts, and smoke textures are all specific to this Prohibition-era brief.
