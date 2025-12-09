# my-gimp-automation

Automate common GIMP workflows for sprite and image processing using Python-fu scripts.

## Overview

**my-gimp-automation** is a collection of Python-fu scripts to automate repetitive GIMP tasks, especially for sprite and image manipulation. The scripts streamline processes such as background removal, cropping, thresholding, blurring, inverting, and batch exporting layers, simplifying the creation of assets with transparent backgrounds, "shadow sprite" assets, and similar workflows.

## Features

- **Background Removal:** Automatically remove backgrounds from images using fuzzy selection or edge detection methods.
  - Two removal methods: Fuzzy Select (color-based) and Edge Detection (edge-based)
  - Adjustable parameters for fine-tuned control
  - Preview mode to verify selection before removing
  - Batch processing support for multiple images
- **Crop and Export:** Automatically crops images to a centered square region and exports processed layers.
- **Layer Threshold and Blur:** Applies a threshold (making the layer black) and iterative blur to each layer, then exports the results as shadow images.
- **Invert Layers:** Batch inverts all layers in the current image.
- **Batch Export:** Saves all layers or selected layers to a dedicated `shadow_sprites` subfolder.
- **Watermark/Overlay:** Apply watermarks or overlay graphics to images with customizable positioning, scale, and opacity.
- **Batch Watermarking:** Process entire folders of images with watermarks automatically.
- **Automatic Output Directory Creation:** Output directories for exported layers are created automatically if they don't exist.

## Scripts

Located in `python-fu/`:
- `background_removal.py`: Automatically removes backgrounds from images using fuzzy select or edge detection. Includes batch processing for multiple images.
- `crop-threshold-blur-export.py`: Crops the image, applies threshold and blur to each layer, and saves results as `_shadow.png` files in `shadow_sprites/`.
- `export_shadow_sprites.py`: Functions for inverting all layers, exporting all layers, or exporting a specific layer by index.
- `watermark_overlay.py`: Apply watermarks or overlay graphics to images with full customization options for positioning, scaling, opacity, and batch processing.

## Setup

### 1. Install GIMP with Python Support

Ensure you have GIMP installed with Python-fu support enabled. Most GIMP distributions include this by default.

- **Windows/Mac:** Download from [gimp.org](https://www.gimp.org/downloads/)
- **Linux:** Install via package manager (e.g., `sudo apt-get install gimp`)

### 2. Locate Your GIMP Plug-ins Folder

The plug-ins folder location varies by operating system:

- **Windows:** `C:\Users\<YourUsername>\AppData\Roaming\GIMP\2.10\plug-ins\`
- **Mac:** `~/Library/Application Support/GIMP/2.10/plug-ins/`
- **Linux:** `~/.config/GIMP/2.10/plug-ins/`

Alternatively, in GIMP go to **Edit → Preferences → Folders → Plug-ins** to see your plug-ins directories.

### 3. Install Scripts

Copy the desired scripts from the `python-fu/` directory into your GIMP plug-ins folder:

```bash
# Example for Linux/Mac
cp python-fu/watermark_overlay.py ~/.config/GIMP/2.10/plug-ins/
chmod +x ~/.config/GIMP/2.10/plug-ins/watermark_overlay.py
```

### 4. Restart GIMP

After copying the scripts, restart GIMP to load the new plug-ins.

## Usage

### Watermark/Overlay Script

The watermark script provides two main functions accessible from GIMP's menu system:

#### Background Removal

To remove backgrounds from images:

**Single Image - Fuzzy Select Method (Best for solid backgrounds):**
1. Open your image in GIMP
2. Go to **Filters > Background Removal > Fuzzy Select...**
3. Adjust parameters:
   - **Selection X/Y Position (%)**: Sample point for background color (default: top-left at 5%, 5%)
   - **Selection Tolerance**: How many similar colors to select (0-255, default: 15)
   - **Edge Feathering**: Smoothing for edges (0-50 pixels, default: 2)
   - **Preview Only**: Check to preview selection before removing
4. Click OK to apply

**Single Image - Edge Detection Method (Best for complex backgrounds):**
1. Open your image in GIMP
2. Go to **Filters > Background Removal > Edge Detection...**
3. Adjust parameters:
   - **Edge Detection Sensitivity**: Detection sensitivity (1.0-10.0, default: 2.0)
   - **Edge Threshold**: Minimum edge strength (0-255, default: 30)
   - **Grow/Shrink Selection**: Expand/contract selection (pixels, default: 2)
   - **Preview Only**: Check to preview selection before removing
4. Click OK to apply

**Batch Processing Multiple Images:**
1. Open GIMP (any image or create new)
2. Go to **Filters > Background Removal > Batch Process...**
3. Select input directory with images
4. Select output directory for processed images
5. Choose removal method (Fuzzy Select or Edge Detection)
6. Adjust method-specific parameters
7. Click OK to process all images

Processed images will be saved as PNG files with "_no_bg" suffix, preserving transparency.

For detailed examples and troubleshooting, see the [examples/README.md](examples/README.md) file.

#### Shadow Sprites

To batch export shadow sprites:
- Run `crop-threshold-blur-export.py` to process and export cropped, thresholded, blurred versions of each layer.
- Alternatively, use `export_shadow_sprites.py`:
  - Run `InvertAll()` to invert all layers.
  - Run `ExportAll()` to export all layers.

Exported files will be found in a `shadow_sprites` subfolder next to your original image.

## Sample Images

Sample images are provided in the `samples/` directory for testing and demonstration:

### Watermark Sample

**`samples/watermarks/sample_watermark.png`**
- A simple transparent watermark with white text and border
- 200x60 pixels
- Use this to test the watermark script functionality

### Input Images

**`samples/input/`** contains three sample images:
- `sample_image_1.png` - Blue gradient with geometric shapes (800x600)
- `sample_image_2.png` - Red gradient with geometric shapes (800x600)
- `sample_image_3.png` - Green gradient with geometric shapes (800x600)

### Testing the Watermark Script

**Single Image:**
1. Open `samples/input/sample_image_1.png` in GIMP
2. Go to **Filters → Watermark → Apply Watermark...**
3. Select `samples/watermarks/sample_watermark.png` as the watermark
4. Try different positions and settings

**Batch Processing:**
1. Open GIMP
2. Go to **Filters → Watermark → Batch Process...**
3. Set watermark to `samples/watermarks/sample_watermark.png`
4. Set input folder to `samples/input/`
5. Set output folder to `samples/output/`
6. Click OK to process all three sample images

### Creating Your Own Watermark

For best results:
- Use PNG format with transparency
- Keep dimensions reasonable (e.g., 200-400 pixels wide)
- Use white or light colors for visibility on dark images
- Use dark colors for visibility on light images
- Consider semi-transparent backgrounds
- Test on various image types before batch processing

Example watermark ideas:
- Copyright text: "© 2024 Your Name"
- Logo or brand mark
- Website URL or social media handle
- QR code linking to your portfolio
- Pattern overlay for texture effects

## Requirements

- GIMP 2.8 or higher with Python-fu enabled
- Python standard library (os module)
- For sample image generation: Python 3 with Pillow (optional)

## Contributing

Pull requests and suggestions are welcome! Please ensure your code follows the existing style and includes appropriate documentation.

## License

This project is open source. Feel free to use and modify these scripts for your own purposes.
