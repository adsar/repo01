import sys
import json

def hw():
    print 'Problem 3: Derive the sentiment of new terms'

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
    term_score = {}
    for line in tweet_lines:
        stream_msg = json.loads(line)
        if "text" in stream_msg:
            est_sent(stream_msg['text'].lower(), scores, term_score)

    for k in term_score:
	v = term_score[k]
        print "%s %f" % (k, sum(v)/float(len(v)))

if __name__ == '__main__':
    main()
