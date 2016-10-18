# mission_slicer slicer 
# Copyright (C) 2016 John Phillips, SPAWAR Systems Center Pacific
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xml.etree.ElementTree as ET

# function for parsing polygon XML file
def polygon_parser(input_name):  
    
    polygon = []
    valid_input = False

    message = ET.ElementTree(file = input_name)

    for area in message.iter(tag = '{http://www.saic.com/navy/miwml.1.0}PolygonArea'):
        # mark as valid message type
        valid_input = True
        
        for part in area.iter():
            # check for position
            if part.tag == '{http://www.saic.com/navy/miwml.1.0}Position':
                coord = []
                for vertex in part:
                    coord.append(float(vertex.text))
                polygon.append(coord)
            
    if valid_input == False:
        print "Error. Invalid Polygon XML File." 
    

    return polygon      

def point_in_polygon(lat, lon, polygon):

    n = len(polygon)
    odd_nodes = False
    
    p1y, p1x = polygon[0]
    
    for i in range(n + 1):
        p2y, p2x = polygon[i % n]
        if lat > min(p1y, p2y):
            if lat <= max(p1y, p2y):
                if lon <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or lon <= xinters:
                        odd_nodes = not odd_nodes
        p1x,p1y = p2x,p2y

    return odd_nodes

def slicer(polygon, input_file, output_file):
    
    # open file
    file = open(input_file, 'r')

    # create / open output file in write mode
    fout = open(output_file, 'w')
    
    # empty list of rows
    rows = []

    prev_value = False
      
    for index, line in enumerate(file):
        # empty row of attributes
        row = []
        
        current_row = line.split(',')
    
        # find lat / long column for given CSV file in header row
        # assumption that header is present
        if index == 0:
            for index, label in enumerate(current_row):
                if label == "latitude":
                    lat_col = index 
                if label == "longitude":
                    lon_col = index
            fout.write(line)
        
            # move to first data row
            continue
        
        lat = float(current_row[lat_col])
        lon = float(current_row[lon_col])
    
        if point_in_polygon(lat, lon, polygon) is True:
            fout.write(line)
        cur_value = point_in_polygon(lat, lon, polygon)
     
        if index == 1:
            pre_value = cur_value
     
        if cur_value is True:
            #fout.write(line)
            pre_value = cur_value
         
        elif cur_value is False and pre_value is True:
            fout.write("-----\n") 
            pre_value = False
#         
    file.close()
    fout.close()






