import myattributes as MA
import xml.etree.ElementTree as ET

#Globals
input_name = "ADCP.csv"
# output_name = "test.csv"
output_name = "SlicedADCP1.csv"

polygon = []
#polygon = [[32.57143, -117.17983], [32.57143, -117.19168], [32.56199, -117.19168], [32.56199, -117.17983]]
constant = []
multiple = []

lat_col = ''
lon_col = ''

lats = []
lons = []

# function for parsing polygon XML file
def polygon_parser(input_name):  
    
    message = ET.ElementTree(file = input_name)
    #TODO: Check that this is a valid file
    for coords in message.iter(tag = MA.XML_contact):
        # list to hold polygon coordinates
        coord = []
        
        for attribute in coords.iter():
#             
#             if attribute.tag == MA.XML_contact:
#                 # add ID to contact attribute list
#                 contact.append(str(attribute.attrib[MA.XML_contact_id]))
#                 
#             if attribute.tag == MA.XML_contact_crn:
#                 # add CRN to contact attribute list
#                 contact.append(attribute.text)
#                 
#             
#         
#         contacts.append(contact)        

lats = [coord[0] for coord in polygon]
lons = [coord[1] for coord in polygon]

def point_in_polygon(lat, lon):
    
    j = len(polygon) - 1
    
    odd_nodes = False

    for i, coord in enumerate(polygon):
        if ((lons[i] < lon) and (lons[j] >= lon) or ((lons[j] < lon) and (lons[i] >= lon))):
            if (((lats[i] + lon - lons[i]) / (lons[j] - lons[i]) * (lats[j] - lats[i])) < lat):
                odd_nodes = True
        j = i

    return odd_nodes

# open file
file = open(input_name, 'r')

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
        #fout.write('\n')
        # move to first data row
        continue
        
    lat = float(current_row[lat_col])
    lon = float(current_row[lon_col])
    
    cur_value = point_in_polygon(lat, lon)
    
    if index == 1:
        pre_value = cur_value
    
    # add header information to XML file
    if cur_value is True:
#         fout.write(str(lat) + ',' + str(lon) + ', True,' + str(lat) + ',' + str(lon) + '\n')
        fout.write(line)
        pre_value = cur_value
      #  fout.write('\n')
#     else:
#         fout.write(str(lat) + ',' + str(lon) + '\n')
    if cur_value is False and pre_value is True:
        fout.write("-----\n") 
        pre_value = False
        
file.close()
fout.close()






