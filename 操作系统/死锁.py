def banker_algorithm(available, max_demand, allocation):
    # 计算每个进程的需求
    need = [[max_demand[i][j] - allocation[i][j] for j in range(len(available))] for i in range(len(allocation))]

    # 安全序列
    safe_sequence = []

    # 进程数量
    num_processes = len(allocation)
    # 资源类型数量
    num_resources = len(available)

    # 完成标志
    finish = [False] * num_processes

    # 工作向量，初始化为可用资源
    work = available[:]

    while len(safe_sequence) < num_processes:
        allocated_this_round = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i + 1)  # 加1以使进程编号从1开始
                allocated_this_round = True

        if not allocated_this_round:
            break

    if len(safe_sequence) == num_processes:
        return True, safe_sequence
    else:
        return False, []

# 可用资源
available_resources = [2, 1, 1]

# 最大需求
maximum_demand = [
    [5, 5, 9],
    [5, 3, 6],
    [4, 0, 11],
    [4, 2, 5],
    [4, 2, 4]
]

# 当前分配
current_allocation = [
    [2, 1, 2],
    [4, 0, 2],
    [4, 0, 5],
    [2, 0, 4],
    [3, 1, 4]
]

# 执行银行家算法
status, sequence = banker_algorithm(available_resources, maximum_demand, current_allocation)
if status:
    print("系统处于安全状态，安全序列为:", sequence)
else:
    print("系统处于不安全状态，无安全序列")
