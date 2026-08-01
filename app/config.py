"""
config.py
---------
Central configuration for the ID Card Generator application.
Change values here to re-brand the app, change card size, DB backend, etc.
"""

import os

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMPLATES_DIR = os.path.join(ASSETS_DIR, "templates")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
DB_PATH = os.path.join(BASE_DIR, "idcards.db")

for _d in (ASSETS_DIR, TEMPLATES_DIR, FONTS_DIR, EXPORTS_DIR):
    os.makedirs(_d, exist_ok=True)

# ----------------------------------------------------------------------
# Card geometry (CR80 card, 3.375in x 2.125in @ 300 DPI)
# ----------------------------------------------------------------------
CARD_WIDTH = 1013
CARD_HEIGHT = 638
CARD_DPI = 300

# ----------------------------------------------------------------------
# Institute branding defaults (editable from the GUI too)
# ----------------------------------------------------------------------
INSTITUTE_NAME = "ABC INSTITUTE OF TECHNOLOGY"
INSTITUTE_TAGLINE = "Identity Card"
ID_PREFIX = "AIT"  # used for automatic ID numbering, e.g. AIT-0001

# ----------------------------------------------------------------------
# Colors (hex) - used when drawing on a blank/generated background
# ----------------------------------------------------------------------
COLOR_PRIMARY = "#1E3A8A"      # deep blue
COLOR_SECONDARY = "#2563EB"    # bright blue
COLOR_ACCENT = "#F59E0B"       # amber
COLOR_WHITE = "#FFFFFF"
COLOR_TEXT_DARK = "#111827"
COLOR_TEXT_MUTED = "#4B5563"

# ----------------------------------------------------------------------
# Database backend: "sqlite" or "mysql"
# ----------------------------------------------------------------------
DB_TYPE = os.environ.get("IDCARD_DB_TYPE", "sqlite")  # "sqlite" | "mysql"

MYSQL_CONFIG = {
    "host": os.environ.get("IDCARD_MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("IDCARD_MYSQL_PORT", "3306")),
    "user": os.environ.get("IDCARD_MYSQL_USER", "root"),
    "password": os.environ.get("IDCARD_MYSQL_PASSWORD", ""),
    "database": os.environ.get("IDCARD_MYSQL_DB", "idcard_generator"),
}

# ----------------------------------------------------------------------
# GUI appearance (customtkinter)
# ----------------------------------------------------------------------
APPEARANCE_MODE = "System"       # "System" | "Dark" | "Light"
COLOR_THEME = "blue"             # "blue" | "green" | "dark-blue"
WINDOW_TITLE = "Premium ID Card Generator"
WINDOW_SIZE = "1360x820"
