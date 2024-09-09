import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
import random

# 定义问题参数
num_parts = 8  # 零配件数量
num_subassemblies = 3  # 半成品数量
num_final_decisions = 5  # 半成品和成品的拆解决策数量

# 成本和次品率参数
part_costs = np.array([2, 8, 12, 2, 8, 12, 8, 12])  # 零配件购买单价
part_detection_costs = np.array([1, 1, 2, 1, 1, 2, 1, 2])  # 零配件检测成本
subassembly_costs = np.array([8, 8, 8])  # 半成品装配成本
subassembly_detection_costs = np.array([4, 4, 4])  # 半成品检测成本
final_assembly_cost = 8  # 最终装配成本
market_price = 200  # 成品市场售价
replacement_loss = 40  # 调换损失
disassembly_cost = 10  # 拆解费用（假设值，根据题目需要调整）

# 定义适应度函数和个体
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # 我们要最小化成本
creator.create("Individual", list, fitness=creator.FitnessMin)

# 定义遗传算法工具箱
toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.choice, [0, 1])
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 
                 n=num_parts + num_subassemblies + 1 + num_subassemblies + 1)  # 增加半成品和成品拆解位
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 适应度评估函数：直接使用总成本作为适应度值，并添加生产逻辑约束
def evaluate(individual):
    total_cost = 0
    penalty = 1000  # 惩罚值，如果不满足生产逻辑，则施加惩罚
    
    # 获取零配件、半成品、成品的选择状态
    parts_selected = individual[:num_parts]
    subassemblies_selected = individual[num_parts:num_parts + num_subassemblies]
    product_selected = individual[num_parts + num_subassemblies]  # 成品选择状态
    subassemblies_disassembly = individual[num_parts + num_subassemblies + 1:num_parts + num_subassemblies + 4]
    product_disassembly = individual[-1]  # 成品拆解状态

    # 计算零配件的总成本
    for i in range(num_parts):
        total_cost += part_costs[i] * (1 - parts_selected[i]) + part_detection_costs[i] * parts_selected[i]
    
    # 计算半成品的总成本，并进行逻辑约束检查
    for j in range(num_subassemblies):
        # 确定每个半成品所需的零配件索引
        required_parts = [0, 1, 2] if j == 0 else [3, 4, 5] if j == 1 else [6, 7]
        # 如果选择了半成品但未选择相应的零配件，则施加惩罚
        if subassemblies_selected[j] and not all(parts_selected[k] for k in required_parts):
            return penalty,  # 违反逻辑约束，返回惩罚值
        # 如果半成品被选择，累加其装配和检测成本
        total_cost += subassembly_costs[j] * subassemblies_selected[j] + subassembly_detection_costs[j] * subassemblies_selected[j]

        # 拆解半成品的成本
        if subassemblies_disassembly[j]:
            total_cost += disassembly_cost * subassemblies_disassembly[j]

    # 计算成品的装配成本和市场售价调整
    if product_selected:
        # 如果选择了成品但未选择所有半成品，则施加惩罚
        if not all(subassemblies_selected):
            return penalty,  # 违反逻辑约束，返回惩罚值
        total_cost += final_assembly_cost + market_price - replacement_loss
    else:
        # 对未选择的成品考虑拆解
        if product_disassembly:
            total_cost += disassembly_cost * product_disassembly

    return total_cost,  # 返回直接的总成本作为适应度

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)
    population = toolbox.population(n=100)
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    # 运行遗传算法，确保目标是最小化成本
    pop, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, verbose=True)
    return pop, log

# 执行遗传算法
pop, log = main()
best_ind = tools.selBest(pop, 1)[0]

# 输出最优个体及其适应度
print("Best individual is %s, Fitness (Cost): %s" % (best_ind, best_ind.fitness.values))

# 可视化适应度（成本）曲线
plt.figure(figsize=(10, 5))
plt.plot(log.select("min"), label='Minimum Cost')
plt.plot(log.select("avg"), label='Average Cost')
plt.title('Cost over Generations')
plt.xlabel('Generation')
plt.ylabel('Cost')
plt.legend()
plt.grid(True)
plt.show()
