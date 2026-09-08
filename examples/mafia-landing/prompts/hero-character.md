# Hero Character Prompt

## The prompt sent to generate_image:

```
A single man in a dark pinstripe three-piece suit, fedora tilted to shadow one eye,
cigarette held between two fingers at his side, standing with weight on his left leg,
chin slightly raised — the confident stance of someone who owns the room.
Full body, head to shoes visible. Facing slightly toward camera-left.

Isolated on a perfectly flat, solid, saturated pure green background (#00FF00).
No shadow cast onto the green background. No ground plane. No floor. No props
unless held by the character. The character must not touch or blend into the green edges.
Leave at least 50 pixels of clean green around every edge of the figure.

Painterly digital illustration with visible brush strokes, reminiscent of noir
movie posters from the 1940s. Rich, saturated shadows with slightly exaggerated
contrast. Not photorealistic, not flat vector — painterly. Warm tungsten key light
from screen-left, casting long dramatic shadows to the right. Deep vignette
darkening all four edges. Fine 35mm film grain visible on close inspection. Color
palette restricted to: #0A0E1A, #1C2333, #D4A854, #F5E6C8, #8B1A1A, #4A5568.
Prohibition-era America, 1920s clothing details.
```

## Post-processing:
1. `python scripts/chroma_key.py hero-raw.png hero-character.png --similarity 0.22 --blend 0.08`
2. `python scripts/verify_alpha.py hero-character.png`
3. If verify fails → re-generate with white/black backgrounds and use `--fallback` mode

## Notes:
- "Pure green background (#00FF00)" — explicit hex prevents the model from interpreting "green" as grass or forest
- "No shadow cast onto the green" — dark shadows on green break the chroma key
- "Leave 50px of clean green" — gives the keying algorithm room to work on edges
- One character per prompt — multiple characters produce inconsistent results
