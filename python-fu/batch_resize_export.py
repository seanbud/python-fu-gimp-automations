#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Batch Resize and Export Images for GIMP
========================================

This Python-Fu script provides batch image processing capabilities for GIMP,
allowing users to resize and export multiple images in a directory with various
customization options.

Features:
- Select a directory containing input images
- Choose custom output sizes (width/height or percent scaling)
- Choose output format (PNG, JPEG, etc.)
- Option to append suffix to filenames
- Specify output directory
- Progress bar and error reporting

Author: GIMP Python-Fu Automation
License: MIT
"""

from gimpfu import *
import os

def batch_resize_export(
    input_dir,
    output_dir,
    resize_mode,
    width,
    height,
    percent,
    output_format,
    filename_suffix,
    maintain_aspect_ratio
):
    """
    Batch resize and export images from input directory.
    
    Parameters:
    -----------
    input_dir : str
        Directory containing input images
    output_dir : str
        Directory where processed images will be saved
    resize_mode : int
        0 = Resize by dimensions (width x height)
        1 = Resize by percentage
    width : int
        Target width in pixels (used when resize_mode=0)
    height : int
        Target height in pixels (used when resize_mode=0)
    percent : float
        Scaling percentage (used when resize_mode=1)
    output_format : int
        0 = PNG, 1 = JPEG, 2 = BMP, 3 = GIF
    filename_suffix : str
        Suffix to append to output filenames (e.g., "_resized")
    maintain_aspect_ratio : int
        0 = No, 1 = Yes (only applies when resize_mode=0)
    """
    
    # Validate input directory
    if not os.path.exists(input_dir):
        gimp.message("Error: Input directory does not exist!")
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            gimp.message("Error creating output directory: " + str(e))
            return
    
    # Define supported input file extensions
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff', '.xcf')
    
    # Get list of image files in input directory
    try:
        all_files = os.listdir(input_dir)
        image_files = [f for f in all_files if f.lower().endswith(supported_extensions)]
    except Exception as e:
        gimp.message("Error reading input directory: " + str(e))
        return
    
    if not image_files:
        gimp.message("No supported image files found in input directory!")
        return
    
    # Define output file extension based on format
    format_extensions = {
        0: '.png',
        1: '.jpg',
        2: '.bmp',
        3: '.gif'
    }
    output_ext = format_extensions.get(output_format, '.png')
    
    # Process statistics
    total_files = len(image_files)
    processed_count = 0
    error_count = 0
    error_messages = []
    
    # Initialize progress bar
    gimp.progress_init("Batch resizing images...")
    
    # Process each image file
    for idx, filename in enumerate(image_files):
        input_path = os.path.join(input_dir, filename)
        
        # Update progress bar
        progress = float(idx) / total_files
        gimp.progress_update(progress)
        
        image = None
        try:
            # Load the image
            image = pdb.gimp_file_load(input_path, input_path)
            
            # Get the active layer (or flatten if multiple layers)
            if len(image.layers) > 1:
                pdb.gimp_image_flatten(image)
            
            layer = image.active_layer
            
            # Calculate new dimensions
            old_width = image.width
            old_height = image.height
            
            if resize_mode == 0:
                # Resize by dimensions
                new_width = width
                new_height = height
                
                if maintain_aspect_ratio:
                    # Calculate aspect ratio
                    aspect_ratio = float(old_width) / float(old_height)
                    
                    # Determine which dimension to fit
                    if float(width) / float(height) > aspect_ratio:
                        # Height is the limiting factor
                        new_height = height
                        new_width = int(height * aspect_ratio)
                    else:
                        # Width is the limiting factor
                        new_width = width
                        new_height = int(width / aspect_ratio)
            else:
                # Resize by percentage
                scale_factor = percent / 100.0
                new_width = int(old_width * scale_factor)
                new_height = int(old_height * scale_factor)
            
            # Ensure minimum dimensions
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
            # Scale the image
            pdb.gimp_image_scale(image, new_width, new_height)
            
            # Prepare output filename
            base_name = os.path.splitext(filename)[0]
            output_filename = base_name + filename_suffix + output_ext
            output_path = os.path.join(output_dir, output_filename)
            
            # Export based on format
            if output_format == 0:
                # PNG
                pdb.file_png_save(
                    image,
                    image.active_layer,
                    output_path,
                    output_path,
                    0,  # interlace
                    9,  # compression level
                    1,  # bkgd
                    1,  # gama
                    1,  # offs
                    1,  # phys
                    1   # time
                )
            elif output_format == 1:
                # JPEG
                pdb.file_jpeg_save(
                    image,
                    image.active_layer,
                    output_path,
                    output_path,
                    0.9,  # quality
                    0,    # smoothing
                    1,    # optimize
                    1,    # progressive
                    "",   # comment
                    0,    # subsmp
                    1,    # baseline
                    0,    # restart
                    0     # dct
                )
            elif output_format == 2:
                # BMP
                pdb.file_bmp_save(
                    image,
                    image.active_layer,
                    output_path,
                    output_path
                )
            elif output_format == 3:
                # GIF
                pdb.file_gif_save(
                    image,
                    image.active_layer,
                    output_path,
                    output_path,
                    0,  # interlace
                    0,  # loop
                    0,  # default delay
                    0   # default dispose
                )
            
            # Clean up - delete the image from GIMP
            pdb.gimp_image_delete(image)
            
            processed_count += 1
            
        except Exception as e:
            error_count += 1
            error_msg = "Error processing '{}': {}".format(filename, str(e))
            error_messages.append(error_msg)
            
            # Try to clean up if image was loaded
            try:
                if image is not None:
                    pdb.gimp_image_delete(image)
            except:
                pass
    
    # Complete progress bar
    gimp.progress_update(1.0)
    
    # Generate summary message
    summary = "Batch Resize Complete!\n\n"
    summary += "Total files: {}\n".format(total_files)
    summary += "Successfully processed: {}\n".format(processed_count)
    summary += "Errors: {}\n".format(error_count)
    
    if error_messages:
        summary += "\nError Details:\n"
        # Limit error messages to first 10 to avoid overwhelming the user
        for error_msg in error_messages[:10]:
            summary += "- " + error_msg + "\n"
        if len(error_messages) > 10:
            summary += "... and {} more errors\n".format(len(error_messages) - 10)
    
    summary += "\nOutput directory: {}".format(output_dir)
    
    # Display summary
    gimp.message(summary)


# Register the plugin with GIMP
register(
    "python_fu_batch_resize_export",
    "Batch resize and export images from a directory",
    "Batch process multiple images: resize them using dimensions or percentage, "
    "and export to various formats (PNG, JPEG, BMP, GIF) with progress tracking "
    "and error reporting.",
    "GIMP Python-Fu Automation",
    "MIT License",
    "2024",
    "<Toolbox>/Filters/Batch Process/Batch Resize and Export...",
    "*",
    [
        (PF_DIRNAME, "input_dir", "Input Directory:", ""),
        (PF_DIRNAME, "output_dir", "Output Directory:", ""),
        (PF_OPTION, "resize_mode", "Resize Mode:", 0, 
         ["By Dimensions (Width x Height)", "By Percentage"]),
        (PF_INT, "width", "Width (pixels):", 800),
        (PF_INT, "height", "Height (pixels):", 600),
        (PF_FLOAT, "percent", "Scale Percentage:", 50),
        (PF_OPTION, "output_format", "Output Format:", 0,
         ["PNG", "JPEG", "BMP", "GIF"]),
        (PF_STRING, "filename_suffix", "Filename Suffix:", "_resized"),
        (PF_TOGGLE, "maintain_aspect_ratio", "Maintain Aspect Ratio:", 1)
    ],
    [],
    batch_resize_export
)

main()
