import MapReduce
import sys

"""
Friend count in social network in the Simple Python MapReduce Framework

"""

mr = MapReduce.MapReduce()

# =============================

def mapper(record):
    # key: person a
    # value: person b (friend)
    mr.emit_intermediate(record[0], 1)

def reducer(key, list_of_values):
    # key: person
    # value: 1

    #print key
    #print list_of_values
    
    friend_count = 0
    for v in list_of_values:
        friend_count += v
    
    mr.emit((key, friend_count))

# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
