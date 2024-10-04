from sympy import *
import decimal
x = symbols('x')
y = (x+1)*(x-1)**3
accuracy = decimal.Decimal(2**-10)
x_0 = decimal.Decimal(1.6)
x_new = decimal.Decimal(1.5)
while true:
        if abs(x_new - x_0) <= accuracy:
                break
        temp = x_new
        x_new = x_0 -y.subs(x, x_0)*(x_new - x_0)/(y.subs(x, x_new) - y.subs(x, x_0))
        x_0 = temp
        print(x_new)