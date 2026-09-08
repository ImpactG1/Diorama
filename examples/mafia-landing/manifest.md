# Component Manifest — 1920s Mafia Speakeasy

Decomposed from the brief: "old school mafia type landing page." Each layer is generated independently, keyed to the Art Bible, and composited as a real DOM element.

## Hero Scene Layers

| # | Layer Name | Role | Transparent? | z-index | Generation Method |
|---|---|---|---|---|---|
| 1 | Background plate | Foggy Prohibition-era street at night, gas lamps, brick buildings receding into fog. No people. | No (base layer) | 0 | Single generation, landscape aspect |
| 2 | Midground props | Parked Model T silhouette, fire hydrant, street lamp post, scattered newspaper pages | Yes | 10 | Green-screen generation → chroma key |
| 3 | Hero character | The Boss — man in pinstripe suit, fedora tilted, cigarette in hand, standing with weight on one leg | Yes | 20 | Green-screen generation → chroma key |
| 4 | Foreground props | Whiskey glass on a surface edge, revolver, stack of bills — framing the bottom of the viewport | Yes | 30 | Green-screen generation → chroma key |
| 5 | Texture: smoke | Wisps of cigarette/cigar smoke drifting slowly left to right | Yes | 40 | Green-screen generation → chroma key |
| 6 | Texture: grain | 35mm film grain pattern, seamless tile | Yes | 41 | Green-screen generation → chroma key |

## Custom Motif Set

| Motif | Usage | Count |
|---|---|---|
| Bullet casing | Custom `<li>` marker for feature lists | 1 |
| Playing card (Ace of Spades) | Section divider ornament | 1 |
| Brass knuckles | CTA button icon | 1 |
| Fedora silhouette | Navigation icon (menu) | 1 |
| Tommy gun silhouette | Navigation icon (features) | 1 |
| Whiskey glass | Navigation icon (about) | 1 |

## Custom Icon Set

| Icon | Usage |
|---|---|
| Stylized "enter" door | Home / main nav |
| Magnifying glass (Art Deco style) | Search |
| Fedora + face silhouette | Profile / about |
| Envelope with wax seal | Contact |

## Content Sections (below hero)

| Section | Layout | Notes |
|---|---|---|
| "The Family" | Three character cards with names/roles | Each card uses a separately generated character cutout |
| "The Code" | Numbered rules list | Uses bullet-casing motifs instead of default numbered markers |
| "The Establishment" | Full-width image break | A second background plate (speakeasy interior) |
| Footer | Contact + social | Uses the custom icon set, not default social media SVGs |
