#!/usr/bin/env python3

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

