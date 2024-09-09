import numpy as np
from scipy.stats import beta as beta_distribution
import random

# 计算检测成本
def calculate_detection_cost(sample_size, detection_cost):
    return sample_size * detection_cost

# 计算不检测的潜在损失成本
def calculate_loss_cost(sample_size, defective_rate, assembly_cost, swap_loss):
    return sample_size * defective_rate * (assembly_cost + defective_rate * swap_loss)

# 贝叶斯更新函数
def bayesian_update(alpha, beta, detected, total):
    return alpha + detected, beta + total - detected

# 蒙特卡洛模拟进行次品率估计
def monte_carlo_simulation(alpha, beta, simulations=1000):
    return np.mean([beta_distribution.rvs(alpha, beta) for _ in range(simulations)])

# 遗传算法的适应度计算函数
def fitness_function(components, product, decisions):
    total_cost = 0
    component_defective_rates = []
    
    # 更新零配件的次品率并计算成本
    for i, component in enumerate(components):
        p = component["defective_rate"]
        d_cost = component["detection_cost"]
        alpha, beta = component["alpha"], component["beta"]
        decision = decisions[0][i]  # 零配件的检测决策
        
        # 贝叶斯更新和蒙特卡洛模拟
        updated_alpha, updated_beta = bayesian_update(alpha, beta, 
                                                      detected=int(p * sample_size), 
                                                      total=sample_size)
        adjusted_p = monte_carlo_simulation(updated_alpha, updated_beta)
        adjusted_p *= (1 - decision)
        
        # 计算检测成本和损失成本
        detection_cost = calculate_detection_cost(sample_size, d_cost)
        loss_cost = calculate_loss_cost(sample_size, p, 0, product["swap_loss"])
        total_cost += detection_cost * decision + loss_cost * (1 - decision)
        
        # 更新零配件的次品率
        component_defective_rates.append(adjusted_p)
    
    # 计算成品的次品率
    product_defective_rate = 1 - np.prod([1 - p for p in component_defective_rates])
    
    # 成品检测和拆解成本
    detect_product = decisions[1][0]
    disassemble_decision = decisions[1][1]
    
    product_detection_cost = calculate_detection_cost(sample_size, product["detection_cost"])
    product_loss_cost = calculate_loss_cost(sample_size, product_defective_rate, product["market_price"], product["swap_loss"])
    disassemble_cost = sample_size * product["disassemble_cost"]
    disassemble_benefit = sample_size * (1 - product_defective_rate) * product["market_price"]
    
    total_cost += product_detection_cost * detect_product + product_loss_cost * (1 - detect_product)
    total_cost += disassemble_cost * disassemble_decision - disassemble_benefit * disassemble_decision
    
    # 适应度是负的总成本
    return -total_cost

# 遗传算法实现
def genetic_algorithm(components, product, generations=50, population_size=20):
    # 初始化种群
    population = [[[random.randint(0, 1) for _ in components], [random.randint(0, 1), random.randint(0, 1)]]
                  for _ in range(population_size)]
    
    for generation in range(generations):
        # 计算适应度
        fitness_scores = [fitness_function(components, product, decisions) for decisions in population]
        
        # 选择优秀个体
        selected_indices = np.argsort(fitness_scores)[-population_size//2:]
        selected_population = [population[i] for i in selected_indices]
        
        # 交叉生成新个体
        new_population = selected_population.copy()
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            # 修正交叉点的选择范围，避免 range 为空
            if len(parent1) > 2:
                crossover_point = random.randint(1, len(parent1) - 2)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
            else:
                child1, child2 = parent1, parent2  # 如果个体过短，不进行交叉
            new_population.extend([child1, child2])
        
        # 变异
        for individual in new_population:
            if random.random() < 0.1:  # 10%变异概率
                step_to_mutate = random.randint(0, len(individual) - 1)
                gene_to_mutate = random.randint(0, len(individual[step_to_mutate]) - 1)
                individual[step_to_mutate][gene_to_mutate] = 1 - individual[step_to_mutate][gene_to_mutate]
        
        population = new_population
    
    # 返回适应度最高的个体
    best_index = np.argmax([fitness_function(components, product, decisions) for decisions in population])
    return population[best_index]

# 定义六种不同的场景参数
scenarios = [
    {
        "components": [
            {"defective_rate": 0.1, "detection_cost": 2, "alpha": 1, "beta": 9},
            {"defective_rate": 0.1, "detection_cost": 3, "alpha": 1, "beta": 9}
        ],
        "product": {
            "components": [0, 1],
            "detection_cost": 5,
            "disassemble_cost": 6,
            "market_price": 100,
            "swap_loss": 20
        }
    },
    {
        "components": [
            {"defective_rate": 0.2, "detection_cost": 2, "alpha": 2, "beta": 8},
            {"defective_rate": 0.2, "detection_cost": 3, "alpha": 2, "beta": 8}
        ],
        "product": {
            "components": [0, 1],
            "detection_cost": 5,
            "disassemble_cost": 6,
            "market_price": 100,
            "swap_loss": 20
        }
    },
    {
        "components": [
            {"defective_rate": 0.1, "detection_cost": 2, "alpha": 1, "beta": 9},
            {"defective_rate": 0.1, "detection_cost": 3, "alpha": 1, "beta": 9}
        ],
        "product": {
            "components": [0, 1],
            "detection_cost": 5,
            "disassemble_cost": 6,
            "market_price": 100,
            "swap_loss": 40
        }
    },
    {
        "components": [
            {"defective_rate": 0.2, "detection_cost": 1, "alpha": 2, "beta": 8},
            {"defective_rate": 0.2, "detection_cost": 1, "alpha": 2, "beta": 8}
        ],
        "product": {
            "components": [0, 1],
            "detection_cost": 4,
            "disassemble_cost": 5,
            "market_price": 100,
            "swap_loss": 30
        }
    },
    {
        "components": [
            {"defective_rate": 0.1, "detection_cost": 8, "alpha": 1, "beta": 9},
            {"defective_rate": 0.2, "detection_cost": 1, "alpha": 1, "beta": 9}
        ],
        "product": {
            "components": [0, 1],
            "detection_cost": 3,
            "disassemble_cost": 5,
            "market_price": 100,
            "swap_loss": 10
        }
    },
    {
        "components": [
            {"defective_rate": 0.05, "detection_cost": 2, "alpha": 1, "beta": 9},
            {"defective_rate": 0.05, "detection_cost": 3, "alpha": 1, "beta": 9}
        ],
        "product": {
            "components": [0, 1],
            "detection_cost": 5,
            "disassemble_cost": 40,
            "market_price": 100,
            "swap_loss": 10
        }
    }
]

# 定义样本量
sample_size = 100

# 计算六种情况的最优决策
optimal_decisions_all_scenarios = [genetic_algorithm(scenario["components"], scenario["product"]) for scenario in scenarios]

print(optimal_decisions_all_scenarios)