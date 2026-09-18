---
name: create-continuous-multi-screen-wallpaper
description: Create culturally grounded, seamless, high-resolution wallpaper sets for two- or three-monitor desks, including portrait screens, mixed resolutions, unequal physical sizes, and vertically offset arrangements. Use when a user wants one continuous scene across dual-screen, triple-screen, panoramic, or multi-monitor displays rather than merely similar images.
---

# One Image Across Screens

Build one continuous scene on a measured virtual canvas, then produce one high-quality wallpaper per display. Use the master scene as the composition contract; do not assume that enlarging small crops preserves enough detail. Never originate the screens as unrelated images.

## 1. Capture the setup

If the current conversation does not already contain one, ask first for a straight-on photo showing every display and its bezels. Require the photo unless the user explicitly declines; do not infer pixel geometry from it alone.

Then collect:

- two or three displays only; if more are present, ask which two or three to include;
- a screenshot of the operating system's display arrangement, or explicit left/right and vertical-offset relationships;
- native or intended wallpaper resolution and orientation for each display;
- approximate physical width or diagonal when displays differ visibly in size;
- whether to compensate for bezels or a physical gap;
- any desktop-icon or widget area that should remain quiet.

Do not ask again for information already visible or stated. Give each display a stable spatial ID such as `left-portrait`, `center-main`, or `right-upper`.

Explain briefly when needed: the desk photo establishes physical placement; the OS screenshot and resolutions establish exact output geometry. A photo by itself is not pixel-accurate.

## 2. Model and verify the canvas

Create a task-local `layout.json` using the schema documented by:

```bash
python3 scripts/wallpaper_layout.py schema
```

Use one common art-space scale across all displays. For equal-density displays, art dimensions may equal output pixels. For unequal physical sizes or pixel densities, make `art_width` and `art_height` proportional to physical screen dimensions; the script resamples each crop to its output resolution. Include bezel or air gaps in `art_x` and `art_y`, not in output dimensions.

Art-space coordinates describe physical composition, not guaranteed source resolution. A small display rectangle inside a generated master may contain far fewer source pixels than its final wallpaper requires.

Render and inspect a guide before choosing the artwork:

```bash
python3 scripts/wallpaper_layout.py guide \
  --layout layout.json --output layout-guide.png
```

Check screen count, orientation, left-to-right order, vertical offsets, relative physical scale, gaps, and the overall canvas aspect ratio. Correct the JSON rather than compensating in the art prompt.

## 3. Guide the art direction

Once geometry is sound, read [references/art-direction.md](references/art-direction.md). Do not offer vague generator-native labels such as `epic fantasy realism`, `painterly concept art`, `high-end 3D render`, or `cinematic AI art`. Guide the user progressively instead of dumping the full catalog:

1. Offer the five culturally grounded families with a short visual distinction and a recommendation based on the setup.
2. After the family is chosen, offer only its relevant historical movements, media, or visual traditions, with one or two known works as conceptual or compositional anchors when useful.
3. Offer a small set of philosophical or literary lenses that materially fit the subject. Do not name-drop a thinker without translating the idea into visible composition.
4. Ask for the subject or universe, mood/palette, and preferred cross-screen interaction. Combine these into two or three concrete scene concepts.
5. Let the user pick a concept or choose `surprise me`.

Use tappable options when available and keep each question focused. If the user already specified a theme or style, preserve it and ask only for decisions that materially affect the result.

Every concept must include:

- one identifiable artistic lineage, period, medium, or public-domain compositional reference;
- one philosophical or literary premise expressed through a concrete visual metaphor;
- one shared background plane or horizon;
- at least one unmistakable bridge across a seam, such as a beam, road, river, sword, tether, smoke trail, gaze, or cause-and-effect action;
- a distinct role for every screen rather than duplicated subjects;
- seam-safe focal placement and quiet zones requested by the user.

Apply the anti-generic test from the reference. If removing the named artistic and philosophical anchors would leave essentially the same prompt, the concept is not grounded enough. Do not proceed until the references change the image's composition, material, palette, or symbolism.

## 4. Generate one composition master

Use the image-generation capability to create a single master panorama at the virtual canvas aspect ratio. Include `layout-guide.png` as a geometry reference when possible, along with any user-supplied visual references. State that colored rectangles, borders, labels, and guide text must not appear in the artwork.

Describe the full scene spatially using display IDs and seams. Specify the shared horizon, crossing element, direction of action, lighting source, quiet zones, and which focal subject belongs on each screen. Do not merely request "matching wallpapers."

