import numpy as np
import pandas as pd
import glob
import os
data = pd.DataFrame({
    'Time':[1,2,3],
    'num':[1,1,2],
    'month_day':['2014/6/29 13:15', '2014/6/29 13:15', '2014/6/29 13:15']
})
data['Day'] = data['Time'].str.split(' ').str[0].str.split("/",n=1).str[1]
sum = data.groupby('Day')['num'].sum().reset_index()

# data = data.drop(data[data['Time'] == data.iloc[-1,0]].index)
data['month_day'] = pd.to_datetime(data['month_day'], format='%Y/%m/%d %M:%S')
data['month_day'] = data['month_day'].dt.strftime('%m%d')

print(min(['12aaa啊啊', 1]))