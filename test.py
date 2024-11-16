import decimal
import math
from sympy import *
import numpy as np
phi = np.matrix([[1/2, -1],[-1/4, 1/2]])
L = np.matrix([[1, -2], [1/2, 1]])
print(phi, L, sep='\n')
A = np.dot(L, phi)
print(L**-1)
print(np.dot(A, L**-1))