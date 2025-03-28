#!/usr/bin/env python3

import sys
from PyPDF2 import PdfReader

def read_pdf(pdf_file):
    """
    Read and display the contents of a PDF file.
    
    Args:
        pdf_file (str): Path to the PDF file
    """
    try:
        # Create a PDF reader object
        reader = PdfReader(pdf_file)
        
        # Get the number of pages
        num_pages = len(reader.pages)
        print(f"\nPDF File: {pdf_file}")
        print(f"Number of pages: {num_pages}\n")
        
        # Read each page
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            print(f"=== Page {page_num + 1} ===")
            print(page.extract_text())
            print("\n")
            
    except Exception as e:
        print(f"Error reading PDF file: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf_reader.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    read_pdf(pdf_file)

if __name__ == "__main__":
    main() 