Include a compact cultural-direction block in the prompt:

- **Artistic lineage:** the selected movement, period, or medium and the concrete visual rules borrowed from it;
- **Philosophical premise:** the idea and the visible tension, metaphor, or staging that expresses it;
- **Material language:** paper, ink, grain, brushwork, photography, textile, glass, engraving, or another specific surface treatment;
- **Anti-generic constraints:** the stock AI tropes, default color grading, and unsupported spectacle to exclude.

Prefer movements, periods, media, and compositional principles over exact imitation of a named artist. Never request a living artist's style. Treat copyrighted works as intellectual references, then translate them into original visual grammar rather than copying a recognizable composition.

Generate the complete rectangular master first. This master proves the scene, placement, lighting, and crossings; it is not automatically the final-resolution source. Do not originate one image per monitor independently. Treat unused canvas gaps as non-display composition space, and keep critical faces, hands, text, or small details away from bezels unless the seam crossing is intentional.

## 5. Measure resolution before accepting crops

Analyze the approved master before treating any crop as final:

```bash
python3 scripts/wallpaper_layout.py analyze \
  --layout layout.json --master master.png
```

The report estimates how many source pixels each display crop actually contains and the linear enlargement required to reach its output resolution. Choose the delivery path per display:

- **Detailed, figurative, photographic, or painterly work:** accept a direct crop only when enlargement is at most `1.33x` and visual inspection confirms adequate detail.
- **Flat, abstract, silhouette, or deliberately soft work:** enlargement up to `2x` may be acceptable after inspection.
- **More than `2x`:** never silently deliver the enlarged crop as final. Re-render that display in HD unless the user explicitly accepts a draft-quality result.

Create draft crops for composition references:

```bash
python3 scripts/wallpaper_layout.py split \
  --layout layout.json --master master.png --output-dir wallpaper-drafts
```

The command emits exact-size draft crops, a fitted master, a manifest with quality diagnostics, and a spatial preview. Do not confuse exact pixel dimensions with native detail.

## 6. Re-render insufficient crops in HD

If any detailed crop exceeds `1.33x`, or if inspection shows softness, read [references/high-resolution-rendering.md](references/high-resolution-rendering.md). Use the full master and each draft crop as composition references, then ask the image-generation model to **faithfully re-render that screen with newly resolved detail** at its own aspect ratio. Do not ask for a generic upscale and do not redesign the scene.

Lock every cross-screen element with an anchor contract: source and destination edges, normalized edge positions, apparent width, direction, color, and lighting. Render the screen containing the origin or main subject first. Render connected screens sequentially, supplying the approved neighboring render as an additional reference. Never generate connected HD screens independently or in parallel.

Prefer this hybrid workflow for detailed art even if only one small display lacks density: keep acceptable direct crops, and re-render only insufficient screens. For flat or abstract styles, direct crops remain a valid quality-first choice because they preserve exact geometry.

Assemble the final HD wallpapers into a spatial preview:

```bash
python3 scripts/wallpaper_layout.py preview \
  --layout layout.json --input-dir wallpapers-hd \
  --output spatial-preview-hd.png
```

If an anchor misses, revise only the receiving screen with the master, its draft crop, and the approved neighboring screen as references. Do not restart unrelated screens.

## 7. Verify and deliver

Inspect the final preview and every full-resolution wallpaper. Verify:

- horizon, large contours, light, and crossing objects continue at the correct height;
- no focal subject is accidentally cut by a bezel;
- each output has the requested resolution and orientation;
- no labels, guide shapes, signatures, or accidental text remain;
- icon-safe areas retain adequate contrast and detail density.

If the master composition itself fails, revise the master. If only HD detail or an anchor fails, revise the affected screen without changing the composition. Use `--fit contain` only when preserving the entire master matters more than edge-to-edge coverage. Default `cover` is preferable when aspect ratios differ slightly.

Provide:

- the composition master and fitted master;
- one clearly named image per display;
- the final HD spatial preview;
- a concise mapping from file to physical screen;
- the recommended wallpaper fit mode, normally `Fill` or its OS equivalent with per-display wallpaper assignment.

Report which displays were direct crops and which were HD re-renders. Mention any remaining uncertainty in scale, bezel compensation, or generative anchor matching. Do not claim pixel-perfect physical continuity when exact display sizes or offsets were unavailable or when independently re-rendered edges were not deterministically seam-locked.
