import numpy as np
import math
import pandas as pd

# 初始化参数
data = pd.DataFrame({
    'situation': [],
    'judge1': [],
    'judge2': [],
    'judge3': [],
    'judge4': [],
    'w': []
}, dtype='int64')

# 各种概率和成本参数
p_1 = [0.1, 0.2, 0.1, 0.2, 0.1, 0.05]
p_2 = [0.1, 0.2, 0.1, 0.2, 0.2, 0.05]
p_3 = [0.1, 0.2, 0.1, 0.2, 0.1, 0.05]
b_1, b_2, b_3 = 4, 18, 6
b_4 = [5, 5, 5, 5, 5, 40]
c_1 = [2, 2, 2, 1, 8, 2]
c_2 = [3, 3, 3, 1, 1, 3]
c_3 = [3, 3, 3, 2, 2, 3]
c_4 = [6, 6, 30, 30, 10, 10]
n_1 = 1000
n_2 = 2000
rounds = 3
price = 56  # 成品售价，计算中不再使用

# 购买零件
def Import_parts(n1, n2):
    return n1 * b_1 + n2 * b_2

# 零件检测
def Parts_inspection(part_1, part_2, c1, c2, p1, p2, judge1, judge2, C_parts_inspection):
    C_parts_inspection += part_1 * c1 * judge1 + part_2 * c2 * judge2
    part_1 = math.floor(part_1 * (1 - p1 * judge1))
    part_2 = math.floor(part_2 * (1 - p2 * judge2))
    return part_1, part_2, C_parts_inspection

# 组装成品
def Assemble_parts(part_1, part_2, b_3, C_assemble_parts):
    N = min(part_1, part_2)
    part_1 -= N
    part_2 -= N
    C_assemble_parts += N * b_3
    return part_1, part_2, C_assemble_parts, N

# 成品检测
def Product_inspection(N, c3, p3, C_product_inspection, judge3):
    C_product_inspection += N * c3 * judge3
    N_sale = N * (1 - p3 * judge3)
    N_unqualified = N - N_sale
    return math.floor(N_sale), math.floor(N_unqualified), C_product_inspection

# 购买不合格数量
def Sale_inspection(N_sale, p1, p2, p3, judge1, judge2, judge3):
    P = 1 - ((1 - p3) * (1 - p1 * (1 - judge1)) * (1 - p2 * (1 - judge2)))
    return math.floor((1 - judge3) * N_sale * P)

# 调换
def Produce_unquailed_exchange(N_sale_unqualified, c4):
    return N_sale_unqualified * c4

# 拆解
def Product_disassemble(n_unqualified, b4, judge4):
    return n_unqualified * judge4, n_unqualified * b4 * judge4

# 主循环，遍历所有情况和决策组合
for situation in range(6):  # 六种情况
    for judge1 in range(2):  # 零件一检测
        for judge2 in range(2):  # 零件二检测
            for judge3 in range(2):  # 成品检测
                for judge4 in range(2):  # 是否调换
                    # 初始化成本和零件数量
                    C_import_parts = Import_parts(n_1, n_2)
                    C_parts_inspection = 0
                    part_1 = n_1
                    part_2 = n_2
                    k = 1

                    # 零件检测
                    part_1, part_2, C_parts_inspection = Parts_inspection(part_1, part_2, c_1[situation], c_2[situation], p_1[situation], p_2[situation], judge1, judge2, C_parts_inspection)
                    w = C_import_parts + C_parts_inspection

                    # 循环生产过程
                    while True:
                        # 初始化生产过程中的成本
                        C_assemble_parts, C_product_inspection, C_exchange, C_disassemble = 0, 0, 0, 0
                        
                        # 组装成品
                        part_1, part_2, C_assemble_parts, N = Assemble_parts(part_1, part_2, b_3, C_assemble_parts)
                        
                        # 成品检测
                        N_sale, N_unqualified, C_product_inspection = Product_inspection(N, c_3[situation], p_3[situation], C_product_inspection, judge3)
                        
                        # 销售后不合格产品的处理
                        N_sale_unqualified = Sale_inspection(N_sale, p_1[situation], p_2[situation], p_3[situation], judge1, judge2, judge3)
                        
                        # 调换不合格成品的成本
                        C_exchange = Produce_unquailed_exchange(N_sale_unqualified, c_4[situation])
                        
                        # 拆解不合格成品
                        n_unqualified, C_disassemble = Product_disassemble(N_unqualified + N_sale_unqualified, b_4[situation], judge4)
                        
                        # 更新零配件库存
                        part_1 += n_unqualified
                        part_2 += n_unqualified
                        
                        # 总成本更新，不考虑销售收入
                        w += C_assemble_parts + C_product_inspection + C_exchange + C_disassemble

                        # 终止条件
                        if part_1 == 0 or part_2 == 0 or k >= rounds:
                            break
                        else:
                            k += 1

                    # 记录当前决策组合的结果
                    new = pd.DataFrame({
                        'situation': [situation + 1],
                        'judge1': [judge1],
                        'judge2': [judge2],
                        'judge3': [judge3],
                        'judge4': [judge4],
                        'w': [w]
                    }, dtype='int64')
                    data = pd.concat([data, new], ignore_index=True)

# 保存结果
data.to_excel('问题2.xlsx', index=False)
