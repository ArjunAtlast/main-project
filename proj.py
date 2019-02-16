"""
Python Sentiment Analysis using TextBlob
"""
from textblob import TextBlob
import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#read dataset with target and tweet columns
dataframe = pd.read_csv("http://127.0.0.1:8080/sentiment140.csv", encoding = "ISO-8859-1", header = None).iloc[:, [0, 5]].sample(frac=1).reset_index(drop=True)

#add headers
dataframe.columns = ["target", "tweet"]

def preprocess_tweet(tweet):
    """
    Used to preprocess the tweet and remove @tags URLs etc. and convert to lowercase
    """
    print("Preprocessing tweet...")

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

def replace_sentiment(sentiment):
    """
    Replace sentiment value as -1 for negetive, 0 for neutral and 1 for positive
    """
    if (sentiment == 0):
        return -1
    elif (sentiment == 2):
        return 0
    else:
        return 1

def match_noun(tag):
    """
    Match tags that are nouns
    """
    return (tag[1]=='NN' or tag[1]=='NNS') and tag[0] != 'AT_USER' and tag[0] != 'URL'

def match_adjective(tag):
    """
    Match tags that are adjectives
    """

    return tag[1] == 'JJ' or tag[1] == 'JJR' or tag[1] == 'JJS'

def match_adverb(tag):
    """
    Match tags that are adverbs
    """

    return tag[1] == 'RB' or tag[1] == 'RBR' or tag[1] == 'RBS'

def extract_words(tag):
    """
    Extract only words from the word-tag tuple
    """
    #return singularized word
    if tag != None:
        return tag[0].singularize()
    #return None itself
    return 'NULL'

def feature_extract(tweet):
    """
    Extract features from tweet
    """
    print("Extracting features...")
    #crete Blob
    blob = TextBlob(tweet)

    #POS tagging
    tags = blob.tags

    #Extract first 2 Nouns
    nouns = list(filter(match_noun, tags))[:2]

    #Extract first 5 Adjectives
    adjectives = list(filter(match_adjective, tags))[:4]

    #Extract first 2 adverbs
    adverbs = list(filter(match_adverb, tags))[:2]

    return np.array(list(map(extract_words, nouns + adjectives + adverbs)))

#extract features from preprocessed tweets into array
features = np.array(np.stack(dataframe['tweet'][:10].apply(preprocess_tweet).apply(feature_extract).values))

#target sentiment into array
sentiments = np.array(dataframe['target'][:10].apply(replace_sentiment).values)

#split into train and test set
X_train, X_test, y_train, y_test = train_test_split(features, sentiments, test_size=0.2, random_state=42)

#create random forest
rf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)

#fit Random Forest
rf.fit(X_train, y_train)

print(rf.score(X_test, y_test))