#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GIMP Python-Fu Watermark/Overlay Script

Automates watermarking or overlaying a graphic onto one or more images.
Features:
- Select watermark/overlay image and target folder
- Custom positioning (corners, center, tiled)
- Scale and opacity controls
- Batch processing
- Output to new folder with updated filenames
"""

from gimpfu import *
import os

# Position constants
POSITION_TOP_LEFT = 0
POSITION_TOP_RIGHT = 1
POSITION_BOTTOM_LEFT = 2
POSITION_BOTTOM_RIGHT = 3
POSITION_CENTER = 4
POSITION_TILED = 5

def apply_watermark_single(image, watermark_path, position, scale, opacity, x_offset, y_offset):
    """
    Apply watermark to a single image.
    
    Args:
        image: The GIMP image to apply watermark to
        watermark_path: Path to watermark image file
        position: Position constant for watermark placement
        scale: Scale factor for watermark (percentage)
        opacity: Opacity of watermark (0-100)
        x_offset: X offset from position anchor (pixels)
        y_offset: Y offset from position anchor (pixels)
    
    Returns:
        The modified image
    """
    # Load watermark image
    watermark_img = pdb.gimp_file_load(watermark_path, watermark_path)
    watermark_layer = pdb.gimp_image_get_active_layer(watermark_img)
    
    # Calculate scaled dimensions
    orig_width = watermark_layer.width
    orig_height = watermark_layer.height
    new_width = int(orig_width * scale / 100.0)
    new_height = int(orig_height * scale / 100.0)
    
    # Scale watermark if needed
    if scale != 100:
        pdb.gimp_layer_scale(watermark_layer, new_width, new_height, False)
    
    # Copy watermark layer to target image
    watermark_copy = pdb.gimp_layer_new_from_drawable(watermark_layer, image)
    pdb.gimp_image_insert_layer(image, watermark_copy, None, 0)
    
    # Set opacity
    pdb.gimp_layer_set_opacity(watermark_copy, opacity)
    
    # Calculate position based on mode
    img_width = image.width
    img_height = image.height
    wm_width = watermark_copy.width
    wm_height = watermark_copy.height
    
    if position == POSITION_TOP_LEFT:
        x = x_offset
        y = y_offset
    elif position == POSITION_TOP_RIGHT:
        x = img_width - wm_width - x_offset
        y = y_offset
    elif position == POSITION_BOTTOM_LEFT:
        x = x_offset
        y = img_height - wm_height - y_offset
    elif position == POSITION_BOTTOM_RIGHT:
        x = img_width - wm_width - x_offset
        y = img_height - wm_height - y_offset
    elif position == POSITION_CENTER:
        x = (img_width - wm_width) / 2 + x_offset
        y = (img_height - wm_height) / 2 + y_offset
    elif position == POSITION_TILED:
        # For tiled mode, we'll create multiple copies
        pdb.gimp_image_remove_layer(image, watermark_copy)
        
        # Calculate number of tiles needed
        tiles_x = int((img_width / wm_width) + 1)
        tiles_y = int((img_height / wm_height) + 1)
        
        for ty in range(tiles_y):
            for tx in range(tiles_x):
                tile_copy = pdb.gimp_layer_new_from_drawable(watermark_layer, image)
                pdb.gimp_image_insert_layer(image, tile_copy, None, 0)
                pdb.gimp_layer_set_opacity(tile_copy, opacity)
                tile_x = tx * wm_width + x_offset
                tile_y = ty * wm_height + y_offset
                pdb.gimp_layer_set_offsets(tile_copy, tile_x, tile_y)
        
        pdb.gimp_image_delete(watermark_img)
        return image
    
    # Set position for non-tiled modes
    pdb.gimp_layer_set_offsets(watermark_copy, int(x), int(y))
    
    # Clean up watermark image
    pdb.gimp_image_delete(watermark_img)
    
    return image


def watermark_batch_process(watermark_path, input_folder, output_folder, 
                            position, scale, opacity, x_offset, y_offset,
                            output_prefix, output_suffix):
    """
    Batch process all images in a folder with watermark.
    
    Args:
        watermark_path: Path to watermark image file
        input_folder: Folder containing images to watermark
        output_folder: Folder to save watermarked images
        position: Position constant for watermark placement
        scale: Scale factor for watermark (percentage)
        opacity: Opacity of watermark (0-100)
        x_offset: X offset from position anchor (pixels)
        y_offset: Y offset from position anchor (pixels)
        output_prefix: Prefix to add to output filenames
        output_suffix: Suffix to add to output filenames (before extension)
    """
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of image files
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff')
    image_files = [f for f in os.listdir(input_folder) 
                   if f.lower().endswith(supported_formats)]
    
    if not image_files:
        pdb.gimp_message("No supported image files found in input folder.")
        return
    
    # Process each image
    for filename in image_files:
        input_path = os.path.join(input_folder, filename)
        
        # Load image
        img = pdb.gimp_file_load(input_path, input_path)
        
        # Apply watermark
        img = apply_watermark_single(img, watermark_path, position, scale, 
                                     opacity, x_offset, y_offset)
        
        # Flatten image for export
        layer = pdb.gimp_image_flatten(img)
        
        # Generate output filename
        name, ext = os.path.splitext(filename)
        output_filename = output_prefix + name + output_suffix + ext
        output_path = os.path.join(output_folder, output_filename)
        
        # Save image
        pdb.gimp_file_save(img, layer, output_path, output_filename)
        
        # Clean up
        pdb.gimp_image_delete(img)
    
    pdb.gimp_message("Batch watermarking complete! Processed %d images." % len(image_files))


def watermark_current_image(image, drawable, watermark_path, position, 
                            scale, opacity, x_offset, y_offset):
    """
    Apply watermark to the currently open image in GIMP.
    
    Args:
        image: The current GIMP image
        drawable: The current drawable/layer
        watermark_path: Path to watermark image file
        position: Position constant for watermark placement
        scale: Scale factor for watermark (percentage, 1-200)
        opacity: Opacity of watermark (0-100)
        x_offset: X offset from position anchor (pixels)
        y_offset: Y offset from position anchor (pixels)
    """
    pdb.gimp_image_undo_group_start(image)
    
    try:
        apply_watermark_single(image, watermark_path, position, scale, 
                              opacity, x_offset, y_offset)
        pdb.gimp_displays_flush()
    except Exception as e:
        pdb.gimp_message("Error applying watermark: %s" % str(e))
    finally:
        pdb.gimp_image_undo_group_end(image)


# Register the current image watermark function
register(
    "python_fu_watermark_current_image",
    "Apply Watermark to Current Image",
    "Applies a watermark or overlay graphic to the current image with customizable positioning, scale, and opacity.",
    "Sean Bud",
    "Sean Bud",
    "2024",
    "<Image>/Filters/Watermark/Apply Watermark...",
    "RGB*, GRAY*",
    [
        (PF_FILE, "watermark_path", "Watermark Image:", ""),
        (PF_OPTION, "position", "Position:", POSITION_BOTTOM_RIGHT,
         ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", "Tiled"]),
        (PF_SLIDER, "scale", "Scale (%):", 100, (1, 200, 1)),
        (PF_SLIDER, "opacity", "Opacity (%):", 50, (0, 100, 1)),
        (PF_INT, "x_offset", "X Offset (pixels):", 10),
        (PF_INT, "y_offset", "Y Offset (pixels):", 10),
    ],
    [],
    watermark_current_image
)

# Register the batch processing function
register(
    "python_fu_watermark_batch_process",
    "Batch Watermark Images",
    "Batch processes all images in a folder with watermark overlay, saving to a new folder with updated filenames.",
    "Sean Bud",
    "Sean Bud",
    "2024",
    "<Image>/Filters/Watermark/Batch Process...",
    "",
    [
        (PF_FILE, "watermark_path", "Watermark Image:", ""),
        (PF_DIRNAME, "input_folder", "Input Folder:", ""),
        (PF_DIRNAME, "output_folder", "Output Folder:", ""),
        (PF_OPTION, "position", "Position:", POSITION_BOTTOM_RIGHT,
         ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", "Tiled"]),
        (PF_SLIDER, "scale", "Scale (%):", 100, (1, 200, 1)),
        (PF_SLIDER, "opacity", "Opacity (%):", 50, (0, 100, 1)),
        (PF_INT, "x_offset", "X Offset (pixels):", 10),
        (PF_INT, "y_offset", "Y Offset (pixels):", 10),
        (PF_STRING, "output_prefix", "Output Filename Prefix:", ""),
        (PF_STRING, "output_suffix", "Output Filename Suffix:", "_watermarked"),
    ],
    [],
    watermark_batch_process
)

main()
