# High-resolution refinement and seam control

Use after master approval and a resolution report showing insufficient source detail. Keep the approved image unchanged in framing and content; this reference governs technical fidelity only.

## Choose the production route

- If the shared master has enough native detail, crop it deterministically.
- If a full-master refinement can supply enough detail, perform it before slicing and verify that the geometry is preserved.
- Otherwise, re-render only insufficient screen regions using their exact draft crops. If an output remains below its target resolution, report the final enlargement.

Independent generative re-renders cannot guarantee pixel-perfect seams. For tight bezels, prefer a shared master or a mask-capable refinement that preserves a shared boundary corridor. Do not hide a seam mismatch with unreported repositioning or stretching.

## Record boundary constraints

For each feature already crossing a display boundary, record:

- source and destination screen IDs and edges;
- intersection positions and visible width as percentages along each edge;
- direction/tangent and depth order;
- color, brightness and texture at the boundary;
- continuation through the measured invisible gap.

Record existing features, not new content requirements. A contour or tonal gradient is as valid a boundary constraint as any other image feature.

## Refine sequentially

1. Select an anchor screen and refine it using the master and its exact draft crop.
2. Verify its framing, silhouette, boundary intersections and appearance against the approved master.
3. Refine each connected screen with the master, its own crop and the accepted neighboring render. When two accepted neighbors constrain an output, include both.
4. Correct only the receiving region if its boundary drifts. Preserve unrelated regions.

Use direct crops unchanged wherever they already pass the quality check.

## Technical prompt fields

Pass only the information relevant to the operation:

```text
Target: <display ID>, <output dimensions and aspect ratio>.
Inputs:
- full approved master: global appearance and geometry reference;
- target draft crop: exact output framing;
- neighboring accepted render(s), if any: boundary reference.

Task: Resolve additional native detail within this crop without changing its
camera, framing, shapes, feature locations, colors, lighting or depth order.
Keep all intentionally cropped features cut off at the same edges.
Preserve <edge>, <intersection percentages>, <width>, <tangent> and
<boundary appearance> from the supplied references.
Return only this display's image, without guides or a monitor mockup.
```

This is a fidelity specification, not a prescription for image content.

## Size and verify

Request the target aspect ratio and available detail, then inspect the returned pixel dimensions. Do not infer native resolution from a requested size. If needed, resize once at the end and report the factor.

Save `wallpaper-<safe-display-id>-<width>x<height>.png` and rebuild the spatial preview with `wallpaper_layout.py preview`.

Inspect both native-detail sharpness and the assembled boundaries. Compare crop intersections, tangent directions, scale, color and brightness at each junction. If exact alignment remains unattainable, state the limitation and offer a shared-master or locked-boundary route; do not claim success from output dimensions alone.
