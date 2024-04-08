import random
import math

#随机取100次放入列表
a = []
for i in range(100):
    a.append(random.randint(0,100)) 

#求平均
temp = 0
for i in a:
    temp = temp + i
x_avg = temp / 100 

#计算标准差
temp = 0
for i in a:
    temp = temp + abs(i - x_avg)**2
s = math.sqrt(temp)/100

#计算标准化结果
b = []
for i in range(100):
    b.append((a[i] - x_avg) / s)

print(b)