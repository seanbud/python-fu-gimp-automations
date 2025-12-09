#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tileset Slicer for GIMP
Slice a tileset image into individual sprite tiles for game development.
"""

from gimpfu import *
import os

def slice_tileset(image, drawable, tile_width, tile_height, margin, spacing, output_dir, filename_prefix):
    """
    Slice a tileset into individual tiles.
    
    Args:
        image: The current image
        drawable: The active layer
        tile_width: Width of each tile in pixels
        tile_height: Height of each tile in pixels
        margin: Margin around the entire tileset
        spacing: Spacing between tiles
        output_dir: Directory to save tiles
        filename_prefix: Prefix for output filenames
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Calculate number of tiles
    img_width = image.width
    img_height = image.height
    
    # Account for margins and spacing
    usable_width = img_width - (2 * margin)
    usable_height = img_height - (2 * margin)
    
    cols = (usable_width + spacing) // (tile_width + spacing)
    rows = (usable_height + spacing) // (tile_height + spacing)
    
    if cols <= 0 or rows <= 0:
        pdb.gimp_message("Error: Tile dimensions too large for image size!")
        return
    
    # Initialize progress
    total_tiles = cols * rows
    gimp.progress_init("Slicing tileset...")
    
    tile_index = 0
    
    # Extract each tile
    for row in range(rows):
        for col in range(cols):
            # Calculate position
            x = margin + col * (tile_width + spacing)
            y = margin + row * (tile_height + spacing)
            
            # Create a new image for this tile
            tile_image = pdb.gimp_image_new(tile_width, tile_height, RGB)
            tile_layer = pdb.gimp_layer_new(tile_image, tile_width, tile_height, 
                                           RGBA_IMAGE, "tile", 100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(tile_image, tile_layer, None, 0)
            
            # Copy the tile region
            pdb.gimp_image_select_rectangle(image, CHANNEL_OP_REPLACE, x, y, tile_width, tile_height)
            pdb.gimp_edit_copy(drawable)
            
            # Paste into new image
            floating = pdb.gimp_edit_paste(tile_layer, False)
            pdb.gimp_floating_sel_anchor(floating)
            
            # Clear selection
            pdb.gimp_selection_none(image)
            
            # Save the tile
            output_filename = "{}{:04d}.png".format(filename_prefix, tile_index)
            output_path = os.path.join(output_dir, output_filename)
            pdb.file_png_save(tile_image, tile_layer, output_path, output_path,
                            0, 9, 1, 1, 1, 1, 1)
            
            # Clean up
            pdb.gimp_image_delete(tile_image)
            
            # Update progress
            tile_index += 1
            gimp.progress_update(float(tile_index) / total_tiles)
    
    pdb.gimp_message("Slicing complete! Exported {} tiles to {}".format(total_tiles, output_dir))

# Register the plugin
register(
    "python_fu_tileset_slicer",
    "Slice tileset into individual sprites",
    "Extracts individual tiles from a tileset image for game development. Configure grid dimensions, margins, and spacing.",
    "Python-Fu GIMP Automation",
    "Python-Fu GIMP Automation",
    "2024",
    "<Image>/Filters/Game Dev/Slice Tileset...",
    "RGB*, GRAY*",
    [
        (PF_INT, "tile_width", "Tile Width (px):", 32),
        (PF_INT, "tile_height", "Tile Height (px):", 32),
        (PF_INT, "margin", "Margin (px):", 0),
        (PF_INT, "spacing", "Spacing (px):", 0),
        (PF_DIRNAME, "output_dir", "Output Directory:", ""),
        (PF_STRING, "filename_prefix", "Filename Prefix:", "tile_")
    ],
    [],
    slice_tileset
)

main()
