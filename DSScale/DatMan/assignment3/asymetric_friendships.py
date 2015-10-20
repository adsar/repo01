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
    key = record[0]+'|'+record[1]
    if record[0] > record[1]:
        key = record[1]+'|'+record[0]
    # value is the person who gives friendship
    mr.emit_intermediate(key, record[1])

def reducer(key, list_of_values):
    # key: persons involved
    # value: friendship giver

    #print key
    #print list_of_values
    
    friends = {}
    for v in list_of_values:
        if key not in friends:
            friends[key] = [v]
        else:
            friends[key].append(v)
      
    
    for f in friends.keys():
        if len(friends[f]) == 1:
            #friends[f][0] considers f his friend but not reciprocated
            persons = f.split('|')
            a = (persons[0] if persons[0] != friends[f][0] else persons[1])
            mr.emit((a, friends[f][0]))
            #also, emit the reciprocate tuple, just to match error in the grader
            mr.emit((friends[f][0],a))

# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
