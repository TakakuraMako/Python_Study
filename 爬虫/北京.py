import pandas as pd
import glob

# 设置文件路径和列名
file_paths = glob.glob("./beijing_weather/545110-99999-*")
column_names = ["Year", "Month", "Day", "Hour", "Temperature", "DewPointTemp", "Pressure", "WindSpeed", "Precipitation", "Other1", "Other2", "Other3"]

# 初始化一个空的 DataFrame 用于存储每日平均温度结果
daily_mean_temperature_all = pd.DataFrame()

# 处理每个文件
for file_path in file_paths:
    # 读取文件并分隔列
    data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    data.columns = column_names

    # 数据换算
    data["Temperature"] = data["Temperature"] / 10
    data["DewPointTemp"] = data["DewPointTemp"] / 10
    data["Pressure"] = data["Pressure"] / 10
    data["WindSpeed"] = data["WindSpeed"] / 10
    data["Precipitation"] = data["Precipitation"] / 10

    # 计算每日平均温度
    data["Date"] = pd.to_datetime(data[["Year", "Month", "Day"]])
    daily_mean_temperature = data.groupby("Date")["Temperature"].mean().reset_index()
    daily_mean_temperature.columns = ["Date", "AverageTemperature"]

    # 合并结果
    daily_mean_temperature_all = pd.concat([daily_mean_temperature_all, daily_mean_temperature])

# 导出合并后的Excel文件
output_file = "./daily_mean_temperature_all_years.xlsx"
daily_mean_temperature_all.to_excel(output_file, index=False)

print("计算完成，结果已保存至：", output_file)
