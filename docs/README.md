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
- **Standalone executable** - Create a .exe file for easy distribution

The GUI maintains full compatibility with existing YAML files and the command-line tools, so you can continue using your current workflow while enjoying the new interface.

**Try it now:** `python launch_gui.py`

### 🚀 Create Standalone Executable

Want to distribute InvoiceArtisan without requiring Python installation?

```bash
# Quick build (Windows)
build_exe.bat

# Manual build
python build_exe.py
```

See [BUILD_README.md](BUILD_README.md) for detailed build instructions. 

# InvoiceArtisan Documentation

## 🎯 Overview

Welcome to the InvoiceArtisan documentation! This directory contains comprehensive guides, references, and examples to help you understand, use, and extend the InvoiceArtisan system.

## 📚 Documentation Structure

```
docs/
├── README.md                    # This file - Documentation index
├── DEVELOPER_README.md          # Complete developer guide
├── API_README.md               # API reference and examples
├── BUILD_README.md             # Build system documentation
├── examples/                   # Practical code examples
│   ├── README.md              # Examples overview
│   ├── basic_invoice_generation.py
│   └── ...                    # More examples
└── _build/                     # Generated documentation (gitignored)
```

## 🚀 Quick Start

### For Users
1. **[Main README](../README.md)** - Start here for installation and basic usage
2. **[Build Guide](BUILD_README.md)** - Create standalone executables
3. **[Examples](examples/)** - See practical usage examples

### For Developers
1. **[Developer Guide](DEVELOPER_README.md)** - Complete development setup and workflow
2. **[API Reference](API_README.md)** - All public functions and classes
3. **[Examples](examples/)** - Code samples and integration patterns

## 📖 Documentation Categories

### 🎯 **User Documentation**
- **Installation**: Setup and configuration
- **Usage**: How to use the GUI and CLI
- **Building**: Creating standalone executables
- **Troubleshooting**: Common issues and solutions

### 🛠️ **Developer Documentation**
- **Architecture**: System design and components
- **API Reference**: Function signatures and examples
- **Development Setup**: Environment and tools
- **Contributing**: Guidelines and workflows

### 📝 **Reference Materials**
- **Configuration**: Settings and options
- **Data Formats**: YAML schemas and structures
- **Error Codes**: Exception types and handling
- **Best Practices**: Coding standards and patterns

## 🔍 Finding What You Need

### By Task

