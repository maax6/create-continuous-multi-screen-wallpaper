#!/usr/bin/env python3
"""Build layout guides, measure crop quality, split masters, and preview wallpapers."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc


PALETTE = ("#2563EB", "#7C3AED", "#DB2777")
SCHEMA = {
    "name": "my-desk",
    "background": "#090B10",
    "monitors": [
        {
            "id": "left-portrait",
            "output_width": 1080,
            "output_height": 1920,
            "art_x": 0,
            "art_y": 0,
            "art_width": 1080,
            "art_height": 1920,
        },
        {
            "id": "center-main",
            "output_width": 2560,
            "output_height": 1440,
            "art_x": 1120,
            "art_y": 300,
            "art_width": 2560,
            "art_height": 1440,
        },
    ],
}


def positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number")
    result = int(round(value))
    if result <= 0:
        raise ValueError(f"{label} must be positive")
    return result


def number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number")
    return float(value)


def load_layout(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read layout JSON: {exc}") from exc

    monitors = data.get("monitors")
    if not isinstance(monitors, list) or not 2 <= len(monitors) <= 3:
        raise ValueError("layout must contain exactly 2 or 3 monitors")

    seen: set[str] = set()
    normalized = []
    for index, raw in enumerate(monitors):
        if not isinstance(raw, dict):
            raise ValueError(f"monitor {index + 1} must be an object")
        monitor_id = str(raw.get("id", "")).strip()
        if not monitor_id or monitor_id in seen:
            raise ValueError("each monitor needs a unique non-empty id")
        seen.add(monitor_id)
        normalized.append(
            {
                "id": monitor_id,
                "output_width": positive_int(raw.get("output_width"), f"{monitor_id}.output_width"),
                "output_height": positive_int(raw.get("output_height"), f"{monitor_id}.output_height"),
                "art_x": number(raw.get("art_x"), f"{monitor_id}.art_x"),
                "art_y": number(raw.get("art_y"), f"{monitor_id}.art_y"),
                "art_width": positive_int(raw.get("art_width"), f"{monitor_id}.art_width"),
                "art_height": positive_int(raw.get("art_height"), f"{monitor_id}.art_height"),
            }
        )

    data["monitors"] = normalized
    data["background"] = str(data.get("background", "#090B10"))
    return data


def bounds(monitors: list[dict[str, Any]]) -> tuple[float, float, float, float]:
    min_x = min(m["art_x"] for m in monitors)
    min_y = min(m["art_y"] for m in monitors)
    max_x = max(m["art_x"] + m["art_width"] for m in monitors)
    max_y = max(m["art_y"] + m["art_height"] for m in monitors)
    return min_x, min_y, max_x, max_y


def check_overlaps(monitors: list[dict[str, Any]]) -> None:
    for index, a in enumerate(monitors):
        for b in monitors[index + 1 :]:
            overlap_x = min(a["art_x"] + a["art_width"], b["art_x"] + b["art_width"]) - max(
                a["art_x"], b["art_x"]
            )
            overlap_y = min(a["art_y"] + a["art_height"], b["art_y"] + b["art_height"]) - max(
                a["art_y"], b["art_y"]
            )
            if overlap_x > 0 and overlap_y > 0:
                raise ValueError(f"art rectangles overlap: {a['id']} and {b['id']}")


def safe_name(value: str) -> str:
    result = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-.")
    return result or "monitor"


def wallpaper_filename(monitor: dict[str, Any]) -> str:
    return (
        f"wallpaper-{safe_name(monitor['id'])}-"
        f"{monitor['output_width']}x{monitor['output_height']}.png"
    )


def fit_master(image: Image.Image, width: int, height: int, mode: str, background: str) -> Image.Image:
    image = image.convert("RGB")
    if mode == "stretch":
        return image.resize((width, height), Image.Resampling.LANCZOS)

    if mode == "cover":
        scale = max(width / image.width, height / image.height)
    else:
        scale = min(width / image.width, height / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    if mode == "cover":
        left = (resized.width - width) // 2
        top = (resized.height - height) // 2
        return resized.crop((left, top, left + width, top + height))

    canvas = Image.new("RGB", (width, height), background)
    canvas.paste(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    return canvas


def quality_recommendation(max_enlargement: float) -> str:
    if max_enlargement <= 1.33:
        return "direct-crop-detailed-ok"
    if max_enlargement <= 2.0:
        return "direct-crop-abstract-only-or-hd-rerender"
    return "hd-rerender-required"


def build_quality_report(
    layout: dict[str, Any], master: Image.Image, fit: str
) -> dict[str, Any]:
    monitors = layout["monitors"]
    min_x, min_y, max_x, max_y = bounds(monitors)
    canvas_w = math.ceil(max_x - min_x)
    canvas_h = math.ceil(max_y - min_y)

    if fit == "stretch":
        scale_x = canvas_w / master.width
        scale_y = canvas_h / master.height
    else:
        scales = (canvas_w / master.width, canvas_h / master.height)
        scale = max(scales) if fit == "cover" else min(scales)
        scale_x = scale_y = scale

    monitor_reports = []
    for monitor in monitors:
        source_crop_w = monitor["art_width"] / scale_x
        source_crop_h = monitor["art_height"] / scale_y
        enlargement_x = monitor["output_width"] / source_crop_w
        enlargement_y = monitor["output_height"] / source_crop_h
        max_enlargement = max(enlargement_x, enlargement_y)
        monitor_reports.append(
            {
                "id": monitor["id"],
                "estimated_source_crop": [round(source_crop_w, 1), round(source_crop_h, 1)],
                "output_resolution": [monitor["output_width"], monitor["output_height"]],
                "linear_enlargement": [round(enlargement_x, 2), round(enlargement_y, 2)],
                "max_linear_enlargement": round(max_enlargement, 2),
                "recommendation": quality_recommendation(max_enlargement),
            }
        )

    return {
        "source_resolution": [master.width, master.height],
        "canvas_resolution": [canvas_w, canvas_h],
        "fit": fit,
        "source_to_canvas_scale": [round(scale_x, 4), round(scale_y, 4)],
        "monitors": monitor_reports,
    }


def print_quality_report(report: dict[str, Any]) -> None:
    for monitor in report["monitors"]:
        source_w, source_h = monitor["estimated_source_crop"]
        output_w, output_h = monitor["output_resolution"]
        factor = monitor["max_linear_enlargement"]
        recommendation = monitor["recommendation"]
        stream = sys.stderr if factor > 1.33 else sys.stdout
        print(
            f"quality: {monitor['id']} source crop ≈ {source_w:g}x{source_h:g} -> "
            f"{output_w}x{output_h}; enlargement {factor:g}x [{recommendation}]",
            file=stream,
        )


def analyze_master(layout: dict[str, Any], master_path: Path, fit: str) -> None:
    try:
        with Image.open(master_path) as master:
            report = build_quality_report(layout, master, fit)
    except OSError as exc:
        raise ValueError(f"Cannot open master image: {exc}") from exc
    print_quality_report(report)
    print(json.dumps(report, indent=2))


def draw_guide(layout: dict[str, Any], output: Path, max_edge: int) -> None:
    monitors = layout["monitors"]
    check_overlaps(monitors)
    min_x, min_y, max_x, max_y = bounds(monitors)
    canvas_w = max_x - min_x
    canvas_h = max_y - min_y
    scale = min(1.0, max_edge / max(canvas_w, canvas_h))
    width = max(1, math.ceil(canvas_w * scale))
    height = max(1, math.ceil(canvas_h * scale))
    image = Image.new("RGB", (width, height), layout["background"])
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for index, monitor in enumerate(monitors):
        x0 = round((monitor["art_x"] - min_x) * scale)
        y0 = round((monitor["art_y"] - min_y) * scale)
        x1 = round((monitor["art_x"] + monitor["art_width"] - min_x) * scale) - 1
        y1 = round((monitor["art_y"] + monitor["art_height"] - min_y) * scale) - 1
        color = PALETTE[index]
        draw.rectangle((x0, y0, x1, y1), fill=color, outline="white", width=max(1, round(3 * scale)))
        label = (
            f"{monitor['id']} | {monitor['output_width']}x{monitor['output_height']} output | "
            f"{monitor['art_width']}x{monitor['art_height']} art"
        )
        box = draw.textbbox((0, 0), label, font=font)
        pad = 5
        draw.rectangle(
            (x0 + 8, y0 + 8, x0 + 8 + box[2] + pad * 2, y0 + 8 + box[3] + pad * 2),
            fill="#000000",
        )
        draw.text((x0 + 8 + pad, y0 + 8 + pad), label, fill="white", font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(f"guide: {output} ({width}x{height})")
    print(f"art canvas: {round(canvas_w)}x{round(canvas_h)}; aspect {canvas_w / canvas_h:.4f}")


def split_master(layout: dict[str, Any], master_path: Path, output_dir: Path, fit: str) -> None:
    monitors = layout["monitors"]
    check_overlaps(monitors)
    min_x, min_y, max_x, max_y = bounds(monitors)
    canvas_w = math.ceil(max_x - min_x)
    canvas_h = math.ceil(max_y - min_y)
    try:
        master = Image.open(master_path)
    except OSError as exc:
        raise ValueError(f"Cannot open master image: {exc}") from exc

    quality_report = build_quality_report(layout, master, fit)
    print_quality_report(quality_report)

    source_aspect = master.width / master.height
    target_aspect = canvas_w / canvas_h
    delta = abs(source_aspect - target_aspect) / target_aspect
    if delta > 0.01:
        print(
            f"warning: master aspect differs from art canvas by {delta:.1%}; fit mode '{fit}' will alter framing",
            file=sys.stderr,
        )

    fitted = fit_master(master, canvas_w, canvas_h, fit, layout["background"])
    output_dir.mkdir(parents=True, exist_ok=True)
    fitted.save(output_dir / "master-fitted.png")

    preview = Image.new("RGB", (canvas_w, canvas_h), layout["background"])
    draw = ImageDraw.Draw(preview)
    quality_by_id = {item["id"]: item for item in quality_report["monitors"]}
    manifest = {
        "master": str(master_path),
        "fit": fit,
        "canvas": [canvas_w, canvas_h],
        "quality": quality_report,
        "outputs": [],
    }

    for monitor in monitors:
        left = round(monitor["art_x"] - min_x)
        top = round(monitor["art_y"] - min_y)
        right = left + monitor["art_width"]
        bottom = top + monitor["art_height"]
        crop = fitted.crop((left, top, right, bottom))
        wallpaper = crop.resize(
            (monitor["output_width"], monitor["output_height"]), Image.Resampling.LANCZOS
        )
        filename = wallpaper_filename(monitor)
        wallpaper.save(output_dir / filename)
        preview.paste(crop, (left, top))
        draw.rectangle((left, top, right - 1, bottom - 1), outline="white", width=2)
        manifest["outputs"].append(
            {
                "id": monitor["id"],
                "file": filename,
                "resolution": [monitor["output_width"], monitor["output_height"]],
                "art_box": [left, top, right, bottom],
                "quality": quality_by_id[monitor["id"]],
            }
        )
        print(f"wallpaper: {output_dir / filename}")

    preview_scale = min(1.0, 2400 / max(preview.width, preview.height))
    if preview_scale < 1.0:
        preview = preview.resize(
            (round(preview.width * preview_scale), round(preview.height * preview_scale)),
            Image.Resampling.LANCZOS,
        )
    preview.save(output_dir / "spatial-preview.png")
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"preview: {output_dir / 'spatial-preview.png'}")


def preview_wallpapers(
    layout: dict[str, Any], input_dir: Path, output: Path, max_edge: int
) -> None:
    monitors = layout["monitors"]
    check_overlaps(monitors)
    min_x, min_y, max_x, max_y = bounds(monitors)
    canvas_w = math.ceil(max_x - min_x)
    canvas_h = math.ceil(max_y - min_y)
    preview = Image.new("RGB", (canvas_w, canvas_h), layout["background"])

    for monitor in monitors:
        path = input_dir / wallpaper_filename(monitor)
        try:
            wallpaper = Image.open(path).convert("RGB")
        except OSError as exc:
            raise ValueError(f"Cannot open wallpaper for {monitor['id']}: {exc}") from exc
        expected = (monitor["output_width"], monitor["output_height"])
        if wallpaper.size != expected:
            raise ValueError(
                f"{path.name} is {wallpaper.width}x{wallpaper.height}; "
                f"expected {expected[0]}x{expected[1]}"
            )
        left = round(monitor["art_x"] - min_x)
        top = round(monitor["art_y"] - min_y)
        rendered = wallpaper.resize(
            (monitor["art_width"], monitor["art_height"]), Image.Resampling.LANCZOS
        )
        preview.paste(rendered, (left, top))

    draw = ImageDraw.Draw(preview)
    for monitor in monitors:
        left = round(monitor["art_x"] - min_x)
        top = round(monitor["art_y"] - min_y)
        right = left + monitor["art_width"]
        bottom = top + monitor["art_height"]
        draw.rectangle((left, top, right - 1, bottom - 1), outline="white", width=2)

    preview_scale = min(1.0, max_edge / max(preview.width, preview.height))
    if preview_scale < 1.0:
        preview = preview.resize(
            (round(preview.width * preview_scale), round(preview.height * preview_scale)),
            Image.Resampling.LANCZOS,
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    preview.save(output)
    print(f"preview: {output} ({preview.width}x{preview.height})")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("schema", help="print an example layout JSON")

    guide = sub.add_parser("guide", help="render a labeled display-layout guide")
    guide.add_argument("--layout", type=Path, required=True)
    guide.add_argument("--output", type=Path, required=True)
    guide.add_argument("--max-edge", type=int, default=2400)

    analyze = sub.add_parser("analyze", help="measure source detail available to each display crop")
    analyze.add_argument("--layout", type=Path, required=True)
    analyze.add_argument("--master", type=Path, required=True)
    analyze.add_argument("--fit", choices=("cover", "contain", "stretch"), default="cover")

    split = sub.add_parser("split", help="split one master into per-display wallpapers")
    split.add_argument("--layout", type=Path, required=True)
    split.add_argument("--master", type=Path, required=True)
    split.add_argument("--output-dir", type=Path, required=True)
    split.add_argument("--fit", choices=("cover", "contain", "stretch"), default="cover")

    preview = sub.add_parser("preview", help="assemble final per-display wallpapers spatially")
    preview.add_argument("--layout", type=Path, required=True)
    preview.add_argument("--input-dir", type=Path, required=True)
    preview.add_argument("--output", type=Path, required=True)
    preview.add_argument("--max-edge", type=int, default=2400)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "schema":
        print(json.dumps(SCHEMA, indent=2))
        return 0
    try:
        layout = load_layout(args.layout)
        if args.command == "guide":
            draw_guide(layout, args.output, args.max_edge)
        elif args.command == "analyze":
            analyze_master(layout, args.master, args.fit)
        elif args.command == "split":
            split_master(layout, args.master, args.output_dir, args.fit)
        elif args.command == "preview":
            preview_wallpapers(layout, args.input_dir, args.output, args.max_edge)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
