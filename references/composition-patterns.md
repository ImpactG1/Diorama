# Composition Patterns — HTML/CSS for Layer-Composited Scenes

These are the concrete code patterns the agent should use when assembling generated assets into a real DOM-based layered scene. Every pattern here serves the same goal: **each transparent layer is an actual positioned element, never flatten back into a single exported image.**

---

## 1. Scene Container & Layer Stacking

The foundation of every Diorama composition. All layers stack inside one positioned container. 
**Crucial Anti-Slop Rule**: Typography is NEVER dumped into a single centered block on top of the hero image. Typography is split across depth planes:
- `z-index: 15`: **Back Typography (Masthead/Watermark)** — sits *behind* the hero character cutout (`z-index: 20`), allowing the character to occlude the lettering (the classic *TIME* or *Vogue* magazine effect).
- `z-index: 5`: **Atmospheric Scrim** — a directional gradient mask that preserves contrast behind text without muddying the character art.
- `z-index: 50`: **Front UI & Copy** — accessible lede, metadata stamps, docket numbers, and interactive CTA buttons.

```html
<section class="diorama-scene archetype-split" id="hero-scene" aria-label="Hero scene">
  <!-- z-index 0: Background plate (full bleed, no transparency) -->
  <div class="diorama-layer" data-depth="0" style="--z: 0">
    <img src="assets/background-plate.png"
         alt=""
         role="presentation"
         loading="eager"
         class="diorama-bg">
  </div>

  <!-- z-index 5: Directional Atmospheric Scrim (protects text zone contrast) -->
  <div class="diorama-scrim diorama-scrim--left" style="--z: 5" aria-hidden="true"></div>

  <!-- z-index 10: Midground props -->
  <div class="diorama-layer" data-depth="0.3" style="--z: 10">
    <img src="assets/midground-props.png"
         alt=""
         role="presentation"
         loading="eager">
  </div>

  <!-- z-index 15: Back typography (Interleaved Masthead behind character) -->
  <div class="diorama-layer diorama-masthead-back" data-depth="0.15" style="--z: 15">
    <span class="masthead-watermark" aria-hidden="true">THE FAMILY</span>
  </div>

  <!-- z-index 20: Hero character cutout (overlaps masthead) -->
  <div class="diorama-layer diorama-layer--hero" data-depth="0.5" style="--z: 20">
    <img src="assets/hero-character.png"
         alt="Don Vittorio standing under tungsten streetlamp"
         loading="eager">
  </div>

  <!-- z-index 30: Foreground props (decorative) -->
  <div class="diorama-layer diorama-layer--fg" data-depth="0.8" style="--z: 30">
    <img src="assets/foreground-props.png"
         alt=""
         role="presentation"
         loading="eager">
  </div>

  <!-- z-index 40: Texture overlay (grain/smoke) -->
  <div class="diorama-layer diorama-texture" data-depth="0" style="--z: 40">
    <img src="assets/texture-grain.png"
         alt=""
         role="presentation"
         loading="lazy">
  </div>

  <!-- z-index 50: Interactive UI & Editorial Content (Asymmetric 12-col grid) -->
  <div class="diorama-grid-content" style="--z: 50">
    <div class="editorial-col">
      <div class="archival-kicker">
        <span class="stamp-tag">DOCKET #1927-NY</span>
        <span class="stamp-date">OCTOBER 14, 1927</span>
      </div>
      <h1 class="editorial-heading">The Five Points Syndicate</h1>
      <p class="editorial-lede">
        Operating beyond municipal jurisdiction since the Volstead Act. Every cask cataloged, every debt honored, no testimony given.
      </p>
      <div class="editorial-cta-row">
        <a href="#ledger" class="cta-button">Open The Ledger</a>
        <a href="#code" class="secondary-link">The Family Code</a>
      </div>
    </div>
  </div>
</section>
```

### Key rules:
- **Text is NEVER baked into images** — it's real DOM nodes for accessibility, localization, and SEO
- **Never center-align all text over a centered character** — use an asymmetric grid (e.g. stage-left text, stage-right character) or depth-interleaving
- **Decorative layers get `role="presentation"` and empty `alt`** — screen readers skip them
- **The hero character gets a real `alt` text** — it's meaningful content
- **`data-depth`** drives parallax intensity: 0 = no movement, 1 = maximum movement

