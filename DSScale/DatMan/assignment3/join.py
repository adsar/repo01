import MapReduce
import sys

"""
Relational Join in the Simple Python MapReduce Framework

SELECT * 
FROM Orders, LineItem 
WHERE Order.order_id = LineItem.order_id
"""

mr = MapReduce.MapReduce()

# =============================

def mapper(record):
    # key: relation name
    # value: row content
    mr.emit_intermediate(record[1], record)

def reducer(key, list_of_values):
    # key: join key
    # value: relation

    #print key
    #print list_of_values
    
    for v in list_of_values[1:]:
        mr.emit(list_of_values[0]+v)

# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
