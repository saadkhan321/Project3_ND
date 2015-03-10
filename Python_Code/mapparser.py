#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
# Source : http://css.dzone.com/articles/processing-xml-python
# Source : http://www.blog.pythonlibrary.org/2013/04/30/python-101-intro-to-xml-parsing-with-elementtree/
# Source : http://stackoverflow.com/questions/3545331/how-can-i-get-dictionary-key-as-variable-directly-in-python-not-by-searching-fr
# Source : https://docs.python.org/2/library/stdtypes.html#dict.items
# Source : http://effbot.org/zone/element-iterparse.htm
# Source : http://www.tutorialspoint.com/python/dictionary_keys.htm

import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE
        
        data_set = {} # initializing the dictionary
        
        for event, elem in ET.iterparse(filename): # using iterparse to iterate over the xml
            
            xml_tag = elem.tag # storing the current xml tag
            
            data_set_keys = data_set.keys() # fetching the keys for data set
            
            if xml_tag in data_set_keys: # checking for tag in data set
                
                data_set[xml_tag] += 1 # add to the existing count if tag already present in data set
            
            else:
                
                data_set[xml_tag] = 1 # intialize a new tag to 1 if not present in data set
        
        return data_set # return data set

def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()