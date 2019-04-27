import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("http://localhost:8080/final.csv")

df = df.drop(columns=df.columns[0])

col = 'piston_stroke'

df_n = df.sort_values(by=[col])
plt.plot(df_n[col].values, df_n['sentiment'].values)
plt.show()