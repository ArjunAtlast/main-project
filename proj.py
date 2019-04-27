import pandas as pd
from twitter_sentiment import avg_sentiment, get_tweets
from time import sleep


def find_avg_sentiment(row):

    print("Finding sentiment of " + row['model'])

    hashtags = row['hashtags'].split("|")

    #get tweets
    tweets = get_tweets(hashtags)

    # print(tweets)

    #get avg_sentiment
    avgs = avg_sentiment(tweets)

    # sleep
    sleep(10)

    return avgs


df = pd.read_csv("http://localhost:8080/predicted.csv")

df['sentiment'] = df.apply(lambda row: find_avg_sentiment(row), axis=1)

df.to_csv('final.csv')
