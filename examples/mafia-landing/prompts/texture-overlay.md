# Texture Overlay Prompt

## Smoke Texture — The prompt sent to generate_image:

```
Wisps of cigarette smoke and cigar smoke drifting slowly from right to left,
thin tendrils and larger lazy plumes, varying density — some areas nearly clear,
others with thick swirling clouds.

The smoke should fill the frame edge to edge as a seamless pattern.
Flat, solid, saturated pure green background (#00FF00) behind the smoke.
The smoke itself should be pale grey-white (#F5E6C8 tinted) and semi-transparent
in appearance. No objects, no shapes, no text, no people — only smoke.

Painterly digital illustration with visible brush strokes, reminiscent of noir
movie posters from the 1940s. Warm tungsten key light from screen-left,
illuminating the smoke edges with a golden tint.
```

## Film Grain Texture:

```
A seamless 35mm film grain texture pattern filling the entire frame edge to edge.
Fine, organic noise with occasional dust specks and subtle light scratches.
The grain should be monochrome — white/light grey noise particles.

Flat, solid, saturated pure green background (#00FF00) behind the grain particles.
No objects, no shapes, no text — ONLY the grain texture.
```

## Post-processing:
1. `python scripts/chroma_key.py smoke-raw.png texture-smoke.png --similarity 0.25`
   (slightly higher similarity to catch green between thin smoke wisps)
2. `python scripts/chroma_key.py grain-raw.png texture-grain.png --similarity 0.20`
3. `python scripts/verify_alpha.py texture-smoke.png texture-grain.png`

## CSS Usage:
```css
/* Smoke: screen blend makes it glow, sits at z-40 */
.texture-smoke {
  mix-blend-mode: screen;
  opacity: 0.3;
  animation: ambient-drift 30s linear infinite;
}

/* Grain: overlay blend adds noise without darkening, sits at z-41 */
.texture-grain {
  mix-blend-mode: overlay;
  opacity: 0.15;
  /* Grain is static — no animation */
}
```
