#!/usr/bin/env python3

"""
Build Script for InvoiceArtisan Executable
This script automates the process of creating a standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import yaml
        import reportlab
        import PyPDF2
        import PIL
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}/")
            shutil.rmtree(dir_name)
    
    # Clean .spec files (keep our custom one)
    for file in os.listdir('.'):
        if file.endswith('.spec') and file != 'invoice_artisan.spec':
            print(f"🧹 Removing {file}")
            os.remove(file)

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building InvoiceArtisan executable...")
    
    # Use our custom spec file
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "invoice_artisan.spec"
    ])
    
    if result.returncode == 0:
        print("✅ Executable built successfully!")
        return True
    else:
        print("❌ Build failed!")
        return False

def verify_build():
    """Verify the build output"""
    dist_dir = Path("dist")
    exe_path = dist_dir / "InvoiceArtisan.exe"
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executable created: {exe_path}")
        print(f"📏 Size: {size_mb:.1f} MB")
        
        # Check if required files are included
        required_files = ['logo', 'sample', 'invoice_generator.py']
        for file in required_files:
            if (dist_dir / file).exists():
                print(f"✅ {file} included")
            else:
                print(f"❌ {file} missing")
        
        return True
    else:
        print("❌ Executable not found!")
        return False

def create_installer_info():
    """Create information about the build"""
    info_file = Path("dist/INSTALLATION_INFO.txt")
    
    info_content = """InvoiceArtisan - Installation Information

This executable contains:
- InvoiceArtisan GUI application
- PDF generation engine
- PDF to YAML converter
- PDF reader
- Sample templates and logo

Usage:
1. Double-click InvoiceArtisan.exe to run
2. The application will create an 'invoices' folder for your files
3. All invoice files are stored locally and not shared

System Requirements:
- Windows 10 or later
- No Python installation required
- Approximately 50-100 MB disk space

Support:
- Check the README.md file for detailed usage instructions
- All source code is available in the project repository

Built with PyInstaller
"""
    
    with open(info_file, 'w') as f:
        f.write(info_content)
    
    print("📝 Installation info created")

def main():
    """Main build process"""
    print("🚀 InvoiceArtisan Executable Builder")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if build_executable():
        # Verify build
        if verify_build():
            # Create installation info
            create_installer_info()
            
            print("\n🎉 Build completed successfully!")
            print(f"📁 Executable location: {os.path.abspath('dist/InvoiceArtisan.exe')}")
            print("\n📋 Next steps:")
            print("1. Test the executable by double-clicking it")
            print("2. Distribute the entire 'dist' folder")
            print("3. Users can run InvoiceArtisan.exe without Python")
        else:
            print("❌ Build verification failed!")
    else:
        print("❌ Build process failed!")

if __name__ == "__main__":
    main()
