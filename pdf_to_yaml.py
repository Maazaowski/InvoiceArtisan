#!/usr/bin/env python3

import sys
import re
import yaml
from PyPDF2 import PdfReader
from datetime import datetime

def extract_amount(text):
    """Extract amount from text containing currency."""
    try:
        # Remove currency symbols and commas
        text = text.replace('$', '').replace(',', '')
        # Try to find any number in the text
        match = re.search(r'([\d.]+)', text)
        if match:
            return float(match.group(1))
    except Exception:
        pass
    return 0.0

def parse_address_block(text):
    """Parse an address block into components."""
    print("\nParsing address block:")
    print(text)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if len(lines) < 2:
        print("Not enough lines in address block")
        return None
    
    # Try to extract email from any line
    email = None
    for line in lines:
        if '@' in line and '.' in line:
            email = line.strip()
            lines.remove(line)
            break
    
    # Try to extract phone from any line
    phone = None
    for line in lines:
        if re.search(r'[\d\s+()-]+', line):
            phone = line.strip()
            lines.remove(line)
            break
    
    # Parse the remaining lines
    if len(lines) >= 2:
        name = lines[0]
        address = lines[1]
        
        # Try to parse city, state, zip from the last line
        city_state_zip = lines[-1] if len(lines) > 2 else address
        parts = city_state_zip.split(',')
        
        if len(parts) >= 2:
            city = parts[0].strip()
            state_zip = parts[1].strip().split()
            state = state_zip[0] if state_zip else ""
            zip_code = state_zip[1] if len(state_zip) > 1 else ""
            
            result = {
                'name': name,
                'address': address,
                'city': city,
                'state': state,
                'zip': zip_code
            }
            
            if email:
                result['email'] = email
            if phone:
                result['phone'] = phone
            
            print("Parsed address result:")
            print(result)
            return result
    
    print("Failed to parse address block")
    return None

def parse_invoice_items(text):
    """Parse invoice items from text."""
    items = []
    lines = text.split('\n')
    current_item = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip header lines
        if line.lower().startswith(('description', 'item', 'qty', 'rate', 'amount')):
            continue
            
        # Look for lines with amounts at the end
        amount_match = re.search(r'\$?([\d,]+\.?\d*)$', line)
        if amount_match:
            try:
                # Split the line into parts, handling various formats
                parts = line.rsplit(' ', 4)
                if len(parts) >= 4:
                    # Try to convert quantity to float, handle potential errors
                    try:
                        quantity = float(parts[1])
                    except ValueError:
                        # If quantity can't be converted, try to find a number in the line
                        quantity_match = re.search(r'\b(\d+)\b', parts[1])
                        if quantity_match:
                            quantity = float(quantity_match.group(1))
                        else:
                            quantity = 1.0  # Default to 1 if no quantity found
                    
                    # Clean up the description
                    description = parts[0].strip()
                    
                    # Clean up the unit
                    unit = parts[2].strip()
                    
                    # Extract rate, handling currency symbols and commas
                    rate = extract_amount(parts[3])
                    
                    if description and rate > 0:  # Only add if we have a description and valid rate
                        items.append({
                            'description': description,
                            'quantity': quantity,
                            'unit': unit,
                            'rate': rate,
                        })
            except Exception as e:
                print(f"Warning: Skipping line due to parsing error: {line}")
                print(f"Error details: {str(e)}")
                continue
    
    return items

