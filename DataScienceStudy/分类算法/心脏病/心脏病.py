from concurrent.futures import ThreadPoolExecutor
from graphviz import Digraph
import numpy as np
import pandas as pd



def entropy(y):
    """Calculate the entropy of a dataset."""
    class_labels = np.unique(y)
    entropy = 0
    for cls in class_labels:
        p_cls = len(y[y == cls]) / len(y)
        entropy += -p_cls * np.log2(p_cls)
    return entropy

def information_gain(X, y, feature, threshold):
    """Calculate the information gain of a split on a given feature."""
    parent_entropy = entropy(y)
    left_mask = X[feature] <= threshold
    right_mask = X[feature] > threshold
    left_subset = y[left_mask]
    right_subset = y[right_mask]
    n = len(y)
    n_left = len(left_subset)
    n_right = len(right_subset)
    if n_left == 0 or n_right == 0:  # Avoid division by zero
        return 0
    entropy_left = entropy(left_subset)
    entropy_right = entropy(right_subset)
    weighted_entropy = (n_left / n) * entropy_left + (n_right / n) * entropy_right
    return parent_entropy - weighted_entropy


class TreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

def build_tree(X, y, depth=0, max_depth=3):
    n_samples, n_features = X.shape
    if n_samples == 0 or depth == max_depth:
        leaf_value = y.mode()[0] if len(y) > 0 else None
        return TreeNode(value=leaf_value)
    best_gain = -1
    best_feature, best_threshold = None, None
    # Use ThreadPoolExecutor to parallelize gain calculations
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = []
        for feature in X.columns:
            thresholds = np.unique(X[feature])
            futures = {executor.submit(information_gain, X, y, feature, threshold): (feature, threshold) for threshold in thresholds}
            for future in futures:
                feature, threshold = futures[future]
                gain = future.result()
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
    if best_gain == -1:
        return TreeNode(value=y.mode()[0])
    left_mask = X[best_feature] <= best_threshold
    right_mask = X[best_feature] > best_threshold
    left_tree = build_tree(X[left_mask], y[left_mask], depth + 1, max_depth)
    right_tree = build_tree(X[right_mask], y[right_mask], depth + 1, max_depth)
    return TreeNode(best_feature, best_threshold, left_tree, right_tree)

def draw_tree(tree, dot=None, parent=None, label=None):
    if dot is None:
        dot = Digraph(comment='Decision Tree')
    if tree.value is not None:
        node_label = f"Leaf: {tree.value}"
        node_shape = 'ellipse'
    else:
        node_label = f"{tree.feature} <= {tree.threshold}"
        node_shape = 'box'
    node_name = str(id(tree))
    dot.node(node_name, label=node_label, shape=node_shape)
    if parent:
        dot.edge(str(id(parent)), node_name, label=label)
    if tree.left:
        draw_tree(tree.left, dot, tree, label="True")
    if tree.right:
        draw_tree(tree.right, dot, tree, label="False")
    return dot

data = pd.read_csv('./DataScienceStudy/分类算法/心脏病/cardio_train.csv', delimiter=',')
#读取数据
data = data.drop(['id'], axis = 1)#去掉id列
X_subset = data.iloc[:, :-1]  # all columns except the last one
y_subset = data.iloc[:, -1]  # last column as the target

tree = build_tree(X_subset, y_subset, max_depth=4)#控制深度减少计算时间同时防止过拟合

dot = draw_tree(tree)
dot.render('output_tree', format='png', cleanup=True)
