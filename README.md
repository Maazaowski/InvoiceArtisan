<p align="center">
  <img src="https://img.shields.io/badge/InvoiceArtisan-1.0.0-blue" alt="InvoiceArtisan Logo" width="300">
</p>

<h1 align="center">InvoiceArtisan</h1>

<p align="center">
  <a href="#features">
    <img src="https://img.shields.io/badge/Elegant-Invoices-blue" alt="Elegant Invoices">
  </a>
  <a href="#installation">
    <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python 3.8+">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green" alt="License: MIT">
  </a>
  <a href="#installation">
    <img src="https://img.shields.io/badge/Easy-Setup-brightgreen" alt="Easy Setup">
  </a>
</p>

<p align="center">
  A professional Python-based invoice generator that creates beautifully designed PDF invoices from YAML templates.
</p>

## 📋 Table of Contents
- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [📝 Usage](#-usage)
  - [🖥️ GUI Application (Recommended)](#️-gui-application-recommended)
  - [💻 Command Line Usage](#-command-line-usage)
  - [Generating Invoices](#generating-invoices)
  - [Reading PDF Invoices](#reading-pdf-invoices)
  - [Converting PDF Invoices to YAML Templates](#converting-pdf-invoices-to-yaml-templates)
- [🖼️ Example Output](#-example-output)
- [🛠️ Customization](#-customization)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

- 🎨 Generate elegant, professional PDF invoices from YAML files
- 🖥️ **NEW: Modern GUI application** for complete invoice management
- 🔄 Flexible, customizable invoice templates
- 📊 Support for multiple line items with automatic numbering
- 🧮 Automatic calculation of subtotals and totals
- 💰 Tax calculation support
- 📋 Cleanly formatted client and company information
- 🔍 PDF reading capability for reviewing generated invoices
- 🔄 Convert existing PDF invoices to YAML templates
- 💼 Professional styling with customizable colors and formatting
- 🚀 **Automation features**: Auto-date setting, invoice numbering, due date calculation

## 🚀 Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/InvoiceArtisan.git
cd InvoiceArtisan
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## 📝 Usage

### 🖥️ GUI Application (Recommended)

InvoiceArtisan now includes a modern, user-friendly GUI application that automates the entire invoice generation process!

**Quick Start:**
```bash
python launch_gui.py
```

**Features:**
- **Complete Invoice Management**: Edit all invoice details through an intuitive interface
- **Real-time Preview**: See your invoice before generating the PDF
- **Automation**: Auto-generate dates, invoice numbers, and calculate totals
- **File Management**: Open, edit, and save YAML files directly
- **One-Click PDF Generation**: Generate professional PDFs with a single click

**Workflow:**
1. Launch the GUI: `python launch_gui.py`
2. Fill in invoice details using the tabbed interface
3. Preview your invoice
4. Click "Generate PDF Invoice"
5. Done! PDF opens automatically

For detailed GUI usage instructions, see [README_GUI.md](README_GUI.md).

### 💻 Command Line Usage

#### Generating Invoices

1. Create a YAML file with your invoice details (or use the provided template)
```yaml
invoice:
  number: INV-001
  date: '2023-04-01'
  due_date: '2023-05-01'
company:
  name: Your Company Name
  # ... other company details
```

2. Run the generator:
```bash
python invoice_generator.py your_invoice.yaml
```

### Reading PDF Invoices

To review a generated PDF invoice or any PDF file:
```bash
python pdf_reader.py your_invoice.pdf
```

### Converting PDF Invoices to YAML Templates

To convert an existing PDF invoice into a YAML template:
```bash
python pdf_to_yaml.py existing_invoice.pdf
```

This creates a YAML template file that can be used for generating new invoices with the same layout.

## 🖼️ Example Output

After running the generator, you'll get a professional PDF invoice that includes:

- Company and client information with proper alignment
- Professional header with logo
- Itemized list of products/services
- Automatic calculations for subtotals and taxes
- Payment details and terms
- Clean and elegant styling

## 🛠️ Customization

InvoiceArtisan offers several ways to customize your invoices:

- **Colors**: Modify the color scheme in `invoice_generator.py`
- **Styling**: Adjust fonts, spacing, and layout in the generator
- **Logo**: Replace the logo file in the `logo/` directory
- **Template**: Modify the YAML structure for custom fields
- **GUI Themes**: Customize the GUI appearance in `invoice_gui.py`
- **Default Data**: Modify default invoice information in the GUI application

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆕 What's New in v2.0

InvoiceArtisan v2.0 introduces a **modern GUI application** that revolutionizes the invoice creation process:

- **No more manual YAML editing** - Everything is done through an intuitive interface
- **Real-time preview** - See your invoice before generating the PDF
- **Automation features** - Auto-generate dates, numbers, and calculate totals
- **Professional workflow** - From invoice creation to PDF generation in minutes

The GUI maintains full compatibility with existing YAML files and the command-line tools, so you can continue using your current workflow while enjoying the new interface.

**Try it now:** `python launch_gui.py` 