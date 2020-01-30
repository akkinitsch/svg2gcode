#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

def generate_gcode(filename, outputfile_name):
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])

    tree = ET.parse(filename)
    root = tree.getroot()
    
    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()                

    if width == None or height == None:
        print "Unable to get width and height for the svg"
        sys.exit(1)

    width = checkAndReturnMeasurementInMillimeter(width)
    height = checkAndReturnMeasurementInMillimeter(height)

    #scale_x = bed_max_x / max(width, height)
    #scale_y = bed_max_y / max(width, height)

    output_file = open(outputfile_name, "w")
    write_gcodeline(output_file, preamble)
    
    for elem in root.iter():
        
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                write_gcodeline(output_file, shape_preamble)
                p = point_generator(d, m, smoothness)
                move_to_startposition_shape_done = False
                for x,y in p:
                    #if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                    #    print "G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y) 
                    #print "G1 X%0.1f Y%0.1f" % (scale_x*x - bed_max_x/2.0, scale_y*y - bed_max_y/2.0)
                    gcode_line ="G1 X%0.1f Y%0.1f" % (x - (bed_max_x/2.0), y - (bed_max_y/2.0))
                    write_gcodeline(output_file, gcode_line)
                    if not move_to_startposition_shape_done:
                        gcode_line_zposition_plotting = "G1 Z%0.1f" %(z_position_plotting)
                        write_gcodeline(output_file, gcode_line_zposition_plotting)
                        move_to_startposition_shape_done = True

                write_gcodeline(output_file, shape_postamble)

    write_gcodeline(output_file, postamble)

def checkAndReturnMeasurementInMillimeter(value):
    if not value[-2:] == "mm":
        #TODO: Exception werfen
        pass
    else:
        result = value.split("mm")
        return float(result[0])

def write_gcodeline(outputfile, line, consoleprint=True):
    outputfile.write(line + "\n")
    if consoleprint:
        print line

if __name__ == "__main__":
    generate_gcode("test.svg", "test.gcode")


