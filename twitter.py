#!/usr/bin/env python3

# Title: Twitter Scraper
# Author: Nick Fiacco
# Date: 4/4/2016

# Arguments: 
#	ticker
#	numTweets

# Example Usage: python twitter.py AAPL 10

# Description: prints the message body of the most recent number
# of tweets specified with the ticker specified

import requests
import json
import sys

ticker = sys.argv[1]

number = sys.argv[2]

url = "https://api.stocktwits.com/api/2/streams/symbol/" + ticker + ".json?limit=" + number

response = requests.get(url)

json_data = response.json()

tweets = json_data["messages"]

for tweet in tweets:
	print(tweet["body"] + "\n")

