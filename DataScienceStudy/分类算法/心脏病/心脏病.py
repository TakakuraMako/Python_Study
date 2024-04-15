import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 



data = pd.read_csv('./DataScienceStudy/分类算法/心脏病/cardio_train.csv')
data = data.drop(columns='id')

X_var = data[['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']].values
Y_var = list(set(data['cardio'].values))
print(Y_var)
a = list(data.columns)[:-1]
print(dict.fromkeys(a,{}))
