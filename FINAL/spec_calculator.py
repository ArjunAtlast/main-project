from sklearn.ensemble import RandomForestClassifier
import numpy as np
from helpers import extract_cols

class SpecCalculator:

    def __init__(self, n_columns, n_estimators=60):

        self.estimators = []

        for _ in range(n_columns):

            self.estimators.append(RandomForestClassifier(n_estimators=n_estimators))
    
    def fit(self, X, Y):

        self.columns = Y.columns

        
        for i,y in enumerate(extract_cols(Y)):

            self.estimators[i].fit(X,y)

            # append next property to input
            X = np.hstack((X, np.reshape(y, [-1,1])))
    
    def score(self, X, Y):

        scores = []

        for i,y in enumerate(extract_cols(Y)):

            scores.append(self.estimators[i].score(X, y))

            # append next property to input
            X = np.hstack((X, np.reshape(y, [-1,1])))

        return max(scores), min(scores), sum(scores)/len(scores)
    
    def score_each(self, X, Y):

        for i,y in enumerate(extract_cols(Y)):

            score= self.estimators[i].score(X, y)

            # append next property to input
            X = np.hstack((X, np.reshape(y, [-1,1])))

            yield self.columns[i], score
    
    def predict(self, X):

        Y = []

        for e in self.estimators:

            y = e.predict(X)

            Y.append(y)

            # append next property to input
            X = np.hstack((X, np.reshape(y, [-1,1])))
        
        return np.transpose(Y)

