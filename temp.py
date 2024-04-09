import math
import sympy
from sympy import diff
from sympy import symbols
delta_t = [0.408,0.295,0.355]
at = [14.834,16.736,12.78]
Ux = [104,145,123]
a = []
b = []
def func(t,U):
    return sympy.log(9.27*10**(-15)/(t*(1+2.26*10**-2*sympy.sqrt(t)))**3/2/U,sympy.E)
t,U = symbols("t,U")

for i in range(3):
    a.append(diff(func(t,U),t).subs([(t,at[i]),(U,Ux[i])]))
    b.append(diff(func(t,U),U).subs([(t,at[i]),(U,Ux[i])]))
Ur = []
q = [1.377*10**(-18),8.178*10**(-19),1.468*10**(-18)]
delta_q = []
n = [9,6,10]
delta_e = []
for i in range(3):
    Ur.append(math.sqrt((a[i]*delta_t[i])**2 + (b[i]*delta_t[i])**2))
    delta_q.append(q[i]*Ur[i])
    delta_e.append(delta_q[i]/n[i])
e = [1.53*10**(-19),1.363*10**(-19),1.468*10**(-19)]
ae = 0
for i in range(3):
    ae += 1/3*e[i]
print((1.6*10**(-19)-ae)/ae)