import urllib
import json

# Put in for loop to output 10 pages
response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft")
pyresponse = json.load(response)
#print pyresponse

#print type(pyresponse)  # A dict
print pyresponse.keys()
#print pyresponse["next_page"]
print pyresponse["page"]
#print pyresponse["results"]

#print type(pyresponse["results"]) # A list

results = pyresponse["results"]
#print type(results[0]) # a dict

#print type(results[0].keys())
print results[0].keys()
print results[0]["text"]

for i in range(10):
	print results[i]["text"]