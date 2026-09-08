# Composition Patterns — HTML/CSS for Layer-Composited Scenes

These are the concrete code patterns the agent should use when assembling generated assets into a real DOM-based layered scene. Every pattern here serves the same goal: **each transparent layer is an actual positioned element, never flatten back into a single exported image.**

---

## 1. Scene Container

The foundation of every Diorama composition. All layers stack inside one positioned container.

```html
<section class="diorama-scene" id="hero-scene" aria-label="Hero scene">
  <!-- z-index 0: Background plate (full bleed, no transparency) -->
  <div class="diorama-layer" data-depth="0" style="--z: 0">
    <img src="assets/background-plate.png"
         alt=""
         role="presentation"
         loading="eager"
         class="diorama-bg">
  </div>

  <!-- z-index 10: Midground props -->
  <div class="diorama-layer" data-depth="0.3" style="--z: 10">
    <img src="assets/midground-props.png"
         alt=""
         role="presentation"
         loading="eager">
  </div>

  <!-- z-index 20: Hero character -->
  <div class="diorama-layer" data-depth="0.6" style="--z: 20">
    <img src="assets/hero-character.png"
         alt="A figure in a fedora and long coat, standing under a streetlight"
         loading="eager">
  </div>

  <!-- z-index 30: Foreground props (decorative) -->
  <div class="diorama-layer" data-depth="0.9" style="--z: 30">
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

  <!-- Text content sits ON TOP of the scene, in the DOM, accessible -->
  <div class="diorama-content" style="--z: 50">
    <h1>The Family</h1>
    <p class="tagline">Every empire starts with a single deal.</p>
    <a href="#story" class="cta-button">Enter the Speakeasy</a>
  </div>
</section>
```

### Key rules:
- **Text is NEVER baked into images** — it's real DOM nodes for accessibility, localization, and SEO
- **Decorative layers get `role="presentation"` and empty `alt`** — screen readers skip them
- **The hero character gets a real `alt` text** — it's meaningful content
- **`data-depth`** drives parallax intensity: 0 = no movement, 1 = maximum movement

---

## 2. Core CSS — Scene Stacking

```css
/* ========================================
   DIORAMA SCENE — Layer Composition System
   ======================================== */

.diorama-scene {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
  /* Contain the stacking context */
  isolation: isolate;
}

.diorama-layer {
  position: absolute;
  inset: 0;
  z-index: var(--z, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none; /* Don't block clicks through to content */
  /* GPU-accelerated for smooth parallax */
  will-change: transform;
}

.diorama-layer img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* Prevent image dragging */
  user-select: none;
  -webkit-user-drag: none;
}

/* Background plate: covers entire scene, no transparency */
.diorama-bg {
  object-fit: cover;
}

/* Texture overlay: blend into the scene */
.diorama-texture {
  mix-blend-mode: overlay;
  opacity: 0.25;
}

/* Content layer: sits on top, receives pointer events */
.diorama-content {
  position: relative;
  z-index: var(--z, 50);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  text-align: center;
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
