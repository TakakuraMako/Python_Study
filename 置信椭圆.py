import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def confidence_ellipse(x,y,ax,n_std=3.0,facecolor='none',**kwargs):
    cov = np.cov(x,y)
    pearson = cov[0,1] / np.sqrt(cov[0,0]*cov[1,1])
    ell_radius_x = np.sqrt(1+pearson)
    ell_radius_y = np.sqrt(1-pearson)
    ellipse = Ellipse((0,0),width=ell_radius_x*2,height=ell_radius_y*2,facecolor=facecolor,**kwargs)
    scale_x = np.sqrt(cov[0,0]*n_std)
    scale_y = np.sqrt(cov[1,1]*n_std)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    transf = transforms.Affine2D()\
        .rotate_deg(45)\
        .scale(scale_x,scale_y)\
        .translate(mean_x,mean_y)
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)
np.random.seed(0)
x=np.random.normal(size=1000)
y=0.5*x+np.random.normal(size=1000)

fig, ax = plt.subplots()
ax.scatter(x, y, s=0.5)

# 定义不同的置信区间
n_std_values = [1, 2, 3]
colors = ['red', 'green', 'blue']

for n_std, color in zip(n_std_values, colors):
    confidence_ellipse(x, y, ax, n_std=n_std, edgecolor=color, label=f'{n_std}σ')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Confidence Ellipse of Randomly Generated 2D Data')
ax.legend()

plt.show()