# InvoiceArtisan API Reference

## 🎯 Overview

This document provides comprehensive API documentation for the InvoiceArtisan project. It covers all public functions, classes, and modules that developers can use to extend and integrate with the system.

## 📚 Core Module API

### Invoice Generator

#### `generate_invoice(invoice_data, output_path=None, template='default')`

Generates a PDF invoice from invoice data.

**Parameters:**
- `invoice_data` (dict|str): Invoice data dictionary or path to YAML file
- `output_path` (str, optional): Output PDF file path. If None, generates in `output/invoices/`
- `template` (str): Template name to use for generation

**Returns:**
- `str`: Path to generated PDF file

**Raises:**
- `ValueError`: If invoice data is invalid
- `FileNotFoundError`: If template file not found
- `PermissionError`: If output directory is not writable

**Example:**
```python
from src.core.invoice_generator import generate_invoice

# Generate from dictionary
data = {
    'invoice': {'number': 'INV-001', 'date': '2025-01-01'},
    'company': {'name': 'My Company'},
    'client': {'name': 'Client Name'},
    'items': [{'name': 'Service', 'quantity': 1, 'rate': 100}]
}

pdf_path = generate_invoice(data, 'my_invoice.pdf')
print(f"Invoice generated: {pdf_path}")

# Generate from YAML file
pdf_path = generate_invoice('invoice_data.yaml')
```

#### `InvoiceGenerator` Class

Main class for invoice generation with advanced options.

**Constructor:**
```python
InvoiceGenerator(template_path=None, config_path=None)
```

**Methods:**

- `generate(data, output_path=None)`: Generate invoice from data
- `set_template(template_path)`: Set custom template
- `set_config(config_path)`: Set custom configuration
- `validate_data(data)`: Validate invoice data structure
- `get_available_templates()`: List available templates

**Example:**
```python
from src.core.invoice_generator import InvoiceGenerator

generator = InvoiceGenerator()
generator.set_template('custom_template.yaml')
generator.set_config('custom_config.yaml')

# Validate data first
if generator.validate_data(invoice_data):
    pdf_path = generator.generate(invoice_data, 'output.pdf')
else:
    print("Invalid invoice data")
```

### PDF Reader

#### `read_pdf(file_path)`

Extracts text content from a PDF file.

**Parameters:**
- `file_path` (str): Path to PDF file

**Returns:**
- `str`: Extracted text content

**Raises:**
- `FileNotFoundError`: If PDF file not found
- `PermissionError`: If file not readable

**Example:**
```python
from src.core.pdf_reader import read_pdf

try:
    content = read_pdf('invoice.pdf')
    print("PDF Content:")
    print(content)
except FileNotFoundError:
    print("PDF file not found")
```

#### `PDFReader` Class

Advanced PDF reading with metadata extraction.

**Methods:**

- `read_text()`: Extract text content
- `get_metadata()`: Get PDF metadata (author, creation date, etc.)
- `get_page_count()`: Get total page count
- `read_page(page_number)`: Read specific page
- `search_text(query)`: Search for specific text

**Example:**
```python
from src.core.pdf_reader import PDFReader

reader = PDFReader('invoice.pdf')
print(f"Pages: {reader.get_page_count()}")
print(f"Metadata: {reader.get_metadata()}")
print(f"Content: {reader.read_text()}")
```

### PDF to YAML Converter

#### `pdf_to_yaml(pdf_path, output_path=None)`

Converts PDF invoice to YAML template.

**Parameters:**
- `pdf_path` (str): Path to PDF file
- `output_path` (str, optional): Output YAML file path

**Returns:**
- `str`: Path to generated YAML file

**Raises:**
- `FileNotFoundError`: If PDF file not found
- `ValueError`: If PDF cannot be parsed

**Example:**
```python
from src.core.pdf_to_yaml import pdf_to_yaml

yaml_path = pdf_to_yaml('invoice.pdf', 'template.yaml')
print(f"Template created: {yaml_path}")
```

#### `PDFToYAMLConverter` Class

Advanced conversion with customization options.

**Methods:**

- `convert()`: Perform conversion
- `set_output_format(format)`: Set output format (yaml, json, xml)
- `set_parsing_options(options)`: Configure parsing behavior
- `get_conversion_stats()`: Get conversion statistics

## 🎨 GUI Module API

### Main Window

#### `InvoiceArtisanGUI` Class

Main application window class.

**Constructor:**
```python
InvoiceArtisanGUI(root, config_path=None)
```

**Parameters:**
- `root`: Tkinter root window
- `config_path` (str, optional): Path to configuration file

**Methods:**

- `load_invoice(file_path)`: Load invoice from file
- `save_invoice(file_path)`: Save invoice to file
- `generate_pdf()`: Generate PDF invoice
- `preview_invoice()`: Show invoice preview
- `reset_form()`: Reset all form fields
- `get_invoice_data()`: Get current invoice data
- `set_invoice_data(data)`: Set invoice data

