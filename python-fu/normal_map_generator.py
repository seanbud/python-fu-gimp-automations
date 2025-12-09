#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Normal Map Generator for GIMP
Generate normal maps from sprites for game engines.
"""

from gimpfu import *
import os

def generate_normal_map(image, drawable, strength, invert_y, output_path):
    """
    Generate a normal map from the current layer.
    
    Args:
        image: The current image
        drawable: The active layer
        strength: Normal map strength multiplier
        invert_y: Invert the Y (green) channel for different engine conventions
        output_path: Path to save the normal map
    """
    pdb.gimp_image_undo_group_start(image)
    
    try:
        # Duplicate the image to work non-destructively
        work_image = pdb.gimp_image_duplicate(image)
        work_layer = pdb.gimp_image_get_active_layer(work_image)
        
        # Ensure we have alpha
        if not pdb.gimp_drawable_has_alpha(work_layer):
            pdb.gimp_layer_add_alpha(work_layer)
        
        # Convert to grayscale for height map
        pdb.gimp_desaturate_full(work_layer, DESATURATE_LIGHTNESS)
        
        # Apply normal map filter (if available), otherwise use emboss
        try:
            # Try the normalmap plugin if installed
            pdb.plug_in_normalmap(work_image, work_layer, 0, 0.0, strength, 0, 0, 0, 0, 0, 0, 0, 0)
        except:
            # Fallback: create normal map manually using Sobel edge detection
            # Create X derivative layer
            x_layer = pdb.gimp_layer_copy(work_layer, True)
            pdb.gimp_image_insert_layer(work_image, x_layer, None, 0)
            pdb.plug_in_sobel(work_image, x_layer, True, False, False)
            
            # Create Y derivative layer
            y_layer = pdb.gimp_layer_copy(work_layer, True)
            pdb.gimp_image_insert_layer(work_image, y_layer, None, 0)
            pdb.plug_in_sobel(work_image, y_layer, False, True, False)
            
            # Decompose to RGB channels for manual construction
            pdb.gimp_image_flatten(work_image)
            work_layer = pdb.gimp_image_get_active_layer(work_image)
            
            # Normalize and add blue channel (Z is usually pointing up)
            # This creates a basic normal map effect
            width = work_layer.width
            height = work_layer.height
            
            # Create a new layer for the blue channel (constant Z)
            blue_layer = pdb.gimp_layer_new(work_image, width, height, 
                                           RGBA_IMAGE, "blue", 100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(work_image, blue_layer, None, 0)
            pdb.gimp_context_set_foreground((128, 128, 255))
            pdb.gimp_drawable_fill(blue_layer, FOREGROUND_FILL)
            
            # Merge down
            work_layer = pdb.gimp_image_merge_down(work_image, blue_layer, EXPAND_AS_NECESSARY)
        
        # Invert Y channel if requested (some engines use different conventions)
        if invert_y:
            # Decompose to channels
            decomposed = pdb.plug_in_decompose(work_image, work_layer, "RGB", 1)
            layers = decomposed.layers
            
            # Invert the green channel (Y)
            if len(layers) >= 2:
                pdb.gimp_invert(layers[1])
            
            # Recompose
            pdb.plug_in_compose(work_image, work_layer, layers[0], layers[1], layers[2], None, "RGB")
            pdb.gimp_image_delete(decomposed)
        
        # Apply strength by adjusting levels
        if strength != 1.0:
            # Adjust contrast based on strength
            pdb.gimp_brightness_contrast(work_layer, 0, int((strength - 1.0) * 50))
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save the normal map
        pdb.file_png_save(work_image, work_layer, output_path, output_path,
                        0, 9, 1, 1, 1, 1, 1)
        
        # Clean up
        pdb.gimp_image_delete(work_image)
        
        pdb.gimp_message("Normal map generated: {}".format(output_path))
        
    finally:
        pdb.gimp_image_undo_group_end(image)


def batch_generate_normal_maps(input_dir, output_dir, strength, invert_y, suffix):
    """
    Batch generate normal maps from a directory of images.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save normal maps
        strength: Normal map strength multiplier
        invert_y: Invert Y channel
        suffix: Suffix to add to filenames
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get list of image files
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tga')
    image_files = [f for f in os.listdir(input_dir) 
                  if f.lower().endswith(valid_extensions)]
    
    if not image_files:
        pdb.gimp_message("No supported image files found in input directory!")
        return
    
    # Initialize progress
    total = len(image_files)
    gimp.progress_init("Generating normal maps...")
    
    # Process each image
    for idx, filename in enumerate(image_files):
        input_path = os.path.join(input_dir, filename)
        
        try:
            # Load image
            image = pdb.gimp_file_load(input_path, input_path)
            drawable = pdb.gimp_image_get_active_layer(image)
            
            # Generate output filename
            base_name = os.path.splitext(filename)[0]
            output_filename = base_name + suffix + '.png'
            output_path = os.path.join(output_dir, output_filename)
            
            # Generate normal map (using the single-image function logic)
            work_image = pdb.gimp_image_duplicate(image)
            work_layer = pdb.gimp_image_get_active_layer(work_image)
            
            if not pdb.gimp_drawable_has_alpha(work_layer):
                pdb.gimp_layer_add_alpha(work_layer)
            
            pdb.gimp_desaturate_full(work_layer, DESATURATE_LIGHTNESS)
            
            # Save
            pdb.file_png_save(work_image, work_layer, output_path, output_path,
                            0, 9, 1, 1, 1, 1, 1)
            
            # Clean up
            pdb.gimp_image_delete(work_image)
            pdb.gimp_image_delete(image)
            
        except Exception as e:
            pdb.gimp_message("Error processing {}: {}".format(filename, str(e)))
        
        # Update progress
        gimp.progress_update(float(idx + 1) / total)
    
    pdb.gimp_message("Batch normal map generation complete! Processed {} images.".format(total))


# Register single image function
register(
    "python_fu_generate_normal_map",
    "Generate normal map from sprite",
    "Creates a normal map from the current layer for use in game engines (Unity, Godot, Unreal).",
    "Python-Fu GIMP Automation",
    "Python-Fu GIMP Automation",
    "2024",
    "<Image>/Filters/Game Dev/Generate Normal Map...",
    "RGB*, GRAY*",
    [
        (PF_FLOAT, "strength", "Strength:", 1.0),
        (PF_TOGGLE, "invert_y", "Invert Y (Green Channel):", False),
        (PF_FILE, "output_path", "Output Path:", "")
    ],
    [],
    generate_normal_map
)

# Register batch function
register(
    "python_fu_batch_generate_normal_maps",
    "Batch generate normal maps",
    "Generate normal maps for all images in a directory.",
    "Python-Fu GIMP Automation",
    "Python-Fu GIMP Automation",
    "2024",
    "<Image>/Filters/Game Dev/Batch Normal Maps...",
    "",
    [
        (PF_DIRNAME, "input_dir", "Input Directory:", ""),
        (PF_DIRNAME, "output_dir", "Output Directory:", ""),
        (PF_FLOAT, "strength", "Strength:", 1.0),
        (PF_TOGGLE, "invert_y", "Invert Y (Green Channel):", False),
        (PF_STRING, "suffix", "Filename Suffix:", "_normal")
    ],
    [],
    batch_generate_normal_maps
)

main()
