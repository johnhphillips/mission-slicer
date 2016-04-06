
import xml.etree.ElementTree as ET

input_name = '20160401_India_ATR_SCM9_Box.xml'

polygon = []
valid_input = False

message = ET.ElementTree(file = input_name)
#TODO: Check that this is a valid file
for area in message.iter(tag = '{http://www.saic.com/navy/miwml.1.0}PolygonArea'):
    # mark as valid message type
    valid_input = True
    
    # list to hold polygon coordinates

        
    for coords in area.iter():
        # check for position
        if coords.tag == '{http://www.saic.com/navy/miwml.1.0}Position':
            for coord in coords:
                print coord.tag, coord.attrib, coord.text
#         if attribute.tag == MA.XML_contact:
#             # add ID to contact attribute list
#             contact.append(str(attribute.attrib[MA.XML_contact_id]))
#                  
#         if attribute.tag == MA.XML_contact_crn:
#             # add CRN to contact attribute list
#             contact.append(attribute.text)
#                  
#     contacts.append(contact)       
