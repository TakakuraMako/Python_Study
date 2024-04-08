import operator
from math import log2
import visual_decision_tree
import pandas as pd


def createDataSet():
    # 数据集D
    #dataSet = pd.read_csv('./不会做/西瓜数据集 2.0.csv')
    
    dataSet = [['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
               ['乌黑', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', '好瓜'],
               ['乌黑', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
               ['青绿', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', '好瓜'],
               ['浅白', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
               ['青绿', '稍蜷', '浊响', '清晰', '稍凹', '软粘', '好瓜'],
               ['乌黑', '稍蜷', '浊响', '稍糊', '稍凹', '软粘', '好瓜'],
               ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '硬滑', '好瓜'],
               ['乌黑', '稍蜷', '沉闷', '稍糊', '稍凹', '硬滑', '坏瓜'],
               ['青绿', '硬挺', '清脆', '清晰', '平坦', '软粘', '坏瓜'],
               ['浅白', '硬挺', '清脆', '模糊', '平坦', '硬滑', '坏瓜'],
               ['浅白', '蜷缩', '浊响', '模糊', '平坦', '软粘', '坏瓜'],
               ['青绿', '稍蜷', '浊响', '稍糊', '凹陷', '硬滑', '坏瓜'],
               ['浅白', '稍蜷', '沉闷', '稍糊', '凹陷', '硬滑', '坏瓜'],
               ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '软粘', '坏瓜'],
               ['浅白', '蜷缩', '浊响', '模糊', '平坦', '硬滑', '坏瓜'],
               ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑', '坏瓜']]

    # 属性集A
    labels = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感']
    return dataSet, labels


# 计算信息熵
def calcShannonEnt(dataSet):
    # 返回数据集的行数
    numDataSet = len(dataSet)
    # 保存每个标签的出现次数的字典
    lableCounts = {}
    # 对每组特征向量进行统计
    for featVec in dataSet:
        # 提取标签信息
        currentLable = featVec[-1]
        # 如果标签未放入统计次数字典，添加进去，初始值0
        if currentLable not in lableCounts.keys():
            lableCounts[currentLable] = 0
        # 样本标签计数
        lableCounts[currentLable] += 1
    infoEntropy = 0.0
    # 计算信息熵
    for key in lableCounts:
        # 当前样本集合中第k类样本所占的比例(指的是标签那一栏，例如：好瓜和坏瓜的占比)
        pk = float(lableCounts[key]) / numDataSet
        # 公式计算信息熵
        infoEntropy -= pk * log2(pk)
    print(infoEntropy)
    return infoEntropy


# 按照特征属性划分数据集
def splitDataSet(dataSet, i, value):
    # 创建返回的数据集列表
    retDataSet = []
    # 遍历数据集（即所取的数据集的某一列）
    for featVec in dataSet:
        # 如果有这个属性，就操作对应的这一行数据
        if featVec[i] == value:
            # 这一行数据去掉i属性
            reducedFeatVec = featVec[:i]
            reducedFeatVec.extend(featVec[i + 1:])
            # 将去掉i属性的每一行数据，合并起来形成一个新的数据集、
            # 它的行数，即len()长度就是它占总体数据集的比重
            retDataSet.append(reducedFeatVec)
            # 返回划分后的数据集
    return retDataSet


# 选择最优划分属性
def selectBestFeatureToSplit(dataSet, i):
    print("*" * 20)
    print("第%d次划分" % i)
    # 特征的数量
    numFeatures = len(dataSet[0]) - 1
    # 数据集D的信息熵
    baseEntropy = calcShannonEnt(dataSet)
    # 信息增益
    bestInfoGain = 0.0
    # 最优属性的索引值
    bestFeature = -1
    # 遍历所有的特征值
    for i in range(numFeatures):
        # 遍历dataSize数据集中的第i个特征属性
        featList = [example[i] for example in dataSet]  # 二维数组按列访问属性
        uniqueVals = set(featList)  # set集合中存储不重复的属性元素
        newEntropy = 0.0  # Dv的信息熵（分支结点属性的信息熵）
        # 对每一个特征属性计算信息增益
        for value in uniqueVals:
            # subDataSet是每个特征按照其几种不同的属性划分的数据集
            subDataSet = splitDataSet(dataSet, i, value)
            # 计算分支结点的权重，也就是子集的概率
            prob = len(subDataSet) / float(len(dataSet))
            # 计算赋予了权重的分支结点的信息熵的和
            newEntropy += prob * calcShannonEnt(subDataSet)
        # 第i个属性的信息增益
        infoGain = baseEntropy - newEntropy
        # 打印属性对应的信息增益
        print("\"%s\"特征的信息增益为%.3f" % (labels[i], infoGain))
        # 寻找最优的特征属性
        if infoGain > bestInfoGain:
            # 更新最优属性的信息熵和索引值
            bestInfoGain = infoGain
            bestFeature = i
    print("bestInfoGain: %.3f" % bestInfoGain)
    # 返回最优属性（最大信息增益）的索引值
    print("本次划分的最优属性是：%s" % labels[bestFeature])
    return bestFeature


# 统计classList中出现次数最多的元素（标签）
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # 根据字典的值降序排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1),
                              reverse=True)
    # 返回classList中出现次数最多的元素
    return sortedClassCount[0][0]


"""
函数说明:递归构建决策树
Parameters:
    dataSet - 训练数据集
    labels - 分类属性标签
    featLabels - 存储选择的最优特征标签
Returns:
    myTree - 决策树
"""


# 准备工作完成，开始递归构建决策树myTree
def createTree(dataSet, labels, featLabels, i):
    i += 1
    # 取分类标签(好瓜or坏瓜)
    classList = [example[-1] for example in dataSet]
    # 如果类别完全相同则停止继续划分，最后输出是好瓜还是坏瓜
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 遍历完所有特征时返回出现次数最多的类标签
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    # select返回最优特征的索引值，bestFeat获取的是索引值
    bestFeat = selectBestFeatureToSplit(dataSet, i)
    # 获取最优属性特征
    bestFeatLabel = labels[bestFeat]
    # 将属性添加到featLables的末尾
    featLabels.append(bestFeatLabel)
    # 根据最优特征的标签生成树
    myTree = {bestFeatLabel: {}}
    # 删除已经使用特征标签
    del (labels[bestFeat])
    # 得到训练集中所有最优特征的属性值
    featValues = [example[bestFeat] for example in dataSet]
    # 去掉重复的属性值
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        # 递归调用函数createTree(),遍历特征，创建决策树。
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels, featLabels, i)
    return myTree


# """
# 函数说明:使用决策树执行分类
# Parameters:
#     inputTree - 已经生成的决策树
#     featLabels - 存储选择的最优特征标签
#     testVec - 测试数据列表，顺序对应最优特征标签
# Returns:
#     classLabel - 分类结果
# """

# # 使用决策树执行分类
# def classify(inputTree, featLabels, testVec):
#     firstStr = next(iter(inputTree))  # 获取决策树结点
#     secondDict = inputTree[firstStr]  # 下一个字典
#     featIndex = featLabels.index(firstStr)
#     for key in secondDict.keys():
#         if testVec[featIndex] == key:
#             if type(secondDict[key]).__name__ == 'dict':
#                 classLabel = classify(secondDict[key], featLabels, testVec)
#             else:
#                 classLabel = secondDict[key]
#     return classLabel


if __name__ == '__main__':
    dataSet, labels = createDataSet()
    featLabels = []
    i = 0
    myTree = createTree(dataSet, labels, featLabels, i)
    print(myTree)
    visual_decision_tree.createPlot(myTree)
    # testVec = ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '软粘']  # 测试数据
    # result = classify(myTree, featLabels, testVec)
    # if result == '好瓜':
    #     print('好瓜')
    # if result == '坏瓜':
    #     print('坏瓜')


