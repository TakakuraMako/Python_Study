import numpy as np
fx = np.array([])
def diff_fun(fx):
    result = np.array([])
    if len(fx) == 1:
        
    for i in range(len(fx) - 1):
        result = np.concatenate(result, fx[i+1] - fx[i])