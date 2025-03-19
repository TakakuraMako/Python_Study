import torch
from torch import nn
from torch.nn import init
import numpy as np
from IPython import display
import torch.utils.data as Data

num_inputs = 500
num_examples = 10000
#
true_w = torch.ones(500,1)*0.0056
true_b = 0.028
#随机生成的数据样本
features = torch.tensor(np.random.normal(0, 1, (num_examples, num_inputs)), dtype=torch.float)#行*列=10000*500
labels = torch.mm(features,true_w) + true_b
labels += torch.tensor(np.random.normal(0, 0.01, size=labels.size()), dtype=torch.float) #扰动项
#训练集和测试集上的样本&标签数----真实的特征和样本
trainfeatures = features[:7000]
trainlabels = labels[:7000]
testfeatures = features[7000:]  
testlabels = labels[7000:]
print(trainfeatures.shape,trainlabels.shape,testfeatures.shape,testlabels.shape)

