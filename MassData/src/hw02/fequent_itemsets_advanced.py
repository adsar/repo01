'''
Created on Oct 22, 2014

@author: adrian
'''

import numpy as np

def pcy():
    int_size = 4
    second_pass_hashtable_entry_size = 12
    
    frequent_pairs = 1000000
    memory_size = np.array([500000000, 100000000, 500000000, 200000000])
    cold_pairs = np.array([3200000000, 120000000, 5000000000, 1600000000])
    
    for i in range(len(memory_size)):
        S = memory_size[i]
        P = cold_pairs[i]
        firstpass_pair_hashtable_size = S / int_size
        prob_of_frequent_bucket = float(frequent_pairs) / firstpass_pair_hashtable_size
        cold_pairs_in_frequent_buckets = P * prob_of_frequent_bucket
        secondpass_hastable_size = cold_pairs_in_frequent_buckets * second_pass_hashtable_entry_size
        print "S=%s, P=%s, 2nd pass hashtable size = %s    -   Diff = %.3f" % ("{:,}".format(S), "{:,}".format(P), "{:,}".format(int(secondpass_hastable_size)), (secondpass_hastable_size-S)/S)
    
    return

def main():
    pcy()


if __name__ == '__main__':
    main()