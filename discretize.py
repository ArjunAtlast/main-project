import pandas as pd
import pickle

dataset_bins = {}

def write_bins():

    global dataset_bins

    # open file for writing in binary mode
    file = open('bins', 'wb')

    # dump values
    pickle.dump(dataset_bins, file)

    # close file
    file.close()


def discretize(dataframe):

    global dataset_bins

    cols = ['compression_ratio', 'cylinder_bore', 'fuel_tank_volume', 'kerb_weight', 'piston_stroke', 'power', 'torque', 'wheelbase']

    num_bins = 8

    for col in cols:

        # find bins
        # bmin = int(df[col].min())
        # bmax = int(df[col].max())

        # bin_size = int((bmax - bmin)/num_bins)

        # create bins
        # bins = list(range(bmin, bmax, bin_size))
        bins = list(map(lambda x: x[0], pd.qcut(dataframe[col].values, num_bins).categories.to_tuples()))

        # save the bins to dict
        dataset_bins[col] = bins

        dataframe[col] = pd.cut(dataframe[col].values, bins, labels=False)
    
    return dataframe
    
df = pd.read_csv("datasets/final.csv")

df = discretize(df)

# write dataset
df.drop(columns=df.columns[0]).to_csv('datasets/final_disc.csv')

# write bins
write_bins()