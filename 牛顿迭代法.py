from sympy import *
import decimal
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 

x = symbols('x')
f_x = (x-10)**3
x_0 = 1
accuracy = decimal.Decimal(2**-5)
x_star = []
f_x_star = []
while true:
    x_new = x_0 - f_x.subs(x, x_0)/f_x.diff(x).subs(x, x_0)
    x_star.append(x_new)
    f_x_star.append(f_x.subs(x, x_new))
    if abs(x_new - x_0) <= accuracy:
        print(float(x_new))
        break
    x_0 = x_new
plt.figure()
plt.plot(x_star, f_x_star)
plt.xlim = range(-10,10)
plt.xticks = range(-10,10)
plt.yticks = range(-10, 10)
plt.xlabel(r'$x*$')
plt.ylabel(r'$f(x*)$')
plt.grid()
plt.show()