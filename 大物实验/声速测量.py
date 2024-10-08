from sympy import *
# x1 = [19, 23.52, 28.2, 33.04, 37.50, 42.02, 46.80, 51.20, 55.80, 59.72]
# x2 = [111.04, 115.72, 120.38, 124.74, 129.48, 134.00, 138.54, 143.34, 148.00, 152.56]
# x_delta = []
# for i in range(len(x1)):
#     x_delta.append(round(x2[i] - x1[i], 2))
# x_d_average = sum(x_delta)/10
# sum = 0
# for i in range(len(x1)):
#     sum += (x_delta[i] - x_d_average) ** 2
# S_x = sqrt(sum / 9)

# print(x_delta, x_d_average, S_x, sep='\n')

x1 = [30.2, 41.08, 50.14, 59.68, 69.16, 78.34, 87.46, 91.1, 106.12, 115.12]
x2 = [122.54, 133.92, 143.32, 152.86, 161.7, 170.6, 180.02, 183.20, 198.58, 207.70]
dx = [92.34, 92.84, 92.96, 93.18, 92.54, 92.26, 92.56, 92.1, 92.38, 92.58]
sum = 0
for i in range(len(dx)):
    sum += dx[i]
dx_average = (round(sum / 10, 2))
temp = 0
for i in range(len(dx)):
    temp += (dx_average - dx[i])**2
S_x = round(sqrt(temp / 9), 4)
print(S_x)
print(331.21*sqrt(1+22.5/237.15))