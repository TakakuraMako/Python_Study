import pandas as pd
import numpy as np

# 加载数据
data_house1 = pd.read_csv('house1.csv')
data_house2 = pd.read_csv('house2.csv')

# 前向填充
data_house1_filled_ffill = data_house1.fillna(method='ffill')
data_house2_filled_ffill = data_house2.fillna(method='ffill')

# 后向填充
data_house1_filled_bfill = data_house1.fillna(method='bfill')
data_house2_filled_bfill = data_house2.fillna(method='bfill')
