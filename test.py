from sympy import *
x = symbols('x')
y = x/2 * sqrt(1 - x**2) + 1/2 * asin(x) + log(x + sqrt(1 + x**2))
print(latex(y.diff(x)))