# Example Images

This directory is for storing example images that demonstrate the background removal functionality.

## Suggested Example Images

Place your example images here to demonstrate:

1. **Simple Background Example:**
   - `input_simple.jpg` or `input_simple.png` - Image with solid/simple background
   - `output_simple.png` - Result after fuzzy select processing
   
2. **Complex Background Example:**
   - `input_complex.jpg` or `input_complex.png` - Image with complex background
   - `output_complex.png` - Result after edge detection processing

3. **Batch Processing Example:**
   - `batch_input/` - Folder with multiple sample images
   - `batch_output/` - Folder with processed results

## Creating Your Own Examples

To create example images:

1. **Using Fuzzy Select Method:**
   ```
   - Open GIMP with an image that has a simple background
   - Go to Filters > Background Removal > Fuzzy Select...
   - Adjust parameters and click OK
   - Export as PNG to preserve transparency
   - Save as output_simple.png
   ```

2. **Using Edge Detection Method:**
   ```
   - Open GIMP with an image that has a complex background
   - Go to Filters > Background Removal > Edge Detection...
   - Adjust parameters and click OK
   - Export as PNG to preserve transparency
   - Save as output_complex.png
   ```

## Image Guidelines

- Use PNG format for output images to show transparency
- Keep file sizes reasonable (< 2MB recommended)
- Show before/after comparisons
- Include images that demonstrate different use cases:
  - Product photography (white background)
  - Portrait photography (complex background)
  - Green screen removal
  - Logo/icon isolation

## Note

Example images are optional but helpful for users to understand the script capabilities.
The repository structure supports them, but you can add your own examples as needed.