---

## 2. Core CSS — Stacking, Asymmetric Grids & Scrims

```css
/* ========================================
   DIORAMA SCENE — Layer Composition System
   ======================================== */

.diorama-scene {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
  isolation: isolate;
}

.diorama-layer {
  position: absolute;
  inset: 0;
  z-index: var(--z, 0);
  pointer-events: none;
  will-change: transform;
}

.diorama-layer img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none;
  -webkit-user-drag: none;
}

/* Character layer positioning (stage right or centered) */
.diorama-layer--hero img {
  position: absolute;
  right: 5%;
  bottom: 0;
  width: auto;
  height: 90vh;
  object-fit: contain;
}

/* Directional Scrim: protects text contrast without muddy drop-shadows */
.diorama-scrim--left {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    rgba(10, 14, 26, 0.95) 0%,
    rgba(10, 14, 26, 0.8) 35%,
    rgba(10, 14, 26, 0.25) 60%,
    transparent 80%
  );
  pointer-events: none;
}

/* Interleaved Back Typography (z: 15) */
.diorama-masthead-back {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.masthead-watermark {
  font-family: var(--font-display);
  font-size: clamp(5rem, 16vw, 20rem);
  font-weight: 900;
  color: var(--ivory);
  opacity: 0.15;
  letter-spacing: -0.04em;
  white-space: nowrap;
  user-select: none;
}

/* Asymmetric 12-Column Grid for Content (z: 50) */
.diorama-grid-content {
  position: absolute;
  inset: 0;
  z-index: var(--z, 50);
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 6rem 2.5rem 3rem;
  align-items: center;
  pointer-events: none;
}

.editorial-col {
  grid-column: 1 / span 6; /* Stage-left: cols 1 to 6 */
  text-align: left;
  pointer-events: auto;
}
```

---

## 3. Parallax — One Orchestrated Motion Moment

Parallax is the scene's single deliberate motion effect. Background layers move slowly, foreground layers move faster, creating physical depth. **Do NOT add separate hover effects, fade-ins, or bounces to individual layers on top of this.**

### Option A: Scroll Parallax (most common)

```js
/**
 * Diorama scroll parallax.
 * Each layer's `data-depth` attribute controls how much it moves.
 * depth=0: stationary (background)
 * depth=1: moves 1:1 with scroll (foreground)
 */
function initDioramaParallax() {
  const scene = document.querySelector('.diorama-scene');
  if (!scene) return;

  // Respect user preferences
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  const layers = scene.querySelectorAll('.diorama-layer[data-depth]');

  function onScroll() {
    const scrollY = window.scrollY;
    const sceneTop = scene.offsetTop;
    const offset = scrollY - sceneTop;

    layers.forEach(layer => {
      const depth = parseFloat(layer.dataset.depth) || 0;
      // Negative direction = layer moves opposite to scroll = depth illusion
      const translate = -(offset * depth * 0.15);
      layer.style.transform = `translate3d(0, ${translate}px, 0)`;
    });
  }

  // Use passive listener for scroll performance
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // Initial position
}

document.addEventListener('DOMContentLoaded', initDioramaParallax);
```

### Option B: Pointer-Follow Parallax (for hero sections above the fold)

```js
/**
 * Diorama pointer parallax.
 * Layers shift subtly based on mouse/touch position.
 * Use this for hero sections that are visible without scrolling.
 */
function initDioramaPointerParallax() {
  const scene = document.querySelector('.diorama-scene');
  if (!scene) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  const layers = scene.querySelectorAll('.diorama-layer[data-depth]');

  function onPointerMove(e) {
    const rect = scene.getBoundingClientRect();
    // Normalize to -0.5 ... +0.5 from center
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;

    layers.forEach(layer => {
      const depth = parseFloat(layer.dataset.depth) || 0;
      const moveX = x * depth * 30; // max 30px shift for depth=1
      const moveY = y * depth * 20; // max 20px shift
      layer.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
    });
  }

  scene.addEventListener('pointermove', onPointerMove, { passive: true });
}

document.addEventListener('DOMContentLoaded', initDioramaPointerParallax);
```

**Choose one or the other** for a given scene. Never both on the same scene — they'll fight for `transform`.

---

## 4. Custom Motif Integration

Replace default bullets, icons, and dividers with theme-specific generated assets.

