# InvoiceArtisan Examples

## 🎯 Overview

This directory contains practical examples and code samples for using InvoiceArtisan in various scenarios. Each example demonstrates different aspects of the system and provides working code that you can adapt for your needs.

## 📁 Example Categories

### 1. **Basic Usage Examples**
- Simple invoice generation
- Basic configuration
- File operations

### 2. **Advanced Features**
- Custom templates
- Batch processing
- Integration examples

### 3. **GUI Customization**
- Custom themes
- Additional tabs
- Enhanced functionality

### 4. **API Integration**
- Web applications
- Desktop applications
- Scripts and automation

## 🚀 Getting Started

### Prerequisites

1. **Install InvoiceArtisan**: Follow the [installation guide](../README.md)
2. **Python Knowledge**: Basic understanding of Python
3. **Dependencies**: Required packages installed

### Running Examples

```bash
# Navigate to examples directory
cd docs/examples

# Run a specific example
python basic_invoice_generation.py

# Run all examples
python run_all_examples.py
```

## 📋 Example List

### Basic Examples

- **[basic_invoice_generation.py](basic_invoice_generation.py)** - Generate a simple invoice
- **[load_and_save_invoice.py](load_and_save_invoice.py)** - Load and save invoice data
- **[custom_template.py](custom_template.py)** - Use custom invoice templates
- **[batch_processing.py](batch_processing.py)** - Process multiple invoices

### GUI Examples

- **[custom_theme.py](custom_theme.py)** - Apply custom GUI themes
- **[add_custom_tab.py](add_custom_tab.py)** - Add new tabs to the GUI
- **[enhanced_validation.py](enhanced_validation.py)** - Custom input validation

### Integration Examples

- **[web_api.py](web_api.py)** - Web API integration
- **[desktop_app.py](desktop_app.py)** - Desktop application integration
- **[automation_script.py](automation_script.py)** - Automated invoice generation

### Advanced Examples

- **[custom_pdf_styling.py](custom_pdf_styling.py)** - Custom PDF styling
- **[multi_language.py](multi_language.py)** - Multi-language support
- **[database_integration.py](database_integration.py)** - Database integration

## 🔧 Customizing Examples

### Configuration

Most examples use the default configuration. To customize:

1. **Copy configuration files**:
   ```bash
   cp config/app_config.yaml config/my_config.yaml
   ```

2. **Modify settings** in your config file

3. **Update example code** to use your config:
   ```python
   config = load_config('config/my_config.yaml')
   ```

### Templates

To use custom templates:

1. **Create template file**:
   ```yaml
   # my_template.yaml
   invoice:
     number: "CUSTOM-001"
     # ... other fields
   ```

2. **Reference in examples**:
   ```python
   pdf_path = generate_invoice(data, template='my_template.yaml')
   ```

## 📚 Learning Path

### Beginner
1. Start with `basic_invoice_generation.py`
2. Try `load_and_save_invoice.py`
3. Experiment with `custom_template.py`

### Intermediate
1. Explore `batch_processing.py`
2. Customize with `custom_theme.py`
3. Learn from `enhanced_validation.py`

### Advanced
1. Study `web_api.py` for integration
2. Examine `custom_pdf_styling.py`
3. Explore `database_integration.py`

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure InvoiceArtisan is properly installed
2. **File Not Found**: Check file paths and working directory
3. **Permission Errors**: Verify file permissions and access rights

### Getting Help

- Check the [main documentation](../README.md)
- Review [API reference](../API_README.md)
- Open an issue on GitHub

## 🤝 Contributing Examples

### Adding New Examples

1. **Create example file** with descriptive name
2. **Add documentation** explaining purpose and usage
3. **Include comments** explaining key concepts
4. **Test thoroughly** before submitting

### Example Template

```python
#!/usr/bin/env python3
"""
Example Name: Brief description

This example demonstrates:
- Key feature 1
- Key feature 2
- Key feature 3

Usage:
    python example_name.py

Requirements:
    - Requirement 1
    - Requirement 2
"""

# Import statements
from src.core.invoice_generator import generate_invoice

def main():
    """Main example function"""
    # Example code here
    pass

if __name__ == "__main__":
    main()
```

## 📊 Example Statistics

- **Total Examples**: 15+
- **Categories**: 4 main categories
- **Complexity Levels**: Beginner to Advanced
- **Coverage**: Core functionality to advanced features

---

## 🎯 Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/InvoiceArtisan.git
cd InvoiceArtisan
python scripts/setup.py

# Run first example
python docs/examples/basic_invoice_generation.py
```

---

**Happy Learning! 🚀**

*These examples should help you understand and extend InvoiceArtisan for your specific needs.*
