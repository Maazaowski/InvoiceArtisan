# InvoiceArtisan Developer Guide

## 🎯 Overview

This guide is for developers who want to contribute to, extend, or understand the InvoiceArtisan codebase. It covers everything from initial setup to advanced development workflows.

## 🏗️ Project Architecture

### High-Level Structure

```
InvoiceArtisan/
├── src/                    # Source code
│   ├── core/              # Core business logic
│   ├── gui/               # GUI application
│   └── utils/             # Utility functions
├── config/                 # Configuration management
├── build/                  # Build and packaging tools
├── tests/                  # Test suite
└── docs/                   # Documentation
```

### Core Components

#### 1. **Core Module** (`src/core/`)
- **`invoice_generator.py`**: PDF generation engine using ReportLab
- **`pdf_reader.py`**: PDF text extraction and parsing
- **`pdf_to_yaml.py`**: PDF to YAML template conversion

#### 2. **GUI Module** (`src/gui/`)
- **`main_window.py`**: Main application window and tab management
- **`tabs/`**: Individual tab components for different invoice sections
- **`utils/`**: GUI-specific utilities (styling, validation)

#### 3. **Utils Module** (`src/utils/`)
- **`config.py`**: Configuration management and loading
- **`file_utils.py`**: File operations and path management
- **`date_utils.py`**: Date handling and formatting

## 🚀 Development Setup

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: For version control
- **IDE**: VS Code, PyCharm, or your preferred editor

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/InvoiceArtisan.git
cd InvoiceArtisan

# Run automated setup
python scripts/setup.py

# Verify installation
python tests/test_structure.py
```

### Manual Setup (Alternative)

```bash
# Install main dependencies
pip install -r build/requirements/requirements.txt

# Install development dependencies
pip install -r build/requirements/requirements-dev.txt

# Install build dependencies
pip install -r build/requirements/requirements-build.txt
```

### Development Environment

```bash
# Activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_core/
pytest tests/test_gui/
pytest tests/test_utils/

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v tests/
```

### Test Structure

```
tests/
├── test_core/             # Core functionality tests
├── test_gui/              # GUI component tests
├── test_utils/            # Utility function tests
└── conftest.py            # Test configuration and fixtures
```

### Writing Tests

```python
# Example test structure
def test_invoice_generation():
    """Test that invoice generation works correctly"""
    # Arrange
    test_data = {...}
    
    # Act
    result = generate_invoice(test_data)
    
    # Assert
    assert result is not None
    assert result.endswith('.pdf')
```

## 🔧 Development Workflow

### 1. **Feature Development**

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Run tests
pytest tests/

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/new-feature
```

### 2. **Bug Fixes**

```bash
# Create bug fix branch
git checkout -b fix/bug-description

# Fix the issue
# ... make changes ...

# Add test for the bug
# ... write test ...

# Verify fix
pytest tests/

# Commit and push
git add .
git commit -m "fix: resolve bug description"
git push origin fix/bug-description
```

### 3. **Code Quality**

```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/

# Run all quality checks
python scripts/quality_check.py
```

## 📚 Code Architecture

### Design Patterns

#### 1. **MVC Pattern** (GUI)
- **Model**: Invoice data and business logic
- **View**: Tkinter GUI components
- **Controller**: Event handlers and data flow

#### 2. **Factory Pattern** (PDF Generation)
- Different invoice templates
- Configurable styling options
- Extensible output formats

#### 3. **Observer Pattern** (Data Updates)
- Real-time preview updates
- Validation feedback
- Configuration changes

### Data Flow

```
User Input → GUI Validation → Data Model → PDF Generation → Output
     ↓              ↓            ↓            ↓           ↓
  Tkinter    Input Validation  YAML      ReportLab    PDF File
```

### Configuration Management

```python
# Loading configuration
from utils.config import load_config

config = load_config('config/app_config.yaml')

# Accessing configuration
theme_color = config['gui']['theme']['primary_color']
window_size = config['gui']['window']['default_width']
```

## 🎨 GUI Development

### Adding New Tabs

1. **Create Tab Class**
```python
# src/gui/tabs/new_tab.py
import tkinter as tk
from tkinter import ttk

class NewTab(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        # Create UI elements
        pass
    
    def get_data(self):
        # Return tab data
        pass
    
    def set_data(self, data):
        # Set tab data
        pass
```

2. **Register in Main Window**
```python
# src/gui/main_window.py
from .tabs.new_tab import NewTab

# Add to notebook
self.notebook.add(NewTab(self.notebook), text="New Tab")
```

### Styling and Themes

```python
# src/gui/utils/styles.py
THEME_COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'accent': '#e74c3c',
    'success': '#27ae60',
    'warning': '#f39c12'
}

def apply_theme(widget, color_scheme='default'):
    """Apply theme to widget"""
    pass
```

## 🔌 API Development

### Core Functions

#### Invoice Generation
```python
from src.core.invoice_generator import generate_invoice

# Generate PDF from YAML data
result = generate_invoice(
    invoice_data,           # Dict or YAML file path
    output_path=None,       # Optional output path
    template='default'      # Template to use
)
```

#### PDF Reading
```python
from src.core.pdf_reader import read_pdf

# Extract text from PDF
text_content = read_pdf('invoice.pdf')
```

