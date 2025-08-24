#!/usr/bin/env python3

import yaml
import sys
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Flowable
from dateutil import parser
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

# Define custom colors for a more elegant look
DARK_BLUE = colors.HexColor('#2c3e50')  # Dark blue for headers
LIGHT_BLUE = colors.HexColor('#f5f9fc')  # Light blue background
HIGHLIGHT_COLOR = colors.HexColor('#3498db')  # Accent color
LIGHT_GRAY = colors.HexColor('#f8f9fa')  # Light gray for alternating rows
MEDIUM_GRAY = colors.HexColor('#e9ecef')  # Medium gray for borders

# Custom horizontal line separator
class HRFlowable(Flowable):
    def __init__(self, width, thickness=1, color=MEDIUM_GRAY, space_before=0, space_after=0):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
        self.space_before = space_before
        self.space_after = space_after
        
    def wrap(self, *args):
        return (self.width, self.thickness + self.space_before + self.space_after)
        
    def draw(self):
        self.canv.setLineWidth(self.thickness)
        self.canv.setStrokeColor(self.color)
        y = self.space_before + self.thickness / 2
        self.canv.line(0, y, self.width, y)

def load_invoice_data(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def calculate_totals(items):
    subtotal = sum(item['quantity'] * item['rate'] for item in items)
    return subtotal

def format_currency(amount):
    return f"${amount:,.2f}"

def generate_invoice(data, output_pdf):
    """Generate a PDF invoice from the provided data."""
    try:
        # Create document with slightly larger margins for a more balanced look
        doc = SimpleDocTemplate(
            output_pdf,
            pagesize=letter,
            rightMargin=0.6*inch,
            leftMargin=0.6*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
        )
        
        styles = getSampleStyleSheet()
        elements = []
        
        # Enhanced styling for the entire document
        doc_style = ParagraphStyle(
            'DocStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            spaceBefore=4,
            spaceAfter=4
        )
        
        # Create a table for the header with logo and invoice title
        logo = Image('logo/MaazLogo.png', width=2*inch, height=1.4*inch)
        
        # Enhanced invoice title style
        invoice_title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=28,
            textColor=DARK_BLUE,
            alignment=TA_RIGHT
        )
        
        invoice_number_style = ParagraphStyle(
            'InvoiceNumber',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=DARK_BLUE,
            alignment=TA_RIGHT
        )
        
        # Use a 3-column layout with middle column as spacer
        # Combine invoice title and number in the same cell with no spacing
        header_table = Table([
            [logo, "", Paragraph(f"""<font color="#2c3e50">INVOICE</font><br/><font size="10" color="#3498db"># {data['invoice']['number']}</font>""", invoice_title_style)]
        ], colWidths=[2*inch, 4*inch, 2*inch])
        
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # Reduce spacing after header
        elements.append(header_table)
        elements.append(Spacer(1, 15))
        
        # Add subtle separator
        elements.append(HRFlowable(width=7.8*inch, thickness=1, color=MEDIUM_GRAY, space_before=0, space_after=10))
        
        # Enhanced company info style
        company_style = ParagraphStyle(
            'CompanyStyle',
            parent=doc_style,
            fontSize=10,
            leading=16,
            leftIndent=0,  # Ensure no left indent to align with bill_to
            firstLineIndent=0  # Ensure first line is also aligned properly
        )
        
        # Company Info with enhanced styling but ensure it's left-aligned
        company_info = f"""
        <font size="12" color="#2c3e50"><b>{data['company']['name']}</b></font><br/>
        {data['company'].get('address1', '')}<br/>
        {data['company'].get('address2', '')}<br/>
        {data['company']['city']}, {data['company']['state']} {data['company']['zip']}<br/>
        {data['company']['country']}<br/>
        {data['company']['phone']}<br/>
        {data['company']['email']}
        """
        elements.append(Paragraph(company_info, company_style))
        elements.append(Spacer(1, 15))
        
        # Enhanced Bill To and Invoice Details styles
        bill_to_title_style = ParagraphStyle(
            'BillToTitle',
            parent=doc_style,
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=DARK_BLUE
        )
        
        bill_to_info_style = ParagraphStyle(
            'BillToInfo',
            parent=doc_style,
            fontSize=10,
            leading=16
        )
        
        right_style = ParagraphStyle(
            'RightAligned',
            parent=doc_style,
            alignment=TA_RIGHT,
            fontSize=10,
            leading=16
        )
        
        # Format dates in a more readable format
        def format_date(date_str):
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%B %d, %Y')  # Example: March 28, 2025
            except:
                return date_str  # Return original if parsing fails
        
        # Create BILL TO and Invoice Details side by side in a table
        bill_to_title = Paragraph("<font color='#2c3e50'><b>BILL TO:</b></font>", bill_to_title_style)
        bill_to_info = Paragraph(f"""
        {data['client']['name']}<br/>
        {data['client']['address']}<br/>
        {data['client']['city']}, {data['client']['state']} {data['client']['zip']}<br/>
        {data['client']['country']}
        """, bill_to_info_style)
        
        invoice_details = Paragraph(f"""
        <font color='#3498db'><b>Month:</b></font> {data['invoice'].get('month', '')}<br/>
        <font color='#3498db'><b>Date:</b></font> {format_date(data['invoice']['date'])}<br/>
        <font color='#3498db'><b>Due Date:</b></font> {format_date(data['invoice']['due_date'])}
        """, right_style)
        
        # Create a table with two rows - title row and content row
        client_invoice_table = Table([
            [bill_to_title, ""],
            [bill_to_info, invoice_details]
        ], colWidths=[5*inch, 2.5*inch])
        
        # Reduce padding in all table cells
        client_invoice_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 1), (-1, 1), 3),
        ]))
        
        elements.append(client_invoice_table)
        elements.append(Spacer(1, 15))
        
        # Items Table Header Style
        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=doc_style,
            fontSize=10,
            fontName='Helvetica-Bold',
            textColor=colors.white
        )
        
        # Item cell style
        item_style = ParagraphStyle(
            'ItemStyle',
            parent=doc_style,
            fontSize=10
        )
        
        # Items Table with improved styling
        table_data = [
            [
                Paragraph("<font color='white'>No.</font>", table_header_style),
                Paragraph("<font color='white'>Item & Description</font>", table_header_style),
                Paragraph("<font color='white'>Quantity</font>", table_header_style),
                Paragraph("<font color='white'>Rate</font>", table_header_style),
                Paragraph("<font color='white'>Amount</font>", table_header_style)
            ]
        ]
        
        # Add items with alternating row colors
        for idx, item in enumerate(data['items'], 1):
            # Handle item name and description separation
            item_text = item.get('name', '')
            description_text = item.get('description', '')
            
            # If only description exists, use it as the item
            if not item_text and description_text:
                item_text = description_text
                description_text = ""
                
            # Format the combined item and description cell
            if description_text:
                item_cell = f"<b>{item_text}</b><br/><font color='#7f8c8d' size='9'>{description_text}</font>"
            else:
                item_cell = f"<b>{item_text}</b>"
                
            amount = item['quantity'] * item['rate']
            table_data.append([
                str(idx),
                Paragraph(item_cell, item_style),
                str(item['quantity']),
                format_currency(item['rate']),
                format_currency(amount)
            ])
        
        # Calculate totals
        subtotal = calculate_totals(data['items'])
        tax = subtotal * data['tax_rate']
        total = subtotal + tax
        
        # Add a blank row before totals for better spacing
        table_data.append(['', '', '', '', ''])
        
        # Create right-aligned style for totals
        total_label_style = ParagraphStyle(
            'TotalLabelStyle',
            parent=doc_style,
            alignment=TA_RIGHT,
            fontSize=10
        )
        
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=doc_style,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=DARK_BLUE
        )
        
        grand_total_style = ParagraphStyle(
            'GrandTotalStyle',
            parent=doc_style,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=DARK_BLUE
        )
        
        # Add totals to table with improved styling
        table_data.extend([
            ['', '', '', Paragraph("Subtotal:", total_label_style), format_currency(subtotal)],
            ['', '', '', Paragraph(f"Tax ({data['tax_rate']*100}%):", total_label_style), format_currency(tax)],
            ['', '', '', Paragraph("<font color='#2c3e50'><b>Total:</b></font>", total_style), Paragraph(f"<font color='#2c3e50'><b>{format_currency(total)}</b></font>", grand_total_style)]
        ])
        
        # More balanced column widths
        table = Table(table_data, colWidths=[0.5*inch, 4*inch, 0.75*inch, 1.25*inch, 1*inch])
        
        # Improved table styling with alternating row colors and better borders
        row_styles = []
        for i in range(len(table_data)):
            if i == 0:  # Header row
                row_styles.append(('BACKGROUND', (0, i), (-1, i), DARK_BLUE))
                row_styles.append(('TEXTCOLOR', (0, i), (-1, i), colors.white))
            elif i % 2 == 1 and i < len(table_data) - 4:  # Alternating rows, excluding total rows
                row_styles.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))
        
        # Make table rows more compact
        table.setStyle(TableStyle([
            # Alignment
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Center the No. column
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Center quantity column
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),   # Right align rate column
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),   # Right align amount column
            
            # Header row styling - reduced padding
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Item rows styling - reduced padding
            ('TOPPADDING', (0, 1), (-1, -5), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -5), 6),
            
            # Grid styling - lighter grid for better appearance
            ('GRID', (0, 0), (-1, -5), 0.5, MEDIUM_GRAY),
            
            # Totals section styling - reduced padding
            ('TOPPADDING', (0, -3), (-1, -1), 6),
            ('BOTTOMPADDING', (0, -3), (-1, -1), 6),
            ('LINEABOVE', (3, -3), (-1, -3), 1, DARK_BLUE),
            ('LINEBELOW', (3, -1), (-1, -1), 1.5, DARK_BLUE),
        ] + row_styles))
        
        elements.append(table)
        
        # Notes with improved styling but less spacing - only show if it contains more than a thank you message
        if data.get('notes') and not any(thank_phrase in data['notes'].lower() for thank_phrase in ['thank', 'thanks', 'thank you', 'business']):
            elements.append(Spacer(1, 15))
            
            notes_title_style = ParagraphStyle(
                'NotesTitle',
                parent=doc_style,
                fontSize=10,
                fontName='Helvetica-Bold',
                textColor=DARK_BLUE,
                spaceAfter=5
            )
            
            notes_style = ParagraphStyle(
                'Notes',
                parent=doc_style,
                fontSize=9,
                leftIndent=10,
                rightIndent=10,
                leading=11
            )
            
            elements.append(Paragraph("<font color='#2c3e50'><b>Notes:</b></font>", notes_title_style))
            elements.append(Paragraph(data['notes'], notes_style))
        
        # Terms and Conditions with improved styling but more compact
        if data.get('terms'):
            elements.append(Spacer(1, 15))
            
            terms_title_style = ParagraphStyle(
                'TermsTitle',
                parent=doc_style,
                fontSize=10,
                fontName='Helvetica-Bold',
                textColor=DARK_BLUE
            )
            
            terms_style = ParagraphStyle(
                'Terms',
                parent=doc_style,
                fontSize=9,
                leftIndent=10,
                rightIndent=10,
                leading=11
            )
            
            # More compact spacing between terms sections
            elements.append(Paragraph("<font color='#2c3e50'><b>Terms & Conditions:</b></font>", terms_title_style))
            
            # Split terms into payment details and other terms
            terms_parts = data['terms'].split("Payment Details:", 1)
            if len(terms_parts) > 1:
                # Add payment details section with less spacing
                elements.append(Spacer(1, 2))
                elements.append(Paragraph("<font color='#3498db'><b>Payment Details:</b></font>", terms_style))
                
                # Process each line of payment details
                payment_lines = terms_parts[1].strip().split('\n')
                for line in payment_lines:
                    if line.strip():  # Only add non-empty lines
                        parts = line.strip().split(':', 1)
                        if len(parts) > 1:
                            elements.append(Paragraph(f"<b>{parts[0]}:</b> {parts[1]}", terms_style))
                        else:
                            elements.append(Paragraph(line.strip(), terms_style))
                
                elements.append(Spacer(1, 3))  # Reduced space after payment details
            
            # Add any other terms if they exist
            if terms_parts[0].strip():
                elements.append(Spacer(1, 2))
                elements.append(Paragraph(terms_parts[0].strip(), terms_style))
        
        # Add a footer with less space before
        elements.append(Spacer(1, 15))
        elements.append(HRFlowable(width=7.8*inch, thickness=1, color=MEDIUM_GRAY, space_before=2, space_after=5))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=doc_style,
            alignment=TA_CENTER,
            fontSize=9,
            textColor=colors.gray
        )
        
        elements.append(Paragraph("Thank you for your business!", footer_style))
        
        doc.build(elements)
        print(f"Successfully generated invoice: {output_pdf}")
        
    except Exception as e:
        print(f"Error generating invoice: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python invoice_generator.py <invoice_yaml_file>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    output_pdf = yaml_file.rsplit('.', 1)[0] + '.pdf'
    
    try:
        data = load_invoice_data(yaml_file)
        generate_invoice(data, output_pdf)
    except Exception as e:
        print(f"Error generating invoice: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 