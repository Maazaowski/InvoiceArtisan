#!/usr/bin/env python3

"""
InvoiceArtisan GUI Launcher
Launches the main GUI application
"""

import sys
import os
import traceback
from pathlib import Path

# Add the src directory to the Python path
# Handle both development and PyInstaller executable paths
if getattr(sys, 'frozen', False):
    # Running as PyInstaller executable
    base_path = sys._MEIPASS
    src_path = os.path.join(base_path, 'src')
    # For frozen executable, log to the same directory as the exe
    log_dir = Path(sys.executable).parent
else:
    # Running in development
    base_path = os.path.dirname(__file__)
    src_path = os.path.join(base_path, '..', 'src')
    log_dir = Path(base_path).parent.parent

sys.path.insert(0, src_path)

def log_error(error_msg, exception=None):
    """Log errors to a file for debugging"""
    log_file = log_dir / "InvoiceArtisan_error.log"
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Error occurred: {error_msg}\n")
            if exception:
                f.write(f"Exception type: {type(exception).__name__}\n")
                f.write(f"Exception details: {str(exception)}\n")
                f.write(f"\nTraceback:\n")
                f.write(traceback.format_exc())
            f.write(f"{'='*60}\n")
    except Exception as log_err:
        # If we can't write to log, try to show error in console
        print(f"Failed to write to log file: {log_err}", file=sys.stderr)
        print(f"Original error: {error_msg}", file=sys.stderr)
        if exception:
            traceback.print_exc()

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
        error_msg = f"Import error: {e}"
        log_error(error_msg, e)
        # Try to show error in a message box if tkinter is available
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Import Error", 
                f"Failed to import required module:\n{str(e)}\n\n"
                f"Please check InvoiceArtisan_error.log for details.")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        log_error(error_msg, e)
        # Try to show error in a message box if tkinter is available
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Application Error", 
                f"An unexpected error occurred:\n{str(e)}\n\n"
                f"Please check InvoiceArtisan_error.log for details.")
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
