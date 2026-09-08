# Props & Motifs Prompt

## The prompt sent to generate_image:

```
A set of 6 individual Prohibition-era objects arranged in a 3x2 grid with generous
spacing between each: a single bullet casing, a playing card (Ace of Spades face
visible), a pair of brass knuckles, a fedora seen from the front, a tommy gun
silhouette in profile, and a whiskey glass (old fashioned, with a single ice cube).

Each object is isolated — no overlap, no connecting lines, no decorative borders.
Flat, solid, saturated pure green background (#00FF00) behind and between every
object. Each object is roughly the same size (2-3 inches). No shadows cast onto
the green. No text labels.

Painterly digital illustration with visible brush strokes, reminiscent of noir
movie posters from the 1940s. Rich, saturated shadows with slightly exaggerated
contrast. Not photorealistic, not flat vector — painterly. Warm tungsten key light
from screen-left, casting long dramatic shadows to the right. Fine 35mm film grain
visible on close inspection. Color palette restricted to: #0A0E1A, #1C2333,
#D4A854, #F5E6C8, #8B1A1A, #4A5568.
```

## Post-processing:
1. `python scripts/chroma_key.py motifs-raw.png motifs-keyed.png`
2. Manually crop each motif from the grid into individual files:
   - `motifs/bullet-casing.png`
   - `motifs/ace-of-spades.png`
   - `motifs/brass-knuckles.png`
   - `motifs/fedora.png`
   - `motifs/tommy-gun.png`
   - `motifs/whiskey-glass.png`
3. `python scripts/verify_alpha.py motifs/`

## Notes:
- Grid layout with spacing makes cropping individual motifs reliable
- These are the highest-leverage assets: a bullet casing as a list marker instead of
  a default `•` is the single biggest tell between "designed" and "AI slop"
- Generate at 1024x1024 minimum so individual crops are still high-res enough for retina
