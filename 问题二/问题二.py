import pandas as pd
import numpy as np
import os
os.environ['CMDSTAN'] = "C:/Users/Mako/.conda/envs/environment/Library/bin/cmdstan"
from prophet import Prophet

df = pd.read_excel('批发随日期变化.xlsx')
# 重命名列名以符合 Prophet 的要求
df.rename(columns={'日期': 'ds', '批发价格(元/千克)': 'y', '分类名称': 'category'}, inplace=True)
print(df.head())
# 按分类名称分组数据
categories = df['category'].unique()
forecasts = {}

# 对每个品类分别应用 Prophet 模型进行预测
for category in categories:
    category_df = df[df['category'] == category].copy()
    
    # 初始化 Prophet 模型并进行拟合
    model = Prophet()
    model.fit(category_df[['ds', 'y']])
    # 创建未来的日期范围（2023-07-01 到 2023-07-07）
    future = model.make_future_dataframe(periods=7)
    
    # 进行预测
    forecast = model.predict(future)
    
    # 过滤出仅包含未来7天的预测结果
    forecast_filtered = forecast[forecast['ds'] >= '2023-07-01']
    
    # 存储预测结果
    forecasts[category] = forecast_filtered[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
# 将所有品类的预测结果合并为一个 DataFrame
forecast_df = pd.concat(forecasts, axis=0)

# 显示预测结果
print(forecast_df)
forecast_df.to_excel('Prophet模型的预测结果.xlsx')