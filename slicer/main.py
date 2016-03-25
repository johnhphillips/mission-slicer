 # open file
 file = open(input_name, 'r')
 # empty list of rows
 rows = []
      
 for line in file:
    # empty row of attributes
    row = []
        
    current_row = line.split(',')
    
    # find lat / long for given CSV file in header row
    if line == 0:
        for label in current_row:
            if label == "latitude":
                lat = 
            if label == "longitude"

    
        
    lat = current_row[0]
    row.append(lat)
    lon = current_row[1]
    row.append(lon)
    depth = current_row[3]
    row.append(depth)
    salinity = current_row[6]
    row.append(salinity)
    temperature = current_row[5]
    row.append(temperature)
    sound_speed = current_row[7]
    row.append(sound_speed)
        
    rows.append(row)
        
file.close()
