# jack elder
# creates dictionary based on csv file for good / bad words

from Stock import *
from dictcreation import *

def create_stock_dict():
    ticker_list = ["MMM","AXP", "AAPL" ,"BA", "CAT","CVX", "CSCO", "KO", "DIS", "DD" ,"XOM","GE","GS","HD",
                   "IBM", "INTC", "JNJ","JPM", "MCD", "MRK", "MSFT","NKE","PFE","PG","TRV", "UTX","UNH","VZ","V","WMT"]

    stock_dict = {}

    for i in range(len(ticker_list)):
        name = ticker_list[i]
        stock = Stock()
        stock_dict[name] = stock

    return stock_dict

def create_sentiment_dictionary():
    file = open("dict.txt", "r")
    sentiment_dictionary = {}
    for line in file:
            s = line.strip()
            sp = s.split(",")
            sentiment_dictionary[sp[0]] = int(sp[1])
    return sentiment_dictionary

def tweetvalue(string):
    tv = 0
    s = string.strip()
    sp = s.split()
    for i in range(len(sp)):
        if sp[i] in sentiment_dict:
            tv += sentiment_dict[sp[i]]
    return tv

def updatestock(string, tv):
    s = string.strip()
    sp = s.split()
    for i in range(len(sp)):
        if sp[i] in stock_dict:
            stock_dict[sp[i]].update(tv)
            print stock_dict[sp[i]]
            print sp[i]
            print stock_dict[sp[i]].shares


def main(string):
    global stock_dict
    stock_dict = create_stock_dict()
    global sentiment_dict
    sentiment_dict = create_sentiment_dictionary()
    updatestock(string, tweetvalue(string))