**Example:**
```python
import tkinter as tk
from src.gui.main_window import InvoiceArtisanGUI

root = tk.Tk()
app = InvoiceArtisanGUI(root)

# Load existing invoice
app.load_invoice('existing_invoice.yaml')

# Generate PDF
app.generate_pdf()

root.mainloop()
```

### Tab Components

#### Base Tab Class

All tab components inherit from `BaseTab`.

**Methods:**

- `setup_ui()`: Initialize UI components
- `get_data()`: Return tab data
- `set_data(data)`: Set tab data
- `validate()`: Validate tab data
- `clear()`: Clear tab data
- `refresh()`: Refresh tab display

#### Invoice Details Tab

**Data Structure:**
```python
{
    'invoice': {
        'number': 'INV-001',
        'date': '2025-01-01',
        'due_date': '2025-02-01',
        'month': 'January'
    },
    'tax_rate': 0.0
}
```

#### Company Tab

**Data Structure:**
```python
{
    'company': {
        'name': 'Company Name',
        'address1': 'Address Line 1',
        'address2': 'Address Line 2',
        'city': 'City',
        'state': 'State',
        'zip': 'ZIP Code',
        'country': 'Country',
        'email': 'email@company.com',
        'phone': '+1234567890'
    }
}
```

#### Client Tab

**Data Structure:**
```python
{
    'client': {
        'name': 'Client Name',
        'address': 'Client Address',
        'city': 'Client City',
        'state': 'Client State',
        'zip': 'Client ZIP',
        'country': 'Client Country',
        'email': 'client@email.com'
    }
}
```

#### Items Tab

**Data Structure:**
```python
{
    'items': [
        {
            'name': 'Item Name',
            'description': 'Item Description',
            'quantity': 1.0,
            'unit': 'unit',
            'rate': 100.0
        }
    ]
}
```

#### Notes & Terms Tab

**Data Structure:**
```python
{
    'notes': 'Additional notes',
    'terms': 'Payment terms and conditions'
}
```

## 🔧 Utils Module API

### Configuration Management

#### `load_config(config_path)`

Load configuration from YAML file.

**Parameters:**
- `config_path` (str): Path to configuration file

**Returns:**
- `dict`: Configuration dictionary

**Example:**
```python
from src.utils.config import load_config

config = load_config('config/app_config.yaml')
theme_color = config['gui']['theme']['primary_color']
```

#### `save_config(config_data, config_path)`

Save configuration to YAML file.

**Parameters:**
- `config_data` (dict): Configuration data
- `config_path` (str): Output file path

**Example:**
```python
from src.utils.config import save_config

new_config = {'gui': {'theme': {'primary_color': '#ff0000'}}}
save_config(new_config, 'custom_config.yaml')
```

### File Utilities

#### `ensure_directory(path)`

Ensure directory exists, create if necessary.

**Parameters:**
- `path` (str): Directory path

**Returns:**
- `bool`: True if directory exists or was created

**Example:**
```python
from src.utils.file_utils import ensure_directory

ensure_directory('output/invoices')
```

#### `get_file_extension(file_path)`

Get file extension from path.

**Parameters:**
- `file_path` (str): File path

**Returns:**
- `str`: File extension (without dot)

**Example:**
```python
from src.utils.file_utils import get_file_extension

ext = get_file_extension('invoice.pdf')  # Returns 'pdf'
```

### Date Utilities

#### `format_date(date, format='%Y-%m-%d')`

Format date object to string.

**Parameters:**
- `date`: Date object or string
- `format` (str): Output format string

**Returns:**
- `str`: Formatted date string

**Example:**
```python
from src.utils.date_utils import format_date
from datetime import date

today = date.today()
formatted = format_date(today, '%B %d, %Y')  # January 01, 2025
```

#### `parse_date(date_string)`

Parse date string to date object.

**Parameters:**
- `date_string` (str): Date string

**Returns:**
- `date`: Date object

**Example:**
```python
from src.utils.date_utils import parse_date

date_obj = parse_date('2025-01-01')
```

## 🏗️ Build System API

### Build Scripts

#### `build_executable(spec_file=None, clean=True)`

Build executable using PyInstaller.

**Parameters:**
- `spec_file` (str, optional): Custom spec file path
- `clean` (bool): Clean build directories before building

**Returns:**
- `bool`: True if build successful

**Example:**
```python
from build.scripts.build_exe import build_executable

success = build_executable('custom.spec', clean=True)
if success:
    print("Executable built successfully!")
```

#### `clean_build_directories()`

Clean build and distribution directories.

**Returns:**
- `bool`: True if cleanup successful

**Example:**
```python
from build.scripts.clean_build import clean_build_directories

clean_build_directories()
```

## 📊 Data Structures

### Invoice Data Schema

