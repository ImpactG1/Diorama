# Anti-Slop Checklist

Run the finished page against every line below. Anything that matches is a default, not a choice made for this brief — revise it, unless the brief itself explicitly asked for that exact look.

## Layout & structure
- [ ] Content chopped into identical rounded cards with one border-radius applied regardless of hierarchy, and the same soft grey shadow under each.
- [ ] Numbered markers (01 / 02 / 03) on content that isn't actually a sequence or timeline.
- [ ] A tracked-out ALL-CAPS "eyebrow" label sitting above every heading whether or not it adds information.
- [ ] Meta strings joined with middle dots ("A · B · C") or labels built as "WORD — fragment" with a spaced em dash, regardless of subject.
- [ ] A "→" appended to every link and button as a reflex rather than a choice.

## Color & type
- [ ] A warm cream background (near `#F4F1EA`) paired with a high-contrast serif and a terracotta/clay accent (near `#D97757`).
- [ ] A near-black background with one bright acid-green or vermilion accent, applied regardless of subject.
- [ ] Tinted near-black (`#0B0B0B`, `#111`) standing in for true black everywhere.
- [ ] The default system-font stack (Inter / system-ui) used because no one chose a typeface on purpose.
- [ ] A monospace face applied to small data labels out of habit rather than because the content is data.
- [ ] Accenting a single word or phrase in a headline (one word bold/italic/colored) as the only typographic idea in the page.

## Imagery & components
- [ ] One flat AI-generated hero image standing in for the entire visual identity, with no separately directable layers behind it.
- [ ] Default icon library glyphs (lucide/heroicons/feather) used on a page with a strong theme, instead of a custom icon set in the same render medium as the rest of the scene.
- [ ] Default `<ul>` bullets or generic dot markers where a theme-specific motif was available and cheap to generate.
- [ ] Any generated asset whose lighting, palette, or render medium doesn't match the rest of the scene — a sign the Art Bible lock wasn't applied consistently.
- [ ] A "transparent" asset that was never actually verified to have a real alpha channel before being composited.

## Motion
- [ ] Fade-and-slide-up entrance animations applied uniformly to every section, with hover transitions on every card — motion applied everywhere instead of once, deliberately.
- [ ] Motion that doesn't respect `prefers-reduced-motion`.
- [ ] No single orchestrated "moment" — the page has scattered small effects but no one deliberate highlight.

## Layer composition (Diorama-specific)
- [ ] Any generated asset composited into the page without running `verify_alpha.py` first — an unverified "transparent" PNG from a model is almost certainly a painted checkerboard, not real alpha.
- [ ] Layers whose lighting direction doesn't match — each asset was generated with a different prompt instead of locking the Art Bible lighting sentence.
- [ ] Layers whose render medium doesn't match — one layer looks like a vector illustration while another looks like a photograph, because the Art Bible medium wasn't pasted verbatim into every prompt.
- [ ] More than one parallax effect on the page — scroll parallax on the hero AND pointer parallax on a second section, or parallax on every section.
- [ ] Custom icons/motifs that don't match the scene's render medium — generated as flat vectors on a gouache-illustrated page, or vice versa.
- [ ] A texture overlay applied without `mix-blend-mode` — just layered on top at reduced opacity, which washes out the scene instead of integrating.
- [ ] All scene layers at the same visual depth — no z-index differentiation, no depth variation, the composition reads flat despite having multiple layers.
- [ ] The scene was flattened back into a single exported image after compositing — defeating the entire purpose of layer-based composition (responsiveness, editability, accessibility).
- [ ] Text baked into a generated image instead of placed as a real DOM node — kills accessibility, localization, and the ability to change copy without re-generating the entire asset.

## Copy
- [ ] Placeholder or generic copy that could belong to any brief in this category, rather than copy grounded in this specific brand/world/content.
- [ ] Passive or system-centric labels ("Submit," "webhook config") instead of active, user-facing language ("Save changes").

## Final gut check
- [ ] Could this exact page have come out of the same prompt for a completely different theme, with only the words swapped? If yes, the design plan leaned on defaults instead of the brief — go back to Step 0 of the skill and tighten the Art Bible.