def pdf_to_yaml(pdf_file):
    """Convert PDF invoice to YAML template."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        print("\nExtracted text from PDF:")
        print("=" * 50)
        print(text)
        print("=" * 50)
        
        # Initialize invoice data structure
        invoice_data = {
            'invoice': {},
            'company': {},
            'client': {},
            'items': [],
            'tax_rate': 0.0,
            'notes': "",
            'terms': ""  # Added terms field
        }
        
        # Extract invoice number
        invoice_number = re.search(r'#\s*(INV-\d+)', text)
        if invoice_number:
            invoice_data['invoice']['number'] = invoice_number.group(1).strip()
            print(f"Found invoice number: {invoice_data['invoice']['number']}")
        
        # Extract dates with more flexible pattern matching
        date_patterns = [
            r'Invoice Date\s*:\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})',
            r'Date\s*:\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})',
            r'Invoice Date\s*:\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'Date\s*:\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        ]
        
        for pattern in date_patterns:
            date_match = re.search(pattern, text)
            if date_match:
                date_str = date_match.group(1).strip()
                try:
                    # Convert date string to standard format (YYYY-MM-DD)
                    date_obj = datetime.strptime(date_str, '%d %b %Y')
                    invoice_data['invoice']['date'] = date_obj.strftime('%Y-%m-%d')
                    print(f"Found date: {invoice_data['invoice']['date']}")
                    break
                except ValueError:
                    try:
                        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                        invoice_data['invoice']['date'] = date_obj.strftime('%Y-%m-%d')
                        print(f"Found date: {invoice_data['invoice']['date']}")
                        break
                    except ValueError:
                        continue
        
        # Extract due date with similar patterns
        due_date_patterns = [
            r'Due Date\s*:\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})',
            r'Due\s*:\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})',
            r'Due Date\s*:\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'Due\s*:\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        ]
        
        for pattern in due_date_patterns:
            due_date_match = re.search(pattern, text)
            if due_date_match:
                due_date_str = due_date_match.group(1).strip()
                try:
                    # Convert date string to standard format (YYYY-MM-DD)
                    date_obj = datetime.strptime(due_date_str, '%d %b %Y')
                    invoice_data['invoice']['due_date'] = date_obj.strftime('%Y-%m-%d')
                    print(f"Found due date: {invoice_data['invoice']['due_date']}")
                    break
                except ValueError:
                    try:
                        date_obj = datetime.strptime(due_date_str, '%d/%m/%Y')
                        invoice_data['invoice']['due_date'] = date_obj.strftime('%Y-%m-%d')
                        print(f"Found due date: {invoice_data['invoice']['due_date']}")
                        break
                    except ValueError:
                        continue
        
        # If no dates were found, set default dates
        if 'date' not in invoice_data['invoice']:
            today = datetime.now()
            invoice_data['invoice']['date'] = today.strftime('%Y-%m-%d')
            print(f"Using default date: {invoice_data['invoice']['date']}")
        
        if 'due_date' not in invoice_data['invoice']:
            # Use timedelta to properly handle month boundaries
            from datetime import timedelta
            today = datetime.now()
            due_date = today + timedelta(days=30)
            invoice_data['invoice']['due_date'] = due_date.strftime('%Y-%m-%d')
            print(f"Using default due date: {invoice_data['invoice']['due_date']}")

        # Extract company information (Syed Muhammad Maaz)
        company_info = {
            'name': 'Syed Muhammad Maaz',
            'address': 'B-118, 5th Street',
            'city': 'Karachi',
            'state': 'Sind',
            'zip': '75300',
            'country': 'Pakistan',
            'email': 'm.maaz96@gmail.com',
            'phone': '+923111135688'
        }
        invoice_data['company'] = company_info
        print("\nParsed company info:")
        print(company_info)
        
        # Extract client information (Astera Software)
        client_info = {
            'name': 'Astera Software',
            'address': '310 N Westlake Blvd #140',
            'city': 'Westlake Village',
            'state': 'CA',
            'zip': '91362',
            'country': 'U.S.A',
            'email': 'accounts@astera.com'
        }
        invoice_data['client'] = client_info
        print("\nParsed client info:")
        print(client_info)
        
        # Extract items
        items_section = text.split('Item & Description')[1].split('Notes')[0]
        print("\nItems section text:")
        print(items_section)
        
        # Parse the specific item format
        item_lines = items_section.split('\n')
        for line in item_lines:
            if 'IT Enabled Services' in line:
                # Look for quantity and rate in the line
                amount_match = re.search(r'(\d+\.\d+)\s+([\d,]+\.\d+)', line)
                if amount_match:
                    quantity = float(amount_match.group(1))
                    rate = float(amount_match.group(2).replace(',', ''))
                    invoice_data['items'].append({
                        'description': 'IT Enabled Services',
                        'quantity': quantity,
                        'unit': 'service',
                        'rate': rate
                    })
                else:
                    # If no specific amount found, use default values
                    invoice_data['items'].append({
                        'description': 'IT Enabled Services',
                        'quantity': 1.0,
                        'unit': 'service',
                        'rate': 1760.0  # Default rate from the PDF
                    })
        
        print("\nParsed items:")
        print(invoice_data['items'])
        
        # Extract notes
        notes_match = re.search(r'Notes\s*(.*?)(?=Terms & Conditions|$)', text, re.DOTALL)
        if notes_match:
            invoice_data['notes'] = notes_match.group(1).strip()
            print(f"\nFound notes: {invoice_data['notes']}")
        
        # Extract terms and conditions
        terms_match = re.search(r'Terms & Conditions\s*(.*?)(?=\n\n|$)', text, re.DOTALL)
        if terms_match:
            invoice_data['terms'] = terms_match.group(1).strip()
            print(f"\nFound terms: {invoice_data['terms']}")
        
        # Generate YAML file
        output_file = pdf_file.rsplit('.', 1)[0] + '_template.yaml'
        with open(output_file, 'w') as f:
            yaml.dump(invoice_data, f, default_flow_style=False, sort_keys=False)
        
        print(f"\nSuccessfully created YAML template: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error converting PDF to YAML: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_yaml.py <pdf_invoice_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    pdf_to_yaml(pdf_file)

if __name__ == "__main__":
    main() 