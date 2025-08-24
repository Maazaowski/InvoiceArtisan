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

class InvoiceArtisanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InvoiceArtisan - Professional Invoice Generator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set theme colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#e74c3c',
            'success': '#27ae60',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff'
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
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure common styles
        style.configure('Header.TLabel', 
                       font=('Helvetica', 16, 'bold'), 
                       foreground=self.colors['primary'])
        
        style.configure('Section.TLabel', 
                       font=('Helvetica', 12, 'bold'), 
                       foreground=self.colors['secondary'])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white')
        
        style.configure('Primary.TButton',
                       background=self.colors['secondary'],
                       foreground='white')
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white')
        
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
                                  font=('Helvetica', 10),
                                  foreground=self.colors['secondary'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # File operations frame
        file_frame = ttk.Frame(header_frame)
        file_frame.pack(side=tk.RIGHT)
        
        # New button
        self.new_btn = ttk.Button(file_frame, 
                                 text="New Invoice", 
                                 command=self.new_invoice,
                                 style='Primary.TButton')
        self.new_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Open button
        self.open_btn = ttk.Button(file_frame, 
                                  text="Open YAML", 
                                  command=self.open_yaml)
        self.open_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Save button
        self.save_btn = ttk.Button(file_frame, 
                                  text="Save YAML", 
                                  command=self.save_yaml,
                                  style='Success.TButton')
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
        self.create_preview_tab()
        
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
        
        ttk.Button(actions_frame, text="Set Today's Date", 
                  command=self.set_today_date).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Set Due Date (+30 days)", 
                  command=self.set_due_date).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Auto-generate Invoice Number", 
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
        
        ttk.Button(buttons_frame, text="Add Item", 
                  command=self.add_item, style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Update Item", 
                  command=self.update_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Delete Item", 
                  command=self.delete_item, style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Clear Form", 
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
        
        self.generate_btn = ttk.Button(generate_frame, text="Generate PDF Invoice", 
                                      command=self.generate_pdf,
                                      style='Success.TButton')
        self.generate_btn.pack(side=tk.RIGHT)
        
        # Preview button
        self.preview_btn = ttk.Button(generate_frame, text="Update Preview", 
                                     command=self.update_preview)
        self.preview_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Label(self.main_container, text="Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W)
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
        
    def bind_events(self):
        """Bind UI events"""
        # Auto-save on tab change
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
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
        # Set default directory to invoices folder
        initial_dir = os.path.join(os.getcwd(), 'invoices')
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
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
                
    def save_yaml(self):
        """Save current data to YAML file"""
        self.collect_data_from_ui()
        
        if not self.current_file:
            # Set default directory to invoices folder
            initial_dir = os.path.join(os.getcwd(), 'invoices')
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
            with open(self.current_file, 'w') as file:
                yaml.dump(self.invoice_data, file, default_flow_style=False, sort_keys=False)
            self.status_bar.config(text=f"Saved: {os.path.basename(self.current_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            
    def generate_pdf(self):
        """Generate PDF invoice"""
        self.collect_data_from_ui()
        
        if not self.current_file:
            messagebox.showwarning("Warning", "Please save the YAML file first before generating PDF.")
            return
        
        # Save current data
        self.save_yaml()
        
        # Generate PDF using the existing invoice_generator.py
        try:
            # Generate PDF in the same directory as the YAML file
            output_pdf = self.current_file.rsplit('.', 1)[0] + '.pdf'
            
            # If the YAML is in the invoices folder, ensure PDF goes there too
            if 'invoices' in self.current_file:
                # Ensure the output directory exists
                output_dir = os.path.dirname(output_pdf)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            
            # Run invoice_generator.py as a subprocess
            result = subprocess.run([
                sys.executable, 'invoice_generator.py', self.current_file
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                messagebox.showinfo("Success", f"PDF invoice generated successfully!\n\nFile: {output_pdf}")
                self.status_bar.config(text=f"PDF generated: {os.path.basename(output_pdf)}")
                
                # Open the generated PDF
                if messagebox.askyesno("Open PDF", "Would you like to open the generated PDF?"):
                    os.startfile(output_pdf) if os.name == 'nt' else subprocess.run(['xdg-open', output_pdf])
            else:
                messagebox.showerror("Error", f"Failed to generate PDF:\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
            
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
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and rate.")
            return
        
        if not self.item_name_var.get().strip():
            messagebox.showerror("Error", "Please enter an item name.")
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
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and rate.")
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

def main():
    root = tk.Tk()
    app = InvoiceArtisanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
