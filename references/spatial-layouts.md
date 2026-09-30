# Spatial Layouts & Typography Archetypes

The #1 hallmark of AI-generated web designs is **The Centering Disease**: slapping every headline, subhead, card, and button in the dead-center of the viewport (`align-items: center; justify-content: center; text-align: center;`). When combined with an illustrated hero cutout, the text directly collides with the character's face and body, creating an unreadable, amateur composite.

Real graphic design, editorial publishing, and cinematic art direction use **asymmetric tension**, **spatial grids**, and **depth-interleaved typography**.

---

## The 4 Spatial Composition Archetypes

Every Diorama hero must choose one of these four archetypes instead of a generic centered flexbox.

---

### Archetype 1: Asymmetric Rule-of-Thirds (Stage-Left Editorial)

**Best for**: Character-driven scenes with strong narrative copy, dossiers, or story introductions.
**How it works**: The 12-column grid allocates cols 1–6 to left-aligned text with a directional scrim, while cols 6–12 are reserved for the character cutout and midground props.

```html
<section class="diorama-scene archetype-split" id="hero-scene">
  <!-- Base background (z: 0) -->
  <div class="diorama-layer" data-depth="0" style="--z: 0">
    <img src="assets/background-plate.png" alt="" role="presentation">
  </div>

  <!-- Directional Scrim (z: 5) — protects text readability on left side -->
  <div class="diorama-scrim diorama-scrim--stage-left" style="--z: 5"></div>

  <!-- Hero Character anchored stage-right (z: 20) -->
  <div class="diorama-layer diorama-layer--stage-right" data-depth="0.4" style="--z: 20">
    <img src="assets/hero-character.png" alt="Don Vittorio in dark overcoat">
  </div>

  <!-- Foreground Atmospheric Prop (z: 30) -->
  <div class="diorama-layer diorama-layer--fg-left" data-depth="0.8" style="--z: 30">
    <img src="assets/foreground-props.png" alt="" role="presentation">
  </div>

  <!-- Text & UI Grid (z: 50) -->
  <div class="diorama-grid-overlay" style="--z: 50">
    <div class="editorial-col">
      <div class="archival-kicker">
        <span class="docket-num">DOC-1927-NY</span>
        <span class="docket-sep">/</span>
        <span class="docket-status">ACTIVE SURVEILLANCE</span>
      </div>
      <h1 class="editorial-title">The Five Points Syndicate</h1>
      <p class="editorial-lede">
        Operating beyond municipal jurisdiction since the Volstead Act. Every cask cataloged, every debt honored, no testimony given.
      </p>
      <div class="editorial-actions">
        <a href="#ledger" class="action-btn">Inspect The Ledger</a>
        <a href="#whisper" class="action-link">Direct Dispatch</a>
      </div>
    </div>
  </div>
</section>
```

```css
.archetype-split .diorama-grid-overlay {
  position: absolute;
  inset: 0;
  z-index: var(--z, 50);
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 6rem 2.5rem 3rem;
  align-items: center;
  pointer-events: none;
}

.archetype-split .editorial-col {
  grid-column: 1 / span 6; /* Stage left */
  text-align: left;
  pointer-events: auto;
}

.diorama-layer--stage-right img {
  position: absolute;
  right: 5%;
  bottom: 0;
  width: auto;
  height: 90vh;
  object-fit: contain;
}

/* Directional scrim: darkens only the text zone, leaves character illuminated */
.diorama-scrim--stage-left {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    rgba(10, 14, 26, 0.95) 0%,
    rgba(10, 14, 26, 0.8) 35%,
    rgba(10, 14, 26, 0.3) 55%,
    transparent 75%
  );
  pointer-events: none;
}
```

---

### Archetype 2: Cinematic Masthead (Interleaved Poster)

**Best for**: Movie posters, high-fashion, dramatic character showcases, title cards.
**How it works**: Giant display lettering sits at `z-index: 15` *behind* the character cutout (`z-index: 20`). The character’s silhouette occludes the letters (the classic *TIME* or *Vogue* magazine masthead). Interactive copy sits at `z-index: 50`.

```html
<section class="diorama-scene archetype-masthead" id="hero-scene">
  <!-- Base background (z: 0) -->
  <div class="diorama-layer" data-depth="0" style="--z: 0">
    <img src="assets/background-plate.png" alt="" role="presentation">
  </div>

  <!-- Giant Masthead BEHIND character (z: 15) -->
  <div class="diorama-layer diorama-masthead-back" data-depth="0.15" style="--z: 15">
    <div class="masthead-lettering" aria-hidden="true">VITTORIO</div>
  </div>

  <!-- Hero Character Cutout OVERLAPPING the masthead (z: 20) -->
  <div class="diorama-layer diorama-character-center" data-depth="0.4" style="--z: 20">
    <img src="assets/hero-character.png" alt="Don Vittorio standing center frame">
  </div>

  <!-- Interactive Controls & Metadata IN FRONT (z: 50) -->
  <div class="diorama-masthead-ui" style="--z: 50">
    <div class="masthead-top-bar">
      <span class="classification-stamp">CLASSIFIED — COSA NOSTRA ARCHIVE</span>
      <span class="file-date">OCTOBER 1928</span>
    </div>
    
    <div class="masthead-bottom-bar">
      <div class="bottom-lede">
        <h1 class="visually-hidden">Don Vittorio</h1>
        <p>A gentleman by daylight. The law by midnight.</p>
      </div>
      <a href="#dossier" class="cta-button">Open Surveillance Dossier</a>
    </div>
  </div>
</section>
```

