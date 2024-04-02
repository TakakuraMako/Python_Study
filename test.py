import numpy as np
import pandas as pd
data = pd.read_csv('数据科学/分类算法/西瓜数据集 2.0.csv')
for index,x in data.iterrows():
    print(index,x['好瓜'])