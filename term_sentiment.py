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

# Read the tweet_file. Extract each tweet per line. Append to the tweet_data list.
def readTweetFile(tf):
	tt = []
	for line in tf:
		response = json.loads(line)
		if "text" in response.keys():
			tt.append(response["text"])
	return tt

def filterTweet(et):
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

def computeTweetSentiment(td, sc):
	sentiments = []
	
	for t in td:
		sentiment = 0.0
		encoded_tweet = t.encode('utf-8') # <type: str>
		words = filterTweet(encoded_tweet)

		# Derive sentiment from each tweet by summing up sentiments of individual words.
		for w in words:
			if w in sc:
				sentiment = sentiment + sc[w]

		#print sentiment
		sentiments.append(sentiment)
	
	return sentiments
	   
def computeTermSentiment(td, sc, ts):
	idx = 0
	occur = {}

	for t in td:
		words = filterTweet(t.encode('utf-8'))
		#occur = {w: 0 for w in words}
		for w in words:
			occur[w] = 0
		#print occur

	for t in td:
		words = filterTweet(t.encode('utf-8'))
		for w in words:
			occur[w] = occur[w] + 1
			if w not in sc:
				sc[w] = ts[idx]
			else:
				sc[w] = (sc[w] + ts[idx]) / occur[w]  # take the average

			#print(w + " occur: ", occur[w])
			print w + " ", sc[w]

		#print "=======tweet " + str(idx)
		idx = idx + 1

	return sc



def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	
	scores = dictFromSentimentFile(sent_file)
	#print scores.items()

	tweet_data = readTweetFile(tweet_file)

	tweet_sentiments = computeTweetSentiment(tweet_data, scores)
	'''for s in tweet_sentiments:
		print s'''
	
	'''for i in range(len(tweet_sentiments)):
		print tweet_sentiments[i]'''

	computeTermSentiment(tweet_data, scores, tweet_sentiments)
		   

if __name__ == '__main__':
	main()
