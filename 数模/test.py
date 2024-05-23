def allocate_bonus(total_bonus, num_people, initial_levels):
    """
    分配奖金的函数
    :param total_bonus: 初始奖金金额
    :param num_people: 分配人数
    :param initial_levels: 初始等级及其对应的金额区间和人数
    :return: 每个等级分配的具体奖金金额
    """
    from scipy.optimize import minimize
    import numpy as np

    # 初始等级的代表值（取平均值）
    level_values = [(level[1] + level[2]) / 2 for level in initial_levels]
    
    # 约束条件
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.dot(x, [level[3] for level in initial_levels]) - total_bonus},
        *({'type': 'ineq', 'fun': lambda x, lb=level[1], ub=level[2]: ub - x[idx]} for idx, level in enumerate(initial_levels)),
        *({'type': 'ineq', 'fun': lambda x, lb=level[1], ub=level[2]: x[idx] - lb} for idx, level in enumerate(initial_levels)),
    )

    # 目标函数
    def objective(x):
        return sum((x[i] - level_values[i]) ** 2 for i in range(len(initial_levels)))

    # 初始猜测值
    x0 = [level_values[i] for i in range(len(initial_levels))]

    # 求解优化问题
    result = minimize(objective, x0, constraints=constraints, method='SLSQP')

    # 输出结果
    if result.success:
        bonus_distribution = result.x
        return bonus_distribution
    else:
        raise ValueError("奖金分配问题无法求解")


# 示例数据
total_bonus = 500000
num_people = 20
initial_levels = [
    ('一等奖', 500, 600, 2),
    ('二等奖', 400, 500, 3),
    ('三等奖', 200, 300, 5),
    ('四等奖', 50, 200, 10)
]

# 分配奖金
bonus_distribution = allocate_bonus(total_bonus, num_people, initial_levels)

# 打印结果
for i, level in enumerate(initial_levels):
    print(f"{level[0]}: 分配奖金 = {bonus_distribution[i]:.2f} 元")

