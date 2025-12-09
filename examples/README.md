# Background Removal Examples

This directory contains example images demonstrating the background removal script functionality.

## Example Workflows

### Single Image Processing

#### Fuzzy Select Method
Best for images with solid or simple gradient backgrounds:

1. Open your image in GIMP
2. Go to **Filters > Background Removal > Fuzzy Select...**
3. Adjust parameters:
   - **Selection X/Y Position (%)**: Position where to sample background color (default: top-left corner at 5%, 5%)
   - **Selection Tolerance**: How similar colors to select (0-255, default: 15)
   - **Edge Feathering**: Smooth the edges (0-50 pixels, default: 2)
   - **Preview Only**: Check this to see selection before removing
4. Click OK to apply

**Tips:**
- Use Preview mode first to verify the selection
- Increase tolerance for backgrounds with color variations
- Increase feathering for softer edges
- Adjust X/Y position to sample the background color you want to remove

#### Edge Detection Method
Best for images with complex backgrounds where the subject has clear edges:

1. Open your image in GIMP
2. Go to **Filters > Background Removal > Edge Detection...**
3. Adjust parameters:
   - **Edge Detection Sensitivity**: How sensitive edge detection is (1.0-10.0, default: 2.0)
   - **Edge Threshold**: Threshold for identifying edges (0-255, default: 30)
   - **Grow/Shrink Selection**: Adjust selection size (pixels, default: 2)
   - **Preview Only**: Check this to see selection before removing
4. Click OK to apply

**Tips:**
- Lower edge sensitivity for cleaner edge detection
- Increase threshold to detect only strong edges
- Use positive grow/shrink values to expand selection and include edge pixels
- Use negative grow/shrink values to contract selection away from edges

### Batch Processing

Process multiple images at once:

1. Open GIMP (any image or create a new one)
2. Go to **Filters > Background Removal > Batch Process...**
3. Configure:
   - **Input Directory**: Folder containing your images
   - **Output Directory**: Where to save processed images
   - **Removal Method**: Choose "Fuzzy Select" or "Edge Detection"
   - Adjust method-specific parameters as needed
4. Click OK to process all images

**Output:**
- Processed images are saved as PNG files with "_no_bg" suffix
- Original files are preserved
- Transparency is maintained in output files

## Expected Results

### Fuzzy Select Method
- **Input**: Image with solid or gradient background
- **Output**: Subject isolated with transparent background
- **Best For**: Product photos, logos, simple backgrounds

### Edge Detection Method
- **Input**: Image with complex background and clear subject edges
- **Output**: Subject extracted based on edge detection
- **Best For**: Photos with detailed backgrounds, natural scenes

## Sample Images

Place your sample images here to demonstrate:
- `input_simple.png` - Image with simple background (for fuzzy select demo)
- `output_simple.png` - Result after fuzzy select processing
- `input_complex.png` - Image with complex background (for edge detection demo)
- `output_complex.png` - Result after edge detection processing

## Troubleshooting

### Issue: Too much or too little selected
- **Solution**: Adjust tolerance (fuzzy) or edge threshold (edge detection)

### Issue: Edges are too sharp
- **Solution**: Increase edge feathering in fuzzy select method

### Issue: Selection includes parts of the subject
- **Solution**: 
  - Fuzzy: Decrease tolerance or change X/Y sampling position
  - Edge: Increase edge sensitivity or adjust threshold

### Issue: Background not fully removed
- **Solution**: 
  - Fuzzy: Increase tolerance or use multiple passes
  - Edge: Decrease threshold or use negative grow/shrink

### Issue: Batch processing fails
- **Solution**: Ensure input directory contains valid image files (jpg, png, bmp, gif, tif)
