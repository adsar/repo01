import MapReduce
import sys

"""
Inverted Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence ids
    distinct = {}
    for v in list_of_values:
      distinct[v] = 1
    mr.emit((key, distinct.keys()))

# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
