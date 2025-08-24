#!/usr/bin/env python3
"""
Template Manager for InvoiceArtisan
Handles loading and applying different invoice templates
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional

class TemplateManager:
    """Manages invoice templates and their styling configurations"""
    
    def __init__(self, config_path: str = None):
        """Initialize the template manager"""
        if config_path is None:
            # Default to the templates directory
            current_dir = Path(__file__).parent.parent.parent
            config_path = current_dir / "assets" / "templates" / "template_configs.yaml"
        
        self.config_path = Path(config_path)
        self.templates = {}
        self.current_template = "modern_blue"  # Default template
        self.load_templates()
    
    def load_templates(self) -> bool:
        """Load all available templates from the configuration file"""
        try:
            if not self.config_path.exists():
                print(f"Warning: Template config file not found at {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            
            if config and 'templates' in config:
                self.templates = config['templates']
                print(f"Loaded {len(self.templates)} templates: {list(self.templates.keys())}")
                return True
            else:
                print("Warning: No templates found in config file")
                return False
                
        except Exception as e:
            print(f"Error loading templates: {e}")
            return False
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available templates with their metadata"""
        return {
            template_id: {
                'id': template_id,
                'name': template_data.get('name', template_id),
                'description': template_data.get('description', ''),
                'colors': template_data.get('colors', {}),
                'fonts': template_data.get('fonts', {}),
                'spacing': template_data.get('spacing', {}),
                'features': template_data.get('features', [])
            }
            for template_id, template_data in self.templates.items()
        }
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific template by ID"""
        if template_id in self.templates:
            return self.templates[template_id]
        else:
            print(f"Warning: Template '{template_id}' not found, using default")
            return self.templates.get(self.current_template, {})
    
    def set_current_template(self, template_id: str) -> bool:
        """Set the current active template"""
        if template_id in self.templates:
            self.current_template = template_id
            print(f"Template changed to: {self.templates[template_id].get('name', template_id)}")
            return True
        else:
            print(f"Error: Template '{template_id}' not found")
            return False
    
    def get_current_template(self) -> Dict[str, Any]:
        """Get the current active template"""
        return self.get_template(self.current_template)
    
    def get_template_colors(self, template_id: str = None) -> Dict[str, str]:
        """Get colors for a specific template"""
        template = self.get_template(template_id or self.current_template)
        return template.get('colors', {})
    
    def get_template_fonts(self, template_id: str = None) -> Dict[str, str]:
        """Get fonts for a specific template"""
        template = self.get_template(template_id or self.current_template)
        return template.get('fonts', {})
    
    def get_template_spacing(self, template_id: str = None) -> Dict[str, int]:
        """Get spacing settings for a specific template"""
        template = self.get_template(template_id or self.current_template)
        return template.get('spacing', {})
    
    def get_template_features(self, template_id: str = None) -> list:
        """Get features for a specific template"""
        template = self.get_template(template_id or self.current_template)
        return template.get('features', [])
    
    def validate_template(self, template_id: str) -> bool:
        """Validate that a template has all required fields"""
        template = self.templates.get(template_id)
        if not template:
            return False
        
        required_sections = ['colors', 'fonts', 'spacing']
        for section in required_sections:
            if section not in template:
                print(f"Warning: Template '{template_id}' missing '{section}' section")
                return False
        
        return True
    
    def get_template_preview_data(self) -> Dict[str, Any]:
        """Get sample data for template previews"""
        return {
            'invoice': {
                'number': 'INV-2025-001',
                'date': '2025-01-15',
                'due_date': '2025-02-15',
                'month': 'January'
            },
            'company': {
                'name': 'Sample Company',
                'address1': '123 Business Street',
                'address2': 'Suite 100',
                'city': 'Business City',
                'state': 'BC',
                'zip': '12345',
                'country': 'United States',
                'email': 'billing@sample.com',
                'phone': '+1-555-0123'
            },
            'client': {
                'name': 'Sample Client',
                'address': '456 Client Avenue',
                'city': 'Client City',
                'state': 'CC',
                'zip': '67890',
                'country': 'United States',
                'email': 'accounts@client.com'
            },
            'items': [
                {
                    'name': 'Sample Service',
                    'description': 'This is a sample service description',
                    'quantity': 2.0,
                    'rate': 100.0
                }
            ],
            'tax_rate': 0.08,
            'notes': 'Thank you for your business!',
            'terms': 'Payment due within 30 days.'
        }
    
    def export_template_config(self, output_path: str) -> bool:
        """Export the current template configuration to a file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.templates, file, default_flow_style=False, sort_keys=False)
            print(f"Template configuration exported to: {output_path}")
            return True
        except Exception as e:
            print(f"Error exporting template config: {e}")
            return False
    
    def import_template_config(self, config_path: str) -> bool:
        """Import template configuration from a file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                new_config = yaml.safe_load(file)
            
            if new_config and 'templates' in new_config:
                # Merge with existing templates
                self.templates.update(new_config['templates'])
                print(f"Imported {len(new_config['templates'])} templates")
                return True
            else:
                print("Error: Invalid template configuration file")
                return False
                
        except Exception as e:
            print(f"Error importing template config: {e}")
            return False

# Global template manager instance
template_manager = TemplateManager()

def get_template_manager() -> TemplateManager:
    """Get the global template manager instance"""
    return template_manager
