# One Image Across Screens

A Codex skill for creating one continuous high-resolution wallpaper across two or three displays, including mixed resolutions, portrait screens, unequal physical sizes, bezels, gaps, and vertical offsets.

The workflow builds a measured virtual canvas, generates one composition master, checks the source-pixel density available to every crop, and re-renders individual displays when a direct crop would be too soft.

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
- Quality analysis before accepting enlarged crops
- Sequential HD re-rendering with cross-screen anchor contracts

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

