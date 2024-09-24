from sympy import *
import decimal
x = symbols('x')
str = input("函数：")
y1 = 0
a = decimal.Decimal(input("下限"))
b = decimal.Decimal(input("上限"))
accuracy = decimal.Decimal(eval(input("精确度")))

f_x = sympify(str)
while(true):
    y2 = f_x.subs(x,(a+b)/2)
    #print(float(y2))
    if y2 == 0:
        print((a + b)/2)
        break
    elif abs(y1 - y2) < accuracy:
        print((a + b)/2)
        break
    elif y2*f_x.subs(x,a) > 0:
        a = (a + b)/2
    elif y2*f_x.subs(x,a) < 0:
        b = (a + b)/2
    
