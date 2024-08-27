import numpy as np
import geatpy as ea
import pandas as pd

# 读取数据
df_1 = pd.read_excel('附件3.xlsx', sheet_name="Sheet1")  # 批发价格数据
df_4 = pd.read_excel('附件4.xlsx', sheet_name="Sheet1")  # 损耗率数据

a_i = df_4["损耗率"].values  # 损耗率
c_i = df_1["批发价格"].values  # 批发价格
beta_0 = df_1["beta0"].values  # beta0 系数
beta_1 = df_1["beta1"].values  # beta1 系数

# 问题类定义
class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name
        M = 1  # 初始化M (目标维数)
        maxormins = [-1]  # 初始化maxormins (目标最小化)
        Dim = 58 * 2 + 6  # 初始化Dim (决策变量维数)
        varTypes = [1] * 58 + [0] * 58 + [1] * 6 + [1] * 6  # 决策变量的类型
        lb = [0] * 58 + [c_i[i] for i in range(58)] + [0] * 6 + [0] * 6  # 决策变量下界
        ub = [1] * 58 + [50] * 58 + [1] * 6 + [1] * 6  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界
        ubin = [1] * Dim  # 决策变量上边界

        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        x = Vars[:, 0:58]  # 进货量
        y = Vars[:, 58:116]  # 定价
        u = Vars[:, 116:122]  # 辅助变量 u_j
        v = Vars[:, 122:128]  # 辅助变量 v_j
        z = (y - beta_0) / beta_1  # 利用定价计算z_i
        
        # 计算总利润
        profit = np.sum((1 - a_i) * (z - c_i) * y * x, axis=1)
        # 添加约束条件
        cons1 = np.sum(x, axis=1) - 33
        cons2 = 27 - np.sum(x, axis=1)
        cons3 = y - 50 * x
        cons4 = 2.5 * x - y
        cons5 = u * (0.6 * np.sum(d, axis=1) - np.sum(y, axis=1))
        cons6 = v * (np.sum(y, axis=1) - np.sum(d, axis=1))
        cons7 = 5 - np.sum(u, axis=1)
        cons8 = 5 - np.sum(v, axis=1)
        
        # 将约束加入惩罚项
        pop.ObjV = profit - 1e6 * (np.maximum(0, cons1) + np.maximum(0, cons2) + np.maximum(0, cons3) +
                                    np.maximum(0, cons4) + np.maximum(0, cons5) + np.maximum(0, cons6) +
                                    np.maximum(0, cons7) + np.maximum(0, cons8))

# 实例化问题对象
problem = MyProblem()

# 算法参数设置
Encoding = "RI"  # 实整数编码
NIND = 200  # 种群规模
Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
population = ea.Population(Encoding, Field, NIND)

myAlgorithm = ea.soea_DE_best_1_L_templet(problem, population)  # 使用差分进化算法
myAlgorithm.MAXGEN = 2000  # 最大进化次数
myAlgorithm.mutOper.F = 0.5  # 突变概率
myAlgorithm.recOper.XOVR = 0.7  # 交叉概率
myAlgorithm.logTras = 0  # 不打印日志
myAlgorithm.verbose = False  # 不输出日志
myAlgorithm.drawing = 1  # 绘图

# 种群进化
[BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体及最后一代种群

# 输出结果
print('评价次数：%s' % (myAlgorithm.evalsNum))
print('花费时间 %s 秒' % (myAlgorithm.passTime))
if BestIndi.sizes != 0:
    print("最优的目标函数值为 %s" % BestIndi.ObjV[0][0])
    print("最优决策变量:")
    for i in range(BestIndi.Phen.shape[1]):
        print(BestIndi.Phen[0, i])
else:
    print("未找到解")
