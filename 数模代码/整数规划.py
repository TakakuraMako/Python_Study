# 匈牙利算法python代码：

from scipy.optimize import linear_sum_assignment
  
cost =np.array([[4,1,3],[2,0,5],[3,2,2]])
row_ind,col_ind=linear_sum_assignment(cost)
print(row_ind)#开销矩阵对应的行索引
print(col_ind)#对应行索引的最优指派的列索引
print(cost[row_ind,col_ind])#提取每个行索引的最优指派列索引所在的元素，形成数组
print(cost[row_ind,col_ind].sum())#数组求和

# 输出：
# [0 1 2]
# [1 0 2] 
# [1 2 2] 
# 5

import numpy as np


def check(x):
	if x.sum() > 400:
		return False
	if x[0]+2*x[1]+2*x[2]+x[3]+6*x[4] > 800:
		return False
	if 2*x[0]+x[1]+6*x[2]>200:
		return False
	if x[2]+x[3]+5*x[3]>200:
		return False

	return True


def get_radom():
	x = np.random.randint(100, size=5)
	while not check(x):
		x = get_radom()
	return x


lim = 10**6
ans = -1

for i in range(lim):
	num = get_radom()
	ans = max(ans, num.all())
	if i % 10000 == 0:
		print(i)

print('ans=' + ans)




