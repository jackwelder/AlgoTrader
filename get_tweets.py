# Chris Davis
# script to grab tweets from Twitter API
# stores raw tweet data in ~/tweet_data/

import sys, requests, urllib, base64, csv

twitter_consumer_key='zvXrkff1xaipt4iPiQr7Q'
twitter_consumer_secret='a2uciWCEkSXs0fvbRDNspqECr6m8pDzFyJcxdGrDE'

def get_credentials():
    creds = {}

    creds['consumer_key']    =  twitter_consumer_key
    creds['consumer_secret'] = twitter_consumer_secret


    print "Using the following credentials:"
    print "\tTwitter consumer key:", creds['consumer_key']
    print "\tTwitter consumer secret:", creds['consumer_secret']


    return creds

def oauth(credentials):

    print "Requesting bearer token from Twitter API"

    try:
        # Encode credentials
        encoded_credentials = base64.b64encode(credentials['consumer_key'] + ':' + credentials['consumer_secret'])
        # Prepare URL and HTTP parameters
        post_url = "https://api.twitter.com/oauth2/token"
        parameters = {'grant_type' : 'client_credentials'}
        # Prepare headers
        auth_headers = {
            "Authorization" : "Basic %s" % encoded_credentials,
            "Content-Type"  : "application/x-www-form-urlencoded;charset=UTF-8"
            }

        # Make a POST call
        results = requests.post(url=post_url, data=urllib.urlencode(parameters), headers=auth_headers)
        response = results.json()

        # Store the access_token and token_type for further use
        auth = {}
        auth['access_token'] = response['access_token']
        auth['token_type']   = response['token_type']

        print "Bearer token received"
        return auth

    except Exception as e:
        print "Failed to authenticate with Twitter credentials:", e
        print "Twitter consumer key:", credentials['consumer_key']
        print "Twitter consumer secret:", credentials['consumer_secret']
        sys.exit()


def search(search_term, num_tweets, auth):
    # This collection will hold the Tweets as they are returned from Twitter
    collection = []
    # The search URL and headers
    url = "https://api.twitter.com/1.1/search/tweets.json"
    search_headers = {
        "Authorization" : "Bearer %s" % auth['access_token']
        }
    max_count = 100
    next_results = ''
    # Can't stop, won't stop
    while True:
        print "Search iteration, Tweet collection size: %d" % len(collection)
        count = min(max_count, int(num_tweets)-len(collection))

        # Prepare the GET call
        if next_results:
            get_url = url + next_results
        else:
            parameters = {
                'q' : search_term,
                'count' : count,
                'lang' : 'en'
                }
            get_url = url + '?' + urllib.urlencode(parameters)

        # Make the GET call to Twitter
        results = requests.get(url=get_url, headers=search_headers)
        response = results.json()

        # Loop over statuses to store the relevant pieces of information
        for status in response['statuses']:
            text = status['text'].encode('utf-8')

            # Filter out retweets
            if status['retweeted'] == True:
                continue
            if text[:3] == 'RT ':
                continue

            tweet = {}
            # Configure the fields you are interested in from the status object
            tweet['text']        = text
            tweet['id']          = status['id']
            tweet['time']        = status['created_at'].encode('utf-8')
            tweet['screen_name'] = status['user']['screen_name'].encode('utf-8')

            collection    += [tweet]

            if len(collection) >= num_tweets:
                print "Search complete! Found %d tweets" % len(collection)
                return collection

        if 'next_results' in response['search_metadata']:
            next_results = response['search_metadata']['next_results']
        else:
            print "Uh-oh! Twitter has dried up. Only collected %d Tweets (requested %d)" % (len(collection), num_tweets)
            print "Last successful Twitter API call: %s" % get_url
            print "HTTP Status:", results.status_code, results.reason
            return collection

def write(ticker, raw_tweets):
    filename = 'tweet_data/' + str(ticker) + '.csv'

    count_before = 0
    try:
        in_file = open(filename, 'rb')
        reader = csv.reader(in_file, delimiter=',')

        for row in reader:
            count_before +=1

        in_file.close()

    except Exception as e:
        print "No File found, creating new file.", e

    finally:
        out_file = open(filename, 'ab')
        writer = csv.writer(out_file, delimiter=',')
        writer.writerow(["id", "text", "screen_name", "time"])

        count_added = 0
        for tweet in raw_tweets:
            writer.writerow([tweet['id'], tweet['text'], tweet['screen_name'], tweet['time']])
            count_added += 1

        out_file.close()

        print str(count_before) + " tweets in " + filename + " before search."
        print "Succesfully added " + str(count_added) + " tweets to " + filename
        print filename + " now contains " + str(count_before + count_added) + " tweets"





def get_tweets(ticker, search_size):
    credentials = get_credentials() # Get the Twitter bearer token
    auth = oauth(credentials)       # Authenticate with oauth
    raw_tweets = search('$' + str(ticker) , search_size, auth) # Pull Tweets down from the Twitter API
    write(ticker, raw_tweets)   # write tweets to file




ticker_list = ['AAPL', 'GOOG', 'MSFT', 'XOM', 'BRK.A', 'WFC', 'JNJ', 'GE', 'CHL', 'JPM','NVS', 'FB', 'WMT', 'PTR', 'PG']
for ticker in ticker_list:
    print "Gathering tweets for " + ticker
    get_tweets(ticker, 1000)
    print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
