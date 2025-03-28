# Invoice Generator

A simple Python-based invoice generator that creates PDF invoices from YAML files.

## Requirements
- Python 3.8+
- Dependencies listed in requirements.txt

## Installation
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generating Invoices
1. Create a YAML file with your invoice details (see `invoice_template.yaml` for an example)
2. Run the generator:
```bash
python invoice_generator.py your_invoice.yaml
```

### Reading PDF Invoices
To read a generated PDF invoice or any PDF file:
```bash
python pdf_reader.py your_invoice.pdf
```

### Converting PDF Invoices to YAML Templates
To convert an existing PDF invoice into a YAML template:
```bash
python pdf_to_yaml.py existing_invoice.pdf
```
This will create a new YAML file with the same name as your PDF (e.g., `existing_invoice_template.yaml`). You can then use this YAML file as a template for generating new invoices with the same layout and structure.

## Features
- Generate professional PDF invoices from YAML files
- Customizable invoice template
- Support for multiple line items
- Automatic calculation of subtotals and totals
- Tax calculation support
- PDF reading capability for reviewing generated invoices
- Convert existing PDF invoices to YAML templates 