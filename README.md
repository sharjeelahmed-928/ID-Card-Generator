# 🪪 Premium ID Card Generator

### Create Professional, Secure & Print-Ready ID Cards with Ease

A modern desktop application built with **Python** and **CustomTkinter** that enables institutions, schools, universities, companies, and organizations to design, preview, export, print, and manage professional ID cards effortlessly.



![](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/CustomTkinter-Modern%20GUI-00C853?style=for-the-badge)
![](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/MySQL-Supported-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![](https://img.shields.io/badge/PDF-Export-red?style=for-the-badge)
![](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)






![](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)



![](https://img.shields.io/badge/Watch-Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)



![](https://img.shields.io/badge/LinkedIn-Sharjeel_Ahmed-0A66C2?style=for-the-badge&logo=linkedin)




---

### ⭐ If you find this project useful, don't forget to give it a Star!



---

# 📖 Table of Contents

- [✨ Overview](#-overview)
- [🚀 Why This Project?](#-why-this-project)
- [🌟 Key Features](#-key-features)
- [🖼 Screenshots](#-screenshots)
- [⚡ Live Preview Workflow](#-live-preview-workflow)
- [🎯 Perfect For](#-perfect-for)
- [🛠 Technology Stack](#-technology-stack)

---

# ✨ Overview

**Premium ID Card Generator** is a professional desktop application designed to simplify the creation of high-quality identity cards.

Instead of relying on complicated design software, this application provides an intuitive graphical interface where users can generate beautiful, print-ready ID cards in just a few clicks.

Every card can include:

- 👤 Personal Information
- 🖼 Photograph
- 🏛 Institute Logo
- ✍ Digital Signature
- 🔳 QR Code
- 📦 Barcode
- 🎨 Background Template

The generated cards can then be:

- 🖼 Exported as High-Resolution PNG
- 📄 Exported as Print-Ready PDF
- 🖨 Printed Directly
- 💾 Stored in a Database

Whether you're creating a single ID card or managing hundreds of records, this application offers a streamlined and professional workflow.

---

# 🚀 Why This Project?

Creating professional ID cards traditionally requires multiple software tools for:

- Designing
- Editing
- Barcode Generation
- QR Code Generation
- Exporting
- Printing

This application combines everything into **one modern desktop application**, allowing you to complete the entire process without switching between different programs.

### Benefits

- ⚡ Fast Workflow
- 🎨 Modern User Interface
- 🖨 Professional Print Quality
- 💾 Built-in Database
- 🔳 Automatic QR Code Generation
- 📦 Automatic Barcode Generation
- 🪪 Professional Card Templates
- 📄 One-Click PDF Export
- 🖼 300 DPI PNG Export
- 🖨 Native Printing Support

---

# 🌟 Key Features

## 🖥 Modern Desktop Interface

Built using **CustomTkinter** for a clean, responsive, and user-friendly experience.

---

## 👤 Smart Information Management

Easily manage:

- Full Name
- ID Number
- Department / Class
- Phone Number
- Address

Changes are reflected instantly in the live preview.

---

## 📷 Professional Photo Processing

Supports:

- PNG
- JPG
- JPEG
- BMP
- WEBP

Automatically:

- Crops
- Resizes
- Centers
- Frames

the uploaded photo for a polished appearance.

---

## 🏛 Institution Branding

Upload your organization's logo and seamlessly integrate it into every ID card.

Ideal for:

- Schools
- Universities
- Colleges
- Companies
- NGOs
- Government Organizations

---

## ✍ Digital Signature Support

Attach an authorized signature to improve authenticity and professionalism.

---

## 🎨 Multiple Background Templates

Choose from built-in templates or add your own custom designs.

Simply place your images inside:

```text
assets/templates/

They will automatically appear inside the application.

⚡ Real-Time Live Preview

Every modification updates instantly.

No refresh.

No reload.

No waiting.

🔢 Automatic ID Generation

Automatically generates professional IDs such as:

GIT-0001
GIT-0002
GIT-0003

You can also manually edit the generated value whenever needed.

🔳 QR Code Generation

Every card includes a QR Code containing:

Name

ID Number

Department

Phone Number

Perfect for instant verification using any smartphone.

📦 Barcode Generation

Professional Code128 barcode generated directly from the ID number.

Suitable for attendance systems and inventory tracking.

🖼 High Resolution Export

Generate professional:

PNG (300 DPI)

Print Ready

High Quality

📄 PDF Export

Export your ID card as a professionally centered A4 PDF complete with cut guides for commercial printing.

🖨 Direct Printing

Print directly to your default printer without leaving the application.

Supports:

Windows

Linux

macOS

💾 Database Integration

Store all records permanently.

Supported Databases:

SQLite (Default)

MySQL (Optional)

Manage records with:

Save

Browse

Reload

Delete

🖼 Screenshots

Coming Soon

Replace this section with screenshots of:

🏠 Main Window

⚡ Live Preview

🎨 Background Templates

💾 Database Viewer

📄 PDF Export

🖨 Printing

Example:



![](screenshots/main.png)



⚡ Live Preview Workflow

Enter Information
        │
        ▼
 Upload Images
        │
        ▼
Choose Template
        │
        ▼
 Live Preview
        │
        ▼
Generate ID Card
        │
        ▼
Export PNG / PDF
        │
        ▼
 Print or Save to Database

🎯 Perfect For

This project is suitable for:

🏫 Schools

🎓 Universities

🏢 Companies

🏥 Hospitals

🏛 Government Offices

👮 Security Agencies

🏭 Industries

🏢 Corporate Organizations

🧑‍💼 Human Resource Departments

📚 Training Institutes

🛠 Technology Stack

Technology

Purpose

Python

Core Programming Language

CustomTkinter

Modern Desktop GUI

Pillow (PIL)

Image Processing

SQLite

Local Database

MySQL

Optional Database Backend

ReportLab

PDF Export

qrcode

QR Code Generation

python-barcode

Code128 Barcode Generation

📌 Next: Installation, project structure, usage guide, configuration, database setup, customization, and export options.



---

# 📂 Project Structure

```text
idcard_generator/
│
├── main.py                        # Application entry point
├── generate_default_assets.py     # Generates default background templates
├── requirements.txt               # Project dependencies
│
├── app/
│   ├── config.py                  # Global configuration
│   ├── database.py                # SQLite/MySQL database layer
│   ├── card_generator.py          # ID card rendering engine
│   ├── gui.py                     # CustomTkinter user interface
│   └── utils.py                   # Helper functions
│
├── assets/
│   ├── templates/                 # Background templates
│   └── fonts/                     # Custom fonts
│
├── exports/                       # Generated PNG & PDF files
│
└── idcards.db                     # SQLite database (created automatically)
```

---

# 🚀 Installation

## 📋 Requirements

Before you begin, ensure you have:

- Python **3.9 or newer**
- Recommended: **Python 3.10 – 3.13**
- Git

> **Note:** Very new Python releases may temporarily lack prebuilt wheels for some dependencies (such as Pillow). If installation fails, Python **3.11** or **3.12** is recommended.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/idcard_generator.git

cd idcard_generator
```

---

## 2️⃣ Create a Virtual Environment

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

## 3️⃣ Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## 📦 Optional MySQL Support

SQLite works out of the box.

If you'd like to use **MySQL**, install:

```bash
pip install mysql-connector-python
```

---

## ⚠ Pillow Installation Issue

If you encounter:

```text
Failed building wheel for Pillow
```

Try:

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

If the issue persists, install **Python 3.11** or **3.12**, recreate your virtual environment, and reinstall the dependencies.

---

# ▶ Running the Application

Start the application with:

```bash
python main.py
```

---

## 🎉 First Launch

On the first run, the application automatically:

- ✅ Generates default background templates
- ✅ Creates the SQLite database
- ✅ Creates required folders
- ✅ Launches the graphical interface

No additional configuration is required.

---

# 📖 How to Use

## Step 1 — Enter Information

Provide the user's:

- Name
- Department / Class
- Phone Number
- Address

The **ID Number** is generated automatically.

---

## Step 2 — Upload Images

Attach:

- 📷 Profile Photo
- 🏛 Institute Logo
- ✍ Digital Signature

Supported formats:

- PNG
- JPG
- JPEG
- BMP
- WEBP

---

## Step 3 — Choose a Background

Select any built-in template or add your own.

Custom templates should be placed in:

```text
assets/templates/
```

---

## Step 4 — Preview

Watch your ID card update instantly in the live preview.

No manual refresh required.

---

## Step 5 — Generate

Click

```text
⚡ Generate ID Card
```

to generate a fresh high-quality card.

---

## Step 6 — Export

Choose one of the available options:

- 💾 Save PNG
- 📄 Export PDF
- 🖨 Print

---

## Step 7 — Save to Database

Store the record for future editing and retrieval.

Later you can:

- Browse
- Reload
- Delete

saved records.

---

# 💾 Database Support

The application supports two database engines.

| Database | Status |
|----------|--------|
| SQLite | ✅ Default |
| MySQL | ✅ Optional |

SQLite requires no setup.

---

# 🛢 Switching to MySQL

### Linux / macOS

```bash
export IDCARD_DB_TYPE=mysql
export IDCARD_MYSQL_HOST=localhost
export IDCARD_MYSQL_USER=root
export IDCARD_MYSQL_PASSWORD=yourpassword
export IDCARD_MYSQL_DB=idcard_generator

python main.py
```

---

### Windows

```cmd
set IDCARD_DB_TYPE=mysql
set IDCARD_MYSQL_HOST=localhost
set IDCARD_MYSQL_USER=root
set IDCARD_MYSQL_PASSWORD=yourpassword
set IDCARD_MYSQL_DB=idcard_generator

python main.py
```

---

If the MySQL connection fails, the application automatically switches back to SQLite so you can continue working without interruption.

---

# 🎨 Customization

The project is designed with modularity in mind.

## ⚙ Configuration

Modify application-wide settings in:

```text
app/config.py
```

You can customize:

- Card Dimensions
- DPI
- Colors
- Fonts
- Default Institute Information
- Export Settings

---

## 🎴 Card Layout

Control every element of the ID card in:

```text
app/card_generator.py
```

Each component is rendered independently.

Example sections include:

- Header
- Photo
- Fields
- QR Code
- Barcode
- Signature
- Footer

making customization simple and maintainable.

---

## 🖼 Custom Background Templates

Simply add your own image files to:

```text
assets/templates/
```

Supported formats:

- PNG
- JPG
- JPEG

Recommended size:

```text
1013 × 638 pixels
```

(CR80 card at 300 DPI)

---

## 🔤 Custom Fonts

Place your TrueType fonts inside:

```text
assets/fonts/
```

and reference them through the font helper in `utils.py`.

---

# 📤 Export Options

## 🖼 PNG

- 300 DPI
- High Resolution
- Print Ready

---

## 📄 PDF

- A4 Layout
- Centered Card
- Professional Cut Guides

Perfect for commercial printing.

---

# 🖨 Printing

The application supports native printing.

### Windows

Uses:

```python
os.startfile(file, "print")
```

No additional configuration is required.

---

### Linux / macOS

Uses the CUPS printing system via:

```bash
lp
```

Verify your printer using:

```bash
lpstat -d
```

---

# 🔒 QR Code

Each generated QR Code securely stores:

- ID Number
- Name
- Department
- Phone Number

The information is encoded as a lightweight JSON payload and can be scanned using most smartphone cameras.

---

# 📦 Barcode

Every card automatically includes a **Code128** barcode generated from the ID number.

This is ideal for:

- Attendance Systems
- Access Control
- Library Management
- Inventory Tracking

---

# 💡 Performance

Designed to provide:

- ⚡ Fast Rendering
- ⚡ Instant Preview
- ⚡ Low Memory Usage
- ⚡ High Resolution Output
- ⚡ Smooth Desktop Experience

Even on entry-level computers.

````md
---

# 🛣️ Roadmap

The following features are planned for future releases.

## 🎯 Upcoming Features

- [ ] Batch ID Card Generation
- [ ] Excel Import (.xlsx)
- [ ] CSV Import
- [ ] Bulk Photo Import
- [ ] Drag & Drop Card Designer
- [ ] Dual-Sided ID Cards
- [ ] Cloud Database Support
- [ ] Authentication System
- [ ] User Roles & Permissions
- [ ] Dark Mode
- [ ] Custom Themes
- [ ] Multi-Language Support
- [ ] Email ID Cards
- [ ] Batch Printing
- [ ] Batch PDF Export
- [ ] Cloud Backup
- [ ] Automatic Updates
- [ ] Card Expiry Management
- [ ] NFC / RFID Integration
- [ ] REST API Support

---

# ❓ Frequently Asked Questions


### Which operating systems are supported?

The application works on:

- Windows
- Linux
- macOS




### Which database does the application use?

SQLite is the default database.

You can also switch to MySQL by setting the appropriate environment variables.




### Can I add my own background templates?

Yes.

Simply copy your PNG or JPG files into:

```text
assets/templates/
```

They will automatically appear in the application.




### Can I customize the card design?

Absolutely.

The rendering engine is modular, allowing you to change:

- Layout
- Colors
- Fonts
- Card Size
- QR Position
- Barcode Position
- Signature Placement
- Footer
- Header




### Can I print directly from the application?

Yes.

The application supports native printing on Windows, Linux, and macOS.



---

# 📈 Future Vision

The goal of **Premium ID Card Generator** is to become a complete desktop solution for identity card management.

Future versions aim to include:

- Cloud Synchronization
- Online Database
- Mobile Companion App
- Smart Card Templates
- Face Detection
- AI Background Removal
- Employee Management
- Student Management
- Attendance Integration
- NFC Smart Cards
- Enterprise Dashboard

---

# 🤝 Contributing

Contributions are always welcome!

If you'd like to improve this project:

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes.

```bash
git commit -m "Add amazing feature"
```

4. Push your branch.

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request.

Every contribution—whether it's fixing bugs, improving documentation, or adding new features—is appreciated.

---

# 🐞 Found a Bug?

If you discover an issue:

- Open a GitHub Issue
- Describe the problem clearly
- Include screenshots (if applicable)
- Explain how to reproduce it

This helps improve the project for everyone.

---

# 💡 Suggestions

Have an idea?

Feature requests are always welcome.

Open an issue and share your suggestion.

---

# 🌟 Support the Project

If you found this project helpful:

⭐ Star the repository

🍴 Fork the project

📢 Share it with others

Every star motivates future development.

---

# 📊 Project Status

| Feature | Status |
|----------|--------|
| Desktop GUI | ✅ Stable |
| PNG Export | ✅ Stable |
| PDF Export | ✅ Stable |
| QR Code | ✅ Stable |
| Barcode | ✅ Stable |
| SQLite | ✅ Stable |
| MySQL | ✅ Supported |
| Printing | ✅ Stable |
| Live Preview | ✅ Stable |
| Template System | ✅ Stable |

---

# 🔒 Security

The project does **not** collect, transmit, or share personal information.

All generated data remains on your local computer unless you explicitly configure your own database server.

---

# 🙏 Acknowledgements

Special thanks to the amazing open-source community and the maintainers of:

- Python
- CustomTkinter
- Pillow
- ReportLab
- qrcode
- python-barcode
- SQLite
- MySQL Connector

Without these projects, this application would not have been possible.

---

# 📄 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute it in accordance with the license terms.

---

# 👨‍💻 Author



## Sharjeel Ahmed

### Software Developer • AI Enthusiast • Full-Stack Developer




![](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)



![](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)



![](https://img.shields.io/badge/YouTube-Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)




*Passionate about building modern software, AI-powered applications, and elegant user experiences.*



---

# 💖 Show Your Support

If you enjoyed this project, consider giving it a ⭐ on GitHub.

It helps more developers discover the project and encourages future improvements.

---



# 🪪 Premium ID Card Generator

### Designed for Professionals • Built with Python • Powered by CustomTkinter

**Create Beautiful, Professional, and Print-Ready ID Cards in Minutes.**

⭐ **Don't forget to Star the Repository!** ⭐

