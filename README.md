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
- **Automatic Output Directory Creation:** Output directories for exported layers are created automatically if they don’t exist.

## Scripts

Located in `python-fu/`:
- `background_removal.py`: Automatically removes backgrounds from images using fuzzy select or edge detection. Includes batch processing for multiple images.
- `crop-threshold-blur-export.py`: Crops the image, applies threshold and blur to each layer, and saves results as `_shadow.png` files in `shadow_sprites/`.
- `export_shadow_sprites.py`: Functions for inverting all layers, exporting all layers, or exporting a specific layer by index.

## Usage

1. **Install GIMP with Python support** (`gimpfu`).
2. Copy the scripts from the `python-fu` directory into your GIMP plug-ins folder.
3. Open your image in GIMP and ensure your layers are named for intended processing.
4. Run the script(s) from the GIMP Python-fu console or assign them to menu actions as needed.

### Example

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

## Requirements

- GIMP with Python-fu enabled.
- Python standard library (os module).

## Contributing

Pull requests and suggestions are welcome!
