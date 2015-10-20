import MapReduce
import sys

"""
unique trimmed nucleotide strings in the Simple Python MapReduce Framework

"""

mr = MapReduce.MapReduce()

# =============================

def mapper(record):
    # key: sequence id, 
    # value: nucleotides
    key = record[0]
    nucleotides = record[1]
    l = len(nucleotides)
    
    mr.emit_intermediate(nucleotides[:l-10], key)

def reducer(key, list_of_values):
    # key: trimmed nucleotides 
    # value: sequence id,

    #print key
    #print list_of_values
       
    
    mr.emit((key))

# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
