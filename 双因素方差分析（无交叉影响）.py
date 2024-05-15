import numpy as np
import scipy.stats as st

alpha = 0.05
A = np.array([[17, 11, 11, 11],
              [8, 9, 9, 8],
              [8, 13.5, 12.5, 12]])
rows, columns = A.shape
row_mean = np.mean(A,1)
column_mean = np.mean(A,0)
A_mean = np.mean(A)

SSR = 0
for i in range(len(row_mean)):
    SSR += columns*(row_mean[i]-A_mean)**2

SSC = 0
for i in range(len(column_mean)):
    SSC += rows*(column_mean[i]-A_mean)**2

SST = 0
for i in range(rows):
    for j in range(columns):
        SST += (A[i][j]-A_mean)**2

SSE = SST-SSR-SSC
MSR = SSR/(rows-1)
MSC = SSC/(columns-1)
MSE = SSE/((rows-1)*(columns-1))
Fr = MSR/MSE
Fc = MSC/MSE
F_ar = st.f.isf(alpha,rows-1,(columns-1)*(rows-1))
F_ac = st.f.isf(alpha,columns-1,(columns-1)*(rows-1))
print('行均值:{}\n列均值:{}\n总体均值:{}'.format(row_mean,column_mean,A_mean))
print('SSR:{},SSC:{},SSE:{}\nMSR:{},MSC:{},MSE:{}\nFr:{},Fc:{}'.format(SSR,SSC,SSE,MSR,MSC,MSE,Fr,Fc))

print('行上分位点:{}\n列上分位点:{}'.format(F_ar,F_ac))