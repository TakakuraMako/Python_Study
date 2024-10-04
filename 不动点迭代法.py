from sympy import *
import decimal
x = symbols('x')
a = decimal.Decimal(1)
b = decimal.Decimal(2)
accuracy = decimal.Decimal(2**-5)
phi_x = 1/2*(10 - x**3)**(1/2)
x_old = (a+b)/2
while(true):
    print(float(x_old))
    x_new = phi_x.subs(x, x_old)
    if abs(x_old - x_new) < accuracy:
        break
    if abs(x_old - x_new) > abs(a-b):
        print('发散')
        break
    x_old = x_new