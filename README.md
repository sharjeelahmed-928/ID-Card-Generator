# Premium ID Card Generator (Python + customtkinter)

A full-featured desktop application for designing, previewing, exporting and
printing professional ID cards — built with a modern `customtkinter` GUI.

## Features

- Enter Name, ID Number, Class/Department, Phone Number, Address
- Upload a Photo (auto-cropped/framed into the card)
- Upload an Institute Logo
- Upload a Digital Signature image
- Choose a Background Template (4 built-in templates, or drop in your own)
- **Live preview** — the card re-renders automatically as you type or upload
- **Automatic ID numbering** (e.g. `GIT-0001`, `GIT-0002`, ...), editable
- **QR code** generation (encodes name/ID/department/phone)
- **Barcode** generation (Code128, based on the ID number)
- Save the finished card as a **PNG** image (300 DPI, print-ready)
- **Export to PDF** (centered on an A4 page with cut guides)
- **Print** directly to your system's default printer
- **Database integration** — SQLite by default, optional MySQL backend
- Browse, reload and delete previously saved records from a built-in viewer

## Project structure

```
idcard_generator/
├── main.py                     # entry point
├── generate_default_assets.py  # creates default background templates
├── requirements.txt
├── app/
│   ├── config.py                # all app-wide settings (paths, colors, DB, card size)
│   ├── database.py               # SQLite/MySQL data layer + auto ID numbering
│   ├── card_generator.py         # renders the final ID card image (PIL)
│   ├── gui.py                    # customtkinter GUI (forms, live preview, actions)
│   └── utils.py                  # QR code, barcode, image, PDF, print helpers
├── assets/
│   ├── templates/                # background templates (.png) — auto-generated
│   └── fonts/                    # drop custom .ttf fonts here (optional)
└── exports/                      # PNG/PDF exports land here by default
```

## Installation

Requires **Python 3.9+** (3.10–3.13 recommended for the widest availability of
prebuilt wheels; very new Python releases, e.g. 3.14, sometimes lag behind on
prebuilt Pillow/customtkinter wheels).

```bash
cd idcard_generator
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Windows + "Failed building wheel for Pillow" / missing zlib**: this means
> pip is trying to compile Pillow from source because no prebuilt wheel
> exists yet for your Python version. `requirements.txt` uses `>=` version
> constraints so `pip install --upgrade pip` followed by a fresh
> `pip install -r requirements.txt` will normally pick up a newer Pillow
> release that does have a wheel. If it still fails, the most reliable fix
> is installing a slightly older, widely-supported Python (3.11 or 3.12)
> alongside your current one and creating the virtual environment with that
> instead.

> `mysql-connector-python` is only needed if you switch the database
> backend to MySQL (see below). If you don't need MySQL, you can safely
> remove that line from `requirements.txt` before installing.

### System requirements for printing

- **Windows**: printing uses the built-in `os.startfile(..., "print")` — no
  extra setup needed, as long as you have a default printer configured.
- **macOS / Linux**: printing uses the `lp` command (CUPS). Make sure CUPS
  is installed and a default printer is configured
  (`lpstat -d` to check).

## Running the app

```bash
python main.py
```

On first run the app will automatically:
1. Generate 4 default background templates into `assets/templates/`.
2. Create the local SQLite database file `idcards.db`.
3. Open the GUI.

## Using the app

1. Fill in **Name**, **Class/Department**, **Phone**, **Address**.
2. The **ID Number** is auto-filled from the database sequence
   (`GIT-0001`, `GIT-0002`, ...) — click **Auto** to regenerate it, or type
   your own.
3. Click **Upload** next to Photo / Institute Logo / Digital Signature to
   attach images (PNG/JPG/BMP/WEBP supported).
4. Pick a **Background Template** from the dropdown (or leave it on
   "Generated (Default)" for a clean programmatic design).
5. Watch the **Live Preview** update automatically on the right.
6. Click **⚡ Generate ID Card** to force a fresh render at any time.
7. Use the action buttons to:
   - **💾 Save PNG** — export a print-ready 300 DPI PNG.
   - **📄 Export PDF** — export a single-page PDF with cut guides.
   - **🖨️ Print** — send directly to your default printer.
   - **🗄️ Save to DB** — persist the record (and a PNG snapshot) to the database.
8. Click **📋 View Saved Records** to browse, reload or delete records that
   were saved to the database.

## Switching to MySQL

By default the app uses a local SQLite file (`idcards.db`). To use MySQL
instead:

```bash
export IDCARD_DB_TYPE=mysql
export IDCARD_MYSQL_HOST=localhost
export IDCARD_MYSQL_USER=root
export IDCARD_MYSQL_PASSWORD=yourpassword
export IDCARD_MYSQL_DB=idcard_generator
python main.py
```

(On Windows use `set VAR=value` instead of `export`.) If the MySQL
connection fails for any reason, the app automatically falls back to
SQLite so you're never locked out.

## Customizing

- **Card size / DPI / colors / institute defaults**: edit `app/config.py`.
- **Card layout** (where the photo, QR code, barcode, signature sit): edit
  `app/card_generator.py` — every element is drawn with clear, separate
  methods (`_draw_header`, `_draw_photo`, `_draw_fields`, `_draw_qr`,
  `_draw_barcode`, `_draw_signature`, `_draw_footer`).
- **More background templates**: drop any `.png`/`.jpg` file into
  `assets/templates/` — it will automatically appear in the dropdown. For
  best results use a `1013x638` px image (CR80 card size at 300 DPI).
- **Custom fonts**: drop `.ttf` files into `assets/fonts/` and reference
  them in `utils.get_font()`.

## Notes

- The QR code encodes a small JSON payload with the ID number, name,
  department and phone number — scan it with any phone camera to verify.
- The barcode is a Code128 symbology generated from the ID number.
- All generated PNG/PDF files default to `exports/`, but you can save
  anywhere via the file dialogs.
