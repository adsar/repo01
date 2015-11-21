#!/usr/bin/env python

import sys

for line in sys.stdin:
    line       = line.strip()      #strip out carriage return
    key_value  = line.split(",")   #split line, into key and value, returns a list
    show     = key_value[0]        #key is first item in list
    val = key_value[1].strip()

    if val.isdigit():
        record_type = 'A'   
    else:
        record_type = 'B'   
    #make sure that all the records that need to be processed together
    #have exactly the same key. Because even if you use only 1 reduce task
    #records with different key will be processed far appart, ** NOT in sort order **
    # Remember, map-reduce 'shuffles' the records, it doesn't sort them,
    # shuffliing means grouping the keys together, like with a hashing function
    # but not sorting them !!!!!!!!!!!!!
    print( '%s\t%s %s' % (show, record_type, val) ) 

#Note that Hadoop expects a tab to separate key value
#but this program assumes the input file has a ',' separating key value
