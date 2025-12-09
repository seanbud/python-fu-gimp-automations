# my-gimp-automation

Automate common GIMP workflows for sprite and image processing using Python-fu scripts.

## Overview

**my-gimp-automation** is a collection of Python-fu scripts to automate repetitive GIMP tasks, especially for sprite and image manipulation. The scripts streamline processes such as cropping, thresholding, blurring, inverting, and batch exporting layers, simplifying the creation of "shadow sprite" assets and similar workflows.

## Features

- **Crop and Export:** Automatically crops images to a centered square region and exports processed layers.
- **Layer Threshold and Blur:** Applies a threshold (making the layer black) and iterative blur to each layer, then exports the results as shadow images.
- **Invert Layers:** Batch inverts all layers in the current image.
- **Batch Export:** Saves all layers or selected layers to a dedicated `shadow_sprites` subfolder.
- **Batch Resize and Export:** Process multiple images from a directory with customizable resize options and format conversion.
- **Automatic Output Directory Creation:** Output directories for exported layers are created automatically if they don’t exist.

## Scripts

Located in `python-fu/`:
- `crop-threshold-blur-export.py`: Crops the image, applies threshold and blur to each layer, and saves results as `_shadow.png` files in `shadow_sprites/`.
- `export_shadow_sprites.py`: Functions for inverting all layers, exporting all layers, or exporting a specific layer by index.
- `batch_resize_export.py`: Batch resize and export multiple images from a directory with customizable dimensions, scaling, and format options.

## Usage

1. **Install GIMP with Python support** (`gimpfu`).
2. Copy the scripts from the `python-fu` directory into your GIMP plug-ins folder.
   - **Windows:** `C:\Users\[Username]\AppData\Roaming\GIMP\2.10\plug-ins\`
   - **Linux:** `~/.config/GIMP/2.10/plug-ins/`
   - **macOS:** `~/Library/Application Support/GIMP/2.10/plug-ins/`
3. Restart GIMP to load the new scripts.
4. Access the scripts from GIMP's menu system.

### Example: Batch Resize and Export

The `batch_resize_export.py` script provides a powerful way to process multiple images at once:

1. **Launch the script:**
   - Open GIMP
   - Go to **Filters → Batch Process → Batch Resize and Export...**

2. **Configure the settings:**
   - **Input Directory:** Select the folder containing your images
   - **Output Directory:** Choose where to save the processed images
   - **Resize Mode:** Choose between:
     - **By Dimensions:** Specify exact width and height in pixels
     - **By Percentage:** Scale images by a percentage (e.g., 50% for half size)
   - **Maintain Aspect Ratio:** Keep original proportions (only for dimension mode)
   - **Output Format:** Choose PNG, JPEG, BMP, or GIF
   - **Filename Suffix:** Add a suffix to distinguish processed files (e.g., "_resized")

3. **Example Scenario 1 - Create Thumbnails:**
   - Input: A folder of high-resolution photos (e.g., 4000x3000 px)
   - Resize Mode: By Dimensions
   - Width: 200, Height: 200
   - Maintain Aspect Ratio: Yes
   - Output Format: JPEG
   - Suffix: "_thumb"
   - Result: Creates thumbnails like `photo1_thumb.jpg`, `photo2_thumb.jpg`

4. **Example Scenario 2 - Reduce File Size:**
   - Input: A folder of images for web use
   - Resize Mode: By Percentage
   - Percentage: 50
   - Output Format: PNG
   - Suffix: "_web"
   - Result: Images scaled to 50% of original size for faster web loading

5. **Progress and Error Reporting:**
   - A progress bar shows processing status
   - After completion, a summary displays:
     - Total files processed
     - Number of successful conversions
     - Any errors encountered with details

### Example: Shadow Sprites

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
