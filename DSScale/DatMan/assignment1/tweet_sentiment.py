import sys
import json

def hw():
    print 'Problem 2: Derive the sentiment of each tweet'

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

def main():
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
    for line in tweet_lines:
        stream_msg = json.loads(line)
        if "text" in stream_msg:
            print eval_sent(stream_msg['text'].lower(), scores)
	else:
	    print 0

if __name__ == '__main__':
    main()
