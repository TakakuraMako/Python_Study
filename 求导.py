from sympy import *
x, y = symbols('x y')
f = exp(x)+x**2
fdy = diff(f, 'x', 2)
print(latex(fdy))