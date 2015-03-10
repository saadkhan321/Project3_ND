#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""
# Source : http://stackoverflow.com/questions/8749158/removing-duplicates-from-dictionary
# Source : http://www.tutorialspoint.com/python/dictionary_keys.htm
# Source : https://docs.python.org/2/library/sets.html#example
# Source : http://en.wikibooks.org/wiki/Python_Programming/Sets
# Source : http://www.dotnetperls.com/remove-duplicates-list-python



def get_user(element): # method that returns the uid from the tag provided as input
    return element.get('uid')


def process_map(filename):
    users = set()
    
    for _, element in ET.iterparse(filename):
        # pass
        if element.tag == "node" or element.tag == "way" or element.tag == "relation": # checking for tag which will contain uids
        
            user_id = get_user(element) # extracting the uid from the get_user method
            users.add(user_id) # adding it to the users set
   
    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()