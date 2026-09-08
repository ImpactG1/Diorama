# Prompt Patterns for Layer Generation

Each layer in a Diorama scene must be generated with a prompt that locks to the Art Bible established in Step 0. These templates show how to structure prompts for each layer type. The agent MUST fill in the `{...}` placeholders from the Art Bible before sending any generation call.

**Critical rule**: Every prompt ends with the same lighting, medium, and palette lines from the Art Bible. This is how independently generated assets read as one scene.

---

## Art Bible Lock Block (append to every prompt)

```
{art_bible_render_medium}. {art_bible_lighting_rule}. Color palette restricted to: {art_bible_palette_hex_list}. {art_bible_era_details}.
```

Example filled:
```
Gouache illustration with visible brush texture. Warm tungsten key light from screen-left, deep vignette, fine film grain. Color palette restricted to: #1A1A2E, #16213E, #0F3460, #E94560, #D4A854, #F5F5DC. Prohibition-era America, 1920s architectural details.
```

---

## Layer: Background Plate

**Role**: Full-bleed environment, no characters or subjects. Sets the world.

```
A wide establishing shot of {scene_description}, empty of people.
{depth_cue — e.g. "foggy street receding into distance" or "interior with depth from foreground bar to back wall"}.
No text, no UI elements, no characters.
Suitable as a website background — horizontally seamless edges preferred.
{art_bible_lock_block}
```

**Key constraints**:
- Do NOT request "transparent background" — this is the base layer
- Request wide/landscape aspect ratio
- Ensure edges can work as a repeating or clamped background

---

## Layer: Character Cutout

**Role**: Focal figure(s), isolated on a solid chroma-key backing.

```
A single {character_description}, full body, standing in a {pose_description}.
Isolated on a perfectly flat, solid, saturated pure green background (#00FF00).
No shadow cast onto the green background. No ground plane. No props unless held by the character.
The character must not touch or blend into the green edges.
{art_bible_lock_block}
```

**Key constraints**:
- Explicitly request `#00FF00` green — not "green background" (models interpret this as grass, forests, etc.)
- "No shadow cast onto the green" prevents dark splotches that break the key
- "No ground plane" prevents feet from fading into a painted floor
- One character per generation — multiple characters in one prompt produce inconsistent poses

**If the model can't hold flat green**, fall back to difference matting:
```
[Same prompt but replace green line with:]
Isolated on a perfectly flat, solid, pure white background (#FFFFFF).
```
Then re-generate with:
```
[Same prompt but:]
Isolated on a perfectly flat, solid, pure black background (#000000).
```
Use `chroma_key.py --fallback --white-input white.png --black-input black.png` to derive alpha.

---

## Layer: Props / Motifs

**Role**: Small thematic objects used as custom list markers, button icons, dividers, and decorative accents. This is the HIGHEST-LEVERAGE, MOST-SKIPPED layer — swapping default bullets and stock icons for theme-specific motifs is the single biggest tell between "designed" and "AI slop."

```
A set of {count} individual {prop_description}, arranged in a grid with generous spacing between each.
Each object is isolated — no overlap, no connecting lines.
Flat, solid, saturated pure green background (#00FF00) behind and between every object.
No shadows. No ground plane. No text labels.
{art_bible_lock_block}
```

**After generation**:
1. Run chroma key on the full grid image
2. Crop each individual motif to its own file
3. Verify alpha on each crop
4. Use as `list-style-image`, `background-image` for custom bullets, or `content` for pseudo-elements

**Common prop sets by theme**:
- Mafia/noir: bullet casings, playing cards, poker chips, fedora silhouette, tommy gun silhouette, whiskey glass, brass knuckles
- Cyberpunk: circuit traces, hex icons, glitch artifacts, neon tubes, data chips
- Medieval: swords, shields, scrolls, wax seals, stone textures, iron rivets
- Space: stars, planets, rockets, satellites, asteroids, nebula wisps

---

## Layer: Texture Overlay

**Role**: Applied as a CSS blend layer (`mix-blend-mode`) over the entire scene. Adds atmosphere without adding objects.

```
A seamless {texture_type} texture pattern, filling the entire frame edge to edge.
{texture_specifics — e.g. "fine 35mm film grain with occasional dust specks" or "wisps of cigarette smoke drifting left to right"}.
On a transparent background — the texture elements should be the ONLY visible pixels.
Flat pure green background (#00FF00) behind the texture elements.
No objects, no shapes, no text.
{art_bible_lock_block — but OMIT the lighting rule for grain/noise textures, keep it for smoke/light-leak textures}
```

**CSS application**:
```css
.texture-overlay {
  position: absolute;
  inset: 0;
  z-index: var(--z-texture);
  mix-blend-mode: overlay;  /* or multiply, screen, soft-light depending on effect */
  opacity: 0.3;             /* subtle — never more than 0.5 */
  pointer-events: none;     /* don't block interaction with layers below */
}
```

---

## Layer: Custom Icon Set

**Role**: Navigation icons, button glyphs, and UI indicators rendered in the SAME medium as the rest of the scene. Using default lucide/heroicons/feather on a themed page is one of the top AI-slop tells.

```
A set of {count} simple icon glyphs for a website navigation: {icon_list — e.g. "home, menu, search, user profile, settings, close"}.
Each icon is roughly the same size, arranged in a single row with clear spacing.
Rendered in {art_bible_render_medium} — NOT as flat vector line icons.
Flat, solid, saturated pure green background (#00FF00).
No text labels below the icons. Monochrome using {art_bible_accent_color} only.
{art_bible_lock_block}
```

**After generation**:
1. Chroma key the strip
2. Crop each icon to its own square file, maintaining consistent padding
3. Verify alpha
4. Use via CSS: `background-image: url(icons/home.png)` or as `<img>` elements in nav

---

## Anti-patterns to avoid in prompts

| Don't | Why | Do instead |
|---|---|---|
| "transparent background" | Models paint a checkerboard, not real alpha | "flat solid pure green (#00FF00) background" |
| "a mafia scene with characters and props" | Produces one flat image, can't be layered | Decompose into separate prompts per layer |
| "dark and moody lighting" | Vague, each generation interprets differently | Lock one specific lighting sentence in the Art Bible |
| "in the style of..." | Models drift across generations | Lock render medium once, paste verbatim in every prompt |
| "some bullets and cards scattered around" | Generic composition | Specify exact count, grid layout, no overlap |
| Multiple characters in one prompt | Inconsistent poses, tangled limbs | One character per generation call |
