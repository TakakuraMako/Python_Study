from sympy import *
import tkinter as tk
import math
import numpy as np
import decimal
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
x = symbols('x')
y = x**3
accuracy = decimal.Decimal(2**-5)
x_0 = 3
plt.figure()
x_plot = np.arange(-10 ,10)
y_plot = x_plot**3
plt.plot(x_plot, y_plot)

while true:
        x_new = x_0 -y.subs(x, x_0)/y.diff(x).subs(x, x_0)
        if abs(x_new - x_0) <= accuracy:
                print(float(x_new))
                break
        y_plot = y.diff(x).subs(x, x_0)*(x_plot - x_0) + y.subs(x, x_0)
        plt.plot(x_plot, y_plot)
        x_0 = x_new


plt.show()