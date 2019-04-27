import pandas as pd
df = pd.read_csv('dataset.csv')


def fill_null(row):

    for col in row.keys():

        if row.isnull()[col]:

            row[col] = df[col].mode()[0]
    
    return row

df = df.transform(lambda row: fill_null(row), axis=1)

df.to_csv('dataset.csv', index=False)