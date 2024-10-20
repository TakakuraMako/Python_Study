import decimal
from sympy import *
x, y = symbols('x y')
f = y *Rational(8,3) * x * (x-1) * (x-2) - 6 * x * (x-0.5) * (x-2) + Rational(2,3) * x * (x-0.5) * (x-1)
g = expand(f)
g = nsimplify(g)
print(g) 