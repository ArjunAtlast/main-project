from twitter import Twitter, OAuth
from textblob import TextBlob
import pandas as pd
import re

#Twitter Credentials
token = "3879702192-iePpyi1RBOu4U8GDYWBneJsusMaZtXEKOgtWSql"
secret = "Q51lZIhlpYW0rVwBo9JnqOmnPblhmnuBVKbJBKbHWhYqu"
consumer_key = "Ht5dtcU8D4h6RiPcAUmE792dc"
consumer_secret = "pd1ZfObtM5MfobP6Jwq2oMDC2BYFNWP9Wvodsh7TDp76bBHLOQ"

#initialize twitter api with authentication
tw = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

def get_tweets(hashtags):
    try:
        tweets = tw.search.tweets(q=" OR ".join(hashtags))
        return list(preprocess_tweet(tweet['text']) for tweet in tweets['statuses'])
    except:
        print("Error ")

def preprocess_tweet(tweet):
    """
    Used to preprocess the tweet and remove @tags URLs etc. and convert to lowercase
    """

    #convert tweet to lowercase
    tweet.lower()

    #convert all urls to sting "URL"
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)

    #convert all @username to "AT_USER"
    tweet = re.sub(r'@[^\s]+','AT_USER', tweet)

    #correct all multiple white spaces to a single white space
    tweet = re.sub(r'[\s]+', ' ', tweet)

    #convert "#topic" to just "topic"
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    return tweet

def avg_sentiment(tweets):

    def is_opinion(tweet):
        return (TextBlob(tweet).sentiment.subjectivity >= 0.3)
    
    opinions = list(filter(is_opinion, tweets))

    n = len(opinions)

    if n == 0:
        return 0

    total_sentiment = sum(TextBlob(tweet).sentiment.polarity for tweet in opinions)

    return total_sentiment / n