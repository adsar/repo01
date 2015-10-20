import oauth2 as oauth
import urllib2 as urllib
import json

# See assignment1.html instructions or README for how to get these credentials

api_key = "ukb6l0DfN9kswHaTO046Rxtih"
api_secret = "0ksKjCOL7Nad74fk7ULLrpDaCX8roT2eRWktMunbuZPDoEnzBE"
access_token_key = "2254382916-XVKzyvGdFb4p2fnqOLFNmzt3RoIgCERkK7qYqhc"
access_token_secret = "58Lx0UfDYLCOU90DCFDUKN3luG1PR0H9Uy6LjzO0gxUtQ"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  #url = "https://api.twitter.com/1.1/geo/search.json?query=California"
  #url = "https://stream.twitter.com/1.1/statuses/filter.json?language=en&track=us"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip().encode('utf-8', errors='ignore')
#    stream_msg = json.loads(line)
#    if "text" in stream_msg:
#        if "place" in stream_msg:
#	    if 'United States' in str(stream_msg['place']):
#	        print stream_msg
if __name__ == '__main__':
  fetchsamples()

