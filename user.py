# title: user.py
# author: nick fiacco
#
# description:
# this program allows you to run a query on all of a user's previous
# tweets, given their StockTwits user name, the number of tweets to
# fetch, and the output file name.
#
# dependencies:
# StockTwits API access
# requests
# json
#
# example usage: python user.py TrustedBinary 1000 output.txt

from __future__ import print_function
import requests
import json
import sys


def user():
	# username from which we will fetch tweets
	user = sys.argv[1]

	# number of tweets to fetch
	count = int(sys.argv[2])

	# output file name
	filename = sys.argv[3]

	# output file
	f = open(filename,'w')

	# initial api request url
	url = "https://api.stocktwits.com/api/2/streams/user/" + user + ".json"

	response = requests.get(url)

	json_data = response.json()

	oldest_id = 0

	for tweet in json_data['messages']:
		print(tweet['body'], file = f)
		print("", file = f)
		oldest_id = int(tweet['id'])


	while True:
		# generate new urls for older tweets using tweet ids
		new_url  = "https://api.stocktwits.com/api/2/streams/user/" + user + ".json?max=" + str(oldest_id)

		response = requests.get(new_url)

		if response == "<Response [500]>":
			print("No more tweets\n")
			break

		if count <= 0:
			print("Reached maximum tweet amount\n")
			break

		json_data = response.json()

		for tweet in json_data['messages']:
			print(tweet['body'], file = f)
			print("", file = f)
			oldest_id = int(tweet['id'])

		count -= 30

	f.close()

user()






