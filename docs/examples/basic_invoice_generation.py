#!/usr/bin/env python3
"""
Basic Invoice Generation Example

This example demonstrates:
- Creating invoice data programmatically
- Generating a PDF invoice
- Basic error handling
- Output file management

Usage:
    python basic_invoice_generation.py

Requirements:
    - InvoiceArtisan installed and configured
    - Output directory writable
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def create_sample_invoice_data():
    """Create sample invoice data for demonstration"""
    return {
        'invoice': {
            'number': 'INV-2025-001',
            'date': '2025-01-15',
            'due_date': '2025-02-15',
            'month': 'January'
        },
        'company': {
            'name': 'Acme Corporation',
            'address1': '123 Business Street',
            'address2': 'Suite 100',
            'city': 'Business City',
            'state': 'BC',
            'zip': '12345',
            'country': 'United States',
            'email': 'billing@acme.com',
            'phone': '+1-555-0123'
        },
        'client': {
            'name': 'Client Industries',
            'address': '456 Client Avenue',
            'city': 'Client City',
            'state': 'CC',
            'zip': '67890',
            'country': 'United States',
            'email': 'accounts@client.com'
        },
        'items': [
            {
                'name': 'Web Development Services',
                'description': 'Custom website development and design',
                'quantity': 40.0,
                'unit': 'hours',
                'rate': 75.0
            },
            {
                'name': 'SEO Optimization',
                'description': 'Search engine optimization services',
                'quantity': 10.0,
                'unit': 'hours',
                'rate': 50.0
            },
            {
                'name': 'Domain Registration',
                'description': 'Annual domain registration and hosting',
                'quantity': 1.0,
                'unit': 'year',
                'rate': 120.0
            }
        ],
        'tax_rate': 8.5,
        'notes': 'Thank you for your business! Please pay within 30 days.',
        'terms': 'Payment is due within 30 days of invoice date. Late payments may incur additional charges.'
    }

def calculate_totals(invoice_data):
    """Calculate invoice totals including tax"""
    subtotal = sum(item['quantity'] * item['rate'] for item in invoice_data['items'])
    tax_amount = subtotal * (invoice_data['tax_rate'] / 100)
    total = subtotal + tax_amount
    
    return {
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total': total
    }

def main():
    """Main example function"""
    print("🚀 InvoiceArtisan - Basic Invoice Generation Example")
    print("=" * 50)
    
    try:
        # Import required modules
        from core.invoice_generator import generate_invoice
        from utils.file_utils import ensure_directory
        
        # Create sample invoice data
        print("📝 Creating sample invoice data...")
        invoice_data = create_sample_invoice_data()
        
        # Calculate totals
        totals = calculate_totals(invoice_data)
        print(f"💰 Invoice totals calculated:")
        print(f"   Subtotal: ${totals['subtotal']:.2f}")
        print(f"   Tax ({invoice_data['tax_rate']}%): ${totals['tax_amount']:.2f}")
        print(f"   Total: ${totals['total']:.2f}")
        
        # Ensure output directory exists
        output_dir = Path("output/invoices")
        ensure_directory(output_dir)
        
        # Generate PDF invoice
        print("\n🔨 Generating PDF invoice...")
        output_path = output_dir / f"{invoice_data['invoice']['number']}.pdf"
        
        pdf_path = generate_invoice(invoice_data, str(output_path))
        
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            print(f"✅ Invoice generated successfully!")
            print(f"📁 File: {pdf_path}")
            print(f"📏 Size: {file_size:.1f} KB")
            
            # Show invoice details
            print(f"\n📋 Invoice Details:")
            print(f"   Number: {invoice_data['invoice']['number']}")
            print(f"   Date: {invoice_data['invoice']['date']}")
            print(f"   Due Date: {invoice_data['invoice']['due_date']}")
            print(f"   Client: {invoice_data['client']['name']}")
            print(f"   Items: {len(invoice_data['items'])}")
            
        else:
            print("❌ Failed to generate invoice")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure InvoiceArtisan is properly installed:")
        print("python scripts/setup.py")
        return False
        
    except Exception as e:
        print(f"❌ Error generating invoice: {e}")
        return False
    
    print("\n🎉 Example completed successfully!")
    print("\n📚 Next steps:")
    print("1. Open the generated PDF to see the result")
    print("2. Try modifying the invoice data")
    print("3. Explore other examples in this directory")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
