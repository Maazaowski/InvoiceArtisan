# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launch_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo', 'logo'),  # Include logo directory
        ('sample', 'sample'),  # Include sample directory
        ('invoice_generator.py', '.'),  # Include PDF generator
        ('pdf_to_yaml.py', '.'),  # Include PDF converter
        ('pdf_reader.py', '.'),  # Include PDF reader
        ('invoices/invoice_template.yaml', '.'),  # Include default template
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'yaml',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.platypus',
        'PyPDF2',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'dateutil',
        'dateutil.parser',
        'subprocess',
        'threading',
        'pathlib',
        'json',
        'datetime',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InvoiceArtisan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo/MaazLogo.PNG',  # Use your logo as icon
    version_file=None,
    uac_admin=False,
    uac_uiaccess=False,
)
