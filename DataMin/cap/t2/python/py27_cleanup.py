import json
from pprint import pprint
import io

inFile = '/media/coursera/data/as/Courses/DataMin/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
outFile = 'yelp_academic_dataset_review_sample_100000.txt'
numReviews = 100000

#with open(inFile) as in_file1:    
#    data1 = json.load(in_file1)
#pprint(data1)

data2 = []
line_count = 0
with open(inFile) as in_file2:
    for line in in_file2:
	line_count += 1
	if line_count > numReviews:
	    break
        data2.append(json.loads(line))

#for d in data2:
    #pprint(d)

out_file1 = open(outFile, "wb+")

# Write Header
out_file1.write("votes_funny\tvotes_useful\tvotes_cool\t")
out_file1.write("user_id\treview_id\tstars\tdate\ttext\ttype\tbusiness_id\n")

for d in data2:
    out_file1.write("{}\t{}\t{}\t".format(d['votes']['funny'], d['votes']['useful'], d['votes']['cool']))    
    out_file1.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(d['user_id'], d['review_id'], d['stars'], d['date'], d['text'].encode('ascii', 'ignore').replace('\t', '  ').replace('\n', '  '), d['type'], d['business_id']))
