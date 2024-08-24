import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from prophet import Prophet

# 读取你上传的文件
df = pd.read_excel('批发随日期变化.xlsx')

# 重命名列名以符合 Prophet 的要求
df.rename(columns={'日期': 'ds', '批发价格(元/千克)': 'y', '分类名称': 'category'}, inplace=True)

# 按分类名称分组数据
categories = df['category'].unique()
results = []

# 对每个品类分别应用 Prophet 模型进行预测并计算指标
for category in categories:
    category_df = df[df['category'] == category].copy()
    
    # 初始化 Prophet 模型并进行拟合
    model = Prophet()
    model.fit(category_df[['ds', 'y']])
    
    # 创建未来的日期范围
    future = model.make_future_dataframe(periods=0)  # 只预测现有的数据，不扩展
    forecast = model.predict(future)
    
    # 计算 MAE, RMSE, R²
    mae = mean_absolute_error(category_df['y'], forecast['yhat'])
    rmse = np.sqrt(mean_squared_error(category_df['y'], forecast['yhat']))
    r2 = r2_score(category_df['y'], forecast['yhat'])
    
    # 存储结果
    results.append({
        'category': category,
        'MAE': mae,
        'RMSE': rmse,
        'R2': r2
    })

# 将结果转换为 DataFrame 以便查看
results_df = pd.DataFrame(results)

# 显示结果
print(results_df)
