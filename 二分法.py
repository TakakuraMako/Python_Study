from sympy import *
import decimal
import numpy as np
x = symbols('x')
# str = input("函数：")
# a = decimal.Decimal(input("下限"))
# b = decimal.Decimal(input("上限"))
# accuracy = decimal.Decimal(eval(input("精确度")))
a = decimal.Decimal(0)
b = decimal.Decimal(1)
accuracy = decimal.Decimal(2**-5)
f_x = exp(-x) - sin(pi*x/2)
x_old = a
while(true):
    x_new = (a+b)/2
    y = f_x.subs(x, x_new)
    if y == 0:
        print(x_new)
        break
    elif abs(x_old - x_new) < accuracy:
        break
    elif y*f_x.subs(x,a) > 0:
        a = (a + b)/2
    elif y*f_x.subs(x,a) < 0:
        b = (a + b)/2
    x_old = x_new
    print(x_old)