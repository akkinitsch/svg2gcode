"""G-code emitted at the start of processing the SVG file"""
preamble = "G28\nM302 S0\nG1 X0.0 F1000\nG1 Y0.0 F1000\nG1 Z5.0"

"""G-code emitted at the end of processing the SVG file"""
postamble = "G28 F1000\nM400\nM84"

"""High of extruder during plotting"""
z_position_plotting = 1.0

z_position_moving = 1.8

"""G-code emitted before processing a SVG shape"""
shape_preamble = "G4 P200"

"""G-code emitted after processing a SVG shape"""
shape_postamble = "G1 Z%0.1f\nG4 P200" %(z_position_moving)

"""Print bed width in mm"""
bed_max_x = 200

"""Print bed height in mm"""
bed_max_y = 200

""" 
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
"""
smoothness = 0.2

pause_every_nth_path = 3

pause_command = "G1 Z%0.1f\nM226" %(z_position_moving)

resume_command = "G1 Z%0.1f" %(z_position_plotting)