```yaml
invoice:
  number: "INV-001"
  date: "2025-01-01"
  due_date: "2025-02-01"
  month: "January"

company:
  name: "Company Name"
  address1: "Address Line 1"
  address2: "Address Line 2"
  city: "City"
  state: "State"
  zip: "ZIP Code"
  country: "Country"
  email: "email@company.com"
  phone: "+1234567890"

client:
  name: "Client Name"
  address: "Client Address"
  city: "Client City"
  state: "Client State"
  zip: "Client ZIP"
  country: "Client Country"
  email: "client@email.com"

items:
  - name: "Item Name"
    description: "Item Description"
    quantity: 1.0
    unit: "unit"
    rate: 100.0

tax_rate: 0.0
notes: "Additional notes"
terms: "Payment terms"
```

### Configuration Schema

```yaml
app:
  name: "InvoiceArtisan"
  version: "2.0.0"
  author: "Developer Name"

gui:
  theme:
    primary_color: "#2c3e50"
    secondary_color: "#3498db"
  window:
    default_width: 1200
    default_height: 800

invoice:
  default:
    tax_rate: 0.0
    due_date_days: 30

pdf:
  output:
    default_format: "A4"
    margins:
      top: 20
      bottom: 20
```

## 🚨 Error Handling

### Common Exceptions

#### `InvoiceArtisanError`

Base exception class for all InvoiceArtisan errors.

#### `ValidationError`

Raised when invoice data validation fails.

**Attributes:**
- `field`: Field that failed validation
- `value`: Invalid value
- `message`: Error message

#### `TemplateError`

Raised when template processing fails.

**Attributes:**
- `template_path`: Path to problematic template
- `message`: Error message

#### `PDFGenerationError`

Raised when PDF generation fails.

**Attributes:**
- `stage`: Generation stage where error occurred
- `message`: Error message

### Error Handling Example

```python
from src.core.invoice_generator import generate_invoice
from src.utils.exceptions import InvoiceArtisanError, ValidationError

try:
    pdf_path = generate_invoice(invoice_data)
    print(f"Success: {pdf_path}")
except ValidationError as e:
    print(f"Validation error in field '{e.field}': {e.message}")
except InvoiceArtisanError as e:
    print(f"Application error: {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔌 Integration Examples

### Web Application Integration

```python
from flask import Flask, request, send_file
from src.core.invoice_generator import generate_invoice

app = Flask(__name__)

@app.route('/generate-invoice', methods=['POST'])
def generate_invoice_api():
    try:
        invoice_data = request.json
        pdf_path = generate_invoice(invoice_data)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return {'error': str(e)}, 400
```

### Batch Processing

```python
import os
from src.core.invoice_generator import generate_invoice

def batch_generate_invoices(input_dir, output_dir):
    """Generate invoices for all YAML files in directory"""
    for filename in os.listdir(input_dir):
        if filename.endswith('.yaml'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{filename[:-5]}.pdf")
            
            try:
                generate_invoice(input_path, output_path)
                print(f"Generated: {output_path}")
            except Exception as e:
                print(f"Failed to generate {filename}: {e}")
```

### Custom Invoice Templates

```python
from src.core.invoice_generator import InvoiceGenerator

class CustomInvoiceGenerator(InvoiceGenerator):
    def __init__(self):
        super().__init__()
        self.template_path = 'custom_template.yaml'
    
    def generate_custom_invoice(self, data, template_variant='default'):
        """Generate invoice with custom template variant"""
        # Load template variant
        template = self.load_template_variant(template_variant)
        
        # Apply custom styling
        styled_data = self.apply_custom_styling(data, template)
        
        # Generate PDF
        return self.generate(styled_data)
```

## 📝 Best Practices

### 1. **Error Handling**
- Always wrap API calls in try-catch blocks
- Use specific exception types when possible
- Provide meaningful error messages

### 2. **Data Validation**
- Validate input data before processing
- Use the built-in validation methods
- Provide clear feedback on validation failures

### 3. **Resource Management**
- Close file handles properly
- Clean up temporary files
- Use context managers when available

### 4. **Performance**
- Cache frequently used data
- Use generators for large datasets
- Profile code for bottlenecks

### 5. **Testing**
- Write tests for all API functions
- Use mock objects for external dependencies
- Test error conditions and edge cases

---

## 🎯 Quick Reference

### Essential Imports

```python
# Core functionality
from src.core.invoice_generator import generate_invoice, InvoiceGenerator
from src.core.pdf_reader import read_pdf, PDFReader
from src.core.pdf_to_yaml import pdf_to_yaml, PDFToYAMLConverter

# GUI components
from src.gui.main_window import InvoiceArtisanGUI

# Utilities
from src.utils.config import load_config, save_config
from src.utils.file_utils import ensure_directory, get_file_extension
from src.utils.date_utils import format_date, parse_date

# Build tools
from build.scripts.build_exe import build_executable
```

### Common Patterns

```python
# Load configuration
config = load_config('config/app_config.yaml')

# Generate invoice
pdf_path = generate_invoice(invoice_data, 'output.pdf')

# Handle errors
try:
    result = some_api_call()
except SpecificError as e:
    handle_error(e)
```

---

**For more detailed examples and advanced usage, see the [examples](examples/) directory and [developer guide](DEVELOPER_README.md).**
