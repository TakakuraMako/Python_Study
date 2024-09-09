import numpy as np
from scipy.optimize import linprog

c = np.array([2, 3, 1])
A_up = np.array([[-1, -4, -2], [-3, -2, 0]])
b_up = np.array([-8, -6])

r = linprog(c, A_ub=A_up, b_ub=b_up, bounds=((0, None), (0, None), (0, None)))

print(r)