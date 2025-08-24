# InvoiceArtisan

<p align="center">
  <img src="https://img.shields.io/badge/InvoiceArtisan-2.0.0-blue" alt="InvoiceArtisan Logo" width="300">
</p>

<p align="center">
  <strong>A professional Python-based invoice generator with modern GUI and command-line tools</strong>
</p>

## 🎯 Overview

InvoiceArtisan is a comprehensive invoice generation system that combines the power of Python with an intuitive graphical interface. Create professional PDF invoices from YAML templates, manage client information, and automate your billing workflow.

## ✨ Features

- 🎨 **Modern GUI Application** - Intuitive tab-based interface for complete invoice management
- 📄 **PDF Generation** - Professional invoice layouts with customizable styling
- 🔄 **YAML Templates** - Flexible, human-readable invoice templates
- 📊 **Item Management** - Add, edit, and calculate line items automatically
- 💰 **Tax Calculation** - Built-in tax rate support and calculations
- 🚀 **Automation** - Auto-generate dates, invoice numbers, and due dates
- 💻 **Command Line** - CLI tools for batch processing and automation
- 🏗️ **Executable Builder** - Create standalone .exe files for easy distribution

## 🏗️ Project Structure

```
InvoiceArtisan/
├── src/                    # Source code
│   ├── core/              # PDF generation, reading, conversion
│   ├── gui/               # GUI application and components
│   └── utils/             # Utility functions and helpers
├── assets/                 # Logos, templates, icons
├── config/                 # Configuration files
├── build/                  # Build tools and PyInstaller config
├── docs/                   # Documentation
├── scripts/                # Launchers and setup scripts
├── tests/                  # Test suite
└── output/                 # Generated files (gitignored)
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/InvoiceArtisan.git
cd InvoiceArtisan

# Run setup script (recommended)
python scripts/setup.py

# Or install manually
pip install -r build/requirements/requirements.txt
```

### 2. Launch Application

```bash
# GUI Application (Recommended)
python scripts/launch_gui.py

# Command Line Interface
python scripts/launch_cli.py --help
```

### 3. Create Your First Invoice

1. Launch the GUI application
2. Fill in company and client information
3. Add invoice items and services
4. Preview your invoice
5. Generate PDF with one click!

## 📖 Documentation

- **[GUI Guide](docs/GUI_README.md)** - Complete GUI usage instructions
- **[Build Guide](docs/BUILD_README.md)** - Creating standalone executables
- **[API Reference](docs/API_README.md)** - Developer documentation
- **[Examples](docs/examples/)** - Usage examples and templates

## 🛠️ Development

### Prerequisites

- Python 3.8+
- Git

### Development Setup

```bash
# Install development dependencies
pip install -r build/requirements/requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black src/
flake8 src/
```

### Project Structure

- **`src/core/`** - Core business logic for invoice generation
- **`src/gui/`** - Tkinter-based GUI application
- **`src/utils/`** - Helper functions and utilities
- **`build/`** - PyInstaller configuration and build scripts
- **`config/`** - Application and build configuration files

## 🔧 Building Executables

Create standalone executables for easy distribution:

```bash
# Quick build (Windows)
build\scripts\build_exe.bat

# Manual build
python build/scripts/build_exe.py
```

See [BUILD_README.md](docs/BUILD_README.md) for detailed instructions.

## 📋 Usage Examples

### GUI Application

```bash
python scripts/launch_gui.py
```

- **Invoice Details Tab** - Set invoice number, dates, and tax rates
- **Company Tab** - Configure your business information
- **Client Tab** - Manage client details
- **Items Tab** - Add and manage line items
- **Notes & Terms** - Customize invoice notes and terms
- **Preview & Generate** - Preview and generate PDF invoices

### Command Line

```bash
# Generate PDF from YAML
python scripts/launch_cli.py generate invoice.yaml

# Read PDF content
python scripts/launch_cli.py read invoice.pdf

# Convert PDF to YAML
python scripts/launch_cli.py convert invoice.pdf
```

## 🎨 Customization

### Themes and Styling

Modify `config/app_config.yaml` to customize:
- GUI colors and themes
- Invoice styling and fonts
- Default values and validation rules
- File paths and output settings

### Invoice Templates

Edit `config/default_invoice.yaml` to set:
- Default company information
- Standard invoice items
- Payment terms and notes
- Tax rates and calculations

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Check the [docs/](docs/) directory
- **Examples**: See [docs/examples/](docs/examples/) for usage examples

## 🆕 What's New in v2.0

- **Complete GUI Overhaul** - Modern, tab-based interface
- **Project Restructuring** - Clean, maintainable codebase
- **Configuration Management** - Centralized settings and templates
- **Build System** - Professional executable creation tools
- **Documentation** - Comprehensive guides and examples
- **Development Tools** - Testing, linting, and code quality tools

---

**Built with ❤️ by Syed Muhammad Maaz**

*Professional invoice generation made simple and elegant.*
