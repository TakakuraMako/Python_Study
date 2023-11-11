import numpy as np
#默认求最大值，约束条件小于等于

#化标准形
def standardize(A,c):
    #系数矩阵行列数
    A_rows = A.shape[0]
    A_colums = A.shape[1]
    #系数矩阵加入松弛变量系数
    E = np.eye(A_rows)
    B = np.append(A,E,axis=1)
    c = np.append(c,np.zeros(A_rows))
    return B,c

#计算检验数
def Change_sigma(A,cb_index,c,rows,colums,sigma):
    sigma = np.zeros([rows+colums])
    for i in range(rows+colums):#控制列
        for x in range(rows):#控制行
            sigma[i] += -c[cb_index[x]]*A[x][i]
        sigma[i] += c[i]
    return sigma
    
#确定出基入基
def En_Out(sigma,A,cb_index,unbounded,inf):
    index_enter = np.argmax(sigma)#入基变量c中索引值
    if A[:,index_enter].max()<=0:
        unbounded = 1
    out = np.zeros(rows)#比值数
    for i in range(rows):
        if A[i][index_enter] <= 0:
            out[i] = np.inf
        else:
            out[i] = A[i][rows+colums] / A[i][index_enter]
    index_out = np.where(out > 0, out, np.inf).argmin()#出基变量行索引值,最小正数
    cb_index[index_out] = index_enter
    for i in range(len(sigma)):
        if i in cb_index:
            continue
        if sigma[i] == 0:
            inf = 1
    return cb_index ,unbounded,inf

#矩阵初等变换
def Simplify(A,cb_index,rows):
    for i in range(rows):
        A[i] = A[i]/A[i][cb_index[i]]#矩阵对应处化为1
        for x in range(rows):
            if x != i:
                A[x] = A[x]-(A[i]*A[x][cb_index[i]])#此列其他行化为0
    return A

#输入矩阵
print("目标函数系数矩阵,空格隔开：")#单行矩阵
c = input()
c = list(map(float,c.split()))
c = np.array(c)

print("约束条件右端值,空格隔开：")#列矩阵
b = input()
b = list(map(float,b.split()))

print("约束条件系数矩阵行和列数,空格隔开：")
rows,colums = map(int,input().split())
A = np.zeros([rows,colums])
print("约束条件系数矩阵：")
n = 0
while(n < rows):
    a = input()
    a = list(map(float,a.split()))
    A[n] = a
    n += 1
A,c = standardize(A,c)
A = np.column_stack((A,b))
# print("加入松弛变量：\nc={0}\nA=\n{1}\n".format(c,A))

unbounded = 0
inf = 0
cb_index = np.arange(colums, colums+rows, 1)#基变量在c的索引值
sigma = np.ones([rows+colums])#初始化
sigma = Change_sigma(A,cb_index,c,rows,colums,sigma)
cb_index, unbounded, inf= En_Out(sigma,A,cb_index,unbounded,inf)
while sigma[np.argmax(sigma)] > 0 and unbounded == 0:
    A = Simplify(A,cb_index,rows)
    sigma = Change_sigma(A,cb_index,c,rows,colums,sigma)
    if sigma[np.argmax(sigma)] > 0:
        cb_index,unbounded, inf= En_Out(sigma,A,cb_index,unbounded,inf)
if unbounded == 1:
    print("无界解")
else:
    print("基变量为")
    for i in range(rows):
        print("x",cb_index[i]+1,end=" ",sep="")
    print("\n值为")
    for i in range(rows):
        print(A[i][rows+colums],end=" ")

    print("目标值为",end="")
    z = 0
    for i in range(rows):
        z += c[cb_index[i]]*A[i][rows+colums]
    print(z)
    if inf == 1:
        print("有无穷解")