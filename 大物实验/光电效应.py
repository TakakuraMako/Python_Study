import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
U_Ak = np.arange(-2.0, 0.0, 0.1)
U_Ak = np.append(U_Ak, np.arange(0.0, 18.0, 3))
U_Ak = np.append(U_Ak, np.array([18.0, 20.0]))
I = np.array([-0.0248, -0.0174, -0.0121, 0.0194, 0.0615, 0.1569,
             0.04, 0.055, 0.086, 0.122, 0.133, 0.188, 0.822, 0.916, 1.080, 1.229, 1.392, 1.574, 1.692, 1.880,
             0.6, 3.82, 7.62, 12.64, 15.85, 18.64,
             21.4, 23.4])
plt.figure()
plt.plot(U_Ak, I, '-')
plt.grid(True)
plt.title('伏安特性曲线  ' + r'$\lambda=365mm, \phi=4$')
plt.ylabel('电压 ' + r'$U_{Ak}/V$')
plt.xlabel('电流 ' + r'$I \times 10^{-10}/A$')
plt.show()