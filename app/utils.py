"""
utils.py
--------
Helper functions used across the app:
  - QR code generation
  - Barcode generation
  - Image utilities (cover-resize, circular/rounded mask, placeholders)
  - PDF export
  - Cross-platform printing
"""

import os
import io
import sys
import platform
import subprocess
from typing import Tuple

from PIL import Image, ImageDraw, ImageOps, ImageFont

import qrcode
from qrcode.constants import ERROR_CORRECT_M

import barcode
from barcode.writer import ImageWriter

from app import config


# ----------------------------------------------------------------------
# QR CODE
# ----------------------------------------------------------------------
def generate_qr_code(data: str, box_size: int = 6, border: int = 2) -> Image.Image:
    """Generate a QR code image (PIL.Image, RGBA) encoding `data`."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("RGBA")


# ----------------------------------------------------------------------
# BARCODE
# ----------------------------------------------------------------------
def generate_barcode(data: str, code_type: str = "code128") -> Image.Image:
    """Generate a 1D barcode (default Code128) as a PIL.Image (RGBA)."""
    # Code128 supports full ASCII, safe default for alphanumeric ID numbers.
    barcode_cls = barcode.get_barcode_class(code_type)
    writer = ImageWriter()
    writer.set_options({
        "module_height": 8.0,
        "module_width": 0.28,
        "quiet_zone": 2.0,
        "font_size": 8,
        "text_distance": 3.0,
        "write_text": True,
    })
    bc = barcode_cls(data, writer=writer)
    buf = io.BytesIO()
    bc.write(buf)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


# ----------------------------------------------------------------------
# IMAGE HELPERS
# ----------------------------------------------------------------------
def load_image_safe(path: str) -> "Image.Image | None":
    """Load an image from disk, return None (never raise) if it fails."""
    if not path or not os.path.exists(path):
        return None
    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)  # respect camera orientation
        return img.convert("RGBA")
    except Exception as exc:
        print(f"[utils] Failed to load image '{path}': {exc}")
        return None


def resize_cover(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """Resize + center-crop `img` to exactly fill `size` (like CSS object-fit: cover)."""
    target_w, target_h = size
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        # source is wider -> match height, crop width
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)

    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def rounded_mask(size: Tuple[int, int], radius: int) -> Image.Image:
    """Return an 'L' mode mask image with rounded corners for pasting."""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size[0] - 1, size[1] - 1)],
                            radius=radius, fill=255)
    return mask


def apply_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    mask = rounded_mask(img.size, radius)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def circular_crop(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    img = resize_cover(img, size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), (size[0] - 1, size[1] - 1)], fill=255)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def placeholder_photo(size: Tuple[int, int]) -> Image.Image:
    """A simple grey silhouette placeholder used when no photo is uploaded."""
    img = Image.new("RGBA", size, (226, 232, 240, 255))
    draw = ImageDraw.Draw(img)
    w, h = size
    # simple head + shoulders silhouette
    draw.ellipse([w * 0.30, h * 0.15, w * 0.70, h * 0.55], fill=(148, 163, 184, 255))
    draw.ellipse([w * 0.05, h * 0.55, w * 0.95, h * 1.25], fill=(148, 163, 184, 255))
    return img


def get_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    """Try to load a decent TTF font, falling back gracefully to PIL default."""
    candidates = []
    if bold and italic:
        candidates += ["DejaVuSans-BoldOblique.ttf"]
    elif bold:
        candidates += ["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"]
    elif italic:
        candidates += ["DejaVuSans-Oblique.ttf"]
    else:
        candidates += ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf"]

    search_dirs = [
        config.FONTS_DIR,
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/truetype/liberation",
        "C:/Windows/Fonts",
    ]
    for d in search_dirs:
        for name in candidates:
            path = os.path.join(d, name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    # last resort: PIL bitmap default (not resizable nicely, but never fails)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


# ----------------------------------------------------------------------
# PDF EXPORT
# ----------------------------------------------------------------------
def export_image_to_pdf(image_path: str, pdf_path: str):
    """Export a PNG/JPG card image to a single-page PDF, centered on an A6-ish page."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as pdf_canvas
    from reportlab.lib.units import mm

    img = Image.open(image_path)
    img_w_px, img_h_px = img.size
    # convert card pixel size (300 DPI) to points (1pt = 1/72in)
    img_w_pt = img_w_px / config.CARD_DPI * 72
    img_h_pt = img_h_px / config.CARD_DPI * 72

    page_w, page_h = A4
    x = (page_w - img_w_pt) / 2
    y = (page_h - img_h_pt) / 2

    c = pdf_canvas.Canvas(pdf_path, pagesize=A4)
    c.setTitle("ID Card")
    c.drawImage(image_path, x, y, width=img_w_pt, height=img_h_pt,
                preserveAspectRatio=True, mask="auto")
    # simple crop-mark style border to guide cutting
    c.setDash(3, 3)
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.rect(x, y, img_w_pt, img_h_pt)
    c.save()


# ----------------------------------------------------------------------
# PRINTING (cross-platform, best-effort)
# ----------------------------------------------------------------------
def print_file(path: str) -> Tuple[bool, str]:
    """
    Send a file to the default system printer.
    Returns (success, message).
    """
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path, "print")  # type: ignore[attr-defined]
            return True, "Sent to default printer."
        elif system == "Darwin":  # macOS
            subprocess.run(["lp", path], check=True)
            return True, "Sent to default printer via lp."
        else:  # Linux / other POSIX
            subprocess.run(["lp", path], check=True)
            return True, "Sent to default printer via lp (CUPS)."
    except FileNotFoundError:
        return False, ("No print command found on this system. Please install "
                        "CUPS ('lp' command) or print the exported file manually.")
    except Exception as exc:
        return False, f"Printing failed: {exc}"
