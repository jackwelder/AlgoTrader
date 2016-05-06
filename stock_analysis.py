#!/bin/python

from yahoo_finance import *
import datetime
import numpy as np

# date string format: Mon May 02 01:15:47 +0000 2016

tweetDate = "Mon May 02 01:15:47 +0000 2016"

def getStockData(ticker, tweetDate, interval):

	tokens = tweetDate.split()
	dateStr = tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[5]

	startDate = datetime.datetime.strptime(dateStr, '%a %b %d %Y')
	endDate = startDate + datetime.timedelta(days=interval)
	print "Getting data for: " + ticker + " from " + str(startDate.date()) + " to " + str(endDate.date())

	stock = Share(ticker)

	results = stock.get_historical(str(startDate.date()), str(endDate.date()))

	data = []	
	for result in results:
		data.append(float(result['Close']))
		print "Price on " + result['Date'] + " at close was: " + result['Close']


	npData = np.array(data).astype(np.float)
	
	x = np.array(range(len(npData)))
 	m, c = np.polyfit(x, npData, 1)

	print "Slope of regression fit to stock data: " + str(m)



getStockData('AAPL', tweetDate, 5)
