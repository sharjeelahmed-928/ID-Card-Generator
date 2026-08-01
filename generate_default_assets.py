"""
generate_default_assets.py
---------------------------
Creates a small set of ready-to-use background templates in
assets/templates/ so the app has something to show in the
"Background Template" dropdown the very first time it's run.

This runs automatically from main.py on first launch, but you can
also run it manually:

    python generate_default_assets.py
"""

import os
from PIL import Image, ImageDraw

from app import config


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def make_gradient(size, color_top, color_bottom):
    w, h = size
    base = Image.new("RGBA", size, color_top)
    top = Image.new("RGBA", size, color_top)
    bottom = Image.new("RGBA", size, color_bottom)
    mask = Image.new("L", size)
    mask_data = []
    for y in range(h):
        mask_data.extend([int(255 * (y / h))] * w)
    mask.putdata(mask_data)
    return Image.composite(bottom, top, mask)


def template_classic_blue(path):
    w, h = config.CARD_WIDTH, config.CARD_HEIGHT
    img = make_gradient((w, h), _hex("#1E3A8A"), _hex("#3B82F6"))
    draw = ImageDraw.Draw(img)
    # white content area
    draw.rounded_rectangle([(0, int(h * 0.22)), (w, h)], radius=0, fill=(255, 255, 255, 255))
    draw.rectangle([(0, 0), (10, h)], fill=_hex("#F59E0B"))
    img.save(path)


def template_emerald(path):
    w, h = config.CARD_WIDTH, config.CARD_HEIGHT
    img = make_gradient((w, h), _hex("#064E3B"), _hex("#10B981"))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, int(h * 0.22)), (w, h)], radius=0, fill=(255, 255, 255, 255))
    draw.rectangle([(0, 0), (10, h)], fill=_hex("#FACC15"))
    img.save(path)


def template_crimson(path):
    w, h = config.CARD_WIDTH, config.CARD_HEIGHT
    img = make_gradient((w, h), _hex("#7F1D1D"), _hex("#EF4444"))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, int(h * 0.22)), (w, h)], radius=0, fill=(255, 255, 255, 255))
    draw.rectangle([(0, 0), (10, h)], fill=_hex("#FCD34D"))
    img.save(path)


def template_slate_minimal(path):
    w, h = config.CARD_WIDTH, config.CARD_HEIGHT
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (w, int(h * 0.22))], fill=_hex("#334155"))
    draw.rectangle([(0, 0), (10, h)], fill=_hex("#64748B"))
    img.save(path)


def generate_all():
    templates = {
        "classic_blue.png": template_classic_blue,
        "emerald.png": template_emerald,
        "crimson.png": template_crimson,
        "slate_minimal.png": template_slate_minimal,
    }
    created = []
    for filename, fn in templates.items():
        path = os.path.join(config.TEMPLATES_DIR, filename)
        if not os.path.exists(path):
            fn(path)
            created.append(filename)
    return created


if __name__ == "__main__":
    made = generate_all()
    if made:
        print("Created default templates:", ", ".join(made))
    else:
        print("Default templates already exist - nothing to do.")
