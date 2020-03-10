#!/usr/bin/env python

import argparse
import math
import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

def generate_gcode(filename, outputfile_name, use_printheight_placeholder=True):
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])

    tree = ET.parse(filename)
    root = tree.getroot()
    
    width = root.get('width')
    height = root.get('height')
    traveled_way = 0
    x_old = None
    y_old = None
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()

    if width == None or height == None:
        print "Unable to get width and height for the svg"
        sys.exit(1)

    width = checkAndReturnMeasurementInMillimeter(width)
    height = checkAndReturnMeasurementInMillimeter(height)

    output_file = open(outputfile_name, "w")
    write_gcodeline(output_file, preamble)

    shape_counter = 0
    z_position_plotting = z_position_plotting_start

    if use_printheight_placeholder:
        gcode_line_zposition_plotting = "G1 Z%s" % (z_position_placeholder)
    else:
        gcode_line_zposition_plotting = "G1 Z%0.1f" % (z_position_plotting)
    
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
                    distance_from_previous_point = 0
                    gcode_line = "G1 X%0.1f Y%0.1f" % (x, y)
                    if x_old and y_old and move_to_startposition_shape_done:
                        distance_from_previous_point = calculateDistance(x_old, y_old, x, y)
                        if distance_from_previous_point > 3:
                            write_gcodeline(output_file, "G1 Z%s" % (z_movement_placeholder))
                            write_gcodeline(output_file, gcode_line, traveled_way, elem.attrib["id"],
                                            distance_from_previous_point)
                            write_gcodeline(output_file, gcode_line_zposition_plotting)
                        else:
                            traveled_way = traveled_way + distance_from_previous_point
                            write_gcodeline(output_file, gcode_line, traveled_way, elem.attrib["id"], distance_from_previous_point)
                    x_old = x
                    y_old = y

                    if not move_to_startposition_shape_done:
                        write_gcodeline(output_file, gcode_line_zposition_plotting)
                        move_to_startposition_shape_done = True

                if use_printheight_placeholder:
                    write_gcodeline(output_file, "G1 Z%s" % (z_movement_placeholder))
                write_gcodeline(output_file, shape_postamble)

                if not use_printheight_placeholder:
                    shape_counter = shape_counter + 1
                    if shape_counter % z_correction_every_nth_shape == 0:
                        z_position_plotting = z_position_plotting - retract_pencil
                        if z_position_plotting < 0.4:
                            pause_printer_for_pencil_retraction()
                            gcode_line_zposition_plotting = "G1 Z%0.1f" % (z_position_plotting_start)
                            write_gcodeline(output_file, gcode_line_zposition_plotting)
                            write_gcodeline(output_file, "M25")
                            z_position_plotting = z_position_plotting_start

    write_gcodeline(output_file, postamble)


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def checkAndReturnMeasurementInMillimeter(value):
    if not value[-2:] == "mm":
        #TODO: Exception werfen
        pass
    else:
        result = value.split("mm")
        return float(result[0])

def write_gcodeline(outputfile, line, plotted_way=0.0, elementID="", distance_from_previous_point=0, consoleprint=True):
    outputfile.write(line + " ; " + str(plotted_way) + " ; " + elementID + " ; " + str(distance_from_previous_point) + "\n")
    if consoleprint:
        print line

def pause_printer_for_pencil_retraction():
    pass#write_gcodeline(output_file, "G1 Z%0.1f\nM25" %(z_position_plotting))

def resume_printjob():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input')
    parser.add_argument('--output', dest='output')
    args = parser.parse_args()
    generate_gcode(args.input, args.output)


