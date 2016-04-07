
import xml.etree.ElementTree as ET

input_name = '20160401_India_ATR_SCM9_Box.xml'

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

lats = [coord[0] for coord in polygon]
lons = [coord[1] for coord in polygon]
  
