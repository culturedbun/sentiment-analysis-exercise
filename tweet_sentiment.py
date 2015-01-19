import sys
import json
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines())) # File is closed right after fp.readLines(). 

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)

    # Read the sentiment file and build dictionary
    scores = {} # initialize an empty dictionary
    for line in sent_file:
    	term, score = line.split("\t") # The file is tab delimited.
    	scores[term] = int(score)

    #print scores.items() # Print every (term, score) pair in the dictionary. As a list.

    # Read the tweet file: "output.txt"
    tweet_data = []
    for line in tweet_file:
        response = json.loads(line)
        '''if "lang" in response.keys():
            print response["lang"]'''
        if "text" in response.keys():
            tweet_data.append(response["text"])
            #print response["text"]
        #print response.keys()

    #print len(tweet_data)

    # For each tweet
    for t in tweet_data:
        total = 0
        # Convert from <type 'unicode'> to <type 'str'>
        encoded_t = t.encode('utf-8')

        words = encoded_t.split()
        # print (str(words)) 

        for w in words:
            if w.startswith("RT") or w.startswith("www") or w.startswith("http"):
                words.remove(w)
        
        # Filtered out non alpha-numeric characters, including @, punctuations.
        pattern = re.compile('[^A-Za-z0-9]+')
        words = [pattern.sub("", w) for w in words] # Sans lambda
        #print words

        # Sum up the sentiment of words in a tweet.
        for w in words:
            if w in scores:
                total = total + scores[w]

        print '%0.2f' % total


if __name__ == '__main__':
    main()
