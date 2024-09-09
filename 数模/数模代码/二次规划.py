import pprint
from cvxopt import matrix, solvers
P = matrix([[4.0,1.0],[1.0,2.0]])
q = matrix([1.0,1.0])
G = matrix([[-1.0,0.0],[0.0,-1.0]])
h = matrix([0.0,0.0])
A = matrix([1.0,1.0],(1,2))#原型为cvxopt.matrix(array,dims)，等价于A = matrix([[1.0],[1.0]]）
b = matrix([1.0])
result = solvers.qp(P,q,G,h,A,b)
 
print('x\n',result['x'])
