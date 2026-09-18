# High-resolution per-screen rendering

Read this reference after the composition master is approved and the quality report shows that one or more crops lack sufficient source pixels.

## Principle

The master is the composition contract. Each per-screen HD image is a faithful semantic re-render of one master region, not a new interpretation and not a conventional pixel upscale. The generator should spend its full image budget on that display while preserving the master’s geometry, lighting, palette, and cross-screen anchors.

The selected artistic lineage, philosophical premise, and material grammar are also invariants. A re-render that becomes smoother, more spectacular, more game-like, or more generically `cinematic` has failed even if its geometry is correct.

Use direct crops when they already contain enough source detail. Re-render only the insufficient screens.

## Record a crossing contract

For every object that crosses between displays, record:

- crossing name and visual role;
- origin display and edge;
- exit position as a percentage along that edge;
- destination display and edge;
- entry position as a percentage along that edge;
- apparent width as a percentage of each edge;
- direction or tangent angle;
- dominant colors, brightness, and depth order;
- what continues invisibly through the bezel or physical gap.

Use normalized percentages rather than master pixels in generation prompts. A broad beam exiting at `72%` of a bottom edge and entering at `8%` of a top edge is more robust than a fragile absolute coordinate.

Prefer one large, simple crossing shape. Keep faces, fingers, text, and other identity-sensitive details away from the crossing corridor.

## Render order

1. Choose the anchor display: normally the display containing the crossing’s origin, main subject, or dominant structure.
2. Re-render it first from the master and its draft crop.
3. Approve its composition before continuing.
4. Re-render each connected display sequentially. Supply the master, that display’s draft crop, and the approved neighboring render as separate references with explicit roles.
5. If a screen connects two neighbors, include both approved neighbors and preserve both anchor contracts.

Do not generate connected screens in parallel. Parallel generation removes the opportunity to condition later screens on the approved boundary geometry.

## Prompt scaffold

Adapt this scaffold to each display:

```text
Use case: stylized-concept
Asset type: high-resolution wallpaper for <display-id>, <output aspect and resolution>

Primary request: Faithfully re-render the <display-id> region of the approved master with newly resolved native detail. This is not a new composition and not a generic upscale.

Input images:
- Image 1: approved full composition master; global geometry, palette, lighting, and story reference.
- Image 2: draft crop for <display-id>; framing and object-placement reference.
- Image 3: approved neighboring wallpaper; boundary-anchor and rendering-fidelity reference.

Cultural direction:
- Artistic lineage: <movement, period, medium, and its concrete visual rules>.
- Philosophical premise: <idea expressed through a visible relation or metaphor>.
- Material grammar: <surface, mark-making, grain, printing, lens, paint, or craft behavior>.

Preserve exactly:
- the draft crop’s camera, horizon, major silhouettes, object positions, and negative space;
- the master’s light direction, atmosphere, palette, and depth order;
- the approved lineage, premise, and material imperfections; do not replace them with a generic digital finish;
- <crossing> exiting/entering the <edge> at <position%>, width <width%>, angle <angle>, with <color/light description>;
- requested icon-safe areas.

Add detail only inside the established forms: material texture, fine environment detail, clean edges, and natural micro-contrast. Do not add, remove, relocate, or reinterpret major subjects.

Constraints: no text, labels, logos, signatures, watermark, border, duplicated subject, guide shapes, or new crossing elements. No stock AI fantasy, game key art, ornamental particles, unsupported cyan glow, excessive volumetric fog, or digitally smooth surfaces unless explicitly required by the approved direction.
```

Describe each input’s role explicitly. Avoid vague phrases such as “make it similar,” “matching wallpaper,” or “upscale this.”

## Boundary strategy

For displays separated by a visible physical gap, semantic anchor matching is usually sufficient: the missing space hides small pixel differences. Keep the crossing broad and tolerate only small positional drift.

For touching displays or very thin bezels, independent re-rendering cannot guarantee a pixel-perfect seam. Use one of these routes:

1. Generate a master with enough native resolution to crop directly.
2. Preserve a narrow shared boundary corridor from the master and refine only the interiors with a mask-capable edit, feathering into the locked corridor.
3. Use flat, abstract, silhouette, fog, glow, or other seam-tolerant art where small texture differences are invisible.

Do not claim exact continuity from two fully independent generative redraws.

## Output sizing

Ask the image generator for the display’s aspect ratio and highest available detail. If it still returns fewer pixels than the native wallpaper resolution, resize only once at the end. A full-frame per-screen render followed by a moderate resize retains substantially more detail than enlarging a small crop extracted from a multi-display master.

Save each approved render with the deterministic filename expected by the preview command:

```text
wallpaper-<safe-display-id>-<width>x<height>.png
```

## Final correction loop

Build the HD spatial preview and inspect the crossing at normal size and zoomed out. If a mismatch remains, edit only the receiving display and restate:

- its exact anchor percentages;
- the neighboring display as an invariant reference;
- the instruction to keep every unrelated region unchanged.

Stop when the physical preview reads as one action and each individual file retains adequate detail. If exact geometry remains impossible with the available generator, explain the limitation and offer the seam-locked or seam-tolerant route instead of hiding the mismatch.
