'''
Created on Nov 4, 2014

@author: adrian
'''


def printData(dataFile):
    pos = 0
    with open(dataFile, 'r') as f:
        data = f.read(32)
        while data != "":
            print "pos: %d  = %s" % (pos, data)
            pos += 32
            f.seek(pos)
            data = f.read(32)


def pattern_count(pattern, data):
    print data
    print pattern
    print
    count = 0
    p = 0
    while p < (len(data) - len(pattern)):
        window_start = p
        window_end = p + len(pattern) 
        #print "pattern: %s == [%s] -  p: %d (len %d) - %s" % (pattern, data[window_start:window_end], p, len(data[window_start:window_end]), (data[window_start:window_end] == pattern)) 
        if data[window_start:window_end] == pattern:
            count += 1
        p += 1
    
    return count

def main():
    dataFile = "data/nucleotide_sequence.txt" 
    #dataFile = "data/Vibrio_cholerae.txt" 
    #pattern = "GATACA"  
    #printData(dataFile)
    
    with open(dataFile, 'r') as f:
        data = f.readlines()
    
    pattern = data[1].replace("\n", "")
    count = pattern_count(pattern, data[0].replace("\n", ""))
    
    print count
       
     

if __name__ == '__main__':
    main()