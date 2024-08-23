import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1, 1)
y1 = 2*x + 1
y2 = 2 ** x

'''
x = np.array([1, 2, 3, 6, 15, 30])
y = np.array([2, 3, 6, 9, 15, 20])
'''

plt.figure(num=3, figsize=(8,5))
l1, = plt.plot(x, y1)
l2, = plt.plot(x, y2)#返回列表，留逗号
plt.xlabel('Xx')
plt.ylabel('Yy')
plt.xlim((0,5))
plt.ylim((0,5))

y_ticks = np.linspace(0, 2, 5)#显示的坐标数据
# y_ticks = np.append(y_ticks, [-1])
plt.yticks(y_ticks)


ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', min(y_ticks)))
ax.spines['left'].set_position(('data', 0))

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(20)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha = 0.7))

plt.legend(handles = [l1,l2,],labels = ['first','second'], loc='best')

x0 = 1
y0 = 2*x0 + 1
plt.scatter(x0, y0, s = 20, color = 'b')#点
plt.plot([x0,x0],[y0,0], 'k--', lw = 2.5)#画一条线

#法1
plt.annotate(r'$2x+1=%s$' % y0,xy = (x0,y0), xycoords='data',xytext=(+30,-30), textcoords='offset points',fontsize = 16, arrowprops=dict(arrowstyle = '->', connectionstyle = 'arc3, rad = .2'))

#法2
plt.text(-3.7,3,r'$This\ is\ the\ some\ text.\ \mu\ \sigma_i\ \alpha_t$', fontdict={'size':16,'color':'r'})

plt.show()