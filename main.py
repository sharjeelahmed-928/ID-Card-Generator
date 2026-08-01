#!/usr/bin/env python3
"""
main.py
-------
Entry point for the Premium ID Card Generator desktop application.

Run with:
    python main.py

On first launch this will:
  1. Generate a handful of default background templates (if missing).
  2. Initialize the local SQLite database (idcards.db).
  3. Launch the customtkinter GUI.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_default_assets import generate_all as generate_default_templates
from app.gui import run_app


def main():
    generate_default_templates()
    run_app()


if __name__ == "__main__":
    main()
