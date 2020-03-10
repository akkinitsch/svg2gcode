"""G-code emitted at the start of processing the SVG file"""
preamble = ""#""G28\nM302 S0\nG1 X0.0 F1000\nG1 Y0.0 F1000\nG1 Z5.0\nM25"

"""G-code emitted at the end of processing the SVG file"""
postamble = "G28 F10000\nM400\nM84"

"""High of extruder during plotting"""
z_position_plotting_start = 1

z_position_moving = 5.0

"""If z-positioning should be done by code of sender, this placeholder will be used
during generation of gcode. Replacement of this placeholder has to be done by sending code."""
z_position_placeholder = "printheight"

"""If z-positioning should be done by code of sender, this placeholder will be used
during generation of gcode. Replacement of this placeholder has to be done by sending code."""
z_movement_placeholder = "movementheight"

"""G-code emitted before processing a SVG shape"""
shape_preamble = "G4 P200"

"""G-code emitted after processing a SVG shape"""
shape_postamble = "G4 P200\nM25"# %(z_position_moving)

"""Print bed width in mm"""
bed_max_x = 100*2

"""Print bed height in mm"""
bed_max_y = 105*2

""" 
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
"""
smoothness = 0.1

z_correction_every_nth_shape = 3

retract_pencil = 0.1


