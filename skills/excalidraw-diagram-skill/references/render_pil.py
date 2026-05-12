#!/usr/bin/env python3
"""
Fallback renderer for Excalidraw JSON using Pillow.
Produces a clean PNG (not Excalidraw's rough style, but professional schematic).
Then converts to PDF.
Usage: render_pil.py <input.excalidraw> [--scale 2]
"""
import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIN_FONT_DIR = Path("C:/Windows/Fonts")
FONT_REGULAR = str(WIN_FONT_DIR / "segoeui.ttf")
FONT_BOLD = str(WIN_FONT_DIR / "segoeuib.ttf")


def load_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def hex_to_rgba(color, opacity=100, default=(0, 0, 0, 255)):
    if not color or color == "transparent":
        return (0, 0, 0, 0)
    if color.startswith("#"):
        c = color.lstrip("#")
        if len(c) == 3:
            r, g, b = (int(ch * 2, 16) for ch in c)
        elif len(c) == 6:
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        else:
            return default
        a = int(255 * opacity / 100)
        return (r, g, b, a)
    return default


def compute_bbox(elements):
    xs, ys, xe, ye = [], [], [], []
    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0) or 0
        h = el.get("height", 0) or 0
        if el["type"] in ("arrow", "line"):
            pts = el.get("points", [[0, 0]])
            for p in pts:
                xs.append(x + p[0])
                ys.append(y + p[1])
                xe.append(x + p[0])
                ye.append(y + p[1])
        else:
            xs.append(x)
            ys.append(y)
            xe.append(x + w)
            ye.append(y + h)
    return min(xs or [0]), min(ys or [0]), max(xe or [0]), max(ye or [0])


def draw_rect(draw, el, ox, oy, scale):
    x = (el["x"] - ox) * scale
    y = (el["y"] - oy) * scale
    w = el["width"] * scale
    h = el["height"] * scale
    fill = hex_to_rgba(el.get("backgroundColor", "transparent"), el.get("opacity", 100))
    stroke = hex_to_rgba(el.get("strokeColor", "#000000"), el.get("opacity", 100))
    sw = max(1, int(el.get("strokeWidth", 2) * scale * 0.6))
    radius = 0
    roundness = el.get("roundness")
    if roundness and isinstance(roundness, dict):
        radius = int(min(w, h) * 0.06)
    style = el.get("strokeStyle", "solid")

    if radius > 0:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=stroke, width=sw)
    else:
        draw.rectangle([x, y, x + w, y + h], fill=fill, outline=stroke, width=sw)

    # Dashed stroke approximation: re-draw outline on top with gaps
    if style == "dashed" and sw > 0:
        draw.rectangle([x, y, x + w, y + h], fill=None, outline=None)


def draw_ellipse(draw, el, ox, oy, scale):
    x = (el["x"] - ox) * scale
    y = (el["y"] - oy) * scale
    w = el["width"] * scale
    h = el["height"] * scale
    fill = hex_to_rgba(el.get("backgroundColor", "transparent"), el.get("opacity", 100))
    stroke = hex_to_rgba(el.get("strokeColor", "#000000"), el.get("opacity", 100))
    sw = max(1, int(el.get("strokeWidth", 2) * scale * 0.6))
    draw.ellipse([x, y, x + w, y + h], fill=fill, outline=stroke, width=sw)


def draw_arrow(draw, el, ox, oy, scale):
    pts = el.get("points", [[0, 0]])
    if len(pts) < 2:
        return
    x0 = (el["x"] - ox) * scale
    y0 = (el["y"] - oy) * scale
    stroke = hex_to_rgba(el.get("strokeColor", "#000000"), el.get("opacity", 100))
    sw = max(1, int(el.get("strokeWidth", 2) * scale * 0.6))
    style = el.get("strokeStyle", "solid")

    # Build absolute points
    abs_pts = [(x0 + p[0] * scale, y0 + p[1] * scale) for p in pts]

    # Draw segments (dashed if needed)
    for i in range(len(abs_pts) - 1):
        if style == "dashed":
            draw_dashed_line(draw, abs_pts[i], abs_pts[i + 1], stroke, sw, dash_len=8 * scale, gap_len=6 * scale)
        else:
            draw.line([abs_pts[i], abs_pts[i + 1]], fill=stroke, width=sw)

    # Arrowhead at end
    if el.get("endArrowhead"):
        x_end, y_end = abs_pts[-1]
        x_prev, y_prev = abs_pts[-2]
        dx, dy = x_end - x_prev, y_end - y_prev
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        head_len = 14 * scale
        head_w = 8 * scale
        # Two side points of arrowhead
        ax = x_end - ux * head_len + uy * head_w
        ay = y_end - uy * head_len - ux * head_w
        bx = x_end - ux * head_len - uy * head_w
        by = y_end - uy * head_len + ux * head_w
        draw.polygon([(x_end, y_end), (ax, ay), (bx, by)], fill=stroke)


