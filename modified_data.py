#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import string
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
# Source : http://www.pasteur.fr/formation/infobio/python/ch10.html
# Source : http://stackoverflow.com/questions/25735516/typeerror-float-argument-must-be-a-string-or-a-number-in-django-distance
# Source : https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# Source : http://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-method
# Source : http://www.tutorialspoint.com/python/string_startswith.htm

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')



CREATED = [ "version", "changeset", "timestamp", "user", "uid"] # for checking created dictionary
CONTACT = [ "website", "email", "phone", "fax"] # for checking contact dictionary

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        
        node['type'] = element.tag # assigning node or way to type
               
        node['created'] = {} # intializing created
        
        for k_value, v_value in element.items(): # iterating through the element
                        
            if k_value == "lat" or k_value == "lon": # checking for lat and lon
                
                lat = element.get('lat')
                lon = element.get('lon')
                
                if lon is not None and lat is not None: # converting to float
                    float_lat = float(lat)
                    float_lon = float(lon)
                    
                    node['pos'] = [float_lat,float_lon] # assigning to pos
            
                        
            elif k_value in CREATED: # populating created
               node['created'][k_value] = v_value
            
            else: # processing as regular tag
                node[k_value] = v_value
                
        node['address'] = {} # initializing address
        node['GNIS'] = {} # initializing GNIS
        node['contact'] = {} # initializing contact
        node['metcouncil'] = {} # initializing metcouncil
        node['nice_ride_mn'] = {} # initializing NRM 
        node['TIGER_db'] = {} # initializing TIGER DB
        node['metro_parks'] = {} # initializing metro parks
        node['UofMN'] = {} # initializing UofM
        node['bicycle_service'] = {} # initializing bycycle service
        node['name_non_latin'] = {} # initializing non-latin names
        node['location'] = {} # initializing location
        node['tree_type'] = {} # initializing tree type
        
        for tag in element.iter("tag"): # iterating through tag
            
            # fetching k and v
            second_k_value = tag.get('k')
            second_v_value = tag.get('v')
            
            # ignoring for problematic chracters
            if re.search(lower, second_k_value) or re.search(lower_colon, second_k_value) or re.search(problemchars, second_k_value):
                pass
            
            
            # ignoring street & import_uuid (repetitve/not-required infomation)
            if ("street:" in second_k_value) or ("import_uuid" in second_k_value):
                continue
            
            # storing in GNIS
            elif second_k_value.startswith('gnis:'):
                node['GNIS'][second_k_value[5:]] = second_v_value
                
            # storing in tree type
            elif second_k_value == "type":
                node['tree_type'] = second_v_value
            
            # storing in name
            elif second_k_value.startswith('name:'):
                node['name_non_latin'][second_k_value[5:]] = second_v_value
                
            # storing in metcouncil
            elif second_k_value.startswith('metcouncil:'):
                node['metcouncil'][second_k_value[11:]] = second_v_value
                
            # storing in nice ride minnesota
            elif second_k_value.startswith('nrm:'):
                node['nice_ride_mn'][second_k_value[4:]] = second_v_value
                
            # storing in TIGER DB
            elif second_k_value.startswith('tiger:'):
                node['TIGER_db'][second_k_value[6:]] = second_v_value
            
            # storing in metro parks
            elif second_k_value.startswith('metrogis:'):
                node['metro_parks'][second_k_value[9:]] = second_v_value
            
            # storing in U of MN
            elif second_k_value.startswith('umn:'):
                node['UofMN'][second_k_value[4:]] = second_v_value
                
            # storing in service
            elif second_k_value.startswith('service:bicycle:'):
                if second_k_value == "service:bicycle:diy":
                    node['bicycle_service']['do_it_yourself'] = second_v_value
                else:
                    node['bicycle_service'][second_k_value[16:]] = second_v_value
                
            # storing in contact 1
            elif second_k_value.startswith('contact:'):
                node['contact'][second_k_value[8:]] = second_v_value
            
            # storing in contact 2
            elif second_k_value in CONTACT:
                node['contact'][second_k_value] = second_v_value
                
            # correcting and storing in elevation in meters
            elif second_k_value.startswith('ele'):
                node['elevation'] = second_v_value + " m"
            
            # storing location
            elif second_k_value.startswith('is_in:'):
                node['location'][second_k_value[6:]] = second_v_value
                
            # updating and storing GaWC ranking
            elif second_k_value.startswith('GaWC'):
                node['GaWC'] = "Beta-"
            
            # processing that has : and not part of address
            elif not second_k_value.startswith('addr:') and ":" in second_k_value:
                node[second_k_value] = second_v_value
                   
            # storing in address
            elif second_k_value.startswith('addr:'):
                
                if second_k_value == "addr:street":
                    better_name = update_name(second_v_value, mapping_last, mapping_first, mapping_middle)
                    node['address']['street'] = better_name
                elif second_k_value == "addr:street" and second_v_value == "55414": # addressing inconsistency in street name
                    continue
                elif second_k_value == "addr:postcode" and second_v_value == "MN": # addressing inconsistency in zip code
                    node['address'][second_k_value[5:]] = "55408"
                elif second_k_value == "addr:postcode" and second_v_value == "100": # addressing inconsistency in zip code
                    node['address'][second_k_value[5:]] = "55401"
                elif second_k_value == "addr:postcode" and second_v_value == "5114": # addressing inconsistency in zip code
                    node['address'][second_k_value[5:]] = "55114"
                elif second_k_value == "addr:postcode" and second_v_value == "Pillsbury Dr": # addressing inconsistency in zip code
                    node['address'][second_k_value[5:]] = "55455"
                elif second_k_value == "addr:housenumber" and second_v_value == "2115 Summit Ave, Saint Paul, MN": # housenumber incorrect
                    node['address'][second_k_value[5:]] = "2115"
                    node['address']['street'] = 'Summit Avenue'
                    node['address']['city'] = 'Saint Paul, MN'
                else:
                    node['address'][second_k_value[5:]] = second_v_value
                
            else: # processing as regular tag
                node[second_k_value] = second_v_value
        
        # initializing node_refs
        node['node_refs'] = []
        for ref in element.iter("nd"): # iterating through nd

            ref_value = ref.get('ref') # assigning ref to ref_value
               
            node['node_refs'].append(ref_value) # appending to node_refs
        
        # removing empty dictionaries
        if node['address'] == {}:
            del node['address']
        if node['node_refs'] == []:
            del node['node_refs']
        if node['GNIS'] == {}:
            del node['GNIS']
        if node['contact'] == {}:
            del node['contact']
        if node['metcouncil'] == {}:
            del node['metcouncil']
        if node['nice_ride_mn'] == {}:
            del node['nice_ride_mn']
        if node['TIGER_db'] == {}:
            del node['TIGER_db']
        if node['metro_parks'] == {}:
            del node['metro_parks']
        if node['UofMN'] == {}:
            del node['UofMN']
        if node['bicycle_service'] == {}:
            del node['bicycle_service']
        if node['name_non_latin'] == {}:
            del node['name_non_latin']
        if node['location'] == {}:
            del node['location']
        if node['tree_type'] == {}:
            del node['tree_type']
        
        
        
        return node
    else:
        return None
   

