#Globals
input_name = "State_PC_SSAM2.csv"
# output_name = "test.csv"
output_name = "SlicedadADCP.csv"

polygon = [[30.1833985, -85.8982186667], [30.178288, -85.8980861667], [30.1782625, -85.8930128333], [30.183373, -85.8930715]]
constant = []
multiple = []

lat_col = ''
lon_col = ''

def point_in_polygon(lat, lon):
    
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

# open file
file = open(input_name, 'r')

# create / open output file in write mode
fout = open(output_name, 'w')
    
# empty list of rows
rows = []
      

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


    # add header information to XML file
    if point_in_polygon(lat, lon) is True:
#         fout.write(str(lat) + ',' + str(lon) + ', True,' + str(lat) + ',' + str(lon) + '\n')
        fout.write(line)
      #  fout.write('\n')
#     else:
#         fout.write(str(lat) + ',' + str(lon) + '\n')

        
file.close()
fout.close()



