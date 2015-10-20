import sys
import json
import csv

def hw():
    print 'Problem 5: Which State is happiest?'

def lines(fp):
    items = fp.readlines()
    #print str(len(items))
    return items

def eval_sent(t, scores):
    s = 0
    terms = t.split()
    #print terms
    for term in terms:
	if term in scores:
	    s = s + scores[term]
    return s

def readCsv(name):
    with open(name, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
	    print '["%s","%s"],' % (row[0], row[1])
sl = [["Alabama","AL"],
["Alaska","AK"],
["Arizona","AZ"],
["Arkansas","AR"],
["California","CA"],
["Colorado","CO"],
["Connecticut","CT"],
["Delaware","DE"],
["Florida","FL"],
["Georgia","GA"],
["Hawaii","HI"],
["Idaho","ID"],
["Illinois","IL"],
["Indiana","IN"],
["Iowa","IA"],
["Kansas","KS"],
["Kentucky","KY"],
["Louisiana","LA"],
["Maine","ME"],
["Maryland","MD"],
["Massachusetts","MA"],
["Michigan","MI"],
["Minnesota","MN"],
["Mississippi","MS"],
["Missouri","MO"],
["Montana","MT"],
["Nebraska","NE"],
["Nevada","NV"],
["New Hampshire","NH"],
["New Jersey","NJ"],
["New Mexico","NM"],
["New York","NY"],
["North Carolina","NC"],
["North Dakota","ND"],
["Ohio","OH"],
["Oklahoma","OK"],
["Oregon","OR"],
["Pennsylvania","PA"],
["Rhode Island","RI"],
["South Carolina","SC"],
["South Dakota","SD"],
["Tennessee","TN"],
["Texas","TX"],
["Utah","UT"],
["Vermont","VT"],
["Virginia","VA"],
["Washington","WA"],
["West Virginia","WV"],
["Wisconsin","WI"],
["Wyoming","WY"]]

def main():
    #readCsv('us_states.csv')
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    sent_lines = lines(sent_file)
    tweet_lines = lines(tweet_file)
    scores = {} # initialize an empty dictionary
    for line in sent_lines:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    # print scores.items() # Print every (term, score) pair in the dictionary

    states = {}
    for s in sl:
        states[s[0]] = []

    for line in tweet_lines:
        stream_msg = json.loads(line)
        if "text" in stream_msg:
	    if "place" in stream_msg:
		if 'United States' in str(stream_msg['place']):
            	    ss = eval_sent(stream_msg['text'].lower(), scores)
		    for i in range(len(sl)):
                        if sl[i][0] in str(stream_msg['place']): states[sl[i][0]].append(ss)
                        elif sl[i][1] in str(stream_msg['place']): states[sl[i][0]].append(ss)

    ssd={}
    mst=''
    m=0
    for s in sl:
	v = states[s[0]]
	if len(v) > 0:
            ssd[s[0]] = (sum(v)/float(len(v)))
            if (mst == '') or (ssd[s[0]]> m): 
                mst=s[1]
	        m=ssd[s[0]]
    print mst
#    print
#    for s in sl:
#	if s[0] in ssd:
#            print s[0], ssd[s[0]]

if __name__ == '__main__':
    main()
