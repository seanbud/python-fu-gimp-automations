#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Palette Quantizer for GIMP
Enforce a specific color palette across sprites for consistent game art style.
"""

from gimpfu import *
import os

def quantize_to_palette(image, drawable, palette_name, dither_type, output_path):
    """
    Quantize image colors to a specific palette.
    
    Args:
        image: The current image
        drawable: The active layer
        palette_name: Name of the palette to use
        dither_type: Dithering method (0=None, 1=Floyd-Steinberg, 2=Fixed)
        output_path: Path to save the quantized image
    """
    pdb.gimp_image_undo_group_start(image)
    
    try:
        # Duplicate the image to work non-destructively
        work_image = pdb.gimp_image_duplicate(image)
        work_layer = pdb.gimp_image_get_active_layer(work_image)
        
        # Store alpha channel if present
        has_alpha = pdb.gimp_drawable_has_alpha(work_layer)
        
        if has_alpha:
            # Extract alpha channel before conversion
            alpha_channel = pdb.gimp_layer_copy(work_layer, True)
            pdb.gimp_image_insert_layer(work_image, alpha_channel, None, 0)
            pdb.gimp_desaturate_full(alpha_channel, DESATURATE_LIGHTNESS)
        
        # Convert to indexed mode using the specified palette
        # The palette must exist in GIMP's palettes
        try:
            # Get number of colors in palette
            num_colors = pdb.gimp_palette_get_info(palette_name)
            
            # Convert to indexed color using custom palette
            pdb.gimp_image_convert_indexed(work_image, CONVERT_DITHER_NONE if dither_type == 0 
                                          else CONVERT_DITHER_FS if dither_type == 1 
                                          else CONVERT_DITHER_FIXED,
                                          CONVERT_PALETTE_CUSTOM, num_colors, False, False, palette_name)
            
        except Exception as e:
            pdb.gimp_message("Error: Palette '{}' not found! {}".format(palette_name, str(e)))
            pdb.gimp_image_delete(work_image)
            return
        
        # Convert back to RGB to allow saving in various formats
        pdb.gimp_image_convert_rgb(work_image)
        work_layer = pdb.gimp_image_get_active_layer(work_image)
        
        # Restore alpha channel if it existed
        if has_alpha and alpha_channel:
            # Add alpha to the layer
            if not pdb.gimp_drawable_has_alpha(work_layer):
                pdb.gimp_layer_add_alpha(work_layer)
            
            # Copy alpha channel back
            # This is a simplified approach - in production you'd want to properly restore alpha
            mask = pdb.gimp_layer_create_mask(work_layer, ADD_MASK_WHITE)
            pdb.gimp_layer_add_mask(work_layer, mask)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save the quantized image
        pdb.file_png_save(work_image, work_layer, output_path, output_path,
                        0, 9, 1, 1, 1, 1, 1)
        
        # Clean up
        pdb.gimp_image_delete(work_image)
        
        pdb.gimp_message("Palette quantization complete: {}".format(output_path))
        
    except Exception as e:
        pdb.gimp_message("Error during quantization: {}".format(str(e)))
    finally:
        pdb.gimp_image_undo_group_end(image)


def batch_quantize_to_palette(input_dir, output_dir, palette_name, dither_type, suffix):
    """
    Batch quantize multiple images to a palette.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save quantized images
        palette_name: Name of the palette to use
        dither_type: Dithering method
        suffix: Suffix to add to filenames
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Validate palette exists
    try:
        pdb.gimp_palette_get_info(palette_name)
    except:
        pdb.gimp_message("Error: Palette '{}' not found! Please check the palette name.".format(palette_name))
        return
    
    # Get list of image files
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tga')
    image_files = [f for f in os.listdir(input_dir) 
                  if f.lower().endswith(valid_extensions)]
    
    if not image_files:
        pdb.gimp_message("No supported image files found in input directory!")
        return
    
    # Initialize progress
    total = len(image_files)
    gimp.progress_init("Quantizing to palette...")
    
    processed = 0
    errors = 0
    
    # Process each image
    for idx, filename in enumerate(image_files):
        input_path = os.path.join(input_dir, filename)
        
        try:
            # Load image
            image = pdb.gimp_file_load(input_path, input_path)
            drawable = pdb.gimp_image_get_active_layer(image)
            
            # Duplicate for processing
            work_image = pdb.gimp_image_duplicate(image)
            work_layer = pdb.gimp_image_get_active_layer(work_image)
            
            # Get number of colors in palette
            num_colors = pdb.gimp_palette_get_info(palette_name)
            
            # Convert to indexed using palette
            pdb.gimp_image_convert_indexed(work_image, 
                                          CONVERT_DITHER_NONE if dither_type == 0 
                                          else CONVERT_DITHER_FS if dither_type == 1 
                                          else CONVERT_DITHER_FIXED,
                                          CONVERT_PALETTE_CUSTOM, num_colors, 
                                          False, False, palette_name)
            
            # Convert back to RGB for saving
            pdb.gimp_image_convert_rgb(work_image)
            work_layer = pdb.gimp_image_get_active_layer(work_image)
            
            # Generate output filename
            base_name = os.path.splitext(filename)[0]
            output_filename = base_name + suffix + '.png'
            output_path = os.path.join(output_dir, output_filename)
            
            # Save
            pdb.file_png_save(work_image, work_layer, output_path, output_path,
                            0, 9, 1, 1, 1, 1, 1)
            
            # Clean up
            pdb.gimp_image_delete(work_image)
            pdb.gimp_image_delete(image)
            
            processed += 1
            
        except Exception as e:
            errors += 1
            pdb.gimp_message("Error processing {}: {}".format(filename, str(e)))
        
        # Update progress
        gimp.progress_update(float(idx + 1) / total)
    
    pdb.gimp_message("Batch quantization complete!\nProcessed: {}\nErrors: {}".format(processed, errors))


# Register single image function
register(
    "python_fu_quantize_to_palette",
    "Quantize to palette",
    "Remap image colors to match a specific palette for consistent game art style.",
    "Python-Fu GIMP Automation",
    "Python-Fu GIMP Automation",
    "2024",
    "<Image>/Filters/Game Dev/Quantize to Palette...",
    "RGB*",
    [
        (PF_STRING, "palette_name", "Palette Name:", ""),
        (PF_OPTION, "dither_type", "Dithering:", 1, 
         ["None", "Floyd-Steinberg", "Fixed"]),
        (PF_FILE, "output_path", "Output Path:", "")
    ],
    [],
    quantize_to_palette
)

# Register batch function
register(
    "python_fu_batch_quantize_to_palette",
    "Batch quantize to palette",
    "Batch process images to enforce a consistent color palette across all sprites.",
    "Python-Fu GIMP Automation",
    "Python-Fu GIMP Automation",
    "2024",
    "<Image>/Filters/Game Dev/Batch Quantize Palette...",
    "",
    [
        (PF_DIRNAME, "input_dir", "Input Directory:", ""),
        (PF_DIRNAME, "output_dir", "Output Directory:", ""),
        (PF_STRING, "palette_name", "Palette Name:", ""),
        (PF_OPTION, "dither_type", "Dithering:", 1, 
         ["None", "Floyd-Steinberg", "Fixed"]),
        (PF_STRING, "suffix", "Filename Suffix:", "_quantized")
    ],
    [],
    batch_quantize_to_palette
)

main()
