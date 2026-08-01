"""
card_generator.py
------------------
Core rendering engine that composites a professional-looking ID card
from user-supplied data (name, id number, department, phone, address),
a photo, an institute logo, an optional digital signature, a QR code,
a barcode and a background template.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Optional

from PIL import Image, ImageDraw

from app import config, utils


@dataclass
class CardData:
    name: str = ""
    id_number: str = ""
    department: str = ""
    phone: str = ""
    address: str = ""
    institute_name: str = config.INSTITUTE_NAME
    institute_tagline: str = config.INSTITUTE_TAGLINE
    photo_path: Optional[str] = None
    logo_path: Optional[str] = None
    signature_path: Optional[str] = None
    template_path: Optional[str] = None  # None => generated default background
    valid_thru: str = ""  # optional, e.g. "06/2027"


class IDCardGenerator:
    """Builds the final ID card image from a CardData object."""

    WIDTH = config.CARD_WIDTH
    HEIGHT = config.CARD_HEIGHT

    def generate(self, data: CardData) -> Image.Image:
        card = self._build_background(data.template_path)
        draw = ImageDraw.Draw(card)

        self._draw_header(card, draw, data)
        self._draw_photo(card, data)
        self._draw_fields(draw, data)
        self._draw_qr(card, data)
        self._draw_barcode(card, data)
        self._draw_signature(card, data)
        self._draw_footer(draw, data)

        return card.convert("RGB")

    # ------------------------------------------------------------------
    # Background
    # ------------------------------------------------------------------
    def _build_background(self, template_path: Optional[str]) -> Image.Image:
        if template_path and os.path.exists(template_path):
            bg = Image.open(template_path).convert("RGBA")
            bg = utils.resize_cover(bg, (self.WIDTH, self.HEIGHT))
            return bg
        return self._default_background()

    def _default_background(self) -> Image.Image:
        """A clean generated background used when no template is selected."""
        card = Image.new("RGBA", (self.WIDTH, self.HEIGHT), utils.__dict__.get(
            "COLOR_WHITE", "#FFFFFF"))
        card = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (255, 255, 255, 255))
        draw = ImageDraw.Draw(card)

        # top color band
        band_h = int(self.HEIGHT * 0.24)
        draw.rectangle([(0, 0), (self.WIDTH, band_h)], fill=_hex(config.COLOR_PRIMARY))
        # accent diagonal stripe
        draw.polygon(
            [(0, band_h), (self.WIDTH * 0.35, band_h), (self.WIDTH * 0.22, band_h + 22),
             (0, band_h + 22)],
            fill=_hex(config.COLOR_ACCENT),
        )
        # bottom footer band
        footer_h = int(self.HEIGHT * 0.10)
        draw.rectangle([(0, self.HEIGHT - footer_h), (self.WIDTH, self.HEIGHT)],
                        fill=_hex(config.COLOR_PRIMARY))
        # subtle side accent
        draw.rectangle([(0, 0), (10, self.HEIGHT)], fill=_hex(config.COLOR_ACCENT))
        return card

    # ------------------------------------------------------------------
    # Header (logo + institute name)
    # ------------------------------------------------------------------
    def _draw_header(self, card: Image.Image, draw: ImageDraw.ImageDraw, data: CardData):
        logo_img = utils.load_image_safe(data.logo_path)
        text_x = 30
        if logo_img:
            logo_size = (86, 86)
            logo_img = utils.resize_cover(logo_img, logo_size)
            logo_img = utils.apply_rounded_corners(logo_img, radius=12)
            card.paste(logo_img, (24, 20), logo_img)
            text_x = 24 + logo_size[0] + 16

        title_font = utils.get_font(30, bold=True)
        tagline_font = utils.get_font(15)

        draw.text((text_x, 26), data.institute_name.upper(), font=title_font,
                   fill=_hex(config.COLOR_WHITE))
        draw.text((text_x, 66), data.institute_tagline, font=tagline_font,
                   fill=_hex(config.COLOR_WHITE))

    # ------------------------------------------------------------------
    # Photo
    # ------------------------------------------------------------------
    def _draw_photo(self, card: Image.Image, data: CardData):
        photo_size = (200, 230)
        photo_img = utils.load_image_safe(data.photo_path)
        if photo_img is None:
            photo_img = utils.placeholder_photo(photo_size)
        else:
            photo_img = utils.resize_cover(photo_img, photo_size)

        photo_img = utils.apply_rounded_corners(photo_img, radius=10)

        px = self.WIDTH - photo_size[0] - 40
        py = int(self.HEIGHT * 0.24) + 26

        # white frame behind the photo for a "premium" card look
        frame_pad = 6
        frame = Image.new("RGBA",
                           (photo_size[0] + frame_pad * 2, photo_size[1] + frame_pad * 2),
                           (255, 255, 255, 255))
        frame = utils.apply_rounded_corners(frame, radius=14)
        card.paste(frame, (px - frame_pad, py - frame_pad), frame)
        card.paste(photo_img, (px, py), photo_img)

    # ------------------------------------------------------------------
    # Text fields
    # ------------------------------------------------------------------
    def _draw_fields(self, draw: ImageDraw.ImageDraw, data: CardData):
        label_font = utils.get_font(15, bold=True)
        value_font = utils.get_font(20, bold=True)
        small_value_font = utils.get_font(16)

        start_y = int(self.HEIGHT * 0.24) + 30
        x = 40
        line_gap = 52

        fields = [
            ("NAME", data.name or "-", value_font),
            ("ID NUMBER", data.id_number or "-", value_font),
            ("DEPARTMENT / CLASS", data.department or "-", small_value_font),
            ("PHONE", data.phone or "-", small_value_font),
        ]

        y = start_y
        for label, value, vfont in fields:
            draw.text((x, y), label, font=label_font, fill=_hex(config.COLOR_ACCENT))
            draw.text((x, y + 20), _truncate(value, vfont, 480), font=vfont,
                       fill=_hex(config.COLOR_TEXT_DARK))
            y += line_gap

        # Address wraps onto up to 2 lines
        draw.text((x, y), "ADDRESS", font=label_font, fill=_hex(config.COLOR_ACCENT))
        addr_lines = _wrap_text(data.address or "-", small_value_font, 480, max_lines=2)
        ay = y + 20
        for line in addr_lines:
            draw.text((x, ay), line, font=small_value_font, fill=_hex(config.COLOR_TEXT_DARK))
            ay += 22

    # ------------------------------------------------------------------
    # QR code
    # ------------------------------------------------------------------
    def _draw_qr(self, card: Image.Image, data: CardData):
        payload = json.dumps({
            "id": data.id_number,
            "name": data.name,
            "dept": data.department,
            "phone": data.phone,
        }, ensure_ascii=False)
        qr_img = utils.generate_qr_code(payload, box_size=4, border=1)
        qr_img = qr_img.resize((110, 110), Image.LANCZOS)
        footer_h = int(self.HEIGHT * 0.10)
        qx, qy = 30, self.HEIGHT - footer_h - 122
        # white backing card for contrast
        backing = Image.new("RGBA", (118, 118), (255, 255, 255, 255))
        backing = utils.apply_rounded_corners(backing, radius=8)
        card.paste(backing, (qx - 4, qy - 4), backing)
        card.paste(qr_img, (qx, qy), qr_img)

    # ------------------------------------------------------------------
    # Barcode
    # ------------------------------------------------------------------
    def _draw_barcode(self, card: Image.Image, data: CardData):
        code_value = _sanitize_for_barcode(data.id_number or "0000")
        try:
            bc_img = utils.generate_barcode(code_value)
        except Exception as exc:
            print(f"[card_generator] Barcode generation failed: {exc}")
            return
        target_w = 330
        ratio = target_w / bc_img.width
        target_h = int(bc_img.height * ratio)
        bc_img = bc_img.resize((target_w, min(target_h, 90)), Image.LANCZOS)

        footer_h = int(self.HEIGHT * 0.10)
        bx = 170
        by = self.HEIGHT - footer_h - 100
        backing = Image.new("RGBA", (target_w + 12, bc_img.height + 12), (255, 255, 255, 255))
        backing = utils.apply_rounded_corners(backing, radius=6)
        card.paste(backing, (bx - 6, by - 6), backing)
        card.paste(bc_img, (bx, by), bc_img)

    # ------------------------------------------------------------------
    # Signature
    # ------------------------------------------------------------------
    def _draw_signature(self, card: Image.Image, data: CardData):
        sig_img = utils.load_image_safe(data.signature_path)
        footer_h = int(self.HEIGHT * 0.10)
        sig_w, sig_h = 170, 60
        sx = self.WIDTH - sig_w - 40
        sy = self.HEIGHT - footer_h - sig_h - 14

        if sig_img:
            sig_img.thumbnail((sig_w, sig_h), Image.LANCZOS)
            paste_x = sx + (sig_w - sig_img.width) // 2
            paste_y = sy + (sig_h - sig_img.height) // 2
            card.paste(sig_img, (paste_x, paste_y), sig_img)

        draw = ImageDraw.Draw(card)
        draw.line([(sx, sy + sig_h), (sx + sig_w, sy + sig_h)],
                   fill=_hex(config.COLOR_TEXT_MUTED), width=2)
        cap_font = utils.get_font(13)
        draw.text((sx + sig_w / 2, sy + sig_h + 6), "Authorized Signature",
                   font=cap_font, fill=_hex(config.COLOR_TEXT_MUTED), anchor="ma")

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------
    def _draw_footer(self, draw: ImageDraw.ImageDraw, data: CardData):
        footer_h = int(self.HEIGHT * 0.10)
        footer_font = utils.get_font(14)
        text = "This card is the property of the institute. If found, please return."
        if data.valid_thru:
            text = f"Valid thru: {data.valid_thru}    |    {text}"
        draw.text((30, self.HEIGHT - footer_h + footer_h / 2), text,
                   font=footer_font, fill=_hex(config.COLOR_WHITE), anchor="lm")


# ----------------------------------------------------------------------
# small local helpers
# ----------------------------------------------------------------------
def _hex(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def _truncate(text: str, font, max_width: int) -> str:
    if font.getlength(text) <= max_width:
        return text
    while font.getlength(text + "...") > max_width and len(text) > 1:
        text = text[:-1]
    return text + "..."


def _wrap_text(text: str, font, max_width: int, max_lines: int = 2):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) == max_lines - 1:
            # last allowed line: fit remaining words + ellipsis if needed
            remaining = " ".join(words[words.index(word):])
            if font.getlength(current + " " + remaining) > max_width or \
               " ".join(words).count(" ") != trial.count(" "):
                pass
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = _truncate(lines[-1], font, max_width)
    return lines or ["-"]


def _sanitize_for_barcode(value: str) -> str:
    # Code128 handles most ASCII; strip anything exotic just in case.
    return "".join(ch for ch in value if 32 <= ord(ch) <= 126) or "0000"
