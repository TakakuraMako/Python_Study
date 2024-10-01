from sympy import *
import tkinter as tk
import math
level, acc_a, acc_b, basis, extra= symbols('level acc_a acc_b basis extra')
x, aa, ab, b, e= symbols('x a_a a_b b e')
fx1 = basis * ((level - 1) ** (0.9 + acc_a / 250)) * level * (level + 1) / (6 + (level ** 2) / (50 * acc_b)) + (level - 1) * extra
fx2 = basis * (level ** (0.9 + acc_a / 250)) * (level + 1) * (level + 2) / (6 + ((level + 1) ** 2) / (50 * acc_b)) + level * extra

fx3 = sympify(fx2 - fx1).subs({basis: b, extra: e, acc_a: aa, acc_b: ab, level: x})
fx4 = expand(fx3)
print(latex(fx3))
print(latex(fx4))
# x = 3
# print('升级到{}级需要经验{}'.format(x, fx1.subs({basis: 30, extra: 20, acc_a: 30, acc_b: 30, level: x})))
# result = fx3.subs({basis: 30, extra: 20, acc_a: 30, acc_b: 30, level: x})
# print('{}级升级到{}级需要经验{}'.format(x, x+1,result))