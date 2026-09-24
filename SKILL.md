---
name: create-continuous-multi-screen-wallpaper
description: Guide a user from a plain-language image idea through an adaptive creative funnel, then create one culturally grounded, narrative, high-resolution scene across two or three monitors. Use for portrait screens, mixed resolutions, unequal physical sizes, and vertically offset arrangements when the displays should interact through one continuous scene rather than show merely similar images.
---

# One Image Across Screens

Build one authored scene on a measured virtual canvas, then produce one high-quality wallpaper per display. Every display must carry a distinct narrative beat, interact with at least one other display, and participate in a visible physical junction across a seam or gap. Use the master scene as the composition contract; do not assume that enlarging small crops preserves enough detail. Never originate the screens as unrelated images or accept mere visual similarity as continuity.

The scene may be real, reconstructed, altered, dreamlike, fully imaginary, or symbolic. It may be quiet, playful, intimate, adventurous, documentary, spectacular, absurd, satirical, dramatic, or something described entirely in the user's own words. Do not assume conflict, tension, philosophy, or a moral message before the user chooses one.

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

Once geometry is sound, read [references/art-direction.md](references/art-direction.md) and run its complete creative funnel. Begin neutrally:

1. Invite a plain-language description of the desired image. Fragments are enough: subjects, place, period, action, colors, atmosphere, or any image the user has in mind. Do not ask for an art movement, tension, or message first.
2. Offer the option to paste or upload visual-identity references. If supplied, translate only their observable palette, contrast, spatial density, edge quality, texture, material, lighting, and image-making process into reusable direction.
3. Clarify the scene's degree of reality: observed real, reconstructed or historical, plausibly altered, dreamlike or surreal, fully imaginary or speculative, or symbolic and graphic. Offer `no preference`.
4. Clarify what carries the scene: people or characters, animals or creatures, machines or objects, architecture or places, landscape or natural forces, or a mixture. Ask for relationships or actions only when they are not already described.
5. Clarify the scene mode and register without privileging drama: observation, encounter, journey, work, ritual, discovery, transformation, confrontation, rescue, contemplation, play, humor, absurdity, satire, celebration, or another user-written intention.
6. Clarify scale, rhythm, and density only when useful: intimate, group, or monumental; still, flowing, or kinetic; sparse, balanced, or abundant.
7. Offer four to six deliberately contrasting visual territories from the reference atlas. Vary period, geography, medium, spatial logic, and energy; include one unexpected but coherent route and recommend one based on the accumulated brief and monitor geometry.
8. Within the chosen territory, offer four to six specific lineages. Then narrow the selected lineage to three interpretations that vary composition, material, viewpoint, palette, or tempo without changing artistic branch.
9. Offer an optional narrative, literary, philosophical, humorous, or satirical lens only when it would add something the user wants. `No added lens` must always be valid.
10. Propose two or three ways to distribute the chosen subject across the screens, including the screen-specific beats, cross-screen interaction, and robust physical junction. Combine the locked choices into two or three complete scene concepts.
11. Let the user choose a concept or `surprise me`.

Use tappable options when available and ask one decision level at a time. Whenever the user has already answered a gate in ordinary language, infer it, summarize it, and skip that gate. At every stage, state what the choice changes visibly, mark a recommendation where useful, recap what is locked, and retire unchosen branches unless the user reopens them. Never turn the funnel into a questionnaire that repeats settled information.

Treat supplied identity images as visual-grammar references, not permission to copy a recognizable composition or imitate a living artist's exact style. Variety belongs in the exploration, not the final blend. The final direction must remain coherent: one dominant lineage, at most one supporting lineage with a precise job, one composition engine, and one material grammar. A conceptual lens is optional.

Every concept must include:

- a one-sentence synopsis saying what is present, what happens or changes, and how another part of the scene responds; use an active verb without requiring conflict;
- the scene carriers and their visible relationships;
- a beat map assigning every screen a distinct narrative role such as initiator, passage, response, reveal, or consequence;
- one identifiable artistic lineage, period, medium, or public-domain compositional reference;
- a clear scene mode and register, plus an optional conceptual lens when the user wants one;
- one unmistakable interaction between screens, such as shared observation, accompaniment, exchange, journey, work, play, dialogue, transformation, pursuit, rescue, confrontation, or cause and effect;
- one physical junction integral to that interaction, such as a passed object, outstretched gesture, rope, road, river, train, fabric, shadow, smoke trail, projectile, or architectural structure that exits one display edge and enters the corresponding edge of another;
- a shared background plane, horizon, lighting field, or spatial system that supports the action without substituting for it;
- seam-safe focal placement and quiet zones requested by the user.

Apply the scene and anti-generic tests from the reference. Reject a concept if its crops would still work unchanged as unrelated standalone wallpapers, if removing one display would leave the same scene relationship intact, or if the only connection is a horizon, palette, atmosphere, or recurring motif. If removing the dominant lineage, composition engine, material grammar, and any optional lens would leave essentially the same prompt, the direction is not grounded enough. Do not proceed until the chosen artistic construction changes the image's staging, viewpoint, material, palette, rhythm, or symbolism.