### Custom List Markers

```css
/* Replace default bullets with theme motifs */
.diorama-list {
  list-style: none;
  padding-left: 0;
}

.diorama-list li {
  position: relative;
  padding-left: 2.5rem;
  margin-bottom: 0.75rem;
}

.diorama-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.25em;
  width: 1.25rem;
  height: 1.25rem;
  background: url('assets/motifs/bullet-casing.png') center/contain no-repeat;
}
```

### Custom Dividers

```css
.diorama-divider {
  border: none;
  height: 2rem;
  background: url('assets/motifs/divider-flourish.png') center/contain no-repeat;
  margin: 3rem 0;
  opacity: 0.6;
}
```

### Custom Navigation Icons

```css
.nav-icon {
  display: inline-block;
  width: 1.5rem;
  height: 1.5rem;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  vertical-align: middle;
}

.nav-icon--home    { background-image: url('assets/icons/home.png'); }
.nav-icon--search  { background-image: url('assets/icons/search.png'); }
.nav-icon--menu    { background-image: url('assets/icons/menu.png'); }
.nav-icon--profile { background-image: url('assets/icons/profile.png'); }
```

---

## 5. Responsive Strategy for Layered Scenes

Layered compositions are the FIRST thing that breaks on narrow viewports. Plan for this.

```css
/* Tablet: reduce parallax intensity, hide least-important layers */
@media (max-width: 1024px) {
  .diorama-layer[data-depth] {
    /* Reduce parallax to prevent layers from separating too much */
    --parallax-scale: 0.5;
  }

  /* Hide foreground props if they crowd the content */
  .diorama-layer[style*="--z: 30"] {
    display: none;
  }
}

/* Mobile: flatten to key layers only */
@media (max-width: 640px) {
  .diorama-scene {
    min-height: 80vh;
  }

  /* Disable parallax entirely — it's disorienting on small touch screens */
  .diorama-layer[data-depth] {
    transform: none !important;
  }

  /* Keep only: background, hero character, content */
  .diorama-layer[style*="--z: 10"],
  .diorama-layer[style*="--z: 30"],
  .diorama-texture {
    display: none;
  }

  /* Adjust content padding for mobile */
  .diorama-content {
    padding: 1.5rem 1rem;
    justify-content: flex-end;
    padding-bottom: 3rem;
  }
}
```

---

## 6. Texture Overlay Blend Modes

Choose based on the texture type:

| Texture | Blend Mode | Opacity | Effect |
|---|---|---|---|
| Film grain | `overlay` | 0.15–0.25 | Adds subtle noise without darkening |
| Smoke/fog | `screen` | 0.2–0.4 | Lightens the scene, adds atmosphere |
| Light leak | `screen` | 0.1–0.3 | Warm glow bleeding from edges |
| Dust/scratches | `multiply` | 0.1–0.2 | Darkens slightly, adds worn texture |
| Paper texture | `soft-light` | 0.2–0.4 | Gentle contrast shift, natural feel |
| Vignette | `multiply` | 0.4–0.6 | Darkens edges, focuses center |

```css
/* Apply the right blend mode per texture type */
.diorama-texture--grain    { mix-blend-mode: overlay;    opacity: 0.2;  }
.diorama-texture--smoke    { mix-blend-mode: screen;     opacity: 0.3;  }
.diorama-texture--lightleak{ mix-blend-mode: screen;     opacity: 0.15; }
.diorama-texture--dust     { mix-blend-mode: multiply;   opacity: 0.15; }
.diorama-texture--paper    { mix-blend-mode: soft-light;  opacity: 0.3;  }
.diorama-texture--vignette { mix-blend-mode: multiply;   opacity: 0.5;  }
```

---

## 7. Accessibility Checklist

- [ ] All text is in real DOM nodes, never baked into images
- [ ] Decorative layers have `role="presentation"` and `alt=""`
- [ ] Meaningful images (hero character) have descriptive `alt` text
- [ ] `prefers-reduced-motion` is respected — parallax disabled
- [ ] `prefers-color-scheme` — scene works on both light and dark if applicable
- [ ] Color contrast ratios pass WCAG 2.1 AA for all text over the scene
- [ ] Interactive elements (buttons, links) are keyboard-focusable
- [ ] Scene is navigable with screen readers — content reads in logical order
