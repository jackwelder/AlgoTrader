# jack elder
# creates dictionary based on csv file for good / bad words

from stock import *
import csv
from dictionarycreation import *
from tweet import Tweet

companies = ["AAPL", "BRK.A", "CHL", "FB", "GE", "GOOG", "JNJ", "JPM", "MSFT", "NVS", "PG", "PTR", "WFC", "WMT", "XOM"]

def parse_csv(ticker):
    filename = 'tweet_data/' + str(ticker) + '.csv'

    tweet_list = []

    in_file = open(filename, 'r')
    reader = csv.reader(in_file, delimiter=',')

    for row in reader:
        tweet = Tweet(ticker, row[0], row[1], row[2], row[3])
        tweet_list.append(tweet)
    in_file.close()
    return tweet_list

def create_sentiment_dictionary():
    file = open("dictionary", "r")
    sentiment_dictionary = {}
    for line in file:
            s = line.strip()
            sp = s.split(",")
            sentiment_dictionary[sp[0]] = int(sp[1])
    return sentiment_dictionary


def increment(ticker):
    sentiment_dict = create_sentiment_dictionary()
    tweet_list = parse_csv(ticker)
    stock = Stock(ticker)
    for tweet in tweet_list:
        s = tweet.body.strip()
        sp = s.split()
        for i in range(len(sp)):
            if sp[i] in sentiment_dict:
                stock.value += sentiment_dict[sp[i]]
    print stock

def main():
    for stock in companies:
        increment(stock)

main()