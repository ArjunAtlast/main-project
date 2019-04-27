from twitter_sentiment import avg_sentiment, get_tweets
from time import sleep
import pickle
import re
import numpy as np

# open the mappings
mappingFile = open('mappings', 'rb')

mappings:dict = pickle.load(mappingFile)

mappingFile.close()

def find_avg_sentiment(row):
    """
    Find average sentiment of an item in dataset
    """

    print("Finding sentiment of " + row['model'])

    hashtags = row['hashtags'].split("|")

    #get tweets
    tweets = get_tweets(hashtags)

    # print(tweets)

    #get avg_sentiment
    avgs = avg_sentiment(tweets)

    # sleep
    sleep(5)

    return avgs

def map_to_value(column_name, index):
    """
    Map id to real value of a column
    """

    global mappings

    if column_name in mappings.keys():

        return mappings[column_name][index]
    
    return index

def feature_list():

    return [
        'abs', 'compression_ratio', 'coupe_type',
        'cylinder_bore', 'doors', 'fuel_tank_volume', 'fuel_type',
        'kerb_weight', 'number_of_cylinders',
        'number_of_gears','number_of_valves_per_cylinder', 'piston_stroke',
        'position_of_cylinders', 'power', 'seats', 'torque', 'wheelbase'
    ]

def beautify_text(text):
    """
    Beautify the sluggified string
    """
    return re.sub(r'[\_\-]+',' ', text).capitalize()

def extract_cols(Y):

    vals = Y.values if hasattr(Y, 'values') else Y

    return np.transpose(vals)