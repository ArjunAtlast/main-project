"""
Twitter Sentiment Analysis
"""
from textblob import TextBlob
import re

#Twitter Credentials
token = "3879702192-iePpyi1RBOu4U8GDYWBneJsusMaZtXEKOgtWSql"
secret = "Q51lZIhlpYW0rVwBo9JnqOmnPblhmnuBVKbJBKbHWhYqu"
consumer_key = "Ht5dtcU8D4h6RiPcAUmE792dc"
consumer_secret = "pd1ZfObtM5MfobP6Jwq2oMDC2BYFNWP9Wvodsh7TDp76bBHLOQ"

#initialize twitter api with authentication
tw = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

#find tweets with #Baleno tag
tweets = tw.search.tweets(q="#vwpolo")


total_polarity = 0
n = 0

def preprocess_tweet(tweet):
    """
    Used to preprocess the tweet and remove @tags URLs etc. and convert to lowercase
    """

    #convert tweet to lowercase
    tweet.lower()

    #convert all urls to sting "URL"
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)

    #convert all @username to "AT_USER"
    tweet = re.sub('@[^\s]+','AT_USER', tweet)

    #correct all multiple white spaces to a single white space
    tweet = re.sub('[\s]+', ' ', tweet)

    #convert "#topic" to just "topic"
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    return tweet

for tweet in tweets['statuses']:

    #get tweet text
    text = preprocess_tweet(tweet['text'])

    #convert to text blob for sentiment analysis
    blob = TextBlob(text)
    
    #get sentiment of the blob
    sentiment = blob.sentiment

    #if text is an opinion
    if sentiment.subjectivity > 0.4:
        
        #increment n
        n+=1

        #extract polarity
        polarity = sentiment.polarity
        
        #add to total polarity
        total_polarity += polarity

# find the average polarity and round upto 8 decimal places
avg_polarity = round(total_polarity/n, 8)

print(avg_polarity)