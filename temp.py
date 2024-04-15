import numpy as np
y = np.array([True, False, True])
x = np.array([1, 2, 3])
a = x[:] < 2
print(x[y])