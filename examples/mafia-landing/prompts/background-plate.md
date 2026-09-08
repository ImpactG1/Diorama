# Background Plate Prompt

## The prompt sent to generate_image:

```
A wide establishing shot of a foggy Prohibition-era American street at night, 1927.
Brick buildings line both sides, receding into thick fog. Gas lamp posts cast warm
pools of light on wet cobblestones. A faded speakeasy sign hangs above a narrow
door. Art Deco iron railings, fire escapes with dripping laundry, a distant
elevated train trestle disappearing into the fog. Empty of people — no characters,
no figures, no silhouettes of people.

No text, no UI elements, no watermarks.

Suitable as a website background — horizontally continuous, no strong focal point
that would compete with overlaid text.

Painterly digital illustration with visible brush strokes, reminiscent of noir
movie posters from the 1940s. Rich, saturated shadows with slightly exaggerated
contrast. Not photorealistic, not flat vector — painterly. Warm tungsten key light
from screen-left, casting long dramatic shadows to the right. Deep vignette
darkening all four edges. Fine 35mm film grain visible on close inspection. Color
palette restricted to: #0A0E1A, #1C2333, #D4A854, #F5E6C8, #8B1A1A, #4A5568.
Prohibition-era America, 1920s architectural details.
```

## Notes:
- Requested landscape/wide aspect ratio
- No chroma key needed — this is the base layer (z-index 0)
- "Empty of people" prevents the model from adding its own characters
- "No strong focal point" ensures overlaid text and character cutouts remain the focus
