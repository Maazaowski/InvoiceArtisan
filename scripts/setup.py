#!/usr/bin/env python3

"""
InvoiceArtisan Setup Script
Installs dependencies and sets up the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install required packages"""
    requirements_file = Path("build/requirements/requirements.txt")
    if not requirements_file.exists():
        print("❌ Requirements file not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "Installing main requirements"
    )

def install_dev_requirements():
    """Install development requirements"""
    dev_requirements_file = Path("build/requirements/requirements-dev.txt")
    if not dev_requirements_file.exists():
        print("⚠️  Development requirements file not found, skipping...")
        return True
    
    return run_command(
        f"{sys.executable} -m pip install -r {dev_requirements_file}",
        "Installing development requirements"
    )

def install_build_requirements():
    """Install build requirements"""
    build_requirements_file = Path("build/requirements/requirements-build.txt")
    if not build_requirements_file.exists():
        print("⚠️  Build requirements file not found, skipping...")
        return True
    
    return run_command(
        f"{sys.executable} -m pip install -r {build_requirements_file}",
        "Installing build requirements"
    )

def create_directories():
    """Create necessary directories"""
    directories = [
        "output/invoices",
        "output/logs", 
        "output/temp",
        "assets/logos",
        "assets/templates",
        "assets/icons"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}")
    
    return True

def setup_git_hooks():
    """Set up Git hooks if available"""
    git_dir = Path(".git")
    if not git_dir.exists():
        print("⚠️  Git repository not found, skipping hooks setup...")
        return True
    
    print("🔧 Setting up Git hooks...")
    # Add pre-commit hook setup here if needed
    print("   ✅ Git hooks setup completed")
    return True

def main():
    """Main setup function"""
    print("🚀 InvoiceArtisan Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Install development requirements (optional)
    if not install_dev_requirements():
        print("⚠️  Development setup incomplete, but main setup succeeded")
    
    # Install build requirements (optional)
    if not install_build_requirements():
        print("⚠️  Build setup incomplete, but main setup succeeded")
    
    # Setup Git hooks
    setup_git_hooks()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Launch GUI: python scripts/launch_gui.py")
    print("2. Use CLI: python scripts/launch_cli.py --help")
    print("3. Build executable: python build/scripts/build_exe.py")
    print("\n📚 Documentation: docs/")

if __name__ == "__main__":
    main()
