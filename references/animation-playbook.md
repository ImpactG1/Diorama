# Animation Playbook — Motion Design for Diorama Scenes

The #1 AI-slop motion tell: **fade-and-slide-up entrance animations applied uniformly to every section, with hover transitions on every card**. Motion applied everywhere instead of once, deliberately.

This playbook enforces the opposite: **one orchestrated moment per scene**, and every other element is quiet.

---

## The One-Moment Rule

Every Diorama scene gets exactly **one deliberate motion highlight**. Choose one:

| Moment Type | Best For | Description |
|---|---|---|
| **Layer entrance stagger** | Hero/above-the-fold scenes | Layers fade in from back to front with staggered delays |
| **Scroll parallax** | Full-page compositions | Layers shift at different speeds on scroll |
| **Pointer parallax** | Interactive hero sections | Layers shift subtly following the cursor |
| **Ambient loop** | Atmospheric scenes | One texture layer drifts slowly (smoke, clouds, particles) |

**Never combine two moment types on the same scene.** If the hero has scroll parallax, it does NOT also get entrance stagger. Pick one.

---

## Moment 1: Layer Entrance Stagger

Layers reveal from back (z-index 0) to front (highest z-index), each with a slight delay. This creates the effect of the scene being "assembled" in front of the user.

```css
/* Base state: all layers start hidden */
.diorama-layer {
  opacity: 0;
  transform: scale(1.05);
  transition:
    opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Stagger delays by z-index: background first, foreground last */
.diorama-layer[style*="--z: 0"]  { transition-delay: 0s;    }
.diorama-layer[style*="--z: 10"] { transition-delay: 0.15s; }
.diorama-layer[style*="--z: 20"] { transition-delay: 0.3s;  }
.diorama-layer[style*="--z: 30"] { transition-delay: 0.45s; }
.diorama-layer[style*="--z: 40"] { transition-delay: 0.6s;  }

/* Content text enters last, after all layers are visible */
.diorama-content {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.6s ease,
    transform 0.6s ease;
  transition-delay: 0.8s;
}

/* Revealed state: triggered by IntersectionObserver or page load */
.diorama-scene.is-revealed .diorama-layer,
.diorama-scene.is-revealed .diorama-content {
  opacity: 1;
  transform: none;
}
```

```js
/**
 * Trigger the layer entrance stagger when the scene enters the viewport.
 */
function initDioramaEntrance() {
  const scene = document.querySelector('.diorama-scene');
  if (!scene) return;

  // Skip animation for reduced-motion users
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    scene.classList.add('is-revealed');
    return;
  }

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        scene.classList.add('is-revealed');
        observer.disconnect(); // Only trigger once
      }
    },
    { threshold: 0.2 }
  );

  observer.observe(scene);
}

document.addEventListener('DOMContentLoaded', initDioramaEntrance);
```

---

## Moment 2: Ambient Drift

A single texture or atmospheric layer drifts continuously. Use for smoke, clouds, dust motes, or light leaks. **Only one layer drifts — the rest are static.**

```css
/* Slow, continuous drift on a single texture layer */
.diorama-ambient-drift {
  animation: ambient-drift 30s linear infinite;
}

@keyframes ambient-drift {
  from {
    transform: translate3d(0, 0, 0);
  }
  50% {
    transform: translate3d(-3%, -1.5%, 0);
  }
  to {
    transform: translate3d(0, 0, 0);
  }
}

/* Pause animation for reduced motion */
@media (prefers-reduced-motion: reduce) {
  .diorama-ambient-drift {
    animation: none;
  }
}
```

**Speed guideline**: Ambient motion should be so slow that you have to stare for 2-3 seconds to notice it's moving. If it's immediately obvious, it's too fast. 20-40 second cycle minimum.

---

## Moment 3: Scroll-Triggered Section Reveals

For content sections BELOW the hero, use IntersectionObserver to reveal them as the user scrolls. But follow these rules:

```js
/**
 * Reveal sections as they enter the viewport.
 * Uses one consistent animation — NOT different effects per section.
 */
function initSectionReveals() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const sections = document.querySelectorAll('.diorama-reveal');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target); // Once only
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
  );

  sections.forEach(section => observer.observe(section));
}

document.addEventListener('DOMContentLoaded', initSectionReveals);
```

```css
.diorama-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition:
    opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.diorama-reveal.is-visible {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .diorama-reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

### Rules for section reveals:
- **Same animation for every section** — not fade-left for one, zoom for another, flip for a third
- **No stagger within a section** — don't animate each paragraph or bullet individually
- **Once only** — `unobserve` after triggering, never re-animate on scroll-up
- **Short and subtle** — 0.5-0.8s duration, small translateY (20-40px), ease-out curve

---

## Motion Timing Custom Properties

Use CSS custom properties to create a single kill-switch for all motion:

```css
:root {
  --motion-speed: 1;
  --motion-distance: 1;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-speed: 0;
    --motion-distance: 0;
  }
}

/* Usage in animations */
.diorama-layer {
  transition-duration: calc(0.8s * var(--motion-speed));
  transform: translateY(calc(20px * var(--motion-distance)));
}

.diorama-ambient-drift {
  animation-duration: calc(30s * var(--motion-speed));
  /* When --motion-speed is 0, duration is 0s, effectively disabling */
}
```

---

## Anti-Patterns — What NOT to Do

| Don't | Why | Do Instead |
|---|---|---|
| Hover scale/glow on every card | Generic AI tell, visual noise | Hover effects only on interactive elements (buttons, links) |
| Different entrance animation per section | Looks uncoordinated, "demo reel" energy | One consistent reveal animation for all sections |
| Animate individual list items with stagger | Tedious, slows down reading | Animate the containing block, not children |
| `animation-iteration-count: infinite` on UI elements | Distracting, battery drain | Only for ambient textures, never for content |
| Parallax on every section | Nausea-inducing, performance cost | Parallax on ONE section (the hero), static everywhere else |
| Spring/bounce easing on everything | "Playful" defaults that don't match serious themes | Match easing to the Art Bible's motion personality |
| 3D perspective transforms on text | Readability disaster | 3D only on decorative layers, never on text |

---

## Easing Reference

Match the easing to the Art Bible's **motion personality**:

| Personality | CSS Easing | Feel |
|---|---|---|
| Slow, heavy, deliberate | `cubic-bezier(0.16, 1, 0.3, 1)` | Weighty, cinematic |
| Snappy, precise | `cubic-bezier(0.33, 1, 0.68, 1)` | Quick settle, professional |
| Smooth, flowing | `cubic-bezier(0.4, 0, 0.2, 1)` | Material Design-like |
| Dramatic, theatrical | `cubic-bezier(0.7, 0, 0.3, 1)` | Slow start, punchy end |
| Bouncy, playful | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Slight overshoot |
