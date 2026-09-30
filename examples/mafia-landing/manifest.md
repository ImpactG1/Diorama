# Component Manifest — 1920s Mafia Speakeasy

Decomposed from the brief: "old school mafia type landing page." Each layer is generated independently, keyed to the Art Bible, and composited as a real DOM element using an asymmetric 12-column grid and depth-interleaved typography.

## Hero Scene Layers

| # | Layer Name | Role | Transparent? | z-index | Generation Method |
|---|---|---|---|---|---|
| 1 | Background plate | Foggy Prohibition-era street at night, gas lamps, brick buildings receding into fog. No people. | No (base layer) | 0 | Single generation, landscape aspect |
| 2 | Directional Scrim | Left-to-right gradient mask protecting text contrast over streetlights | CSS | 5 | Linear gradient overlay |
| 3 | Midground props | Parked Model T silhouette, fire hydrant, street lamp post, scattered newspaper pages | Yes | 10 | Green-screen generation → chroma key |
| 4 | **Back Masthead** | Giant display lettering ("VITTORIO") interleaved behind character silhouette | DOM (Text) | 15 | HTML/CSS text node |
| 5 | Hero character | The Boss — man in pinstripe suit, fedora tilted, cigarette in hand, standing stage-right | Yes | 20 | Green-screen generation → chroma key |
| 6 | Foreground props | Whiskey glass on a surface edge, revolver, stack of bills — framing bottom viewport | Yes | 30 | Green-screen generation → chroma key |
| 7 | Texture: smoke | Wisps of cigarette/cigar smoke drifting slowly left to right | Yes | 40 | Green-screen generation → chroma key |
| 8 | Texture: grain | 35mm film grain pattern, seamless tile | Yes | 41 | Green-screen generation → chroma key |
| 9 | **Front UI & Copy** | Stage-left editorial column, docket stamp, authenticated lede, primary CTA buttons | DOM (UI) | 50 | HTML/CSS interactive elements |

## Custom Motif Set

| Motif | Usage | Count |
|---|---|---|
| Bullet casing | Custom marker for dossier metadata | 1 |
| Playing card (Ace of Spades) | Section divider ornament | 1 |
| Brass knuckles | Primary action button icon | 1 |
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
| "The Covenants" | Tabular Syndicate Ledger (Docket #, Covenants, Execution Status) | Replaces generic bullet points with authentic accounting table |
| "The Directorate" | Asymmetric character cards with archival docket stamps | Three character cards with names, clearance levels, and roles |
| "The Vault" | Full-width atmospheric break | Speakeasy interior plate |
| Footer | Bureau dossier closing tag & micro-metadata | Uses custom typography and metadata timestamps |
