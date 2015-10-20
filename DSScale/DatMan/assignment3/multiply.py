import MapReduce
import sys

"""
Matrix multiplication in the Simple Python MapReduce Framework

"""

mr = MapReduce.MapReduce()

# =============================
n = 5

def mapper(record):
    # key: matrix, i, j 
    # value: value
    matrix = record[0]
    i = record[1]
    j = record[2]
    v = record[3]

    for k in range(n):
        if matrix == 'a':
            key = "{}-{}".format(i,k)
            mr.emit_intermediate(key, [j, v])
        else:
            key = "{}-{}".format(k,j)
            mr.emit_intermediate(key, [i, v])
        #print key, [k, v]

def reducer(key, list_of_values):
    # key: i, j 
    # value: k, value

    #print key, list_of_values
    
    i = int(key.split('-')[0])
    j = int(key.split('-')[1])
    
    values = {}
    prod = 0
    for v in list_of_values:
        k = v[0]
        if k not in values:
            values[k] = v[1]
        else:
            prod += (values[k] * v[1])
    if prod != 0:
        mr.emit((i, j, prod))

# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