# def update_name() used from Audit.py(Lesson 6) to improve street names and directly store in json file

# mapping variable updated accordingly to accomodate various inconsistencies in the street names in the osm file

# mapping_last used from imroving last part of street address
mapping_last = {"St": "Street","St.": "Street", "Ave": "Avenue", "Rd.": "Road", "Pl" : "Plaza", "Blvd" : "Boulevard", "Dr" : "Drive",
                "SE" : "Southeast", "Ln" : "Lane", "Ave.": "Avenue", "N" : "North", "N." : "North", "NE" : "Northeast",
                "Pkwy" : "Parkway", "Rd": "Road", "Rd/Pkwy" : "Parkway", "S" : "South", "SE" : "Southeast", "W" : "West",
                "S.E." : "Southeast"}

# mapping_first used from imroving first part of street address
mapping_first = {"N." : "North", "S" : "South", "E" : "East", "N" : "North", "SE" : "Southeast", "NE" : "Northeast", "E." : "East"}

# mapping_middle used from imroving middle part of street address
mapping_middle = {"Ave": "Avenue", "Ave.": "Avenue", "Dr" : "Drive", "St": "Street", "St.": "Street"}

   
def update_name(name, map_last, map_first, map_middle): # modified update_name() method used for impoving street names
    
    # YOUR CODE HERE
    name_value = name.split(' ') # Splitting the street address by space and storing in a list (for correction of last part)
    
    # storing the first part of the street name, except the last word
    name_first_part = name_value[:-1]
    
    # storing the last word of the street name
    name_last = name_value[-1]
    
    for k,m in map_last.items(): # iterating over the mapping dictionary
        
        # correcting last part of street names (mapping_last)
        if name_last == k: # checking if last word of address is present in dictionary key
            
            name_last = m.split() # replacing last word with a better name
            
            name_last_list = name_first_part + name_last # combining first part and last word
            
            name = " ".join(name_last_list) # converting list to a string
            
    
    name_value = name.split(' ') # Splitting the street address by space and storing in a list (for correction of first part)
    
    # storing the first word of the street name
    name_first = name_value[0]
    
    # storing the last part of the street name, except the first word
    name_last_part = name_value[1:]
    
    for x,y in map_first.items(): # iterating over the mapping dictionary
        
        # correcting first part of street names (mapping_first)
        if name_first == x: # checking if first word of address is present in dictionary key
            
            name_first = y.split() # replacing first word with a better name
            
            name_first_list = name_first + name_last_part # combining first word and last part
            
            name = " ".join(name_first_list) # converting list to a string
        
    name_value = name.split(' ') # Splitting the street address by space and storing in a list (for correction of middle part)
    
    if len(name_value) == 3: # correcting 3 words street names     
        
        # storing the first word of the street name
        name_first = name_value[0].split()

        # storing the last word of the street name
        name_last = name_value[-1].split()

        # storing the middle part of the street name
        name_middle_part = name_value[1]
        
        for s,t in map_middle.items(): # iterating over the mapping dictionary

            # correcting middle part of street names (mapping_middle)
            if name_middle_part == s: # checking if middle word of address is present in dictionary key

                name_middle_part = t.split() # replacing middle part with a better name

                name_middle_list = name_first + name_middle_part + name_last # combining first, middle and last part

                name = " ".join(name_middle_list) # converting list to a string
    
    name_value = name.split(' ') # Splitting the street address by space and storing in a list (for correction of special cases)
    
    if len(name_value) == 4:# correcting 4 words street names (only one instance: "1320 4th St SE")        
            
        # correcting the street name
        name_value[2] = "Street"
        name = " ".join(name_value)
        
    if len(name_value) == 7:# correcting 7 words street names (only one instance: "10th Avenue SE & 5th Street Southeast")        
        
        # correcting the street name
        name_value[2] = "Southeast"
        name_value[3] = "and"
        name = " ".join(name_value)
        
    return name    

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    
    with codecs.open(file_out, "w", encoding='utf8') as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2, ensure_ascii=False)+"\n")
                    
                else:
                    fo.write(json.dumps(el, ensure_ascii=False) + "\n")
    return data
    
'''    
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                    
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
'''    
def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('final_minneapolis.osm', False)
    #pprint.pprint(data)
    '''
    assert data[0] == {
                        "id": "261114295", 
                        "visible": "true", 
                        "type": "node", 
                        "pos": [
                          41.9730791, 
                          -87.6866303
                        ], 
                        "created": {
                          "changeset": "11129782", 
                          "user": "bbmiller", 
                          "version": "7", 
                          "uid": "451048", 
                          "timestamp": "2012-03-28T18:31:23Z"
                        }
                      }
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]
    '''
if __name__ == "__main__":
    test()