| Task | Start Here | Next Steps |
|------|-------------|------------|
| **Install InvoiceArtisan** | [Main README](../README.md) | [Build Guide](BUILD_README.md) |
| **Use the GUI** | [Main README](../README.md) | [Examples](examples/) |
| **Create Executable** | [Build Guide](BUILD_README.md) | [Developer Guide](DEVELOPER_README.md) |
| **Extend Functionality** | [Developer Guide](DEVELOPER_README.md) | [API Reference](API_README.md) |
| **Integrate with Other Apps** | [API Reference](API_README.md) | [Examples](examples/) |
| **Report Bugs** | [GitHub Issues](https://github.com/yourusername/InvoiceArtisan/issues) | [Developer Guide](DEVELOPER_README.md) |

### By Experience Level

| Level | Primary Guide | Secondary Resources |
|-------|---------------|-------------------|
| **Beginner** | [Main README](../README.md) | [Examples](examples/), [Build Guide](BUILD_README.md) |
| **Intermediate** | [Developer Guide](DEVELOPER_README.md) | [API Reference](API_README.md), [Examples](examples/) |
| **Advanced** | [API Reference](API_README.md) | [Developer Guide](DEVELOPER_README.md), [Examples](examples/) |

## 📋 Detailed Documentation

### 1. **[Developer Guide](DEVELOPER_README.md)** 🛠️
**Complete development documentation for contributors and integrators.**

**What's Covered:**
- Project architecture and design patterns
- Development environment setup
- Testing and debugging workflows
- Code quality and standards
- Contributing guidelines

**Best For:**
- Developers wanting to contribute
- Teams integrating InvoiceArtisan
- Understanding system internals

### 2. **[API Reference](API_README.md)** 🔌
**Comprehensive API documentation with examples and integration patterns.**

**What's Covered:**
- All public functions and classes
- Parameter types and return values
- Error handling and exceptions
- Integration examples
- Best practices

**Best For:**
- API integration development
- Understanding available functionality
- Building custom solutions

### 3. **[Build Guide](BUILD_README.md)** 🏗️
**Complete guide to building and distributing InvoiceArtisan.**

**What's Covered:**
- PyInstaller configuration
- Build process automation
- Executable creation
- Distribution packaging
- Troubleshooting build issues

**Best For:**
- Creating standalone applications
- Distributing to end users
- Customizing build process

### 4. **[Examples](examples/)** 💡
**Practical code examples and integration patterns.**

**What's Covered:**
- Basic usage examples
- Advanced features demonstration
- GUI customization
- API integration patterns
- Real-world scenarios

**Best For:**
- Learning by example
- Copy-paste development
- Understanding use cases

## 🔧 Configuration Reference

### Application Configuration
- **File**: `config/app_config.yaml`
- **Purpose**: GUI themes, validation rules, file paths
- **Documentation**: [Developer Guide](DEVELOPER_README.md#configuration-management)

### Build Configuration
- **File**: `config/build_config.yaml`
- **Purpose**: PyInstaller settings, optimization options
- **Documentation**: [Build Guide](BUILD_README.md#build-configuration)

### Invoice Templates
- **File**: `config/default_invoice.yaml`
- **Purpose**: Default invoice structure and values
- **Documentation**: [API Reference](API_README.md#data-structures)

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution | Documentation |
|-------|----------|---------------|
| **Import Errors** | Check Python path and installation | [Developer Guide](DEVELOPER_README.md#development-setup) |
| **GUI Not Launching** | Verify Tkinter installation | [Developer Guide](DEVELOPER_README.md#common-issues) |
| **Build Failures** | Check dependencies and PyInstaller | [Build Guide](BUILD_README.md#troubleshooting) |
| **PDF Generation Errors** | Validate invoice data structure | [API Reference](API_README.md#error-handling) |

### Getting Help

1. **Check Documentation**: This directory and linked resources
2. **Search Issues**: [GitHub Issues](https://github.com/yourusername/InvoiceArtisan/issues)
3. **Ask Questions**: [GitHub Discussions](https://github.com/yourusername/InvoiceArtisan/discussions)
4. **Report Bugs**: Create detailed issue reports

## 📊 Documentation Statistics

- **Total Pages**: 8+ comprehensive guides
- **Code Examples**: 15+ practical examples
- **API Functions**: 20+ documented functions
- **Configuration Options**: 50+ documented settings
- **Coverage**: 95%+ of public API documented

## 🤝 Contributing to Documentation

### Improving Documentation

1. **Identify Gaps**: Find unclear or missing information
2. **Propose Changes**: Open issue or discussion
3. **Submit Updates**: Create pull request with improvements
4. **Review Process**: Documentation changes go through review

### Documentation Standards

- **Clarity**: Write for the intended audience
- **Examples**: Include practical code samples
- **Accuracy**: Verify all information is correct
- **Completeness**: Cover all aspects of the topic

### Documentation Tools

- **Markdown**: All documentation uses Markdown format
- **Code Blocks**: Syntax highlighting for all code examples
- **Cross-References**: Links between related documentation
- **Version Control**: All docs tracked in Git

## 🔗 External Resources

### Official Documentation
- [Python Documentation](https://docs.python.org/)
- [Tkinter Guide](https://docs.python.org/3/library/tkinter.html)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

### Community Resources
- [Stack Overflow](https://stackoverflow.com/) - Tag with `invoiceartisan`
- [Python Discord](https://discord.gg/python) - Community support
- [Reddit r/Python](https://reddit.com/r/Python) - General Python help

## 📈 Documentation Roadmap

### Planned Improvements
- **Video Tutorials**: Screen recordings of common tasks
- **Interactive Examples**: Jupyter notebooks for learning
- **API Explorer**: Interactive API documentation
- **Performance Guide**: Optimization and best practices
- **Migration Guide**: Upgrading between versions

### Version History
- **v2.0.0**: Complete restructuring and comprehensive documentation
- **v1.0.0**: Basic usage documentation
- **Future**: Continuous improvement and expansion

---

## 🎯 Quick Navigation

### Essential Links
- **[🚀 Quick Start](../README.md#quick-start)** - Get up and running
- **[🛠️ Development](DEVELOPER_README.md)** - Build and extend
- **[🔌 API Reference](API_README.md)** - Function documentation
- **[💡 Examples](examples/)** - Code samples
- **[🏗️ Build System](BUILD_README.md)** - Create executables

### Search by Topic
- **GUI Development**: [Developer Guide](DEVELOPER_README.md#gui-development)
- **PDF Generation**: [API Reference](API_README.md#invoice-generator)
- **Configuration**: [Developer Guide](DEVELOPER_README.md#configuration-management)
- **Testing**: [Developer Guide](DEVELOPER_README.md#testing)
- **Error Handling**: [API Reference](API_README.md#error-handling)

---

**Happy Learning! 🚀**

*This documentation should help you get the most out of InvoiceArtisan. If you need clarification on any section, please open an issue or discussion on GitHub.* 