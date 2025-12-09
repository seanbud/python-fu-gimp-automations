# Background Removal - Quick Start Guide

## Installation

1. **Locate your GIMP plug-ins folder:**
   - **Linux**: `~/.config/GIMP/2.10/plug-ins/` or `~/.gimp-2.8/plug-ins/`
   - **Windows**: `C:\Users\[Username]\AppData\Roaming\GIMP\2.10\plug-ins\`
   - **macOS**: `~/Library/Application Support/GIMP/2.10/plug-ins/`

2. **Copy the script:**
   ```bash
   cp python-fu/background_removal.py [your-gimp-plugins-folder]/
   ```

3. **Make it executable (Linux/macOS only):**
   ```bash
   chmod +x [your-gimp-plugins-folder]/background_removal.py
   ```

4. **Restart GIMP** to load the new script.

## Quick Start

### Method 1: Fuzzy Select (Color-Based Removal)

**Best for:** Images with solid color or simple gradient backgrounds (white, green screen, studio backgrounds)

**Steps:**
1. Open your image in GIMP
2. Navigate to: `Filters > Background Removal > Fuzzy Select...`
3. A dialog will appear with these options:

   - **Selection X Position (%)**: Default is 5 (top-left corner)
     - Set to 5 to sample from top-left
     - Set to 95 to sample from top-right
     - Set to 50 for center
   
   - **Selection Y Position (%)**: Default is 5 (top-left corner)
     - Similar to X position, controls vertical sampling point
   
   - **Selection Tolerance**: Default is 15
     - Low (5-15): Only selects very similar colors
     - Medium (15-40): Selects similar color ranges
     - High (40-100): Selects broader color ranges
   
   - **Edge Feathering (px)**: Default is 2
     - 0: Hard, sharp edges
     - 2-5: Slightly soft edges (recommended)
     - 10+: Very soft, blended edges
   
   - **Preview Only**: Default is False
     - Check this to see the selection without removing it
     - Useful for testing tolerance settings

4. Click "OK" to execute

**Tips:**
- Start with "Preview Only" checked to verify your selection
- Adjust the X/Y position to sample the background color you want to remove
- If selection is too small, increase tolerance
- If selection includes subject, decrease tolerance

### Method 2: Edge Detection (Shape-Based Removal)

**Best for:** Images with complex/varied backgrounds where the subject has clear, defined edges

**Steps:**
1. Open your image in GIMP
2. Navigate to: `Filters > Background Removal > Edge Detection...`
3. A dialog will appear with these options:

   - **Edge Detection Sensitivity**: Default is 2.0
     - Low (1.0-2.0): Detects only strong edges (recommended for most images)
     - Medium (2.0-5.0): More sensitive edge detection
     - High (5.0-10.0): Very sensitive, may detect texture as edges
   
   - **Edge Threshold**: Default is 30
     - Low (0-30): Includes weaker edges
     - Medium (30-100): Moderate edge strength required
     - High (100-255): Only very strong edges
   
   - **Grow/Shrink Selection (px)**: Default is 2
     - Positive values (1-10): Expand selection outward (include more)
     - 0: No adjustment
     - Negative values (-10 to -1): Contract selection inward (exclude more)
   
   - **Preview Only**: Default is False
     - Check this to see the selection without removing it

4. Click "OK" to execute

**Tips:**
- Use lower sensitivity values (1.5-2.5) for cleaner results
- Positive grow/shrink helps include edge pixels for complete subject
- If background remains, decrease threshold or increase sensitivity
- If subject edges are removed, increase threshold or decrease sensitivity

### Method 3: Batch Processing

**Best for:** Processing multiple images with similar backgrounds

**Steps:**
1. Open GIMP (you can open any image or create a new one)
2. Navigate to: `Filters > Background Removal > Batch Process...`
3. A dialog will appear with these options:

   - **Input Directory**: Browse to folder containing your images
   - **Output Directory**: Browse to where you want processed images saved
   - **Removal Method**: Choose "Fuzzy Select" or "Edge Detection"
   - Then set parameters for your chosen method (same as above)

4. Click "OK" to start batch processing

**Output:**
- Processed images are saved with "_no_bg" suffix
- Format is PNG to preserve transparency
- Original files are not modified
- Failed images are skipped with error messages

**Tips:**
- Test parameters on a single image first using Method 1 or 2
- Use the same parameters for batch processing
- All images in input folder will be processed
- Supported formats: JPG, PNG, BMP, GIF, TIF

## Common Issues & Solutions

### Issue: Nothing is selected
**Solution:** 
- Fuzzy: Increase tolerance or change X/Y sampling position
- Edge: Decrease threshold or increase sensitivity

### Issue: Too much selected (includes subject)
**Solution:** 
- Fuzzy: Decrease tolerance
- Edge: Increase threshold or decrease sensitivity

### Issue: Rough/jagged edges
**Solution:** 
- Fuzzy: Increase edge feathering
- Edge: Use positive grow/shrink value

### Issue: Background remains around edges
**Solution:** 
- Fuzzy: Increase tolerance slightly
- Edge: Use positive grow/shrink value (2-5 pixels)

### Issue: Subject partially removed
**Solution:** 
- Fuzzy: Position X/Y away from subject, decrease tolerance
- Edge: Increase threshold, use negative grow/shrink value

### Issue: Script doesn't appear in menu
**Solution:**
- Ensure script is in correct plug-ins folder
- Ensure script is executable (Linux/macOS)
- Restart GIMP completely
- Check GIMP error console for messages

## Parameter Cheat Sheet

### Fuzzy Select Quick Settings

**White background (product photo):**
- X: 5%, Y: 5%
- Tolerance: 15-25
- Feather: 2

**Green screen:**
- X: 50%, Y: 50%
- Tolerance: 40-60
- Feather: 2-3

**Gradient background:**
- X: 5%, Y: 5%
- Tolerance: 30-50
- Feather: 3-5

### Edge Detection Quick Settings

**Clean subject (logo, illustration):**
- Sensitivity: 1.5-2.0
- Threshold: 30-50
- Grow/Shrink: 1-2

**Detailed subject (person, product):**
- Sensitivity: 2.0-3.0
- Threshold: 20-40
- Grow/Shrink: 2-4

**Complex/textured subject:**
- Sensitivity: 2.5-4.0
- Threshold: 15-30
- Grow/Shrink: 3-5

## Advanced Usage

### Combining Methods

For best results on difficult images:
1. Use Edge Detection method first with preview enabled
2. Note which areas are well-selected
3. Use Fuzzy Select on remaining background areas
4. Use GIMP's selection tools to manually refine if needed

### Working with Layers

The script works on the active layer. To process multiple layers:
1. Select a layer in the Layers panel
2. Run the script
3. Repeat for each layer

### Undo

All operations support GIMP's undo (Ctrl+Z / Cmd+Z):
- Single undo removes the background removal
- You can undo and retry with different parameters

## Performance Notes

- **Processing Time**: Depends on image size and method
  - Fuzzy Select: Very fast (< 1 second)
  - Edge Detection: Moderate (2-5 seconds)
- **Batch Processing**: Processes images sequentially
  - Expect ~2-10 seconds per image depending on size
- **Memory**: Large images (> 4000x4000px) may require more RAM

## Next Steps

1. Practice with the provided examples in `examples/` folder
2. Start with preview mode enabled
3. Experiment with parameters on test images
4. Save your preferred settings for different image types
5. Use batch processing for production workflows

For more information, see:
- Main documentation: [README.md](../README.md)
- Detailed examples: [examples/README.md](README.md)
