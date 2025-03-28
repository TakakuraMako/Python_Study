import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 使plt支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data = pd.DataFrame(np.array([[184, 207, 236, 262, 284, 311, 354, 437, 485, 550, 693, 762, 803, 896, 1070, 1331, 1746, 2336, 2641, 2834, 2972, 3180],
                     [138, 158, 178, 199, 221, 246, 283, 347, 376, 417, 508, 553, 571, 621, 718, 855, 1118, 1434, 1768, 1876, 1895, 1973],
                     [405, 434, 496, 562, 576, 603, 662, 802, 920, 1089, 1431, 1568, 1686, 1925, 2356, 3027, 3891, 4874, 5430, 5796, 6217, 6651]]).T, index=range(1978, 2000), columns=['全国居民', '农村居民', '城镇居民'])

# 每一列分为10组，分别做直方图
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, col in enumerate(data.columns):
    data[col].plot(kind='hist', bins=10, ax=axes[i], title=col)
    axes[i].set_xlabel('频数')
    axes[i].set_xlim(0, 7000)

plt.show()