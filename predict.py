import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
import numpy as np

# read structured dataset
train = pd.read_csv('http://localhost:8080/out_relation.csv')

train_set = train.drop(columns=["brand", "model", "generation"])

# read dataset with null values
df = pd.read_csv('http://localhost:8080/out.csv')

predict_set = df.drop(columns=["brand", "model", "generation", "hashtags"])

# allowed cols
cols = ["power","compression_ratio", "cylinder_bore", "fuel_tank_volume", "kerb_weight", "piston_stroke", "torque", "number_of_cylinders", "wheelbase"]

# select only needed rows from training dataset
train_df = train[cols]

predict_df = df[cols]

def create_reg(dataset, predict_column):

    X = dataset.drop(columns=[predict_column])
    y = dataset[predict_column]

    reg = LinearRegression().fit(X=X, y=y)

    return reg

def predict_col(predictor, row, class_col):

    if (row.isnull()[class_col] and row.isnull().sum() < 2):
        pred = row.drop(labels=[class_col]).values.reshape(1,-1)
        row[class_col] = predictor.predict(pred)

    return row[class_col]

def create_classifier(dataset, predict_column):
    X = dataset.drop(columns=[predict_column])
    y = dataset[predict_column]

    clf = SVC(gamma="auto")
    clf.fit(X,y)

    return clf

# Predict torque
# torque depend on power

torque_reg = create_reg(train_df[['power', 'torque']], 'torque')

df['torque'] = predict_df[['power', 'torque']].apply(lambda row: predict_col(torque_reg, row, 'torque'), axis=1)

# predict cylinder_bore
cylinder_bore_reg = create_reg(train_df[['fuel_tank_volume', 'cylinder_bore']], 'cylinder_bore')

df['cylinder_bore'] = predict_df[['fuel_tank_volume', 'cylinder_bore']].apply(lambda row: predict_col(cylinder_bore_reg, row, 'cylinder_bore'), axis=1)

# predict fuel tank volume

fuel_tank_volume_reg = create_reg(train_df[['fuel_tank_volume', 'cylinder_bore']], 'fuel_tank_volume')

df['fuel_tank_volume'] = predict_df[['fuel_tank_volume', 'cylinder_bore']].apply(lambda row: predict_col(fuel_tank_volume_reg, row, 'fuel_tank_volume'), axis=1)

# reinit predict df
predict_df = df[cols]

# predict piston stroke

piston_stroke_reg = create_reg(train_df[['fuel_tank_volume', 'cylinder_bore', 'piston_stroke']], 'piston_stroke')

df['piston_stroke'] = predict_df[['fuel_tank_volume', 'cylinder_bore', 'piston_stroke']].apply(lambda row: predict_col(piston_stroke_reg, row, 'piston_stroke'), axis=1)

# print(df['piston_stroke'].isnull().sum())

# reinit predict dataframe
predict_df = df[cols]

complete_cols = ['power','torque','fuel_tank_volume', 'cylinder_bore', 'piston_stroke', 'compression_ratio']
# predict compression_ratio
compression_ratio_reg = create_reg(train_df[complete_cols], 'compression_ratio')

df['compression_ratio'] = predict_df[complete_cols].apply(lambda row: predict_col(compression_ratio_reg, row, 'compression_ratio'), axis=1)

# print(df['compression_ratio'].isnull().sum())

# reinit predict dataframe
predict_df = df[cols]

# predict kerb_weight

# first predict from wheelbase

kerb_weight_reg = create_reg(train_df[['wheelbase', 'kerb_weight']], 'kerb_weight')

df['kerb_weight'] = predict_df[['wheelbase', 'kerb_weight']].apply(lambda row: predict_col(kerb_weight_reg, row, 'kerb_weight'), axis=1)

# predict the rest using all columns

# add kerb_weight to complete cols
complete_cols.append('kerb_weight')

kerb_weight_reg = create_reg(train_df[complete_cols], 'kerb_weight')

df['kerb_weight'] = predict_df[complete_cols].apply(lambda row: predict_col(kerb_weight_reg, row, 'kerb_weight'), axis=1)

# print(df['kerb_weight'].isnull().sum())

# predict wheelbase from kerb_weight

wheelbase_reg = create_reg(train_df[['wheelbase', 'kerb_weight']], 'wheelbase')

df['wheelbase'] = predict_df[['wheelbase', 'kerb_weight']].apply(lambda row: predict_col(wheelbase_reg, row, 'wheelbase'), axis=1)

# extend complete cols
complete_cols.append("wheelbase")

# predict categories
to_predict = ["number_of_cylinders", "number_of_valves_per_cylinder", "seats"]

for p_col in to_predict:
    # append new col to complete cols
    complete_cols.append(p_col)
    clf = create_classifier(train_set[complete_cols], p_col)
    df[p_col] = predict_set[complete_cols].apply(lambda row: predict_col(clf, row, p_col), axis=1)


df.to_csv("datasets/predicted.csv")