# InvoiceArtisan Template System

## Overview

The InvoiceArtisan Template System allows users to select from multiple pre-designed invoice templates, each with unique styling, colors, fonts, and spacing. Users can choose a template that matches their brand or preference without needing design skills.

## Features

- **6 Professional Templates**: Modern Blue, Classic Black, Corporate Green, Elegant Purple, Minimal Gray, and Warm Orange
- **Template Selection**: Easy dropdown selection in the GUI
- **Live Preview**: See template details and features before generating
- **Sample Generation**: Generate sample PDFs to preview templates
- **Consistent Styling**: Each template maintains professional appearance while offering distinct visual identity

## Available Templates

### 1. Modern Blue
- **Theme**: Professional blue theme with clean lines and modern typography
- **Colors**: Dark blue headers, blue accents, light blue backgrounds
- **Fonts**: Helvetica family
- **Features**: Alternating row colors, rounded corners, subtle shadows

### 2. Classic Black
- **Theme**: Traditional black and white theme with elegant typography
- **Colors**: Pure black, dark gray accents, white backgrounds
- **Fonts**: Times family (serif)
- **Features**: Traditional layout, serif typography, formal appearance

### 3. Corporate Green
- **Theme**: Business green theme with professional appearance
- **Colors**: Dark green headers, medium green accents, light green backgrounds
- **Fonts**: Arial family
- **Features**: Professional green theme, business-focused design

### 4. Elegant Purple
- **Theme**: Sophisticated purple theme with luxury feel
- **Colors**: Dark purple headers, medium purple accents, light purple backgrounds
- **Fonts**: Georgia family (serif)
- **Features**: Luxury appearance, sophisticated colors, premium typography

### 5. Minimal Gray
- **Theme**: Clean minimal theme with subtle gray tones
- **Colors**: Dark gray headers, medium gray accents, off-white backgrounds
- **Fonts**: Roboto family
- **Features**: Minimal design, clean typography, subtle colors

### 6. Warm Orange
- **Theme**: Friendly orange theme with warm, approachable feel
- **Colors**: Dark orange headers, medium orange accents, light orange backgrounds
- **Fonts**: Verdana family
- **Features**: Warm colors, friendly appearance, approachable design

## How to Use

### 1. Select Template in GUI
- Open the InvoiceArtisan application
- Use the template dropdown in the header to select your preferred template
- The selection applies to all future PDF generations

### 2. Preview Template
- Go to the "Template" tab
- See detailed information about the selected template
- View colors, fonts, spacing, and features
- Generate a sample PDF to preview the final result

### 3. Generate Invoice
- Fill in your invoice data in the appropriate tabs
- Click "Generate PDF Invoice" in the Preview & Generate tab
- The PDF will be generated using your selected template

## Template Configuration

Templates are defined in `assets/templates/template_configs.yaml`. Each template includes:

```yaml
template_id:
  name: "Template Display Name"
  description: "Detailed description of the template"
  colors:
    primary: "#hex_color"      # Main header color
    secondary: "#hex_color"    # Accent color
    background: "#hex_color"   # Background color
    text: "#hex_color"         # Text color
    accent: "#hex_color"       # Highlight color
    light_gray: "#hex_color"   # Light row color
    medium_gray: "#hex_color"  # Border color
  fonts:
    header: "FontName-Bold"    # Header font
    body: "FontName"           # Body font
    accent: "FontName-Bold"    # Accent font
  spacing:
    header_margin: 15          # Header spacing
    section_margin: 15         # Section spacing
    item_padding: 6            # Item row padding
  features:
    - feature1                 # Template features list
    - feature2
```

## Adding New Templates

### 1. Create Template Configuration
Add a new template section to `assets/templates/template_configs.yaml`:

```yaml
my_custom_template:
  name: "My Custom Template"
  description: "A custom template with my brand colors"
  colors:
    primary: "#1a1a1a"
    secondary: "#ff6b6b"
    background: "#ffffff"
    text: "#333333"
    accent: "#4ecdc4"
    light_gray: "#f8f9fa"
    medium_gray: "#dee2e6"
  fonts:
    header: "Arial-Bold"
    body: "Arial"
    accent: "Arial-Bold"
  spacing:
    header_margin: 18
    section_margin: 18
    item_padding: 7
  features:
    - custom_colors
    - modern_typography
    - balanced_spacing
```

### 2. Test the Template
Run the test script to verify your template works:

```bash
python test_templates.py
```

### 3. Use in Application
The new template will automatically appear in the template dropdown.

## Technical Details

### Template Manager
- **File**: `src/utils/template_manager.py`
- **Class**: `TemplateManager`
- **Functions**: Load, validate, and manage templates

### Integration Points
- **GUI**: Template selection in header and dedicated Template tab
- **PDF Generation**: `generate_invoice()` function accepts template parameter
- **Fallback**: Default styling if template manager unavailable

### File Structure
```
assets/
  templates/
    template_configs.yaml      # Template definitions
src/
  utils/
    template_manager.py        # Template management
  core/
    invoice_generator.py       # PDF generation with templates
  gui/
    main_window.py            # GUI with template selection
```

## Testing

### Run Template Tests
```bash
python test_templates.py
```

### Test Individual Components
```python
# Test template manager
from src.utils.template_manager import get_template_manager
tm = get_template_manager()
templates = tm.get_available_templates()

# Test PDF generation with template
from src.core.invoice_generator import generate_invoice
pdf_path = generate_invoice(data, output_path, "modern_blue")
```

## Troubleshooting

### Common Issues

1. **Template Not Loading**
   - Check `assets/templates/template_configs.yaml` exists
   - Verify YAML syntax is correct
   - Check file permissions

2. **Template Not Applying**
   - Ensure template ID is correct
   - Check template validation passes
   - Verify template has required sections

3. **Font Issues**
   - Ensure fonts are available on the system
   - Use fallback fonts if specific fonts unavailable
   - Check font names match system font names

### Debug Mode
Enable debug output by setting environment variable:
```bash
export INVOICE_ARTISAN_DEBUG=1
```

## Future Enhancements

- **Template Categories**: Group templates by style (Professional, Creative, Minimal)
- **Custom Color Schemes**: Allow users to modify template colors
- **Template Import/Export**: Share custom templates between users
- **Live Preview**: Real-time preview of template changes
- **Template Ratings**: User feedback and ratings for templates

## Support

For template-related issues:
1. Check the template configuration file
2. Run the test script
3. Verify template validation
4. Check console output for error messages

## Contributing

To contribute new templates:
1. Follow the template configuration format
2. Test with the test script
3. Ensure consistent styling and professional appearance
4. Document any special features or requirements
