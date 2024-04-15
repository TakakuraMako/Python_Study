import pandas as pd
import numpy as np

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
    
    # Create subsets based on the threshold
    left_mask = X[feature] <= threshold
    right_mask = X[feature] > threshold
    left_subset = y[left_mask]
    right_subset = y[right_mask]
    
    # Calculate the weighted average entropy of the subsets
    n = len(y)
    n_left = len(left_subset)
    n_right = len(right_subset)
    
    if n_left == 0 or n_right == 0:  # Avoid division by zero
        return 0
    
    entropy_left = entropy(left_subset)
    entropy_right = entropy(right_subset)
    weighted_entropy = (n_left / n) * entropy_left + (n_right / n) * entropy_right
    
    # Information gain is the reduction in entropy
    return parent_entropy - weighted_entropy

class TreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        """
        Initialize a decision tree node.
        
        :param feature: Feature index used for splitting the data
        :param threshold: Threshold value at which the dataset is split
        :param left: Left child (TreeNode)
        :param right: Right child (TreeNode)
        :param value: Class label if it is a leaf node, else None
        """
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

def build_tree(X, y, depth=0, max_depth=3):
    """
    Recursively build the decision tree.
    
    :param X: Features dataset
    :param y: Target values
    :param depth: Current depth of the tree
    :param max_depth: Maximum depth of the tree
    :return: TreeNode
    """
    n_samples, n_features = X.shape
    # If there are no samples or max depth is reached, return a leaf node
    if n_samples == 0 or depth == max_depth:
        leaf_value = y.mode()[0] if len(y) > 0 else None
        return TreeNode(value=leaf_value)
    
    # Find the best split
    best_gain = -1
    best_feature, best_threshold = None, None
    for feature in X.columns:
        thresholds = np.unique(X[feature])
        for threshold in thresholds:
            gain = information_gain(X, y, feature, threshold)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_threshold = threshold

    # If no informative split was found, return a leaf node
    if best_gain == -1:
        return TreeNode(value=y.mode()[0])

    # Split the dataset
    left_mask = X[best_feature] <= best_threshold
    right_mask = X[best_feature] > best_threshold
    left_tree = build_tree(X[left_mask], y[left_mask], depth + 1, max_depth)
    right_tree = build_tree(X[right_mask], y[right_mask], depth + 1, max_depth)
    
    # Return decision node
    return TreeNode(best_feature, best_threshold, left_tree, right_tree)

# Load and prepare the data
data = pd.read_csv('./DataScienceStudy/分类算法/心脏病/cardio_train.csv', delimiter=',')

X_subset = data.iloc[:, :-1]  # all columns except the last one
y_subset = data.iloc[:, -1]  # last column as the target

# Build the decision tree on the subset
tree = build_tree(X_subset, y_subset, max_depth=3)

# Function to print the tree structure for visualization
def print_tree(node, depth=0):
    if node.value is not None:
        print("\t" * depth + f"Leaf: {node.value}")
    else:
        print("\t" * depth + f"[{node.feature} <= {node.threshold}]")
        print_tree(node.left, depth + 1)
        print_tree(node.right, depth + 1)

# Visualize the tree
print_tree(tree)
