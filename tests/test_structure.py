"""
Test the new project structure and imports
"""

import sys
import os
from pathlib import Path

def test_project_structure():
    """Test that the new project structure is correct"""
    
    # Add src to path
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Test core imports
    try:
        from core import invoice_generator, pdf_reader, pdf_to_yaml
        print("✅ Core modules imported successfully")
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False
    
    # Test GUI imports
    try:
        from gui import main_window
        print("✅ GUI modules imported successfully")
    except ImportError as e:
        print(f"❌ GUI import failed: {e}")
        return False
    
    # Test directory structure
    required_dirs = [
        "src/core",
        "src/gui", 
        "src/utils",
        "assets/logos",
        "assets/templates",
        "config",
        "build/scripts",
        "build/requirements",
        "docs",
        "scripts",
        "tests",
        "output/invoices"
    ]
    
    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"❌ Directory missing: {directory}")
            return False
        print(f"✅ Directory exists: {directory}")
    
    # Test configuration files
    required_configs = [
        "config/default_invoice.yaml",
        "config/app_config.yaml", 
        "config/build_config.yaml"
    ]
    
    for config_file in required_configs:
        if not Path(config_file).exists():
            print(f"❌ Config file missing: {config_file}")
            return False
        print(f"✅ Config file exists: {config_file}")
    
    # Test requirements files
    required_reqs = [
        "build/requirements/requirements.txt",
        "build/requirements/requirements-build.txt",
        "build/requirements/requirements-dev.txt"
    ]
    
    for req_file in required_reqs:
        if not Path(req_file).exists():
            print(f"❌ Requirements file missing: {req_file}")
            return False
        print(f"✅ Requirements file exists: {req_file}")
    
    print("\n🎉 All structure tests passed!")
    return True

if __name__ == "__main__":
    test_project_structure()