## 4. Generate one composition master

Use the image-generation capability to create a single master panorama at the virtual canvas aspect ratio. Include `layout-guide.png` as a geometry reference when possible, along with any user-supplied visual references. In the prompt, name the observable traits to borrow from each identity reference while requiring an original composition and content. State that colored rectangles, borders, labels, and guide text must not appear in the artwork.

Describe the full scene spatially using display IDs and seams. Specify the story sentence, cast or forces, beat on every display, interaction, shared world, direction of action, lighting source, quiet zones, and exact physical junction. The junction must exit one named edge and enter the corresponding edge at compatible positions. Do not merely request "matching wallpapers" or a continuous landscape.

Include a compact cultural-direction block in the prompt:

- **Plain-language brief:** the user's own description, preserved without adding an unrequested theme;
- **Reality mode:** real, reconstructed, altered, dreamlike, imaginary, speculative, symbolic, or another user-defined mode;
- **Scene carriers:** the people, characters, creatures, objects, machines, places, architecture, landscape, or forces that visibly carry the image;
- **Scene mode and register:** what kind of event or moment this is, including humor or satire only when chosen;
- **Scene synopsis:** who or what acts, toward whom or what, and what visibly changes;
- **Beat map:** the distinct narrative function and principal action assigned to each display;
- **Cross-screen interaction:** the shared observation, accompaniment, exchange, journey, work, play, dialogue, reveal, transformation, pursuit, rescue, confrontation, or cause and effect that makes the screens depend on one another;
- **Physical junction:** the specific object, gesture, path, force, shadow, or structure that crosses each seam, with source and destination edges;
- **Artistic lineage:** the dominant movement, period, or medium and the concrete visual rules borrowed from it, plus at most one supporting lineage with its exact purpose;
- **Composition engine:** the locked interpretation's viewpoint, spatial rhythm, tempo, scale, and direction of action;
- **Optional lens:** the narrative, literary, philosophical, humorous, or satirical idea and its visible effect, or `none`;
- **Material language:** paper, ink, grain, brushwork, photography, textile, glass, engraving, or another specific surface treatment;
- **Anti-generic constraints:** the stock AI tropes, default color grading, and unsupported spectacle to exclude.

Prefer movements, periods, media, and compositional principles over exact imitation of a named artist. Never request a living artist's style. Treat copyrighted works as intellectual references, then translate them into original visual grammar rather than copying a recognizable composition.

Generate the complete rectangular master first. This master proves the scene, beat progression, interaction, placement, lighting, and junctions; it is not automatically the final-resolution source. Compose one scene, not a row of self-contained vignettes. Do not originate one image per monitor independently. Treat unused canvas gaps as non-display composition space, and keep critical faces, hands, text, or small details away from bezels unless the seam crossing is intentional and broad enough to survive re-rendering.

## 5. Measure resolution before accepting crops

Analyze the approved master before treating any crop as final:

```bash
python3 scripts/wallpaper_layout.py analyze \
  --layout layout.json --master master.png
```

The report estimates how many source pixels each display crop actually contains and the linear enlargement required to reach its output resolution. Choose the delivery path per display:

- **Detailed, figurative, photographic, or painterly work:** accept a direct crop only when enlargement is at most `1.33x` and visual inspection confirms adequate detail.
- **Graphic narrative work with large shapes, silhouettes, or deliberately soft material treatment:** enlargement up to `2x` may be acceptable after inspection, but the scene and interaction requirements still apply.
- **More than `2x`:** never silently deliver the enlarged crop as final. Re-render that display in HD unless the user explicitly accepts a draft-quality result.

Create draft crops for composition references:

```bash
python3 scripts/wallpaper_layout.py split \
  --layout layout.json --master master.png --output-dir wallpaper-drafts
```

The command emits exact-size draft crops, a fitted master, a manifest with quality diagnostics, and a spatial preview. Do not confuse exact pixel dimensions with native detail.

## 6. Re-render insufficient crops in HD

If any detailed crop exceeds `1.33x`, or if inspection shows softness, read [references/high-resolution-rendering.md](references/high-resolution-rendering.md). Use the full master and each draft crop as composition references, then ask the image-generation model to **faithfully re-render that screen with newly resolved detail** at its own aspect ratio. Do not ask for a generic upscale and do not redesign the scene.

Lock every cross-screen element with an anchor contract: narrative role, source and destination edges, normalized edge positions, apparent width, direction, color, lighting, and the action it carries. Render the screen containing the initiating action or main subject first. Render connected screens sequentially, supplying the approved neighboring render as an additional reference. Never generate connected HD screens independently or in parallel.

Prefer this hybrid workflow for detailed art even if only one small display lacks density: keep acceptable direct crops, and re-render only insufficient screens. For graphic narrative scenes with large, materially simple forms, direct crops remain a valid quality-first choice because they preserve exact geometry.

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
- every display contributes a readable beat, the interaction remains legible, and the junction carries the action across the physical gap;
- removing any display would make the intended narrative incomplete rather than merely narrower;
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
