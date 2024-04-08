import numpy as np
from scipy.optimize import linprog

c = np.array([100, 200, 150, 100, 80])
A_up = np.array([[0.5, 0.5, 0, 0, 0], [0, 0, 0.2, 0.4, 0.2]])
b_up = np.array([22, 15])

r = linprog(c, A_ub=A_up, b_ub=b_up, bounds=((0, None), (0, None), (0, None), (0, None), (0, None)))

print(r)