```css
.diorama-masthead-back {
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  overflow: hidden;
}

.masthead-lettering {
  font-family: var(--font-display);
  font-size: clamp(6rem, 18vw, 22rem);
  font-weight: 900;
  text-transform: uppercase;
  color: var(--ivory);
  opacity: 0.18;
  letter-spacing: -0.04em;
  line-height: 0.8;
  user-select: none;
  white-space: nowrap;
}

.diorama-character-center img {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  height: 92vh;
  width: auto;
  object-fit: contain;
}

.diorama-masthead-ui {
  position: absolute;
  inset: 0;
  z-index: var(--z, 50);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 5rem 3rem 2.5rem;
  pointer-events: none;
}

.masthead-top-bar,
.masthead-bottom-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  pointer-events: auto;
}
```

---

### Archetype 3: The Peripheral Frame (HUD / Marginalia)

**Best for**: Immersive worlds, cyberpunk, retro sci-fi, military manifests, architectural archives.
**How it works**: The center 60% of the screen is completely unobstructed artwork. Text is distributed to the 4 corners and margins, anchored with vertical text runners and coordinate stamps.

```css
.archetype-peripheral {
  display: grid;
  grid-template-areas:
    "top-left   .         top-right"
    "spine-left center    spine-right"
    "bot-left   bot-mid   bot-right";
  grid-template-columns: 240px 1fr 280px;
  grid-template-rows: auto 1fr auto;
  padding: 2rem;
  min-height: 100vh;
}

.spine-runner {
  grid-area: spine-left;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  font-family: var(--font-meta);
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  opacity: 0.5;
  align-self: center;
}
```

---

### Archetype 4: Editorial Monograph / Ledger

**Best for**: Authentic historical documents, speakeasy menus, inventory manifests, investigative journalism.
**How it works**: Uses a tactile, asymmetric backing card with hairline metallic borders (`1px solid rgba(212, 168, 84, 0.3)`) and an authentic ledger/table layout instead of bullet points.

---

## 3-Tier Locked Typography System

In Step 0, every Diorama Art Bible must lock 3 distinct typographic tiers:

| Tier | Role | Characteristics | Anti-Slop Constraint |
|---|---|---|---|
| **Tier 1: Display** | Main titles, masthead | Expressive, period/theme-accurate, distinctive letterforms | Negative tracking (`-0.02em` to `-0.05em`) for large sizes. NEVER use default sans-serif. |
| **Tier 2: Editorial / Body** | Story lede, narratives | High readability, warm texture, graceful italics | Generous line-height (`1.65–1.85`), max line-length 60ch. |
| **Tier 3: Archival / Meta** | Docket numbers, timestamps, coordinates, stamps | Technical, monospace or small-caps engraving | Wide tracking (`+0.1em` to `+0.25em`), uppercase, small scale (`0.7rem–0.85rem`). |

### Thematic Font Pairing Matrix

| Theme | Display Face (Tier 1) | Editorial Face (Tier 2) | Archival / Meta Face (Tier 3) |
|---|---|---|---|
| **Noir / 1920s Speakeasy** | `Playfair Display` or `Cinzel` (900 wt) | `Libre Baskerville` or `Cormorant Garamond` | `Courier Prime` or `Special Elite` |
| **Cyberpunk / Dystopia** | `Syne` or `Clash Display` (800 wt) | `Space Grotesk` or `Plus Jakarta Sans` | `JetBrains Mono` or `Share Tech Mono` |
| **Gothic / Dark Fantasy** | `Cinzel Decorative` or `UnifrakturMaguntia` | `EB Garamond` or `Crimson Pro` | `IM Fell English SC` |
| **Retro-SciFi 1970s** | `Righteous` or `Bungee` | `Archivo` or `Work Sans` | `DM Mono` |
| **Brutalist / Industrial** | `Bebas Neue` or `Anton` (900 wt) | `Inter Tight` or `IBM Plex Sans` | `Space Mono` or `OCR-A` |

---

## Atmospheric Scrims — Eliminating Muddy Text Shadows

Never use heavy `text-shadow: 0 0 30px #000` to make text legible. Use **Art-Directed Scrims**:

1. **Directional Linear Scrim**:
   ```css
   .scrim-stage-left {
     background: linear-gradient(90deg, rgba(10,14,26,0.92) 0%, rgba(10,14,26,0.7) 40%, transparent 80%);
   }
   ```
2. **Radial Focus Scrim**:
   ```css
   .scrim-radial {
     background: radial-gradient(ellipse at 25% 50%, rgba(10,14,26,0.85) 0%, transparent 70%);
   }
   ```
3. **Tactile Editorial Slabs (Backing Cards)**:
   ```css
   .editorial-slab {
     background: rgba(28, 35, 51, 0.65);
     backdrop-filter: blur(12px) saturate(1.2);
     border: 1px solid rgba(212, 168, 84, 0.25);
     box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
   }
   ```

---

## Archival Micro-Typography Accents

Give the composition authentic texture with real editorial accents:

- **Rotated Archival Stamps**:
  ```css
  .stamp-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border: 2px solid var(--crimson);
    color: var(--crimson);
    font-family: var(--font-meta);
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    transform: rotate(-4deg);
    mask-image: radial-gradient(circle, black 70%, transparent 100%);
  }
  ```
- **Vertical Runners**:
  ```css
  .vertical-runner {
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    letter-spacing: 0.2em;
    font-family: var(--font-meta);
    font-size: 0.7rem;
    opacity: 0.5;
  }
  ```
- **Tabular Ledger Tables** (replacing generic `<ul>` lists):
  ```html
  <table class="diorama-ledger">
    <thead>
      <tr>
        <th>RECORD</th>
        <th>OPERATIVE</th>
        <th>STATUS</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>#104-B</td>
        <td>Salvatore M.</td>
        <td class="status-cleared">ACTIVE</td>
      </tr>
    </tbody>
  </table>
  ```
