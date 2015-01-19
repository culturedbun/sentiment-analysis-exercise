import sys
import json
import re

# Read the sentiment_file, and build a dictionary of terms and their scores.
def dictFromSentimentFile(sf):
	scores = {}
	for line in sf:
		term, score = line.split('\t')
		scores[term] = int(score)
	#print scores.items()
	return scores

def filterTweet(t):
	et = t.encode('utf-8') # <type: str>
	# Remove punctuations and non-alphanumeric chars from each tweet string
	pattern = re.compile('[^A-Za-z0-9]+')
	et = pattern.sub(' ', et)
	#print encoded_tweet

	words = et.split()

	# Filter unnecessary words
	for w in words:
		if w.startswith("RT") or w.startswith("www") or w.startswith("http"):
			words.remove(w)

	return words

# Derive each tweet's sentiment
def computeTweetSentiment(td, sc):	
	sentiment = 0.0
	words = filterTweet(td)

	# Derive sentiment from each tweet by summing up sentiments of individual words.
	for w in words:
		if w in sc:
			sentiment = sentiment + sc[w]

	#print sentiment
	return sentiment

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	scores = dictFromSentimentFile(sent_file)

	count = {}
	state_sents = []
	max = 0.0
	happiest = ""

	for line in tweet_file:
		sent = 0.0
		response = json.loads(line)

		if (response.get('place') != None):
			if (response['place']['country_code'] == 'US'):
				#print response['place']['full_name'].split(',')[1]
				state = (response['place']['full_name'].split(',')[1]).encode('utf-8').strip()
				#print state
				if "text" in response.keys():
					sent = computeTweetSentiment(response["text"], scores)
					if state in count:
						#print "another " + state, sent
						count[state] = count[state] + sent
					else:
						count[state] = sent
					#print count

	for s in count.keys():
		if count[s] > max:
			max = count[s]
			happiest = s

	print happiest
	

if __name__ == '__main__':
	main()
