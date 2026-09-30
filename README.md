# One Image Across Screens

Technical production for continuous wallpapers across two or three monitors: physical layout, virtual-canvas geometry, exact-size crops, source-resolution checks and seam verification.

The base model handles image creation and the conversation with the user. This skill does not impose a creative questionnaire or image content.

## Workflow

1. Establish resolutions, orientations, physical sizes, offsets and gaps.
2. Model the setup in `layout.json` and inspect its guide.
3. Obtain explicit approval of the complete master image.
4. Analyze crop resolution, split, and refine insufficient regions if needed.
5. Verify the spatial preview and deliver one file per display.

Supports unequal pixel densities, portrait displays and offset layouts. Output pixels and physical art-space coordinates are separate. Physical estimates and generative seam limitations must be disclosed.

## Install

```bash
git clone https://github.com/maax6/create-continuous-multi-screen-wallpaper.git \
  ~/.codex/skills/create-continuous-multi-screen-wallpaper
python3 -m pip install Pillow
```

Invoke:

```text
$create-continuous-multi-screen-wallpaper
```

## Layout helper

```bash
python3 scripts/wallpaper_layout.py schema

python3 scripts/wallpaper_layout.py guide \
  --layout layout.json --output layout-guide.png
```

After approval of the displayed master:

```bash
python3 scripts/wallpaper_layout.py analyze \
  --layout layout.json --master master.png

python3 scripts/wallpaper_layout.py split \
  --layout layout.json --master master.png --output-dir wallpaper-drafts

python3 scripts/wallpaper_layout.py preview \
  --layout layout.json --input-dir wallpapers-hd --output spatial-preview-hd.png
```

Use the same `--fit` mode for analysis and splitting. The default is `cover`; `contain` adds padding, and `stretch` changes proportions.

The helper's quality recommendations depend on enlargement: up to 1.33×, direct crop subject to inspection; up to 2×, inspect or refine; above 2×, refinement required unless draft quality is explicitly accepted. Exact output dimensions do not imply native detail.

## Requirements and outputs

Python 3.10+ and Pillow. An image-generation/refinement capability is needed only when creating or refining image content; an adequate existing master can be cropped directly.

Deliverables: master, fitted master, per-display PNGs, spatial preview, file-to-screen mapping and actual source/final dimensions. OS wallpaper settings are not changed automatically.

See [SKILL.md](SKILL.md) and the [resolution and seam reference](references/high-resolution-rendering.md).
