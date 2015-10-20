import sys
import json
import csv

def hw():
    print 'Problem 5: Which State is happiest?'

def lines(fp):
    items = fp.readlines()
    #print str(len(items))
    return items

def est_sent(t, scores, term_score):
    s = 0
    terms = t.split()
    #print terms
    for term in terms:
	if term in scores:
	    s = s + scores[term]
    c = len(terms)
    mean = s / float(c)

    for term in terms:
	if term not in scores:
	    if term in term_score:
	        term_score[term].append(mean)
	    else:
		term_score[term] = [mean]
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
    readCsv('us_states.csv')
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

#    for line in tweet_lines:
#        stream_msg = json.loads(line)
#        if "text" in stream_msg:
#	    if "place" in stream_msg:
#		if 'United States' in str(stream_msg['place']):
#            	    print eval_sent(stream_msg['text'], scores)
    states = {}
    sts = {}
    statemap = {}
    for s in sl:
        states[s[0]] = []
	sts[s[1]] = []
	statemap[s[1]]=s[0]

    term_score = {}
    for line in tweet_lines:
        stream_msg = json.loads(line)
        if "text" in stream_msg:
            est_sent(stream_msg['text'].lower(), scores, term_score)

    for k in term_score:
	v = term_score[k]
        ts = (sum(v)/float(len(v)))
	if (k in states): states[k].append(ts)
	if (k in sts): sts[k].append(ts)
    for s in sl:
        if len(sts[s[1]]) > 0:
	    states[statemap[s[1]]].extend(sts[s[1]])
    mstate=''
    m=0
    for s in sl:
	v = states[s[0]]
	if len(v) > 0:
            ss = (sum(v)/float(len(v)))
            if (mstate == '') or (ss> m): 
                mstate=s[0]
	        m=ss
    print mstate, m

if __name__ == '__main__':
    main()
