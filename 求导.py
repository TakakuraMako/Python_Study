from sympy import *
x, y = symbols('x y')
f = exp(x)+x**2
fdy = limit(f, x, 0)
print(latex(fdy))