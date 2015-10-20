import sys
import json

def hw():
    print 'Problem 6: Top ten hash tags'

def lines(fp):
    items = fp.readlines()
    #print str(len(items))
    return items


def main():
    tweet_file = open(sys.argv[1])
    tweet_lines = lines(tweet_file)

    term_freq = {}
    for line in tweet_lines:
        stream_msg = json.loads(line)
        if "entities" in stream_msg:
	    if 'hashtags' in str(stream_msg['entities']):
	        hashs = stream_msg['entities']['hashtags']
	        for h in hashs:
		    t = h['text']
		    if (len(t)>0) and (t in term_freq):
			term_freq[t] += 1
		    else:
			term_freq[t] = 1

    k = 10
    for w in sorted(term_freq, key=term_freq.get, reverse=True):
	v = term_freq[w]
        print "%s %d" % (w, v)
	k = k - 1
	if k == 0: break


if __name__ == '__main__':
    main()
