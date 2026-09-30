---
name: create-continuous-multi-screen-wallpaper
description: Prepare continuous wallpapers for two or three monitors using physical layout, virtual-canvas geometry, per-screen crops, resolution checks, and seam verification. Supports mixed resolutions, orientations, sizes, and offsets.
---

# Multi-screen wallpaper production

This skill controls display geometry and image production only. Image content and the conversation guiding its creation remain with the base model and the user.

## 1. Establish the display geometry

Reuse the supplied or confirmed setup. Collect only missing technical inputs:

- two or three displays, each with a stable spatial ID;
- intended output width and height, in the installed orientation;
- left/right order and vertical offsets;
- active display width/height or diagonal when physical sizes differ;
- measured bezels/gaps and reserved screen regions, if requested.

A desk photo gives physical placement; an OS arrangement screenshot gives desktop relationships, not physical scale. Logical desktop points are not necessarily native pixels. Do not invent resolutions or measurements. Mark accepted physical estimates as approximate; add no unrequested gap compensation or reserved region.

Create a task-local `layout.json` using:

```bash
python3 scripts/wallpaper_layout.py schema
```

Keep output pixels separate from the shared art-space coordinates:

- `output_width/height`: exact exported pixel dimensions.
- `art_width/height`: active screen size at one common physical scale.
- `art_x/y`: screen position in that scale, including physical gaps.

For a diagonal `d` and width-to-height ratio `r`, active width is `d*r/sqrt(r*r+1)` and height is `d/sqrt(r*r+1)`. Convert every screen and gap to the same units. For portrait orientation, use the oriented ratio. Use output pixels as art units only when pixel densities are equal.

The canvas is the bounding rectangle of all screens. Do not independently normalize each display or turn bezel gaps into output pixels.

```bash
python3 scripts/wallpaper_layout.py guide \
  --layout layout.json --output layout-guide.png
```

Inspect screen count, orientation, offsets, relative physical sizes, gaps and overall aspect ratio. Fix the layout before image production.

## 2. Prepare the master and obtain approval

Use one complete master at the canvas aspect ratio. Supply the verified guide as a geometry reference when the image tool supports it; guide labels and frames must not become artwork. Technical constraints are screen bounds, crop boundaries, gaps and any user-requested reserved regions.

Show the full master and wait for explicit approval of that file/version before resolution analysis, draft crops, quality enhancement or per-screen delivery. Record approval in task notes. Approval of an idea or earlier version is insufficient.

If the master changes, show it again and renew approval. Detail refinement and seam corrections that preserve the approved composition do not require new master approval.

## 3. Measure detail and split

```bash
python3 scripts/wallpaper_layout.py analyze \
  --layout layout.json --master master.png
```

Inspect source crop dimensions and enlargement, not just output dimensions:

- At most `1.33x`: direct crops may suffice after inspection.
- Between `1.33x` and `2x`: inspect at target size; fine detail may require refinement.
- Above `2x`: refine the source or re-render the affected region unless the user explicitly accepts draft quality.

Resizing alone adds no native detail. Record actual generated dimensions and any final enlargement.

```bash
python3 scripts/wallpaper_layout.py split \
  --layout layout.json --master master.png --output-dir wallpaper-drafts
```

The helper emits crops, a fitted master, a quality manifest and a spatial preview. Use the same fit mode for analysis and splitting: `cover` fills the canvas with a centered crop; `contain` preserves the source with padding. Avoid `stretch` unless explicitly requested. A large aspect mismatch requires checking the fitted framing before delivery.

## 4. Refine insufficient regions without losing alignment

When more source detail is needed, read [references/high-resolution-rendering.md](references/high-resolution-rendering.md).

Prefer a sufficiently detailed shared master and deterministic crops when exact seams matter. If per-screen re-rendering is necessary, keep the approved crop geometry and shared boundaries fixed, supply neighboring outputs as references, and process connected displays sequentially.

Resize each accepted render only once to its final dimensions. Use the filenames expected by the helper:

```text
wallpaper-<safe-display-id>-<width>x<height>.png
```

## 5. Verify and deliver

```bash
python3 scripts/wallpaper_layout.py preview \
  --layout layout.json --input-dir wallpapers-hd --output spatial-preview-hd.png
```

Inspect the spatial preview and each full-resolution output. Check dimensions, orientation, crop fidelity, boundary positions/tangents, scale, color and brightness across gaps, and requested reserved regions. Correct the affected output without moving unrelated regions. A layout or composition change requires new approval.

Provide the master, fitted master, per-display PNGs, final spatial preview and file-to-screen mapping. State which files are direct crops or re-renders, their actual source dimensions, and any final resize. Recommend the appropriate OS fit mode, normally Fill.

Do not claim pixel-perfect physical alignment from estimated measurements or fully generative redraws. Report unresolved geometry or seam differences. Producing the files does not authorize changing the user's OS settings.
