from sympy import *
import decimal
x = symbols('x')
f_x = x**3
x_0 = 1
accuracy = decimal.Decimal(2**-5)
while true:
    x_new = x_0 - f_x.subs(x, x_0)/f_x.diff(x).subs(x, x_0)
    if abs(x_new - x_0) <= accuracy:
        print(float(x_new))
        break
    x_0 = x_new
    