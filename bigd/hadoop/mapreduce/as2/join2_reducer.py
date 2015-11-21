#!/usr/bin/env python

import sys

# --------------------------------------------------------------------------
tot_count = 0
channel = ''
prev_show = ''
included = ''

for line in sys.stdin:
    line       = line.strip()       #strip out carriage return
    key_value  = line.split('\t')   #split line, into key and value, returns a list

    # Parse key fields
    show   = key_value[0]

    # Parse value fields
    value_fields = key_value[1].split(' ')
    record_type = value_fields[0]
    channel = ''
    count = 0
    if record_type == 'A':
        count = int(value_fields[1])
    else:
        channel = value_fields[1]

    # Group By
    if show != prev_show:
        if included == 'Y':
            print ("%s %d" % (prev_show, tot_count))
        included = ''
        prev_show = show
        tot_count = 0

    # Process value fields
    if record_type == 'A':
        tot_count += count
    if channel == 'ABC':
        included = 'Y'

 
