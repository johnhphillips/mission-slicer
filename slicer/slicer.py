import myattributes as MA
import xml.etree.ElementTree as ET

input_csv = "ADCP.csv"
input_polygon = "20160401_India_ATR_SCM9_Box"

OUTPUT_PREFIX = "Sliced_"
output_name = OUTPUT_PREFIX + input_csv


#polygon = [[32.57143, -117.17983], [32.57143, -117.19168], [32.56199, -117.19168], [32.56199, -117.17983]]



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

def point_in_polygon(lat, lon, lats, lons):
    
    j = len(lats) - 1
    
    odd_nodes = False

    for i, coord in enumerate(lats):
        if ((lons[i] < lon) and (lons[j] >= lon) or ((lons[j] < lon) and (lons[i] >= lon))):
            if (((lats[i] + lon - lons[i]) / (lons[j] - lons[i]) * (lats[j] - lats[i])) < lat):
                odd_nodes = True
        j = i

    return odd_nodes

def slicer(polygon, input_file, output_file):
    lats = [coord[0] for coord in polygon]
    lons = [coord[1] for coord in polygon]
    
    # open file
    file = open(input_file, 'r')

    # create / open output file in write mode
    fout = open(output_name, 'w')
    
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
    
        cur_value = point_in_polygon(lat, lon, lats, lons)
    
        if index == 1:
            pre_value = cur_value
    
        if cur_value is True:
            fout.write(line)
            pre_value = cur_value
        
        elif cur_value is False and pre_value is True:
            fout.write("-----\n") 
            pre_value = False
        
    file.close()
    fout.close()






