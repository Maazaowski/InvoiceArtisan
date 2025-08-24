#!/usr/bin/env python3

"""
InvoiceArtisan GUI Launcher
Launches the main GUI application
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Launch the InvoiceArtisan GUI application"""
    try:
        from gui.main_window import InvoiceArtisanGUI
        import tkinter as tk
        
        # Create and run the GUI
        root = tk.Tk()
        app = InvoiceArtisanGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"Error: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install -r build/requirements/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
