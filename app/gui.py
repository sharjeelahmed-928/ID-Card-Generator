"""
gui.py
------
Premium customtkinter GUI for the ID Card Generator.

Layout:
  - Left panel: scrollable data-entry form (personal info, uploads,
    template picker) + action buttons (Generate / Save PNG / Export PDF /
    Print / Save to DB / View Records).
  - Right panel: live, auto-updating preview of the card.
"""

import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk
from PIL import Image

from app import config, utils
from app.database import IDCardDatabase
from app.card_generator import IDCardGenerator, CardData

ctk.set_appearance_mode(config.APPEARANCE_MODE)
ctk.set_default_color_theme(config.COLOR_THEME)

PREVIEW_SCALE = 0.62  # preview shown at ~62% of true 300dpi card size


class IDCardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(config.WINDOW_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.minsize(1150, 720)

        self.generator = IDCardGenerator()
        self.db = IDCardDatabase()

        # uploaded asset paths
        self.photo_path: Optional[str] = None
        self.logo_path: Optional[str] = None
        self.signature_path: Optional[str] = None

        self.last_card_image: Optional[Image.Image] = None  # full-res PIL image
        self._preview_ctk_img = None  # keep a reference so tkinter doesn't GC it
        self._debounce_job = None

        self._build_layout()
        self._populate_templates()
        self._auto_fill_id_number()
        self._schedule_preview_update()

    # ------------------------------------------------------------------
    # Layout construction
    # ------------------------------------------------------------------
    def _build_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_form_panel()
        self._build_preview_panel()

    # ---------------------------- FORM PANEL --------------------------
    def _build_form_panel(self):
        form_scroll = ctk.CTkScrollableFrame(self, width=400, label_text="ID Card Details")
        form_scroll.grid(row=0, column=0, sticky="nswe", padx=(16, 8), pady=16)
        form_scroll.grid_columnconfigure(0, weight=1)

        # --- Section: Personal info -----------------------------------
        section = self._section_label(form_scroll, "Personal Information")
        section.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.entry_name = self._labeled_entry(form_scroll, "Full Name", 1, placeholder="e.g. John Carter")
        self.entry_dept = self._labeled_entry(form_scroll, "Class / Department", 3, placeholder="e.g. Computer Science - Sem 5")
        self.entry_phone = self._labeled_entry(form_scroll, "Phone Number", 5, placeholder="e.g. +1 555 123 4567")

        ctk.CTkLabel(form_scroll, text="Address", anchor="w").grid(
            row=7, column=0, sticky="we", pady=(6, 2))
        self.text_address = ctk.CTkTextbox(form_scroll, height=60)
        self.text_address.grid(row=8, column=0, sticky="we", pady=(0, 10))
        self.text_address.bind("<KeyRelease>", self._on_field_change)

        # --- Section: ID number -----------------------------------
        id_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        id_frame.grid(row=9, column=0, sticky="we", pady=(4, 10))
        id_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(id_frame, text="ID Number (auto-generated, editable)", anchor="w").grid(
            row=0, column=0, columnspan=2, sticky="w")
        self.entry_id = ctk.CTkEntry(id_frame, placeholder_text="e.g. GIT-0001")
        self.entry_id.grid(row=1, column=0, sticky="we", padx=(0, 6))
        self.entry_id.bind("<KeyRelease>", self._on_field_change)
        ctk.CTkButton(id_frame, text="Auto", width=60,
                      command=self._auto_fill_id_number).grid(row=1, column=1)

        # --- Section: Uploads -----------------------------------
        section2 = self._section_label(form_scroll, "Images")
        section2.grid(row=10, column=0, sticky="w", pady=(10, 6))

        self.lbl_photo = self._upload_row(form_scroll, 11, "Photo", self._upload_photo)
        self.lbl_logo = self._upload_row(form_scroll, 13, "Institute Logo", self._upload_logo)
        self.lbl_signature = self._upload_row(form_scroll, 15, "Digital Signature", self._upload_signature)

        # --- Section: Template -----------------------------------
        section3 = self._section_label(form_scroll, "Background Template")
        section3.grid(row=17, column=0, sticky="w", pady=(10, 6))
        self.template_var = tk.StringVar(value="Generated (Default)")
        self.template_menu = ctk.CTkOptionMenu(
            form_scroll, variable=self.template_var,
            values=["Generated (Default)"], command=self._on_field_change)
        self.template_menu.grid(row=18, column=0, sticky="we", pady=(0, 10))

        # --- Section: Institute branding -----------------------------------
        section4 = self._section_label(form_scroll, "Institute Branding")
        section4.grid(row=19, column=0, sticky="w", pady=(10, 6))
        self.entry_institute = self._labeled_entry(
            form_scroll, "Institute Name", 20, placeholder=config.INSTITUTE_NAME,
            default=config.INSTITUTE_NAME)
        self.entry_tagline = self._labeled_entry(
            form_scroll, "Tagline", 22, placeholder=config.INSTITUTE_TAGLINE,
            default=config.INSTITUTE_TAGLINE)
        self.entry_valid = self._labeled_entry(
            form_scroll, "Valid Thru (optional)", 24, placeholder="e.g. 06/2027")

        # --- Actions -----------------------------------
        section5 = self._section_label(form_scroll, "Actions")
        section5.grid(row=25, column=0, sticky="w", pady=(14, 6))

        btn_generate = ctk.CTkButton(form_scroll, text="⚡ Generate ID Card",
                                      command=self.generate_card, height=42,
                                      font=ctk.CTkFont(size=15, weight="bold"))
        btn_generate.grid(row=26, column=0, sticky="we", pady=(0, 8))

        row_btns = ctk.CTkFrame(form_scroll, fg_color="transparent")
        row_btns.grid(row=27, column=0, sticky="we", pady=(0, 6))
        row_btns.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(row_btns, text="💾 Save PNG", command=self.save_png).grid(
            row=0, column=0, sticky="we", padx=(0, 4), pady=4)
        ctk.CTkButton(row_btns, text="📄 Export PDF", command=self.export_pdf).grid(
            row=0, column=1, sticky="we", padx=(4, 0), pady=4)
        ctk.CTkButton(row_btns, text="🖨️ Print", command=self.print_card).grid(
            row=1, column=0, sticky="we", padx=(0, 4), pady=4)
        ctk.CTkButton(row_btns, text="🗄️ Save to DB", command=self.save_to_db).grid(
            row=1, column=1, sticky="we", padx=(4, 0), pady=4)

        ctk.CTkButton(form_scroll, text="📋 View Saved Records", fg_color="transparent",
                      border_width=1, command=self.open_records_window).grid(
            row=28, column=0, sticky="we", pady=(6, 4))
        ctk.CTkButton(form_scroll, text="🧹 Clear Form", fg_color="transparent",
                      border_width=1, command=self.clear_form).grid(
            row=29, column=0, sticky="we", pady=(4, 4))

    def _section_label(self, parent, text):
        return ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=15, weight="bold"),
                             text_color=("#1E3A8A", "#60A5FA"))

    def _labeled_entry(self, parent, label, row, placeholder="", default=""):
        ctk.CTkLabel(parent, text=label, anchor="w").grid(row=row, column=0, sticky="we", pady=(4, 2))
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        if default:
            entry.insert(0, default)
        entry.grid(row=row + 1, column=0, sticky="we", pady=(0, 4))
        entry.bind("<KeyRelease>", self._on_field_change)
        return entry

    def _upload_row(self, parent, row, label, command):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="we", pady=4)
        frame.grid_columnconfigure(0, weight=1)
        status = ctk.CTkLabel(frame, text=f"{label}: not set", anchor="w",
                               text_color=("#6B7280", "#9CA3AF"))
        status.grid(row=0, column=0, sticky="we")
        ctk.CTkButton(frame, text="Upload", width=80, command=command).grid(row=0, column=1)
        return status

    # ---------------------------- PREVIEW PANEL --------------------------
    def _build_preview_panel(self):
        right = ctk.CTkFrame(self)
        right.grid(row=0, column=1, sticky="nswe", padx=(8, 16), pady=16)
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(right, text="Live Preview", font=ctk.CTkFont(size=18, weight="bold"))
        header.grid(row=0, column=0, pady=(12, 8))

        preview_container = ctk.CTkFrame(right, fg_color=("#E5E7EB", "#1F2937"))
        preview_container.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)
        preview_container.grid_rowconfigure(0, weight=1)
        preview_container.grid_columnconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(preview_container, text="")
        self.preview_label.grid(row=0, column=0)

        self.status_var = tk.StringVar(value="Ready. Fill in the form and click Generate ID Card.")
        status_bar = ctk.CTkLabel(right, textvariable=self.status_var, anchor="w",
                                   text_color=("#4B5563", "#9CA3AF"))
        status_bar.grid(row=2, column=0, sticky="we", padx=20, pady=(0, 12))

    # ------------------------------------------------------------------
    # Template population
    # ------------------------------------------------------------------
    def _populate_templates(self):
        names = ["Generated (Default)"]
        if os.path.isdir(config.TEMPLATES_DIR):
            for fname in sorted(os.listdir(config.TEMPLATES_DIR)):
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    names.append(fname)
        self.template_menu.configure(values=names)
        self.template_var.set(names[0])

    def _selected_template_path(self) -> Optional[str]:
        val = self.template_var.get()
        if val == "Generated (Default)":
            return None
        return os.path.join(config.TEMPLATES_DIR, val)

    # ------------------------------------------------------------------
    # Auto ID numbering
    # ------------------------------------------------------------------
    def _auto_fill_id_number(self):
        next_id = self.db.get_next_id_number()
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, next_id)
        self._on_field_change()

    # ------------------------------------------------------------------
    # Upload handlers
    # ------------------------------------------------------------------
    def _upload_photo(self):
        path = filedialog.askopenfilename(
            title="Select Photo", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.photo_path = path
            self.lbl_photo.configure(text=f"Photo: {os.path.basename(path)}")
            self._on_field_change()

    def _upload_logo(self):
        path = filedialog.askopenfilename(
            title="Select Institute Logo", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.logo_path = path
            self.lbl_logo.configure(text=f"Logo: {os.path.basename(path)}")
            self._on_field_change()

    def _upload_signature(self):
        path = filedialog.askopenfilename(
            title="Select Signature", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.signature_path = path
            self.lbl_signature.configure(text=f"Signature: {os.path.basename(path)}")
            self._on_field_change()

    # ------------------------------------------------------------------
    # Data collection
    # ------------------------------------------------------------------
    def _collect_data(self) -> CardData:
        return CardData(
            name=self.entry_name.get().strip(),
            id_number=self.entry_id.get().strip(),
            department=self.entry_dept.get().strip(),
            phone=self.entry_phone.get().strip(),
            address=self.text_address.get("1.0", tk.END).strip(),
            institute_name=self.entry_institute.get().strip() or config.INSTITUTE_NAME,
            institute_tagline=self.entry_tagline.get().strip() or config.INSTITUTE_TAGLINE,
            photo_path=self.photo_path,
            logo_path=self.logo_path,
            signature_path=self.signature_path,
            template_path=self._selected_template_path(),
            valid_thru=self.entry_valid.get().strip(),
        )

    # ------------------------------------------------------------------
    # Live preview (debounced so typing stays smooth)
    # ------------------------------------------------------------------
    def _on_field_change(self, event=None):
        if self._debounce_job is not None:
            self.after_cancel(self._debounce_job)
        self._debounce_job = self.after(400, self._render_preview)

    def _schedule_preview_update(self):
        self._render_preview()

    def _render_preview(self):
        try:
            data = self._collect_data()
            image = self.generator.generate(data)
            self.last_card_image = image

            preview_size = (int(config.CARD_WIDTH * PREVIEW_SCALE),
                             int(config.CARD_HEIGHT * PREVIEW_SCALE))
            preview_img = image.resize(preview_size, Image.LANCZOS)
            self._preview_ctk_img = ctk.CTkImage(light_image=preview_img,
                                                  dark_image=preview_img,
                                                  size=preview_size)
            self.preview_label.configure(image=self._preview_ctk_img, text="")
        except Exception as exc:
            self.status_var.set(f"Preview error: {exc}")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def generate_card(self):
        self._render_preview()
        self.status_var.set("Card generated. You can now Save PNG, Export PDF, Print, "
                             "or Save to Database.")

    def _validate(self) -> bool:
        data = self._collect_data()
        if not data.name:
            messagebox.showwarning("Missing information", "Please enter the Name field.")
            return False
        if not data.id_number:
            messagebox.showwarning("Missing information", "Please enter or auto-generate an ID Number.")
            return False
        return True

    def save_png(self):
        if not self._validate():
            return
        if self.last_card_image is None:
            self.generate_card()
        id_number = self.entry_id.get().strip() or "id_card"
        default_name = f"{id_number}.png".replace("/", "-")
        path = filedialog.asksaveasfilename(
            title="Save ID Card as PNG", defaultextension=".png",
            initialdir=config.EXPORTS_DIR, initialfile=default_name,
            filetypes=[("PNG Image", "*.png")])
        if not path:
            return
        self.last_card_image.save(path, "PNG", dpi=(config.CARD_DPI, config.CARD_DPI))
        self.status_var.set(f"Saved PNG to: {path}")
        messagebox.showinfo("Saved", f"ID card saved as:\n{path}")

    def export_pdf(self):
        if not self._validate():
            return
        if self.last_card_image is None:
            self.generate_card()
        id_number = self.entry_id.get().strip() or "id_card"
        default_name = f"{id_number}.pdf".replace("/", "-")
        pdf_path = filedialog.asksaveasfilename(
            title="Export ID Card as PDF", defaultextension=".pdf",
            initialdir=config.EXPORTS_DIR, initialfile=default_name,
            filetypes=[("PDF Document", "*.pdf")])
        if not pdf_path:
            return
        tmp_png = os.path.join(config.EXPORTS_DIR, "_tmp_export_for_pdf.png")
        self.last_card_image.save(tmp_png, "PNG", dpi=(config.CARD_DPI, config.CARD_DPI))
        try:
            utils.export_image_to_pdf(tmp_png, pdf_path)
            self.status_var.set(f"Exported PDF to: {pdf_path}")
            messagebox.showinfo("Exported", f"ID card exported as PDF:\n{pdf_path}")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))
        finally:
            if os.path.exists(tmp_png):
                os.remove(tmp_png)

    def print_card(self):
        if not self._validate():
            return
        if self.last_card_image is None:
            self.generate_card()
        tmp_png = os.path.join(config.EXPORTS_DIR, "_tmp_print.png")
        self.last_card_image.save(tmp_png, "PNG", dpi=(config.CARD_DPI, config.CARD_DPI))
        ok, message = utils.print_file(tmp_png)
        self.status_var.set(message)
        if ok:
            messagebox.showinfo("Print", message)
        else:
            messagebox.showwarning("Print", message)

    def save_to_db(self):
        if not self._validate():
            return
        if self.last_card_image is None:
            self.generate_card()
        data = self._collect_data()

        existing = self.db.get_record_by_id_number(data.id_number)
        if existing:
            confirm = messagebox.askyesno(
                "ID already exists",
                f"An ID '{data.id_number}' already exists in the database.\n"
                f"Do you want to overwrite/update that record?")
            if not confirm:
                return

        os.makedirs(config.EXPORTS_DIR, exist_ok=True)
        safe_id = data.id_number.replace("/", "-")
        card_image_path = os.path.join(config.EXPORTS_DIR, f"{safe_id}.png")
        self.last_card_image.save(card_image_path, "PNG",
                                   dpi=(config.CARD_DPI, config.CARD_DPI))

        record = {
            "id_number": data.id_number,
            "name": data.name,
            "department": data.department,
            "phone": data.phone,
            "address": data.address,
            "photo_path": data.photo_path,
            "logo_path": data.logo_path,
            "signature_path": data.signature_path,
            "template_path": data.template_path,
            "card_image_path": card_image_path,
        }

        try:
            if existing:
                self.db.update_record(existing["id"], record)
                self.status_var.set(f"Updated database record for {data.id_number}.")
            else:
                self.db.insert_record(record)
                self.status_var.set(f"Saved new database record for {data.id_number}.")
            messagebox.showinfo("Database", "Record saved successfully.")
        except Exception as exc:
            messagebox.showerror("Database error", str(exc))

    def clear_form(self):
        for entry in (self.entry_name, self.entry_dept, self.entry_phone, self.entry_valid):
            entry.delete(0, tk.END)
        self.text_address.delete("1.0", tk.END)
        self.entry_institute.delete(0, tk.END)
        self.entry_institute.insert(0, config.INSTITUTE_NAME)
        self.entry_tagline.delete(0, tk.END)
        self.entry_tagline.insert(0, config.INSTITUTE_TAGLINE)
        self.photo_path = self.logo_path = self.signature_path = None
        self.lbl_photo.configure(text="Photo: not set")
        self.lbl_logo.configure(text="Institute Logo: not set")
        self.lbl_signature.configure(text="Digital Signature: not set")
        self.template_var.set("Generated (Default)")
        self._auto_fill_id_number()

    # ------------------------------------------------------------------
    # Records viewer window
    # ------------------------------------------------------------------
    def open_records_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Saved ID Card Records")
        win.geometry("900x480")
        win.grid_columnconfigure(0, weight=1)
        win.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(win, text="Saved Records", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        list_frame = ctk.CTkScrollableFrame(win)
        list_frame.grid(row=1, column=0, sticky="nswe", padx=16, pady=(0, 16))
        list_frame.grid_columnconfigure(0, weight=1)

        records = self.db.get_all_records()
        if not records:
            ctk.CTkLabel(list_frame, text="No records saved yet.").grid(row=0, column=0, pady=20)
            return

        for i, rec in enumerate(records):
            row = ctk.CTkFrame(list_frame, corner_radius=8)
            row.grid(row=i, column=0, sticky="we", pady=4, padx=2)
            row.grid_columnconfigure(1, weight=1)

            summary = (f"{rec.get('id_number')}  —  {rec.get('name')}\n"
                       f"{rec.get('department') or ''}   {rec.get('phone') or ''}")
            ctk.CTkLabel(row, text=summary, justify="left", anchor="w").grid(
                row=0, column=1, sticky="we", padx=10, pady=8)

            ctk.CTkButton(row, text="Load", width=70,
                          command=lambda r=rec, w=win: self._load_record(r, w)).grid(
                row=0, column=2, padx=6)
            ctk.CTkButton(row, text="Delete", width=70, fg_color="#B91C1C",
                          hover_color="#7F1D1D",
                          command=lambda r=rec, w=win: self._delete_record(r, w)).grid(
                row=0, column=3, padx=6)

    def _load_record(self, rec, window):
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, rec.get("name") or "")
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, rec.get("id_number") or "")
        self.entry_dept.delete(0, tk.END)
        self.entry_dept.insert(0, rec.get("department") or "")
        self.entry_phone.delete(0, tk.END)
        self.entry_phone.insert(0, rec.get("phone") or "")
        self.text_address.delete("1.0", tk.END)
        self.text_address.insert("1.0", rec.get("address") or "")

        self.photo_path = rec.get("photo_path") or None
        self.logo_path = rec.get("logo_path") or None
        self.signature_path = rec.get("signature_path") or None
        self.lbl_photo.configure(text=f"Photo: {os.path.basename(self.photo_path)}" if self.photo_path else "Photo: not set")
        self.lbl_logo.configure(text=f"Institute Logo: {os.path.basename(self.logo_path)}" if self.logo_path else "Institute Logo: not set")
        self.lbl_signature.configure(text=f"Digital Signature: {os.path.basename(self.signature_path)}" if self.signature_path else "Digital Signature: not set")

        template_path = rec.get("template_path")
        if template_path and os.path.exists(template_path):
            self.template_var.set(os.path.basename(template_path))
        else:
            self.template_var.set("Generated (Default)")

        window.destroy()
        self._render_preview()
        self.status_var.set(f"Loaded record {rec.get('id_number')} from database.")

    def _delete_record(self, rec, window):
        confirm = messagebox.askyesno("Delete record", f"Delete record '{rec.get('id_number')}'?")
        if confirm:
            self.db.delete_record(rec["id"])
            window.destroy()
            self.open_records_window()

    # ------------------------------------------------------------------
    def on_close(self):
        self.db.close()
        self.destroy()


def run_app():
    app = IDCardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
