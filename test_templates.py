#!/usr/bin/env python3
"""
Test script for the InvoiceArtisan template system
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_template_manager():
    """Test the template manager functionality"""
    print("🧪 Testing Template Manager...")
    
    try:
        from utils.template_manager import get_template_manager
        template_manager = get_template_manager()
        
        print("✅ Template manager imported successfully")
        
        # Test getting available templates
        templates = template_manager.get_available_templates()
        print(f"✅ Found {len(templates)} templates:")
        for template_id, template_data in templates.items():
            print(f"   - {template_data['name']} ({template_id})")
        
        # Test getting a specific template
        modern_blue = template_manager.get_template('modern_blue')
        if modern_blue:
            print("✅ Modern Blue template loaded successfully")
            print(f"   Colors: {list(modern_blue.get('colors', {}).keys())}")
            print(f"   Fonts: {list(modern_blue.get('fonts', {}).keys())}")
        else:
            print("❌ Failed to load Modern Blue template")
        
        # Test template validation
        for template_id in templates.keys():
            if template_manager.validate_template(template_id):
                print(f"✅ Template '{template_id}' is valid")
            else:
                print(f"❌ Template '{template_id}' is invalid")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing template manager: {e}")
        return False

def test_invoice_generator_with_templates():
    """Test the invoice generator with different templates"""
    print("\n🧪 Testing Invoice Generator with Templates...")
    
    try:
        from core.invoice_generator import generate_invoice
        from utils.template_manager import get_template_manager
        
        template_manager = get_template_manager()
        
        # Get sample data
        sample_data = template_manager.get_template_preview_data()
        print("✅ Sample data created successfully")
        
        # Test with different templates
        test_templates = ['modern_blue', 'classic_black', 'corporate_green']
        
        for template_id in test_templates:
            try:
                output_path = f"test_invoice_{template_id}.pdf"
                print(f"   Testing template: {template_id}")
                
                # Generate PDF with template
                pdf_path = generate_invoice(sample_data, output_path, template_id)
                
                if pdf_path and os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path) / 1024  # KB
                    print(f"   ✅ Generated: {pdf_path} ({file_size:.1f} KB)")
                    
                    # Clean up test file
                    os.remove(pdf_path)
                    print(f"   🧹 Cleaned up test file")
                else:
                    print(f"   ❌ Failed to generate PDF with template {template_id}")
                    
            except Exception as e:
                print(f"   ❌ Error with template {template_id}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing invoice generator: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 InvoiceArtisan Template System Test")
    print("=" * 50)
    
    success = True
    
    # Test template manager
    if not test_template_manager():
        success = False
    
    # Test invoice generator with templates
    if not test_invoice_generator_with_templates():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Template system is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
