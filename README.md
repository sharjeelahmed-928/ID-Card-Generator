# 🪪 Premium ID Card Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green?style=for-the-badge)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge)
![MySQL](https://img.shields.io/badge/Optional-MySQL-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

### 🚀 A Modern Desktop Application for Creating Professional ID Cards

Generate beautiful, high-quality, print-ready ID cards with **Live Preview**, **QR Codes**, **Barcodes**, **Database Integration**, **PDF Export**, and **Direct Printing**.

---

### 👨‍💻 Developed by **Sharjeel Ahmed**

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github&style=for-the-badge)](https://github.com/sharjeelahmed-928)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/sharjeel-ahmed-3ba220368)
[![YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?logo=youtube&style=for-the-badge)](https://www.youtube.com/@SharjeelAhmed928)

</div>

---

# ✨ Features

## 🎨 Professional ID Card Designer
- Beautiful modern interface built using **CustomTkinter**
- Live card preview while editing
- Professional card templates
- Custom backgrounds supported

## 👤 Personal Information
- Full Name
- ID Number
- Department / Class
- Phone Number
- Address

## 🖼️ Image Support
- Upload Profile Photo
- Upload Institute Logo
- Upload Digital Signature
- Automatic image positioning

## 📱 Smart Technologies
- QR Code Generation
- Code128 Barcode Generation
- Automatic ID Number Generation

## 💾 Export Options
- High Quality PNG (300 DPI)
- Professional PDF Export
- Direct Printing
- Print-ready Output

## 🗄 Database Integration
- SQLite Support
- Optional MySQL Support
- Save Records
- Reload Existing Records
- Delete Records

---


# 📂 Project Structure

```text
idcard_generator/
│
├── main.py
├── requirements.txt
├── generate_default_assets.py
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── gui.py
│   ├── database.py
│   ├── utils.py
│   └── card_generator.py
│
├── assets/
│   ├── fonts/
│   └── templates/
│
├── exports/
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/sharjeelahmed-928/idcard_generator.git
```

```bash
cd idcard_generator
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
python main.py
```

---

# 🖥️ Technologies Used

- Python
- CustomTkinter
- Pillow (PIL)
- SQLite
- MySQL Connector
- QRCode
- Barcode
- ReportLab
- Tkinter
- OS Printing

---

# 🚀 Workflow

```text
Enter Details
      │
      ▼
Upload Images
      │
      ▼
Live Preview
      │
      ▼
Generate ID Card
      │
      ▼
Save / Print / Export PDF
      │
      ▼
Store in Database
```

---

# ⭐ Key Highlights

✔ Modern GUI

✔ Automatic ID Generation

✔ QR Code Support

✔ Barcode Generation

✔ SQLite Database

✔ Optional MySQL

✔ PDF Export

✔ PNG Export

✔ Direct Printing

✔ Live Preview

✔ Professional Templates

✔ High Resolution Output

---

# 🛠 Customization

You can easily customize:

- Card Dimensions
- Fonts
- Colors
- Templates
- Logos
- QR Code Position
- Barcode Position
- Footer
- Header
- Export Resolution

Simply edit:

```
app/config.py
```

and

```
app/card_generator.py
```

---

# 📄 Export Formats

| Format | Supported |
|---------|-----------|
| PNG | ✅ |
| PDF | ✅ |
| Print | ✅ |

---

# 💾 Database Support

### SQLite (Default)

Automatically creates:

```
idcards.db
```

### MySQL (Optional)

Simply configure:

```bash
IDCARD_DB_TYPE=mysql
```

along with your database credentials.

---

# 🎯 Future Improvements

- Employee Cards
- Student Cards
- NFC Support
- Cloud Database
- Multiple Card Sizes
- Themes
- Dark Mode
- CSV Import
- Batch ID Generation
- User Authentication

---

# 🤝 Contributing

Contributions are always welcome!

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 👨‍💻 Author

## Sharjeel Ahmed

**GitHub**

https://github.com/sharjeelahmed-928

**LinkedIn**

https://www.linkedin.com/in/sharjeel-ahmed-3ba220368

**YouTube**

https://www.youtube.com/@SharjeelAhmed928

---

# ⭐ Support

If you like this project, don't forget to **Star ⭐ the repository**.

It really helps and motivates future development.

---

<div align="center">

## 💙 Thank You for Visiting

**Made with ❤️ using Python**

⭐ Star • 🍴 Fork • 📢 Share

</div>
