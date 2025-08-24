# InvoiceArtisan Project Restructure Plan

## New Directory Structure

```
InvoiceArtisan/
├── src/                          # Source code
│   ├── core/                     # Core application logic
│   │   ├── __init__.py
│   │   ├── invoice_generator.py  # PDF generation engine
│   │   ├── pdf_reader.py         # PDF reading utilities
│   │   └── pdf_to_yaml.py        # PDF to YAML converter
│   ├── gui/                      # GUI application
│   │   ├── __init__.py
│   │   ├── main_window.py        # Main GUI window
│   │   ├── tabs/                 # Tab components
│   │   │   ├── __init__.py
│   │   │   ├── invoice_tab.py
│   │   │   ├── company_tab.py
│   │   │   ├── client_tab.py
│   │   │   ├── items_tab.py
│   │   │   ├── notes_tab.py
│   │   │   └── preview_tab.py
│   │   └── utils/                # GUI utilities
│   │       ├── __init__.py
│   │       ├── styles.py         # GUI styling
│   │       └── validators.py     # Input validation
│   └── utils/                    # General utilities
│       ├── __init__.py
│       ├── config.py             # Configuration management
│       ├── file_utils.py         # File operations
│       └── date_utils.py         # Date handling
├── assets/                       # Static assets
│   ├── logos/                    # Company logos
│   ├── templates/                # Invoice templates
│   └── icons/                    # Application icons
├── config/                       # Configuration files
│   ├── default_invoice.yaml      # Default invoice template
│   ├── app_config.yaml           # Application configuration
│   └── build_config.yaml         # Build configuration
├── build/                        # Build tools and scripts
│   ├── __init__.py
│   ├── pyinstaller/              # PyInstaller configuration
│   │   ├── __init__.py
│   │   ├── spec_files/           # PyInstaller spec files
│   │   └── hooks/                # Custom PyInstaller hooks
│   ├── scripts/                  # Build scripts
│   │   ├── __init__.py
│   │   ├── build_exe.py          # Main build script
│   │   ├── build_exe.bat         # Windows batch file
│   │   └── clean_build.py        # Clean build directories
│   └── requirements/              # Dependency management
│       ├── requirements.txt       # Main requirements
│       ├── requirements-dev.txt   # Development dependencies
│       └── requirements-build.txt # Build dependencies
├── docs/                         # Documentation
│   ├── README.md                 # Main project README
│   ├── GUI_README.md             # GUI usage guide
│   ├── BUILD_README.md           # Build instructions
│   ├── API_README.md             # API documentation
│   └── examples/                 # Usage examples
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_core/                # Core functionality tests
│   ├── test_gui/                 # GUI tests
│   └── test_utils/               # Utility tests
├── scripts/                      # Utility scripts
│   ├── __init__.py
│   ├── launch_gui.py             # GUI launcher
│   ├── launch_cli.py             # CLI launcher
│   └── setup.py                  # Setup script
├── output/                       # Generated files (gitignored)
│   ├── invoices/                 # Generated invoices
│   ├── logs/                     # Application logs
│   └── temp/                     # Temporary files
├── .gitignore                    # Git ignore rules
├── LICENSE                       # Project license
└── README.md                     # Project overview
```

## Benefits of This Structure

1. **Separation of Concerns**: Clear separation between core logic, GUI, utilities, and build tools
2. **Modularity**: Easy to maintain and extend individual components
3. **Clear Dependencies**: Build tools separated from source code
4. **Professional Layout**: Follows Python project best practices
5. **Easy Navigation**: Logical grouping of related files
6. **Scalability**: Easy to add new features and modules
7. **Testing**: Dedicated test directory structure
8. **Documentation**: Centralized documentation location
9. **Assets Management**: Organized static resources
10. **Configuration**: Centralized configuration management

## Migration Strategy

1. Create new directory structure
2. Move and reorganize existing files
3. Update import statements
4. Update documentation references
5. Test functionality
6. Clean up old structure
