# One Image Across Screens

A Codex skill for developing an image from an ordinary verbal description, then creating one culturally grounded continuous scene across two or three displays, including mixed resolutions, portrait screens, unequal physical sizes, bezels, gaps, and vertical offsets.

The adaptive creative funnel can move from real to unreal, identify the scene's people, creatures, objects, places, or natural forces, explore quiet, playful, adventurous, documentary, humorous, satirical, dramatic, and other user-defined registers, and narrow a broad artistic atlas into one coherent direction. The production workflow then gives every screen a distinct beat, requires an interaction and a physical junction, builds a measured virtual canvas, generates one composition master, checks source-pixel density, and re-renders individual displays when a direct crop would be too soft.


https://github.com/user-attachments/assets/aca8e260-bdc1-4f7f-8e47-68841f347f00

## Install

```bash
git clone https://github.com/maax6/create-continuous-multi-screen-wallpaper.git \
  ~/.codex/skills/create-continuous-multi-screen-wallpaper
python3 -m pip install Pillow
```

Restart Codex after installation, then invoke:

```text
$create-continuous-multi-screen-wallpaper
```

## What it supports

- Two- and three-display desks
- Landscape and portrait displays
- Mixed native resolutions and pixel densities
- Unequal physical display sizes
- Vertical offsets, bezels, and physical air gaps
- Icon-safe and widget-safe quiet zones
- A plain-language starting point with an adaptive, non-repetitive creative funnel
- Real, reconstructed, altered, dreamlike, imaginary, speculative, and symbolic scenes
- People, characters, animals, creatures, objects, machines, architecture, landscapes, and natural forces
- Quiet, playful, intimate, adventurous, documentary, humorous, absurd, satirical, dramatic, and user-defined registers
- Diverse historical, vernacular, photographic, performative, craft, popular, and digital art directions
- A distinct narrative role for every display
- Cross-screen interaction and a story-bearing physical junction
- Rejection of merely similar wallpapers or decorative continuity without a shared event
- Quality analysis before accepting enlarged crops
- Sequential HD re-rendering that preserves narrative and cross-screen anchor contracts

## Layout helper

Print the `layout.json` schema:

```bash
python3 scripts/wallpaper_layout.py schema
```

Render a measured layout guide:

```bash
python3 scripts/wallpaper_layout.py guide \
  --layout layout.json \
  --output layout-guide.png
```

Analyze a composition master and estimate enlargement per display:

```bash
python3 scripts/wallpaper_layout.py analyze \
  --layout layout.json \
  --master master.png
```

Create draft crops and a spatial preview:

```bash
python3 scripts/wallpaper_layout.py split \
  --layout layout.json \
  --master master.png \
  --output-dir wallpaper-drafts
```

Assemble final per-display renders into a physical-layout preview:

```bash
python3 scripts/wallpaper_layout.py preview \
  --layout layout.json \
  --input-dir wallpapers-hd \
  --output spatial-preview-hd.png
```

## Requirements

- Python 3.10+
- Pillow
- An image-generation capability available to the agent

See [SKILL.md](SKILL.md) for the full workflow and quality rules.
