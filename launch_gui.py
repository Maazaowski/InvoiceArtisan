#!/usr/bin/env python3

"""
InvoiceArtisan GUI Launcher
Simple launcher script for the InvoiceArtisan GUI application
"""

import sys
import os

def main():
    try:
        # Import and run the GUI
        from invoice_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
