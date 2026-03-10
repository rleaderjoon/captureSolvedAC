"""
Image composition: combine AC RATING and Streak screenshots into one image.

Layout:
  ┌─────────────────────────────────────────┐
  │  solved.ac / {handle}       2026-03-11  │  ← header bar
  ├─────────────────────────────────────────┤
  │  [AC RATING section screenshot]         │
  ├─────────────────────────────────────────┤
  │  [Streak section screenshot]            │
  └─────────────────────────────────────────┘
"""
import io
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from config import (
    HEADER_HEIGHT, SECTION_GAP,
    HEADER_BG_COLOR, HEADER_TEXT_COLOR, HEADER_DATE_COLOR
)

# Windows fonts to try (in order of preference)
_FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/calibri.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/malgun.ttf",
]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def compose_image(
    rating_png: bytes,
    streak_png: bytes,
    handle: str,
    output_path: str,
) -> str:
    """
    Compose rating + streak screenshots into a single PNG.
    Returns the output_path on success.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    rating_img = Image.open(io.BytesIO(rating_png)).convert("RGB")
    streak_img = Image.open(io.BytesIO(streak_png)).convert("RGB")

    # Normalize both images to the same width (scale narrower one up)
    target_w = max(rating_img.width, streak_img.width)
    rating_img = _resize_to_width(rating_img, target_w)
    streak_img = _resize_to_width(streak_img, target_w)

    canvas_w = target_w
    canvas_h = HEADER_HEIGHT + rating_img.height + SECTION_GAP + streak_img.height

    canvas = Image.new("RGB", (canvas_w, canvas_h), HEADER_BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # --- Header bar ---
    font_handle = _load_font(18)
    font_date = _load_font(15)

    handle_text = f"solved.ac / {handle}"
    text_y = (HEADER_HEIGHT - 20) // 2

    draw.text((16, text_y), handle_text, fill=HEADER_TEXT_COLOR, font=font_handle)

    # Right-align date
    try:
        bbox = draw.textbbox((0, 0), today, font=font_date)
        date_w = bbox[2] - bbox[0]
    except AttributeError:
        date_w = len(today) * 9  # rough fallback

    draw.text((canvas_w - date_w - 16, text_y + 2), today, fill=HEADER_DATE_COLOR, font=font_date)

    # --- Paste sections ---
    y = HEADER_HEIGHT
    canvas.paste(rating_img, (0, y))
    y += rating_img.height + SECTION_GAP
    canvas.paste(streak_img, (0, y))

    # --- Save ---
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    canvas.save(output_path, "PNG", optimize=True)
    return output_path


def _resize_to_width(img: Image.Image, target_w: int) -> Image.Image:
    if img.width == target_w:
        return img
    ratio = target_w / img.width
    new_h = int(img.height * ratio)
    return img.resize((target_w, new_h), Image.LANCZOS)
