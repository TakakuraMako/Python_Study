import numpy as np

#初始方案 西北角法
def Northwest_func(A,produce_provide,sell_use,produce_num,sell_num):
    x, y = 0, 0 
    n = 0   #初始化退化解下标
    while(x < produce_num and y < sell_num):
            m = min(produce_provide[x],sell_use[y])
            A[x][y] = m   #第x个产地给第y个销地运量
            produce_provide[x] -= m #剩下的产量
            sell_use[y] -= m    #剩下的销量
            if produce_provide[x] == 0: #产地供应完毕，去下一个产地
                 x += 1
            elif sell_use[y] == 0:  #销地供应完毕，去下一个销地
                 y += 1
    return A

#求检验数 位势法
def Calculate_Sigma(A,Sigma,Price,produce_num,sell_num):
    u = np.zeros(produce_num)
    v = np.zeros(sell_num) #初始化位势法的u，v
    u_change = np.zeros(produce_num)    #判断是否计算过u
    v_change = np.zeros(sell_num)
    u_change[0] = 1
    while (u_change.min() != 1 or v_change.min() != 1):    #均改变才可结束计算
        for i in range(produce_num):    #通过基变量计算出uv
            for x in range(sell_num):
                if A[i][x] != 0:    #运量不为0,或者为退化解，基变量
                    if u_change[i] == 1 and v_change[x] == 0:
                        v[x] = Price[i][x] - u[i]
                        v_change[x] = 1
                    elif u_change[i] == 0 and v_change[x] == 1:
                        u[i] = Price[i][x] - v[x]
                        u_change[i] = 1
    Sigma = np.zeros([produce_num,sell_num])
    for i in range(produce_num):
        for x in range(sell_num):
            if A[i][x] == 0:    #运量为0，非基变量
                Sigma[i][x] = Price[i][x] - u[i] - v[x]
    return Sigma
                  
#调整基变量 闭回路调整法 抹点法
def Change_A(Sigma,A,produce_num,sell_num):
    sigma_min = np.min(Sigma)
    a, b = np.unravel_index(np.argmin(Sigma),Sigma.shape)   #检验数最小值的索引值
    A_x = A.copy()  #不可直接相等，否则会导致联动修改
    A_x[a][b] = 1   #闭回路起点看做基变量
    flag = 1    #是否有抹去的点，没有则是0
    while(flag):
        flag = 0
        for r in range(produce_num):
            if sorted(A_x[r])[-2] == 0 and sorted(A_x[r])[-1] > 0: #行有且只有一个基变量，即第二小的数是0，则抹去最大数，使其为0
                flag = 1
                A_x[r][np.argmax(A_x[r])] = 0
        for c in range(sell_num):   #列有且只有一个基变量，即第二小的数是0，则抹去最大数，使其为0
            if sorted(A_x[:,c])[-2] == 0 and sorted(A_x[:,c])[-1] > 0:
                flag = 1
                A_x[np.argmax(A_x[:,c])][c] = 0
                
    node = np.ones((produce_num+sell_num-1,2),dtype=np.int64) #每行储存一个闭回路序号在A_x的行索引值
    node = -node
    node[0,:] = a,b
    A_x[node[0,0]][node[0,1]] = 0
    index = 0
    while(np.max(A_x) > 0):
        r, c = node[index,:]
        index += 1
        if np.max(A_x[r,:]) > 0:   #行大于零处则为结点
            node[index,:] = np.unravel_index(np.argmax(A_x[r,:]),A_x.shape) #切片，因此都是1行，需要手动加入实际行数
            node[index][0] = r
        elif np.max(A_x[:,c]) > 0:
            node[index,:] = np.unravel_index(np.argmax(A_x[:,c]),A_x.shape)
            node[index][0] = c  #此处是列大于零处，node每一行第2列储存的行索引值，需要翻转
            node[index,:] = np.flip(node[index,:])
        A_x[node[index][0]][node[index][1]] = 0   #记录后的节点赋值0

    even = node[1::2,:]   #找到闭回路中编号为偶的数，即索引奇数行
    temp = [A[even[i][0]][even[i][1]] for i in range(len(even[:,0])) if even[i][0] >= 0]   #储存偶数序号的值，求最小值
    temp = np.array(temp)
    even_min =np.min(temp)   
    odd = node[::2,:]
    for i in range(len(temp)):
        A[even[i][0]][even[i][1]] -= even_min
    for i in range(len(temp)):
        A[odd[i][0]][odd[i][1]] += even_min
    return A


produce_num = int(input("产地数量"))
produce_provide = np.array(list(map(float, input("请输入产地的产量，空格隔开").split())))
if len(produce_provide) != produce_num:
    raise ValueError("产地数和产量不匹配")

sell_num = int(input("销地数量"))
sell_use = np.array(list(map(float, input("请输入销地的销量，空格隔开").split())))
if len(sell_use) != sell_num:
    raise ValueError("销地数和销量不匹配")

if np.sum(produce_provide) != np.sum(sell_use):
    raise ValueError("产销不平衡")

Price = np.zeros([produce_num,sell_num])    #初始化运价矩阵，行为产地数，列为销地数
A = np.zeros([produce_num,sell_num])    #初始化运量矩阵
Sigma = np.zeros([produce_num,sell_num])    #初始化检验数矩阵
print("按行输入单位运价，空格隔开，回车换行")
for i in range(produce_num):
    Price[i] = list(map(float, input().split()))

A = Northwest_func(A,produce_provide,sell_use,produce_num,sell_num) #西北角法
print("西北角法得初始方案\n",A)

Sigma = Calculate_Sigma(A,Sigma,Price,produce_num,sell_num)
print("\n计算检验数\n",Sigma)

while(Sigma.min() < 0):
    A = Change_A(Sigma,A,produce_num,sell_num)
    print("迭代\n",A)
    Sigma = Calculate_Sigma(A,Sigma,Price,produce_num,sell_num)
    print("\n计算检验数\n",Sigma)
print("最优运输方案\n",A)