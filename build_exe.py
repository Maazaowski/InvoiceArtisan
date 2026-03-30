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
    print("Checking dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=False
        )
        if result.returncode != 0:
            print("❌ Failed to install PyInstaller")
            return False
    
    # Check project dependencies from requirements.txt
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        print("📦 Checking project dependencies from requirements.txt...")
        try:
            # Try importing key packages to see if they're installed
            import yaml
            import reportlab
            import PyPDF2
            from PIL import Image
            print("✅ All required packages are installed")
        except ImportError as e:
            print(f"⚠️  Missing package: {e}")
            print("Installing requirements from requirements.txt...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=False
            )
            if result.returncode != 0:
                print("⚠️  Some packages may not have installed correctly")
    else:
        print("⚠️  requirements.txt not found, skipping dependency check")
    
    return True

def clean_build_dirs():
    """Clean previous build directories"""
    print("\nCleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}/")
            try:
                shutil.rmtree(dir_name)
            except Exception as e:
                print(f"⚠️  Warning: Could not remove {dir_name}: {e}")
    
    # Clean __pycache__ directories recursively
    print("🧹 Cleaning __pycache__ directories...")
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
            except Exception as e:
                print(f"⚠️  Warning: Could not remove {cache_dir}: {e}")

def build_executable(debug=False):
    """Build the executable using PyInstaller"""
    print("\n🔨 Building InvoiceArtisan executable...")
    if debug:
        print("🔍 Debug mode: Console will be enabled to see errors")
    
    # Check if spec file exists
    spec_file = Path("InvoiceArtisan.spec")
    if not spec_file.exists():
        print("❌ InvoiceArtisan.spec not found!")
        print("   Please ensure InvoiceArtisan.spec exists in the root directory")
        return False
    
    print(f"📋 Using spec file: {spec_file}")
    
    # For debug builds, temporarily modify console setting
    if debug:
        # Read spec file
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
        
        # Temporarily enable console
        modified_spec = spec_content.replace('console=False', 'console=True')
        debug_spec = spec_file.parent / "InvoiceArtisan_debug.spec"
        with open(debug_spec, 'w', encoding='utf-8') as f:
            f.write(modified_spec)
        build_spec = debug_spec
        print(f"📋 Using debug spec file: {build_spec}")
    else:
        build_spec = spec_file
    
    # Build using PyInstaller
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        str(build_spec)
    ])
    
    # Clean up debug spec if created
    if debug and debug_spec.exists():
        debug_spec.unlink()
    
    if result.returncode == 0:
        print("✅ Executable built successfully!")
        return True
    else:
        print("❌ Build failed!")
        return False

def verify_build():
    """Verify the build output"""
    print("\nVerifying build output...")
    dist_dir = Path("dist")
    exe_path = dist_dir / "InvoiceArtisan.exe"
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executable created: {exe_path}")
        print(f"📏 Size: {size_mb:.1f} MB")
        
        # Check if required directories are included (for one-dir builds)
        # Note: For one-file builds, these won't be in dist/
        required_dirs = ['assets', 'config', 'src']
        found_dirs = []
        for dir_name in required_dirs:
            if (dist_dir / dir_name).exists():
                found_dirs.append(dir_name)
                print(f"✅ {dir_name}/ included")
        
        if not found_dirs:
            print("ℹ️  One-file build detected (all resources bundled in exe)")
        
        return True
    else:
        print("❌ Executable not found!")
        return False

def create_installer_info():
    """Create information about the build"""
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    info_file = dist_dir / "INSTALLATION_INFO.txt"
    
    info_content = """InvoiceArtisan - Installation Information

This executable contains:
- InvoiceArtisan GUI application
- PDF generation engine
- PDF to YAML converter
- PDF reader
- Templates and configuration files
- Company logo and assets

Usage:
1. Double-click InvoiceArtisan.exe to run
2. The application will create an 'output' folder for your files
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
    
    try:
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)
        print("📝 Installation info created")
    except Exception as e:
        print(f"⚠️  Could not create installation info: {e}")

def main():
    """Main build process"""
    print("🚀 InvoiceArtisan Executable Builder")
    print("=" * 50)
    
    # Check for debug flag
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed!")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if build_executable(debug=debug_mode):
        # Verify build
        if verify_build():
            # Create installation info
            create_installer_info()
            
            print("\n" + "=" * 50)
            print("🎉 Build completed successfully!")
            print("=" * 50)
            exe_path = os.path.abspath('dist/InvoiceArtisan.exe')
            print(f"📁 Executable location: {exe_path}")
            print("\n📋 Next steps:")
            print("1. Test the executable by double-clicking it")
            if debug_mode:
                print("   (Debug mode: Console window will show errors)")
            else:
                print("   (If it doesn't work, check InvoiceArtisan_error.log in the dist folder)")
                print("   (Or rebuild with --debug flag: python build_exe.py --debug)")
            print("2. Distribute the executable (or entire 'dist' folder if one-dir build)")
            print("3. Users can run InvoiceArtisan.exe without Python")
        else:
            print("\n❌ Build verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Build process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
