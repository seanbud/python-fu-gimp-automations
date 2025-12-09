# my-gimp-automation

Automate common GIMP workflows for sprite and image processing using Python-fu scripts.

## Overview

**my-gimp-automation** is a collection of Python-fu scripts to automate repetitive GIMP tasks, especially for sprite and image manipulation. The scripts streamline processes such as cropping, thresholding, blurring, inverting, batch exporting layers, and applying watermarks or overlays to images, simplifying the creation of "shadow sprite" assets and other image processing workflows.

## Features

- **Crop and Export:** Automatically crops images to a centered square region and exports processed layers.
- **Layer Threshold and Blur:** Applies a threshold (making the layer black) and iterative blur to each layer, then exports the results as shadow images.
- **Invert Layers:** Batch inverts all layers in the current image.
- **Batch Export:** Saves all layers or selected layers to a dedicated `shadow_sprites` subfolder.
- **Watermark/Overlay:** Apply watermarks or overlay graphics to images with customizable positioning, scale, and opacity.
- **Batch Watermarking:** Process entire folders of images with watermarks automatically.
- **Automatic Output Directory Creation:** Output directories for exported layers are created automatically if they don't exist.

## Scripts

Located in `python-fu/`:
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

#### Apply Watermark to Current Image

Located in **Filters → Watermark → Apply Watermark...**

1. Open an image in GIMP
2. Go to **Filters → Watermark → Apply Watermark...**
3. Configure the settings:
   - **Watermark Image:** Select your watermark/overlay image file (PNG with transparency recommended)
   - **Position:** Choose placement (Top Left, Top Right, Bottom Left, Bottom Right, Center, or Tiled)
   - **Scale (%):** Adjust watermark size (1-200%)
   - **Opacity (%):** Set watermark transparency (0-100%)
   - **X/Y Offset:** Fine-tune position with pixel offsets
4. Click **OK** to apply the watermark

**Features:**
- **Corners/Center positioning:** Precisely place watermarks in standard positions
- **Tiled mode:** Repeat watermark across entire image for security/branding
- **Scale control:** Resize watermark from 1% to 200% of original size
- **Opacity control:** From fully transparent (0%) to fully opaque (100%)
- **Pixel-perfect positioning:** Fine-tune with X/Y offset controls

#### Batch Process Multiple Images

Located in **Filters → Watermark → Batch Process...**

1. Open GIMP (no need to open an image first)
2. Go to **Filters → Watermark → Batch Process...**
3. Configure the settings:
   - **Watermark Image:** Select your watermark file
   - **Input Folder:** Select folder containing images to watermark
   - **Output Folder:** Select where to save watermarked images
   - **Position, Scale, Opacity, Offsets:** Same as single image mode
   - **Output Filename Prefix:** Optional prefix for output files
   - **Output Filename Suffix:** Suffix added before extension (default: "_watermarked")
4. Click **OK** to process all images

**Supported formats:** PNG, JPG, JPEG, BMP, GIF, TIF, TIFF

**Output:** Watermarked images are saved to the output folder with updated filenames. Original files remain untouched.

### Shadow Sprites Scripts

#### crop-threshold-blur-export.py

1. Open an image with multiple layers in GIMP
2. Run the script from the Python-fu console
3. The script will:
   - Crop the image to a centered square (60% of original width)
   - Convert each layer to black (threshold)
   - Apply blur 15 times to create shadow effect
   - Export each layer as `<layername>_shadow.png` in `shadow_sprites/` subfolder

#### export_shadow_sprites.py

Run from the Python-fu console:
- `InvertAll()` - Inverts all layers in the current image
- `ExportAll()` - Exports all layers to `shadow_sprites/` subfolder
- `ExportLayer(i)` - Exports a specific layer by index

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
