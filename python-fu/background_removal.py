#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Background Removal Script for GIMP
Automatically removes backgrounds from images using fuzzy selection or edge detection.
"""

from gimpfu import *
import os

def remove_background_fuzzy(image, drawable, x_coord, y_coord, tolerance, feather, preview_only):
	"""
	Remove background using fuzzy select (select by color) method.
	
	Args:
		image: The current image
		drawable: The active layer
		x_coord: X coordinate for selection point (0-100%, 50 = center)
		y_coord: Y coordinate for selection point (0-100%, 50 = center)
		tolerance: Selection tolerance (0-255, higher = more colors selected)
		feather: Edge feathering amount in pixels
		preview_only: If True, only shows selection without removing
	"""
	# Start an undo group
	pdb.gimp_image_undo_group_start(image)
	
	try:
		# Ensure the layer has an alpha channel
		if not pdb.gimp_drawable_has_alpha(drawable):
			pdb.gimp_layer_add_alpha(drawable)
		
		# Calculate actual coordinates from percentages
		actual_x = int(image.width * x_coord / 100.0)
		actual_y = int(image.height * y_coord / 100.0)
		
		# Perform fuzzy select
		pdb.gimp_fuzzy_select(drawable, actual_x, actual_y, tolerance, 
		                      CHANNEL_OP_REPLACE, True, False, 0, False)
		
		# Feather the selection if specified
		if feather > 0:
			pdb.gimp_selection_feather(image, feather)
		
		if not preview_only:
			# Delete the selected background
			pdb.gimp_edit_clear(drawable)
			# Remove selection
			pdb.gimp_selection_none(image)
		
		# Refresh the display
		gimp.displays_flush()
		
	finally:
		# End the undo group
		pdb.gimp_image_undo_group_end(image)

def remove_background_edge(image, drawable, edge_amount, threshold, grow_shrink, preview_only):
	"""
	Remove background using edge detection method.
	
	Args:
		image: The current image
		drawable: The active layer
		edge_amount: Edge detection sensitivity (1.0-10.0, higher = more sensitive)
		threshold: Threshold for edge detection (0-255)
		grow_shrink: Grow (positive) or shrink (negative) selection in pixels
		preview_only: If True, only shows selection without removing
	"""
	# Start an undo group
	pdb.gimp_image_undo_group_start(image)
	
	try:
		# Ensure the layer has an alpha channel
		if not pdb.gimp_drawable_has_alpha(drawable):
			pdb.gimp_layer_add_alpha(drawable)
		
		# Create a copy of the layer for edge detection
		temp_layer = pdb.gimp_layer_copy(drawable, True)
		pdb.gimp_image_insert_layer(image, temp_layer, None, 0)
		
		# Convert to grayscale for edge detection
		pdb.gimp_desaturate_full(temp_layer, DESATURATE_LIGHTNESS)
		
		# Apply edge detection
		pdb.plug_in_edge(image, temp_layer, edge_amount, 1, 0)
		
		# Threshold the edge-detected layer
		pdb.gimp_drawable_threshold(temp_layer, HISTOGRAM_VALUE, threshold, 255)
		
		# Select by color (select the edges - white areas)
		pdb.gimp_by_color_select(temp_layer, (255, 255, 255), 15,
		                         CHANNEL_OP_REPLACE, True, False, 0, False)
		
		# Invert selection to select the subject instead of edges
		pdb.gimp_selection_invert(image)
		
		# Grow or shrink the selection
		if grow_shrink > 0:
			pdb.gimp_selection_grow(image, grow_shrink)
		elif grow_shrink < 0:
			pdb.gimp_selection_shrink(image, abs(grow_shrink))
		
		# Remove the temporary layer
		pdb.gimp_image_remove_layer(image, temp_layer)
		
		# Invert selection again to select background
		pdb.gimp_selection_invert(image)
		
		if not preview_only:
			# Delete the selected background
			pdb.gimp_edit_clear(drawable)
			# Remove selection
			pdb.gimp_selection_none(image)
		
		# Refresh the display
		gimp.displays_flush()
		
	finally:
		# End the undo group
		pdb.gimp_image_undo_group_end(image)

def batch_remove_background(input_dir, output_dir, method, x_coord, y_coord, 
                            tolerance, feather, edge_amount, threshold, grow_shrink):
	"""
	Batch process multiple images for background removal.
	
	Args:
		input_dir: Directory containing input images
		output_dir: Directory to save processed images
		method: 0 for fuzzy select, 1 for edge detection
		x_coord: X coordinate for fuzzy select (percentage)
		y_coord: Y coordinate for fuzzy select (percentage)
		tolerance: Tolerance for fuzzy select method
		feather: Feathering amount for fuzzy select
		edge_amount: Edge detection sensitivity
		threshold: Threshold for edge detection
		grow_shrink: Grow/shrink selection amount
	"""
	# Create output directory if it doesn't exist
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	
	# Get list of image files
	valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff')
	image_files = [f for f in os.listdir(input_dir) 
	              if f.lower().endswith(valid_extensions)]
	
	for filename in image_files:
		input_path = os.path.join(input_dir, filename)
		
		try:
			# Load the image
			image = pdb.gimp_file_load(input_path, input_path)
			drawable = pdb.gimp_image_get_active_layer(image)
			
			# Apply background removal based on method
			if method == 0:  # Fuzzy select method
				remove_background_fuzzy(image, drawable, x_coord, y_coord, tolerance, feather, False)
			else:  # Edge detection method
				remove_background_edge(image, drawable, edge_amount, threshold, 
				                      grow_shrink, False)
			
			# Prepare output filename (change extension to PNG to preserve transparency)
			base_name = os.path.splitext(filename)[0]
			output_filename = base_name + '_no_bg.png'
			output_path = os.path.join(output_dir, output_filename)
			
			# Export the layer with transparency preserved
			pdb.gimp_file_save(image, drawable, output_path, output_path)
			
			# Delete the image from memory
			pdb.gimp_image_delete(image)
			
		except Exception as e:
			gimp.message("Error processing %s: %s" % (filename, str(e)))
			continue

# Register the fuzzy select background removal function
register(
	"python_fu_remove_background_fuzzy",
	"Remove background using fuzzy select method",
	"Automatically removes background from an image using fuzzy selection. Samples background color at specified X/Y position and removes similar colors.",
	"Python-Fu GIMP Automation",
	"Python-Fu GIMP Automation",
	"2024",
	"<Image>/Filters/Background Removal/Fuzzy Select...",
	"RGB*, GRAY*",
	[
		(PF_SLIDER, "x_coord", "Selection X Position (%)", 5, (0, 100, 1)),
		(PF_SLIDER, "y_coord", "Selection Y Position (%)", 5, (0, 100, 1)),
		(PF_SLIDER, "tolerance", "Selection Tolerance", 15, (0, 255, 1)),
		(PF_SLIDER, "feather", "Edge Feathering (px)", 2, (0, 50, 1)),
		(PF_TOGGLE, "preview_only", "Preview Only (don't remove)", False)
	],
	[],
	remove_background_fuzzy
)

# Register the edge detection background removal function
register(
	"python_fu_remove_background_edge",
	"Remove background using edge detection method",
	"Automatically removes background from an image using edge detection to identify the subject.",
	"Python-Fu GIMP Automation",
	"Python-Fu GIMP Automation",
	"2024",
	"<Image>/Filters/Background Removal/Edge Detection...",
	"RGB*, GRAY*",
	[
		(PF_SPINNER, "edge_amount", "Edge Detection Sensitivity", 2.0, (1.0, 10.0, 0.1)),
		(PF_SLIDER, "threshold", "Edge Threshold", 30, (0, 255, 1)),
		(PF_SPINNER, "grow_shrink", "Grow/Shrink Selection (px)", 2, (-50, 50, 1)),
		(PF_TOGGLE, "preview_only", "Preview Only (don't remove)", False)
	],
	[],
	remove_background_edge
)

# Register the batch processing function
register(
	"python_fu_batch_remove_background",
	"Batch remove backgrounds from multiple images",
	"Process multiple images in a directory to remove backgrounds. Uses either fuzzy select or edge detection method.",
	"Python-Fu GIMP Automation",
	"Python-Fu GIMP Automation",
	"2024",
	"<Image>/Filters/Background Removal/Batch Process...",
	"",
	[
		(PF_DIRNAME, "input_dir", "Input Directory", ""),
		(PF_DIRNAME, "output_dir", "Output Directory", ""),
		(PF_OPTION, "method", "Removal Method", 0, ["Fuzzy Select", "Edge Detection"]),
		(PF_SLIDER, "x_coord", "Fuzzy X Position (%)", 5, (0, 100, 1)),
		(PF_SLIDER, "y_coord", "Fuzzy Y Position (%)", 5, (0, 100, 1)),
		(PF_SLIDER, "tolerance", "Fuzzy Select Tolerance", 15, (0, 255, 1)),
		(PF_SLIDER, "feather", "Fuzzy Select Feathering", 2, (0, 50, 1)),
		(PF_SPINNER, "edge_amount", "Edge Sensitivity", 2.0, (1.0, 10.0, 0.1)),
		(PF_SLIDER, "threshold", "Edge Threshold", 30, (0, 255, 1)),
		(PF_SPINNER, "grow_shrink", "Grow/Shrink (px)", 2, (-50, 50, 1))
	],
	[],
	batch_remove_background
)

main()
