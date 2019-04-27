import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spec_calculator import SpecCalculator

df = pd.read_csv('dataset.csv').drop(columns=['brand', 'model', 'generation', 'hashtags'])

msk = np.random.rand(len(df)) < 0.8

train = df[msk]

test = df[~msk]

base_col = 'power'

X_train = train[[base_col, 'sentiment']]
Y_train = train.drop(columns=[base_col, 'sentiment'])

X_test = test[[base_col, 'sentiment']]
Y_test = test.drop(columns=[base_col, 'sentiment'])


max_points = []
min_points = []
mean_points = []

feats = {}

for col in Y_train.columns:
    feats[col] = []

x_points = list(range(150, 300))

for i in x_points:

    sc = SpecCalculator(16, i)

    sc.fit(X_train, Y_train)

    max_score, min_score, mean_score = sc.score(X_test, Y_test)

    max_points.append(max_score)
    min_points.append(min_score)
    mean_points.append(mean_score)

    # for col,score in sc.score_each(X_test, Y_test):
    #     feats[col].append(score)

# setup plot
plt.xlabel('n_estimators')
plt.ylabel('Accuracy')

plt.plot(x_points, max_points)
plt.plot(x_points, min_points)
plt.plot(x_points, mean_points)

legends = ['max score', 'min score', 'mean score']

# for k,v in feats.items():
#     plt.plot(x_points, v)
#     legends.append(k)

plt.legend(legends, loc='upper left')

plt.show()

# each
# for k,v in feats.items():
#     plt.ylabel(k)
#     plt.plot(x_points, v)
#     plt.show()
