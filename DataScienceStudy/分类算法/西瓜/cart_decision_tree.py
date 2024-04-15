
import pandas as pd
import numpy as np

def gini_index(y):
    if len(y) == 0: return 0
    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    return 1 - np.sum(np.square(probabilities))

def split_dataset(X, y, feature, value):
    mask = X[feature] == value
    X_left, y_left = X[mask], y[mask]
    X_right, y_right = X[~mask], y[~mask]
    return X_left, y_left, X_right, y_right

def best_split(X, y):
    best_gini = 1.0
    best_feature = None
    best_value = None
    for feature in X.columns:
        unique_values = X[feature].unique()
        for value in unique_values:
            _, y_left, _, y_right = split_dataset(X, y, feature, value)
            gini = gini_index(y_left) * (len(y_left) / len(y)) + gini_index(y_right) * (len(y_right) / len(y))
            if gini < best_gini:
                best_gini = gini
                best_feature = feature
                best_value = value
    return best_feature, best_value

def build_tree(X, y, depth=0, max_depth=3):
    if len(np.unique(y)) == 1:
        return {'label': np.unique(y)[0]}
    if depth == max_depth:
        return {'label': np.bincount(y).argmax()}
    best_feature, best_value = best_split(X, y)
    X_left, y_left, X_right, y_right = split_dataset(X, y, best_feature, best_value)
    left_subtree = build_tree(X_left, y_left, depth+1, max_depth)
    right_subtree = build_tree(X_right, y_right, depth+1, max_depth)
    return {'feature': best_feature, 'value': best_value, 'left': left_subtree, 'right': right_subtree}

def main():
    watermelon_dataset_path = '西瓜数据集 2.0.csv'
    watermelon_data = pd.read_csv(watermelon_dataset_path)
    watermelon_data = watermelon_data.drop(['编号'], axis=1)
    watermelon_data_encoded = pd.get_dummies(watermelon_data, drop_first=True)
    X = watermelon_data_encoded.drop('好瓜_是', axis=1)
    y = watermelon_data_encoded['好瓜_是']
    decision_tree = build_tree(X, y, max_depth=3)
    print(decision_tree)

if __name__ == "__main__":
    main()