#### PDF to YAML Conversion
```python
from src.core.pdf_to_yaml import pdf_to_yaml

# Convert PDF to YAML template
yaml_data = pdf_to_yaml('invoice.pdf', 'template.yaml')
```

### Extending Core Functions

```python
# src/core/custom_generator.py
from .invoice_generator import InvoiceGenerator

class CustomInvoiceGenerator(InvoiceGenerator):
    def __init__(self, template_path):
        super().__init__(template_path)
    
    def generate_custom_invoice(self, data):
        """Custom invoice generation logic"""
        pass
```

## 🏗️ Build System

### PyInstaller Configuration

```bash
# Build executable
python build/scripts/build_exe.py

# Clean build
python build/scripts/clean_build.py

# Custom build options
pyinstaller build/pyinstaller/spec_files/custom.spec
```

### Build Configuration

```yaml
# config/build_config.yaml
build:
  target: "executable"
  platform: "windows"
  
pyinstaller:
  options:
    one_file: false
    console: false
    debug: false
```

## 📝 Documentation Standards

### Code Documentation

```python
def generate_invoice(invoice_data, output_path=None, template='default'):
    """
    Generate a PDF invoice from invoice data.
    
    Args:
        invoice_data (dict|str): Invoice data dictionary or YAML file path
        output_path (str, optional): Output PDF file path
        template (str): Template name to use for generation
        
    Returns:
        str: Path to generated PDF file
        
    Raises:
        ValueError: If invoice data is invalid
        FileNotFoundError: If template file not found
        
    Example:
        >>> data = {'invoice': {'number': 'INV-001'}}
        >>> generate_invoice(data, 'output.pdf')
        'output.pdf'
    """
    pass
```

### Function Documentation Template

- **Purpose**: What the function does
- **Parameters**: Input parameters and types
- **Returns**: Output and type
- **Raises**: Exceptions that may occur
- **Examples**: Usage examples
- **Notes**: Additional important information

## 🚨 Common Issues and Solutions

### Import Errors

```bash
# Problem: Module not found
ModuleNotFoundError: No module named 'core'

# Solution: Check Python path
import sys
sys.path.insert(0, 'path/to/src')
```

### GUI Issues

```bash
# Problem: Tkinter not available
ImportError: No module named 'tkinter'

# Solution: Install tkinter
# On Ubuntu/Debian: sudo apt-get install python3-tk
# On macOS: brew install python-tk
```

### Build Issues

```bash
# Problem: PyInstaller missing dependencies
ImportError: No module named 'reportlab'

# Solution: Install all requirements
pip install -r build/requirements/requirements.txt
```

## 🔍 Debugging

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='output/logs/debug.log'
)

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Debug Mode

```bash
# Run with debug output
python -v scripts/launch_gui.py

# Use Python debugger
python -m pdb scripts/launch_gui.py
```

## 📊 Performance Optimization

### Profiling

```bash
# Profile code execution
python -m cProfile -o profile.stats scripts/launch_gui.py

# Analyze profile results
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Memory Usage

```python
import tracemalloc

# Start memory tracking
tracemalloc.start()

# ... your code ...

# Get memory snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
print("[ Top 10 memory users ]")
for stat in top_stats[:10]:
    print(stat)
```

## 🤝 Contributing Guidelines

### Code Standards

1. **Python Style**: Follow PEP 8
2. **Documentation**: Docstrings for all functions
3. **Testing**: Tests for new functionality
4. **Type Hints**: Use type hints where appropriate

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Document** any new features
6. **Submit** pull request

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Scope**: core, gui, utils, build, docs

**Examples**:
- `feat(gui): add new invoice preview tab`
- `fix(core): resolve PDF generation memory leak`
- `docs(readme): update installation instructions`

## 📚 Additional Resources

### External Documentation

- [Python Official Docs](https://docs.python.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

### Project-Specific

- [Configuration Guide](config/README.md)
- [Build System Guide](docs/BUILD_README.md)
- [API Reference](docs/API_README.md)
- [Examples](docs/examples/)

### Development Tools

- **Code Quality**: Black, Flake8, MyPy
- **Testing**: Pytest, Coverage
- **Documentation**: Sphinx, MkDocs
- **Build**: PyInstaller, Setuptools

## 🆘 Getting Help

### Internal Resources

1. **Code Comments**: Check inline documentation
2. **Test Files**: Examples of usage
3. **Configuration Files**: Default settings and options
4. **Issues**: Check existing GitHub issues

### External Support

- **Stack Overflow**: Tag with `invoiceartisan`
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Use GitHub Discussions for questions

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Development
python scripts/setup.py              # Setup environment
python scripts/launch_gui.py         # Launch GUI
python scripts/launch_cli.py --help  # CLI help
pytest tests/                        # Run tests

# Building
python build/scripts/build_exe.py    # Build executable
python build/scripts/clean_build.py  # Clean build files

# Quality
black src/                           # Format code
flake8 src/                          # Lint code
mypy src/                            # Type checking
```

### File Locations

- **Source Code**: `src/`
- **Configuration**: `config/`
- **Tests**: `tests/`
- **Build Tools**: `build/`
- **Documentation**: `docs/`
- **Scripts**: `scripts/`

---

**Happy Coding! 🚀**

*This guide should help you get started with InvoiceArtisan development. If you need clarification on any section, please open an issue or discussion on GitHub.*
