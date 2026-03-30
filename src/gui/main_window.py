#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yaml
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import threading
from PIL import Image, ImageTk
import json
import traceback

# Add the src directory to the Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

class InvoiceArtisanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InvoiceArtisan - Professional Invoice Generator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set modern, futuristic theme colors with high contrast
        self.colors = {
            'primary': '#1a1a2e',      # Dark navy
            'secondary': '#16213e',    # Darker blue
            'accent': '#0f3460',       # Deep blue
            'highlight': '#00d4ff',    # Cyan/neon blue
            'success': '#00ff88',      # Neon green
            'warning': '#ffaa00',      # Amber
            'error': '#ff3366',        # Coral red
            'background': '#0d1117',   # Very dark
            'background_light': '#161b22',  # Slightly lighter dark
            'text': '#ffffff',         # White
            'text_secondary': '#c9d1d9',  # Light gray
            'border': '#30363d',       # Border gray
            'white': '#ffffff',
            'dark': '#1a1a2e'
        }
        
        # Configure styles
        self.setup_styles()
        
        # Initialize data
        self.invoice_data = self.get_default_invoice_data()
        self.current_file = None
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
        
        # Load default data
        self.load_data_to_ui()
        
        # Bind events
        self.bind_events()
        
    def setup_styles(self):
        """Configure ttk styles for modern, futuristic appearance with high contrast"""
        style = ttk.Style()
        
        # Try to use a modern theme, fallback to default
        try:
            style.theme_use('clam')  # Better for custom styling
        except:
            pass
        
        # Configure root window background
        self.root.configure(bg=self.colors['background'])
        
        # Configure common styles with high contrast
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 18, 'bold'), 
                       foreground=self.colors['highlight'],
                       background=self.colors['background'])
        
        style.configure('Section.TLabel', 
                       font=('Segoe UI', 11, 'bold'), 
                       foreground=self.colors['highlight'],
                       background=self.colors['background'])
        
        # Modern button styles with high contrast and visibility
        style.configure('Modern.Primary.TButton',
                       background=self.colors['highlight'],
                       foreground=self.colors['primary'],
                       borderwidth=2,
                       relief='raised',
                       padding=(15, 8),
                       font=('Segoe UI', 10, 'bold'))
        style.map('Modern.Primary.TButton',
                 background=[('active', '#00b8e6'), ('pressed', '#0099cc')])
        
        style.configure('Modern.Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['primary'],
                       borderwidth=2,
                       relief='raised',
                       padding=(15, 8),
                       font=('Segoe UI', 10, 'bold'))
        style.map('Modern.Success.TButton',
                 background=[('active', '#00e699'), ('pressed', '#00cc77')])
        
        style.configure('Modern.Warning.TButton',
                       background=self.colors['warning'],
                       foreground=self.colors['primary'],
                       borderwidth=2,
                       relief='raised',
                       padding=(15, 8),
                       font=('Segoe UI', 10, 'bold'))
        style.map('Modern.Warning.TButton',
                 background=[('active', '#ffbb33'), ('pressed', '#ff9900')])
        
        style.configure('Modern.Error.TButton',
                       background=self.colors['error'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='raised',
                       padding=(15, 8),
                       font=('Segoe UI', 10, 'bold'))
        style.map('Modern.Error.TButton',
                 background=[('active', '#ff4d7a'), ('pressed', '#ff1a4d')])
        
        # Default button style for better visibility
        style.configure('TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='raised',
                       padding=(12, 6),
                       font=('Segoe UI', 9))
        style.map('TButton',
                 background=[('active', self.colors['highlight']), 
                            ('pressed', self.colors['secondary'])],
                 foreground=[('active', self.colors['primary'])])
        
        # Notebook (tabs) styling
        style.configure('TNotebook',
                       background=self.colors['background'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=self.colors['background_light'],
                       foreground=self.colors['text_secondary'],
                       padding=(20, 10),
                       font=('Segoe UI', 10))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['secondary'])],
                 foreground=[('selected', self.colors['highlight']),
                            ('active', self.colors['text'])])
        
        # Frame styling
        style.configure('TFrame',
                       background=self.colors['background'])
        style.configure('TLabelFrame',
                       background=self.colors['background'],
                       foreground=self.colors['highlight'],
                       borderwidth=2,
                       relief='solid')
        style.configure('TLabelFrame.Label',
                       background=self.colors['background'],
                       foreground=self.colors['highlight'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Entry and Combobox styling
        style.configure('TEntry',
                       fieldbackground=self.colors['background_light'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='solid',
                       insertcolor=self.colors['highlight'])
        style.configure('TCombobox',
                       fieldbackground=self.colors['background_light'],
                       foreground=self.colors['text'],
                       borderwidth=2,
                       relief='solid')
        
        # Label styling
        style.configure('TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 9))
        
        # Status bar styling
        style.configure('Status.TLabel',
                       background=self.colors['background_light'],
                       foreground=self.colors['highlight'],
                       relief='sunken',
                       borderwidth=1,
                       font=('Segoe UI', 9))
        
    def create_header(self):
        """Create the application header"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="InvoiceArtisan", 
                               style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, 
                                  text="Professional Invoice Generator", 
                                  font=('Segoe UI', 10),
                                  foreground=self.colors['text_secondary'],
                                  background=self.colors['background'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
                # File operations frame
        file_frame = ttk.Frame(header_frame)
        file_frame.pack(side=tk.RIGHT)
        
        # Template selector
        template_frame = ttk.Frame(header_frame)
        template_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        ttk.Label(template_frame, text="Template:", 
                 font=('Segoe UI', 9),
                 foreground=self.colors['text_secondary'],
                 background=self.colors['background']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.template_var = tk.StringVar(value="modern_blue")
        self.template_combo = ttk.Combobox(template_frame, 
                                          textvariable=self.template_var,
                                          width=15,
                                          state='readonly')
        self.template_combo.pack(side=tk.LEFT)
        
        # Load available templates
        self.load_available_templates()
        
        # New button
        self.new_btn = ttk.Button(file_frame, 
                                  text="🆕 New Invoice", 
                                  command=self.new_invoice,
                                  style='Modern.Primary.TButton')
        self.new_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Open button
        self.open_btn = ttk.Button(file_frame, 
                                   text="📂 Open YAML", 
                                   command=self.open_yaml,
                                   style='Modern.Primary.TButton')
        self.open_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Save button
        self.save_btn = ttk.Button(file_frame, 
                                   text="💾 Save YAML", 
                                   command=self.save_yaml,
                                   style='Modern.Success.TButton')
        self.save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
    def create_main_content(self):
        """Create the main content area with notebook tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_invoice_tab()
        self.create_company_tab()
        self.create_client_tab()
        self.create_items_tab()
        self.create_notes_tab()
        self.create_template_tab()
        self.create_preview_tab()
        
        # Initialize template preview after all tabs are created
        self.update_template_preview()
        
    def create_invoice_tab(self):
        """Create the invoice details tab"""
        invoice_frame = ttk.Frame(self.notebook)
        self.notebook.add(invoice_frame, text="Invoice Details")
        
        # Main content
        content_frame = ttk.Frame(invoice_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Invoice number
        ttk.Label(content_frame, text="Invoice Number:", 
                 style='Section.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.invoice_number_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.invoice_number_var, 
                 width=30).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Date
        ttk.Label(content_frame, text="Invoice Date:", 
                 style='Section.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.invoice_date_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.invoice_date_var, 
                 width=30).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Due date
        ttk.Label(content_frame, text="Due Date:", 
                 style='Section.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.due_date_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.due_date_var, 
                 width=30).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Month
        ttk.Label(content_frame, text="Month:", 
                 style='Section.TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(content_frame, textvariable=self.month_var, 
                                  values=['January', 'February', 'March', 'April', 'May', 'June',
                                         'July', 'August', 'September', 'October', 'November', 'December'],
                                  width=27, state='readonly')
        month_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Tax rate
        ttk.Label(content_frame, text="Tax Rate (%):", 
                 style='Section.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.tax_rate_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.tax_rate_var, 
                 width=30).grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Quick actions
        actions_frame = ttk.Frame(content_frame)
        actions_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(actions_frame, text="📅 Set Today's Date", 
                  command=self.set_today_date).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="📆 Set Due Date (+30 days)", 
                  command=self.set_due_date).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="🔢 Auto-generate Invoice Number", 
                  command=self.auto_generate_number).pack(side=tk.LEFT)
        
    def create_company_tab(self):
        """Create the company information tab"""
        company_frame = ttk.Frame(self.notebook)
        self.notebook.add(company_frame, text="Company")
        
        content_frame = ttk.Frame(company_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Company name
        ttk.Label(content_frame, text="Company Name:", 
                 style='Section.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.company_name_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_name_var, 
                 width=40).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Address 1
        ttk.Label(content_frame, text="Address Line 1:", 
                 style='Section.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.company_address1_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_address1_var, 
                 width=40).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Address 2
        ttk.Label(content_frame, text="Address Line 2:", 
                 style='Section.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.company_address2_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_address2_var, 
                 width=40).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # City
        ttk.Label(content_frame, text="City:", 
                 style='Section.TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.company_city_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_city_var, 
                 width=40).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # State
        ttk.Label(content_frame, text="State:", 
                 style='Section.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.company_state_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_state_var, 
                 width=40).grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # ZIP
        ttk.Label(content_frame, text="ZIP Code:", 
                 style='Section.TLabel').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.company_zip_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_zip_var, 
                 width=40).grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Country
        ttk.Label(content_frame, text="Country:", 
                 style='Section.TLabel').grid(row=6, column=0, sticky=tk.W, pady=5)
        self.company_country_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_country_var, 
                 width=40).grid(row=6, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Email
        ttk.Label(content_frame, text="Email:", 
                 style='Section.TLabel').grid(row=7, column=0, sticky=tk.W, pady=5)
        self.company_email_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_email_var, 
                 width=40).grid(row=7, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Phone
        ttk.Label(content_frame, text="Phone:", 
                 style='Section.TLabel').grid(row=8, column=0, sticky=tk.W, pady=5)
        self.company_phone_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.company_phone_var, 
                 width=40).grid(row=8, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
    def create_client_tab(self):
        """Create the client information tab"""
        client_frame = ttk.Frame(self.notebook)
        self.notebook.add(client_frame, text="Client")
        
        content_frame = ttk.Frame(client_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Client name
        ttk.Label(content_frame, text="Client Name:", 
                 style='Section.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.client_name_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_name_var, 
                 width=40).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Address
        ttk.Label(content_frame, text="Address:", 
                 style='Section.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.client_address_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_address_var, 
                 width=40).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # City
        ttk.Label(content_frame, text="City:", 
                 style='Section.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.client_city_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_city_var, 
                 width=40).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # State
        ttk.Label(content_frame, text="State:", 
                 style='Section.TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.client_state_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_state_var, 
                 width=40).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # ZIP
        ttk.Label(content_frame, text="ZIP Code:", 
                 style='Section.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.client_zip_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_zip_var, 
                 width=40).grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Country
        ttk.Label(content_frame, text="Country:", 
                 style='Section.TLabel').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.client_country_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_country_var, 
                 width=40).grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Email
        ttk.Label(content_frame, text="Email:", 
                 style='Section.TLabel').grid(row=6, column=0, sticky=tk.W, pady=5)
        self.client_email_var = tk.StringVar()
        ttk.Entry(content_frame, textvariable=self.client_email_var, 
                 width=40).grid(row=6, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
    def create_items_tab(self):
        """Create the invoice items tab"""
        items_frame = ttk.Frame(self.notebook)
        self.notebook.add(items_frame, text="Items")
        
        content_frame = ttk.Frame(items_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Items list
        items_list_frame = ttk.Frame(content_frame)
        items_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for items
        columns = ('name', 'description', 'quantity', 'rate', 'amount')
        self.items_tree = ttk.Treeview(items_list_frame, columns=columns, show='headings', height=10)
        
        # Define headings
        self.items_tree.heading('name', text='Item Name')
        self.items_tree.heading('description', text='Description')
        self.items_tree.heading('quantity', text='Quantity')
        self.items_tree.heading('rate', text='Rate ($)')
        self.items_tree.heading('amount', text='Amount ($)')
        
        # Define column widths
        self.items_tree.column('name', width=200)
        self.items_tree.column('description', width=250)
        self.items_tree.column('quantity', width=100)
        self.items_tree.column('rate', width=100)
        self.items_tree.column('amount', width=100)
        
        # Add scrollbar
        items_scrollbar = ttk.Scrollbar(items_list_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        # Pack tree and scrollbar
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Item editing frame
        item_edit_frame = ttk.LabelFrame(content_frame, text="Add/Edit Item", padding=10)
        item_edit_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Item name
        ttk.Label(item_edit_frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.item_name_var = tk.StringVar()
        ttk.Entry(item_edit_frame, textvariable=self.item_name_var, 
                 width=30).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Description
        ttk.Label(item_edit_frame, text="Description:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.item_description_var = tk.StringVar()
        ttk.Entry(item_edit_frame, textvariable=self.item_description_var, 
                 width=30).grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Quantity
        ttk.Label(item_edit_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.item_quantity_var = tk.StringVar()
        ttk.Entry(item_edit_frame, textvariable=self.item_quantity_var, 
                 width=15).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Rate
        ttk.Label(item_edit_frame, text="Rate ($):").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.item_rate_var = tk.StringVar()
        ttk.Entry(item_edit_frame, textvariable=self.item_rate_var, 
                 width=15).grid(row=1, column=3, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Buttons
        buttons_frame = ttk.Frame(item_edit_frame)
        buttons_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(buttons_frame, text="➕ Add Item", 
                  command=self.add_item, style='Modern.Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="✏️ Update Item", 
                  command=self.update_item, style='Modern.Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="🗑️ Delete Item", 
                  command=self.delete_item, style='Modern.Warning.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="🗑️ Clear Form", 
                  command=self.clear_item_form).pack(side=tk.LEFT)
        
        # Bind selection event
        self.items_tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
    def create_notes_tab(self):
        """Create the notes and terms tab"""
        notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(notes_frame, text="Notes & Terms")
        
        content_frame = ttk.Frame(notes_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Notes
        ttk.Label(content_frame, text="Notes:", 
                 style='Section.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.notes_text = scrolledtext.ScrolledText(content_frame, height=6, width=80)
        self.notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Terms and Conditions
        ttk.Label(content_frame, text="Terms & Conditions:", 
                 style='Section.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.terms_text = scrolledtext.ScrolledText(content_frame, height=8, width=80)
        self.terms_text.pack(fill=tk.BOTH, expand=True)
        
        # Quick templates
        templates_frame = ttk.LabelFrame(content_frame, text="Quick Templates", padding=10)
        templates_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(templates_frame, text="Standard Terms", 
                  command=self.load_standard_terms).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(templates_frame, text="Payment Details", 
                  command=self.load_payment_details).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(templates_frame, text="Clear All", 
                  command=self.clear_notes_terms).pack(side=tk.LEFT)
        
    def create_template_tab(self):
        """Create the template selection and preview tab"""
        template_frame = ttk.Frame(self.notebook)
        self.notebook.add(template_frame, text="Template")
        
        content_frame = ttk.Frame(template_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Template selection section
        selection_frame = ttk.LabelFrame(content_frame, text="Select Template", padding=10)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Template dropdown
        ttk.Label(selection_frame, text="Invoice Template:", 
                 style='Section.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        self.template_preview_combo = ttk.Combobox(selection_frame, 
                                                   textvariable=self.template_var,
                                                   width=40,
                                                   state='readonly')
        self.template_preview_combo.pack(anchor=tk.W, pady=(0, 10))
        
        # Template description
        self.template_description = ttk.Label(selection_frame, text="", 
                                            wraplength=500,
                                            justify=tk.LEFT)
        self.template_description.pack(anchor=tk.W, pady=(0, 10))
        
        # Template features
        self.template_features = ttk.Label(selection_frame, text="", 
                                         wraplength=500,
                                         justify=tk.LEFT)
        self.template_features.pack(anchor=tk.W, pady=(0, 10))
        
        # Preview section
        preview_frame = ttk.LabelFrame(content_frame, text="Template Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Preview text area
        self.template_preview_text = scrolledtext.ScrolledText(preview_frame, height=20, width=80)
        self.template_preview_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Preview buttons
        preview_buttons_frame = ttk.Frame(preview_frame)
        preview_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(preview_buttons_frame, text="Update Preview", 
                   command=self.update_template_preview).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(preview_buttons_frame, text="Generate Sample PDF", 
                   command=self.generate_template_sample).pack(side=tk.LEFT)
        
        # Update template preview when template changes
        self.template_preview_combo.bind('<<ComboboxSelected>>', self.update_template_preview)
        
    def create_preview_tab(self):
        """Create the preview and generate tab"""
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="Preview & Generate")
        
        content_frame = ttk.Frame(preview_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Preview area
        preview_label = ttk.Label(content_frame, text="Invoice Preview", 
                                 style='Section.TLabel')
        preview_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Preview text area
        self.preview_text = scrolledtext.ScrolledText(content_frame, height=20, width=80)
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Generate button
        generate_frame = ttk.Frame(content_frame)
        generate_frame.pack(fill=tk.X)
        
        self.generate_btn = ttk.Button(generate_frame, text="📄 Generate PDF Invoice", 
                                      command=self.generate_pdf,
                                      style='Modern.Success.TButton')
        self.generate_btn.pack(side=tk.RIGHT)
        
        # Preview button
        self.preview_btn = ttk.Button(generate_frame, text="👁️ Update Preview", 
                                     command=self.update_preview,
                                     style='Modern.Primary.TButton')
        self.preview_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Label(self.main_container, text="Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W,
                                   style='Status.TLabel')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def get_default_invoice_data(self):
        """Get default invoice data structure"""
        today = datetime.now()
        due_date = today + timedelta(days=30)
        
        return {
            'invoice': {
                'number': f"INV-{today.strftime('%Y%m%d')}-001",
                'date': today.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'month': today.strftime('%B')
            },
            'company': {
                'name': 'Syed Muhammad Maaz',
                'address1': 'B-118, 5th Street',
                'address2': 'Block 18, Gulshan-E-Iqbal',
                'city': 'Karachi',
                'state': 'Sind',
                'zip': '75300',
                'country': 'Pakistan',
                'email': 'm.maaz96@gmail.com',
                'phone': '+923111135688'
            },
            'client': {
                'name': 'Astera Software',
                'address': '310 N Westlake Blvd #140',
                'city': 'Westlake Village',
                'state': 'CA',
                'zip': '91362',
                'country': 'U.S.A',
                'email': 'accounts@astera.com'
            },
            'items': [
                {
                    'name': 'IT Services',
                    'description': 'Professional IT consulting and development services',
                    'quantity': 1.0,
                    'rate': 100.0
                }
            ],
            'tax_rate': 0.0,
            'notes': 'Thank you for your business!',
            'terms': 'Payment due within 30 days of invoice date.'
        }
        
    def load_data_to_ui(self):
        """Load invoice data into UI fields"""
        # Invoice details
        self.invoice_number_var.set(self.invoice_data['invoice']['number'])
        self.invoice_date_var.set(self.invoice_data['invoice']['date'])
        self.due_date_var.set(self.invoice_data['invoice']['due_date'])
        self.month_var.set(self.invoice_data['invoice']['month'])
        self.tax_rate_var.set(str(self.invoice_data['tax_rate']))
        
        # Company details
        self.company_name_var.set(self.invoice_data['company']['name'])
        self.company_address1_var.set(self.invoice_data['company'].get('address1', ''))
        self.company_address2_var.set(self.invoice_data['company'].get('address2', ''))
        self.company_city_var.set(self.invoice_data['company']['city'])
        self.company_state_var.set(self.invoice_data['company']['state'])
        self.company_zip_var.set(self.invoice_data['company']['zip'])
        self.company_country_var.set(self.invoice_data['company']['country'])
        self.company_email_var.set(self.invoice_data['company']['email'])
        self.company_phone_var.set(self.invoice_data['company']['phone'])
        
        # Client details
        self.client_name_var.set(self.invoice_data['client']['name'])
        self.client_address_var.set(self.invoice_data['client']['address'])
        self.client_city_var.set(self.invoice_data['client']['city'])
        self.client_state_var.set(self.invoice_data['client']['state'])
        self.client_zip_var.set(self.invoice_data['client']['zip'])
        self.client_country_var.set(self.invoice_data['client']['country'])
        self.client_email_var.set(self.invoice_data['client']['email'])
        
        # Items
        self.refresh_items_tree()
        
        # Notes and terms
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(1.0, self.invoice_data.get('notes', ''))
        
        self.terms_text.delete(1.0, tk.END)
        self.terms_text.insert(1.0, self.invoice_data.get('terms', ''))
        
    def refresh_items_tree(self):
        """Refresh the items treeview"""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Add items from data
        for item in self.invoice_data['items']:
            amount = item['quantity'] * item['rate']
            self.items_tree.insert('', 'end', values=(
                item.get('name', ''),
                item.get('description', ''),
                item['quantity'],
                f"${item['rate']:.2f}",
                f"${amount:.2f}"
            ))
        
        # Update totals
        self.update_totals()
        
    def update_totals(self):
        """Update totals display"""
        subtotal = sum(item['quantity'] * item['rate'] for item in self.invoice_data['items'])
        tax = subtotal * self.invoice_data['tax_rate']
        total = subtotal + tax
        
        # Update status bar with totals
        self.status_bar.config(text=f"Subtotal: ${subtotal:.2f} | Tax: ${tax:.2f} | Total: ${total:.2f}")
        
    def collect_data_from_ui(self):
        """Collect data from UI fields back to invoice_data"""
        # Invoice details
        self.invoice_data['invoice']['number'] = self.invoice_number_var.get()
        self.invoice_data['invoice']['date'] = self.invoice_date_var.get()
        self.invoice_data['invoice']['due_date'] = self.due_date_var.get()
        self.invoice_data['invoice']['month'] = self.month_var.get()
        
        try:
            self.invoice_data['tax_rate'] = float(self.tax_rate_var.get()) / 100.0
        except ValueError:
            self.invoice_data['tax_rate'] = 0.0
        
        # Company details
        self.invoice_data['company']['name'] = self.company_name_var.get()
        self.invoice_data['company']['address1'] = self.company_address1_var.get()
        self.invoice_data['company']['address2'] = self.company_address2_var.get()
        self.invoice_data['company']['city'] = self.company_city_var.get()
        self.invoice_data['company']['state'] = self.company_state_var.get()
        self.invoice_data['company']['zip'] = self.company_zip_var.get()
        self.invoice_data['company']['country'] = self.company_country_var.get()
        self.invoice_data['company']['email'] = self.company_email_var.get()
        self.invoice_data['company']['phone'] = self.company_phone_var.get()
        
        # Client details
        self.invoice_data['client']['name'] = self.client_name_var.get()
        self.invoice_data['client']['address'] = self.client_address_var.get()
        self.invoice_data['client']['city'] = self.client_city_var.get()
        self.invoice_data['client']['state'] = self.client_state_var.get()
        self.invoice_data['client']['zip'] = self.client_zip_var.get()
        self.invoice_data['client']['country'] = self.client_country_var.get()
        self.invoice_data['client']['email'] = self.client_email_var.get()
        
        # Notes and terms
        self.invoice_data['notes'] = self.notes_text.get(1.0, tk.END).strip()
        self.invoice_data['terms'] = self.terms_text.get(1.0, tk.END).strip()
        
    def load_available_templates(self):
        """Load available invoice templates"""
        try:
            from utils.template_manager import get_template_manager
            template_manager = get_template_manager()
            templates = template_manager.get_available_templates()
            
            # Populate template combo box
            template_names = [f"{t['name']} ({t['id']})" for t in templates.values()]
            template_ids = list(templates.keys())
            
            self.template_combo['values'] = template_names
            self.template_combo.set(template_names[0])  # Set first template as default
            
            # Store template mapping
            self.template_mapping = dict(zip(template_names, template_ids))
            
        except ImportError:
            # Fallback if template manager is not available
            self.template_combo['values'] = ['Modern Blue (modern_blue)']
            self.template_combo.set('Modern Blue (modern_blue)')
            self.template_mapping = {'Modern Blue (modern_blue)': 'modern_blue'}
    
    def get_selected_template(self):
        """Get the currently selected template ID"""
        selected = self.template_var.get()
        return self.template_mapping.get(selected, 'modern_blue')
    
    def bind_events(self):
        """Bind UI events"""
        # Auto-save on tab change
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Template change event
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_changed)
        
    def on_template_changed(self, event):
        """Handle template change events"""
        selected_template = self.get_selected_template()
        print(f"Template changed to: {selected_template}")
        # Update template preview
        self.update_template_preview()
    
    def update_template_preview(self):
        """Update the template preview with current selection"""
        try:
            from utils.template_manager import get_template_manager
            template_manager = get_template_manager()
            
            selected_template = self.get_selected_template()
            template = template_manager.get_template(selected_template)
            
            if template:
                # Update description
                description = template.get('description', 'No description available')
                self.template_description.config(text=description)
                
                # Update features
                features = template.get('features', [])
                features_text = "Features: " + ", ".join(features) if features else "No features listed"
                self.template_features.config(text=features_text)
                
                # Update preview text
                preview_text = f"""TEMPLATE PREVIEW: {template.get('name', selected_template)}
{'='*50}

COLORS:
Primary: {template.get('colors', {}).get('primary', 'N/A')}
Secondary: {template.get('colors', {}).get('secondary', 'N/A')}
Background: {template.get('colors', {}).get('background', 'N/A')}
Text: {template.get('colors', {}).get('text', 'N/A')}
Accent: {template.get('colors', {}).get('accent', 'N/A')}

FONTS:
Header: {template.get('fonts', {}).get('header', 'N/A')}
Body: {template.get('fonts', {}).get('body', 'N/A')}
Accent: {template.get('fonts', {}).get('accent', 'N/A')}

SPACING:
Header Margin: {template.get('spacing', {}).get('header_margin', 'N/A')}px
Section Margin: {template.get('spacing', {}).get('section_margin', 'N/A')}px
Item Padding: {template.get('spacing', {}).get('item_padding', 'N/A')}px

FEATURES:
{chr(10).join(f"• {feature}" for feature in template.get('features', []))}
"""
                
                self.template_preview_text.delete(1.0, tk.END)
                self.template_preview_text.insert(1.0, preview_text)
                
        except ImportError:
            self.template_description.config(text="Template manager not available")
            self.template_features.config(text="")
            self.template_preview_text.delete(1.0, tk.END)
            self.template_preview_text.insert(1.0, "Template preview not available")
    
    def generate_template_sample(self):
        """Generate a sample PDF using the current template"""
        try:
            from utils.template_manager import get_template_manager
            from core.invoice_generator import generate_invoice
            
            template_manager = get_template_manager()
            selected_template = self.get_selected_template()
            
            # Get sample data
            sample_data = template_manager.get_template_preview_data()
            
            # Generate sample PDF
            output_path = f"output/invoices/sample_{selected_template}.pdf"
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generate PDF with selected template
            pdf_path = generate_invoice(sample_data, output_path, selected_template)
            
            if pdf_path and os.path.exists(pdf_path):
                messagebox.showinfo("Success", f"Sample PDF generated successfully!\n\nFile: {pdf_path}")
                
                # Open the generated PDF
                if messagebox.askyesno("Open PDF", "Would you like to open the generated sample PDF?"):
                    os.startfile(pdf_path) if os.name == 'nt' else subprocess.run(['xdg-open', pdf_path])
            else:
                self.show_error("Sample PDF Generation Error",
                              "Failed to generate sample PDF: No output file created",
                              context=f"Template: {selected_template}\nOutput Path: {output_path}")
                
        except Exception as e:
            self.show_error("Sample PDF Generation Error",
                          f"Failed to generate sample PDF: {str(e)}",
                          exception=e,
                          context=f"Template: {selected_template}\nOutput Path: {output_path}")
        
    def on_tab_changed(self, event):
        """Handle tab change events"""
        # Auto-save data when switching tabs
        self.collect_data_from_ui()
        
    def new_invoice(self):
        """Create a new invoice"""
        if messagebox.askyesno("New Invoice", "Are you sure you want to create a new invoice? All unsaved changes will be lost."):
            self.invoice_data = self.get_default_invoice_data()
            self.current_file = None
            self.load_data_to_ui()
            self.status_bar.config(text="New invoice created")
            
    def open_yaml(self):
        """Open a YAML file"""
        # Set default directory to output/invoices folder
        initial_dir = os.path.join(os.getcwd(), 'output', 'invoices')
        if not os.path.exists(initial_dir):
            initial_dir = os.getcwd()
            
        file_path = filedialog.askopenfilename(
            title="Open YAML File",
            initialdir=initial_dir,
            filetypes=[("YAML files", "*.yaml"), ("YAML files", "*.yml"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.invoice_data = yaml.safe_load(file)
                self.current_file = file_path
                self.load_data_to_ui()
                self.status_bar.config(text=f"Opened: {os.path.basename(file_path)}")
            except Exception as e:
                self.show_error("File Open Error",
                              f"Failed to open YAML file: {str(e)}",
                              exception=e,
                              context=f"File Path: {file_path}")
                
    def save_yaml(self):
        """Save current data to YAML file"""
        self.collect_data_from_ui()
        
        if not self.current_file:
            # Set default directory to output/invoices folder
            initial_dir = os.path.join(os.getcwd(), 'output', 'invoices')
            if not os.path.exists(initial_dir):
                initial_dir = os.getcwd()
                
            file_path = filedialog.asksaveasfilename(
                title="Save YAML File",
                initialdir=initial_dir,
                defaultextension=".yaml",
                filetypes=[("YAML files", "*.yaml"), ("YAML files", "*.yml"), ("All files", "*.*")]
            )
            if file_path:
                self.current_file = file_path
            else:
                return
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                yaml.dump(self.invoice_data, file, default_flow_style=False, sort_keys=False)
            self.status_bar.config(text=f"Saved: {os.path.basename(self.current_file)}")
        except Exception as e:
            self.show_error("File Save Error",
                          f"Failed to save YAML file: {str(e)}",
                          exception=e,
                          context=f"File Path: {self.current_file}")
            
    def generate_pdf(self):
        """Generate PDF invoice with comprehensive error handling"""
        self.collect_data_from_ui()
        
        if not self.current_file:
            messagebox.showwarning("Warning", "Please save the YAML file first before generating PDF.")
            return
        
        # Save current data
        try:
            self.save_yaml()
        except Exception as e:
            self.show_error("Save Error", 
                          f"Failed to save YAML file before generating PDF: {str(e)}",
                          exception=e,
                          context=f"File: {self.current_file}")
            return
        
        # Generate PDF using the core invoice generator
        output_pdf = None
        pdf_path = None
        
        try:
            # Import the generate_invoice function
            from core.invoice_generator import generate_invoice
            
            # Generate PDF in the same directory as the YAML file
            output_pdf = self.current_file.rsplit('.', 1)[0] + '.pdf'
            
            # Validate output path
            output_dir = os.path.dirname(output_pdf)
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    raise Exception(f"Cannot create output directory '{output_dir}': {str(e)}")
            
            # Check write permissions
            if os.path.exists(output_dir) and not os.access(output_dir, os.W_OK):
                raise Exception(f"No write permission for directory: {output_dir}")
            
            # Load the YAML data first
            try:
                with open(self.current_file, 'r', encoding='utf-8') as file:
                    invoice_data = yaml.safe_load(file)
                if not invoice_data:
                    raise Exception("YAML file is empty or invalid")
            except yaml.YAMLError as e:
                raise Exception(f"Invalid YAML format in file: {str(e)}")
            except Exception as e:
                raise Exception(f"Failed to read YAML file: {str(e)}")
            
            # Validate invoice data structure
            required_fields = ['invoice', 'company', 'client', 'items']
            for field in required_fields:
                if field not in invoice_data:
                    raise Exception(f"Missing required field in YAML: '{field}'")
            
            # Get selected template
            selected_template = self.get_selected_template()
            
            # Generate PDF using the imported function with selected template
            pdf_path = generate_invoice(invoice_data, output_pdf, selected_template)
            
            # Validate PDF was created
            if not pdf_path:
                raise Exception("PDF generation function returned None. Check console/logs for details.")
            
            if not os.path.exists(pdf_path):
                raise Exception(f"PDF file was not created at expected path: {pdf_path}")
            
            # Check file size (should be > 0)
            file_size = os.path.getsize(pdf_path)
            if file_size == 0:
                raise Exception(f"PDF file was created but is empty (0 bytes): {pdf_path}")
            
            # Success!
            messagebox.showinfo("Success", 
                              f"PDF invoice generated successfully!\n\n"
                              f"File: {pdf_path}\n"
                              f"Size: {file_size:,} bytes")
            self.status_bar.config(text=f"PDF generated: {os.path.basename(pdf_path)}")
            
            # Open the generated PDF
            if messagebox.askyesno("Open PDF", "Would you like to open the generated PDF?"):
                try:
                    if os.name == 'nt':
                        os.startfile(pdf_path)
                    else:
                        subprocess.run(['xdg-open', pdf_path], check=False)
                except Exception as e:
                    self.show_error("Open PDF Error",
                                  f"PDF was generated successfully but could not be opened: {str(e)}",
                                  exception=e,
                                  context=f"PDF Path: {pdf_path}")
                
        except ImportError as e:
            self.show_error("Import Error",
                          f"Failed to import invoice generator module.\n\n"
                          f"Please ensure the application is properly installed and all dependencies are available.",
                          exception=e,
                          context=f"Module: core.invoice_generator")
        except Exception as e:
            error_context = f"Output Path: {output_pdf}\nYAML File: {self.current_file}\nTemplate: {self.get_selected_template()}"
            self.show_error("PDF Generation Error",
                          f"Failed to generate PDF invoice.\n\n"
                          f"Error: {str(e)}",
                          exception=e,
                          context=error_context)
            
    def update_preview(self):
        """Update the preview tab"""
        self.collect_data_from_ui()
        
        preview_text = f"""INVOICE PREVIEW
{'='*50}

INVOICE: {self.invoice_data['invoice']['number']}
Date: {self.invoice_data['invoice']['date']}
Due Date: {self.invoice_data['invoice']['due_date']}
Month: {self.invoice_data['invoice']['month']}

FROM:
{self.invoice_data['company']['name']}
{self.invoice_data['company'].get('address1', '')}
{self.invoice_data['company'].get('address2', '')}
{self.invoice_data['company']['city']}, {self.invoice_data['company']['state']} {self.invoice_data['company']['zip']}
{self.invoice_data['company']['country']}
Email: {self.invoice_data['company']['email']}
Phone: {self.invoice_data['company']['phone']}

BILL TO:
{self.invoice_data['client']['name']}
{self.invoice_data['client']['address']}
{self.invoice_data['client']['city']}, {self.invoice_data['client']['state']} {self.invoice_data['client']['zip']}
{self.invoice_data['client']['country']}
Email: {self.invoice_data['client']['email']}

ITEMS:
"""
        
        # Add items
        subtotal = 0
        for i, item in enumerate(self.invoice_data['items'], 1):
            amount = item['quantity'] * item['rate']
            subtotal += amount
            preview_text += f"{i}. {item.get('name', '')} - {item.get('description', '')}\n"
            preview_text += f"   Quantity: {item['quantity']} x ${item['rate']:.2f} = ${amount:.2f}\n\n"
        
        # Add totals
        tax = subtotal * self.invoice_data['tax_rate']
        total = subtotal + tax
        
        preview_text += f"""
TOTALS:
Subtotal: ${subtotal:.2f}
Tax ({self.invoice_data['tax_rate']*100:.1f}%): ${tax:.2f}
Total: ${total:.2f}

Notes: {self.invoice_data.get('notes', '')}

Terms: {self.invoice_data.get('terms', '')}
"""
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, preview_text)
        
    def set_today_date(self):
        """Set today's date"""
        today = datetime.now()
        self.invoice_date_var.set(today.strftime('%Y-%m-%d'))
        
    def set_due_date(self):
        """Set due date to 30 days from today"""
        today = datetime.now()
        due_date = today + timedelta(days=30)
        self.due_date_var.set(due_date.strftime('%Y-%m-%d'))
        
    def auto_generate_number(self):
        """Auto-generate invoice number"""
        today = datetime.now()
        self.invoice_number_var.set(f"INV-{today.strftime('%Y%m%d')}-001")
        
    def add_item(self):
        """Add a new item"""
        try:
            quantity = float(self.item_quantity_var.get())
            rate = float(self.item_rate_var.get())
        except ValueError as e:
            self.show_error("Validation Error",
                          "Please enter valid numbers for quantity and rate.",
                          exception=e,
                          context=f"Quantity: '{self.item_quantity_var.get()}', Rate: '{self.item_rate_var.get()}'")
            return
        
        if not self.item_name_var.get().strip():
            self.show_error("Validation Error",
                          "Please enter an item name.",
                          context="Item name field is empty")
            return
        
        new_item = {
            'name': self.item_name_var.get().strip(),
            'description': self.item_description_var.get().strip(),
            'quantity': quantity,
            'rate': rate
        }
        
        self.invoice_data['items'].append(new_item)
        self.refresh_items_tree()
        self.clear_item_form()
        
    def update_item(self):
        """Update selected item"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to update.")
            return
        
        try:
            quantity = float(self.item_quantity_var.get())
            rate = float(self.item_rate_var.get())
        except ValueError as e:
            self.show_error("Validation Error",
                          "Please enter valid numbers for quantity and rate.",
                          exception=e,
                          context=f"Quantity: '{self.item_quantity_var.get()}', Rate: '{self.item_rate_var.get()}'")
            return
        
        # Find and update the item
        item_index = self.items_tree.index(selection[0])
        self.invoice_data['items'][item_index] = {
            'name': self.item_name_var.get().strip(),
            'description': self.item_description_var.get().strip(),
            'quantity': quantity,
            'rate': rate
        }
        
        self.refresh_items_tree()
        self.clear_item_form()
        
    def delete_item(self):
        """Delete selected item"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            item_index = self.items_tree.index(selection[0])
            del self.invoice_data['items'][item_index]
            self.refresh_items_tree()
            self.clear_item_form()
            
    def clear_item_form(self):
        """Clear the item form"""
        self.item_name_var.set('')
        self.item_description_var.set('')
        self.item_quantity_var.set('')
        self.item_rate_var.set('')
        
    def on_item_select(self, event):
        """Handle item selection"""
        selection = self.items_tree.selection()
        if selection:
            item_index = self.items_tree.index(selection[0])
            item = self.invoice_data['items'][item_index]
            
            self.item_name_var.set(item.get('name', ''))
            self.item_description_var.set(item.get('description', ''))
            self.item_quantity_var.set(str(item['quantity']))
            self.item_rate_var.set(str(item['rate']))
            
    def load_standard_terms(self):
        """Load standard terms and conditions"""
        standard_terms = """Payment is due within 30 days of invoice date.
Late payments may incur additional charges.
All work is guaranteed to meet specifications.
Changes to scope must be approved in writing."""
        
        self.terms_text.delete(1.0, tk.END)
        self.terms_text.insert(1.0, standard_terms)
        
    def load_payment_details(self):
        """Load payment details template"""
        payment_details = """Payment Details:
NAME: SYED MUHAMMAD MAAZ
Bank Name: BANK ALFALAH
Bank Country: PAKISTAN
IBAN Number: PK24ALFH0740001009144194"""
        
        self.terms_text.delete(1.0, tk.END)
        self.terms_text.insert(1.0, payment_details)
        
    def clear_notes_terms(self):
        """Clear notes and terms"""
        self.notes_text.delete(1.0, tk.END)
        self.terms_text.delete(1.0, tk.END)
    
    def show_error_details(self, title, error_message, exception=None, context=None):
        """Show detailed error dialog with stack trace and copy functionality"""
        # Create error dialog window
        error_window = tk.Toplevel(self.root)
        error_window.title(f"Error: {title}")
        error_window.geometry("700x600")
        error_window.configure(bg=self.colors['background'])
        error_window.transient(self.root)
        error_window.grab_set()
        
        # Main container
        main_frame = ttk.Frame(error_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.configure(style='TFrame')
        
        # Error icon and title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, 
                               text=f"❌ {title}",
                               font=('Segoe UI', 14, 'bold'),
                               foreground=self.colors['error'],
                               background=self.colors['background'])
        title_label.pack(anchor=tk.W)
        
        # Error message
        msg_label = ttk.Label(main_frame,
                             text=error_message,
                             wraplength=650,
                             justify=tk.LEFT,
                             font=('Segoe UI', 10),
                             foreground=self.colors['text'],
                             background=self.colors['background'])
        msg_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Context information if provided
        if context:
            context_label = ttk.Label(main_frame,
                                     text=f"Context: {context}",
                                     wraplength=650,
                                     justify=tk.LEFT,
                                     font=('Segoe UI', 9),
                                     foreground=self.colors['text_secondary'],
                                     background=self.colors['background'])
            context_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Stack trace section
        trace_frame = ttk.LabelFrame(main_frame, text="Error Details & Stack Trace", padding=10)
        trace_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrolled text for stack trace
        trace_text = scrolledtext.ScrolledText(trace_frame, 
                                              height=15,
                                              width=80,
                                              bg=self.colors['background_light'],
                                              fg=self.colors['text'],
                                              insertbackground=self.colors['highlight'],
                                              font=('Consolas', 9),
                                              wrap=tk.WORD)
        trace_text.pack(fill=tk.BOTH, expand=True)
        
        # Build trace content
        trace_content = []
        if exception:
            trace_content.append(f"Exception Type: {type(exception).__name__}\n")
            trace_content.append(f"Exception Message: {str(exception)}\n")
            trace_content.append("\n" + "="*70 + "\n")
            trace_content.append("Full Stack Trace:\n")
            trace_content.append("="*70 + "\n")
            trace_content.append(traceback.format_exc())
        else:
            trace_content.append("No exception details available.\n")
            trace_content.append("This error occurred without a Python exception.\n")
        
        trace_text.insert(1.0, ''.join(trace_content))
        trace_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def copy_to_clipboard():
            """Copy error details to clipboard"""
            self.root.clipboard_clear()
            full_text = f"{title}\n\n{error_message}\n\n"
            if context:
                full_text += f"Context: {context}\n\n"
            full_text += trace_text.get(1.0, tk.END)
            self.root.clipboard_append(full_text)
            messagebox.showinfo("Copied", "Error details copied to clipboard!")
        
        ttk.Button(button_frame, 
                  text="📋 Copy to Clipboard",
                  command=copy_to_clipboard,
                  style='Modern.Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Close",
                  command=error_window.destroy,
                  style='Modern.Primary.TButton').pack(side=tk.RIGHT)
        
        # Center the window
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (error_window.winfo_width() // 2)
        y = (error_window.winfo_screenheight() // 2) - (error_window.winfo_height() // 2)
        error_window.geometry(f"+{x}+{y}")
    
    def show_error(self, title, error_message, exception=None, context=None):
        """Show error with option to view details"""
        # Show details dialog directly
        self.show_error_details(title, error_message, exception, context)

def main():
    root = tk.Tk()
    app = InvoiceArtisanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
