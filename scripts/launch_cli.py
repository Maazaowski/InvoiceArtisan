#!/usr/bin/env python3

"""
InvoiceArtisan CLI Launcher
Launches command-line operations for invoice generation
"""

import sys
import os
import argparse

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Launch InvoiceArtisan CLI operations"""
    parser = argparse.ArgumentParser(
        description="InvoiceArtisan - Professional Invoice Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_cli.py generate invoice.yaml          # Generate PDF from YAML
  python launch_cli.py read invoice.pdf               # Read PDF content
  python launch_cli.py convert invoice.pdf            # Convert PDF to YAML
        """
    )
    
    parser.add_argument(
        'action',
        choices=['generate', 'read', 'convert'],
        help='Action to perform'
    )
    
    parser.add_argument(
        'file',
        help='Input file (YAML for generate, PDF for read/convert)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (optional)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.action == 'generate':
            from core.invoice_generator import generate_invoice
            generate_invoice(args.file)
            print(f"✅ Invoice generated successfully!")
            
        elif args.action == 'read':
            from core.pdf_reader import read_pdf
            content = read_pdf(args.file)
            print("📄 PDF Content:")
            print(content)
            
        elif args.action == 'convert':
            from core.pdf_to_yaml import pdf_to_yaml
            output_file = args.output or args.file.replace('.pdf', '.yaml')
            pdf_to_yaml(args.file, output_file)
            print(f"✅ PDF converted to YAML: {output_file}")
            
    except ImportError as e:
        print(f"Error: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install -r build/requirements/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