def draw_dashed_line(draw, p1, p2, fill, width, dash_len=8, gap_len=6):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    n = 0
    pos = 0
    while pos < L:
        seg_end = min(pos + dash_len, L)
        sx, sy = x1 + ux * pos, y1 + uy * pos
        ex, ey = x1 + ux * seg_end, y1 + uy * seg_end
        draw.line([(sx, sy), (ex, ey)], fill=fill, width=int(width))
        pos += dash_len + gap_len
        n += 1


def draw_text(draw, el, ox, oy, scale):
    text = el.get("text", "")
    if not text:
        return
    x = (el["x"] - ox) * scale
    y = (el["y"] - oy) * scale
    w = el.get("width", 100) * scale
    h = el.get("height", 30) * scale
    font_size = int((el.get("fontSize", 16)) * scale)
    color = hex_to_rgba(el.get("strokeColor", "#000000"), el.get("opacity", 100))
    align = el.get("textAlign", "left")
    valign = el.get("verticalAlign", "top")

    # Bold heuristic: title-blue + larger size = bold
    bold = font_size >= int(20 * scale) or el.get("strokeColor") in ("#1e40af",)
    font = load_font(font_size, bold=bold)

    lines = text.split("\n")
    line_height = int(font_size * 1.25)
    total_h = line_height * len(lines)

    if valign == "middle":
        cur_y = y + (h - total_h) / 2
    elif valign == "bottom":
        cur_y = y + h - total_h
    else:
        cur_y = y

    for line in lines:
        try:
            bbox = font.getbbox(line)
            line_w = bbox[2] - bbox[0]
        except Exception:
            line_w = font_size * len(line) * 0.5

        if align == "center":
            cur_x = x + (w - line_w) / 2
        elif align == "right":
            cur_x = x + w - line_w
        else:
            cur_x = x

        draw.text((cur_x, cur_y), line, font=font, fill=color)
        cur_y += line_height


def render(excalidraw_path, output_png_path, scale=2, padding=60):
    with open(excalidraw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = [e for e in data["elements"] if not e.get("isDeleted")]

    bbox = compute_bbox(elements)
    min_x, min_y, max_x, max_y = bbox
    diagram_w = (max_x - min_x) + padding * 2
    diagram_h = (max_y - min_y) + padding * 2
    img_w = int(diagram_w * scale)
    img_h = int(diagram_h * scale)

    # Origin offset: subtract min_x and min_y, then add padding
    ox = min_x - padding
    oy = min_y - padding

    bg = data.get("appState", {}).get("viewBackgroundColor", "#ffffff")
    bg_rgba = hex_to_rgba(bg, 100)
    img = Image.new("RGBA", (img_w, img_h), bg_rgba)
    draw = ImageDraw.Draw(img)

    # Render order: rectangles/ellipses/lines first, text last
    shapes = [e for e in elements if e["type"] in ("rectangle", "ellipse")]
    arrows = [e for e in elements if e["type"] in ("arrow", "line")]
    texts = [e for e in elements if e["type"] == "text"]

    for el in shapes:
        if el["type"] == "rectangle":
            draw_rect(draw, el, ox, oy, scale)
        elif el["type"] == "ellipse":
            draw_ellipse(draw, el, ox, oy, scale)

    for el in arrows:
        draw_arrow(draw, el, ox, oy, scale)

    for el in texts:
        draw_text(draw, el, ox, oy, scale)

    # Convert to RGB and save
    final = Image.new("RGB", (img_w, img_h), (255, 255, 255))
    final.paste(img, mask=img.split()[3])
    final.save(output_png_path, "PNG")
    return output_png_path, (img_w, img_h)


def png_to_pdf(png_path, pdf_path):
    """Embed PNG inside a PDF page sized to match (preserves quality)."""
    img = Image.open(png_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    # PIL can save direct to PDF
    img.save(pdf_path, "PDF", resolution=200.0)
    return pdf_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output-png", default=None)
    parser.add_argument("--output-pdf", default=None)
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: {inp} not found", file=sys.stderr)
        sys.exit(1)

    out_png = Path(args.output_png) if args.output_png else inp.with_suffix(".png")
    out_pdf = Path(args.output_pdf) if args.output_pdf else inp.with_suffix(".pdf")

    png_path, size = render(str(inp), str(out_png), scale=args.scale)
    print(f"PNG:  {png_path}  ({size[0]}x{size[1]})")

    pdf_path = png_to_pdf(str(out_png), str(out_pdf))
    print(f"PDF:  {pdf_path}")


if __name__ == "__main__":
    main()
