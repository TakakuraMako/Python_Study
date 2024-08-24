import numpy as np
from deap import base, creator, tools, algorithms
import pandas as pd
# 1. 数据加载与处理
df_attachment3 = pd.read_excel('./附件3.xlsx')
df_filtered_products = pd.read_excel('./问题三/筛选单品_进价.xlsx')
df_prophet_results = pd.read_excel('./问题二/Prophet模型的预测结果.xlsx')
df_attachment4 = pd.read_excel('./附件4.xlsx')

# 筛选出61个单品
df_filtered = df_filtered_products[df_filtered_products['日期'] == '2023-06-30']
c_i = df_filtered['批发价格(元/千克)'].values  # 批发价格
d_i = df_prophet_results[df_prophet_results['ds'] == '2023-07-01']['yhat'].values  # 需求预测
a_i = df_attachment4['平均损耗率(%)_小分类编码_不同值'].values / 100  # 损耗率

n = len(c_i)  # 单品数量
beta_0 = np.random.uniform(0.5, 2.0, n)  # 随机生成，实际需根据数据调整
beta_1 = np.random.uniform(0.01, 0.05, n)  # 随机生成，实际需根据数据调整

# 2. 定义遗传算法的环境
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# 决策变量：x_i 表示是否选择该单品（0或1），y_i 表示进货量，z_i 表示定价
toolbox.register("attr_bool", np.random.randint, 2)
toolbox.register("attr_float", np.random.uniform, 2.5, 50)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_bool, toolbox.attr_float, toolbox.attr_float), n=n)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 目标函数定义
def evalProfit(individual):
    x = np.array(individual[:n])
    y = np.array(individual[n:2*n])
    z = np.array(individual[2*n:])

    # 计算利润
    profit = np.sum((1 - a_i) * (z - c_i) * y * x)
    return profit,

# 注册遗传算法操作
toolbox.register("evaluate", evalProfit)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# 3. 设置遗传算法的参数
population = toolbox.population(n=300)
NGEN = 2000
CXPB = 0.7  # 交叉概率
MUTPB = 0.5  # 突变概率

# 4. 运行遗传算法
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))

# 5. 获取结果
best_individual = tools.selBest(population, k=1)[0]
optimal_x = best_individual[:n]
optimal_y = best_individual[n:2*n]
optimal_z = best_individual[2*n:]

print("最优进货决策：", optimal_x)
print("最优进货量：", optimal_y)
print("最优定价策略：", optimal_z)
print("最大利润：", evalProfit(best_individual)[0])
