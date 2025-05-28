# eval.py

import os
import torch
import torch.nn as nn
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
from model1 import RAFResNet            # 根据你的文件名调整
from sklearn.metrics import (
    accuracy_score,
    precision_score, recall_score, f1_score,
    cohen_kappa_score,
    classification_report, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # —— 基本配置 —— #
    DATA_DIR   = './深度学习/RAF-DB/data/DATASET'
    TEST_DIR   = os.path.join(DATA_DIR, 'test')
    BATCH_SIZE = 64
    DEVICE     = 'cuda' if torch.cuda.is_available() else 'cpu'
    MODEL_PATH = 'best_model.pth'
    NUM_CLASSES = 7

    # —— 数据预处理 —— #
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]
    test_transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    # —— 构建测试集 DataLoader —— #
    test_ds = datasets.ImageFolder(root=TEST_DIR, transform=test_transform)
    class_names = test_ds.classes
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # —— 加载模型 —— #
    model = RAFResNet(num_classes=NUM_CLASSES, dropout_p=0.5).to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()

    # —— 评估 —— #
    criterion = nn.CrossEntropyLoss(reduction='sum')  # sum 方便后面算平均

    all_preds  = []
    all_labels = []
    total_loss = 0.0

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            outputs = model(imgs)
            loss    = criterion(outputs, labels)
            total_loss += loss.item()

            preds = outputs.argmax(dim=1)
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(labels.cpu().tolist())

    # 平均 loss 和各类指标
    test_loss = total_loss / len(test_ds)
    acc       = accuracy_score(all_labels, all_preds)
    prec_m    = precision_score(all_labels, all_preds, average='macro')
    rec_m     = recall_score(all_labels, all_preds, average='macro')
    f1_m      = f1_score(all_labels, all_preds, average='macro')
    prec_i    = precision_score(all_labels, all_preds, average='micro')
    rec_i     = recall_score(all_labels, all_preds, average='micro')
    f1_i      = f1_score(all_labels, all_preds, average='micro')
    kappa     = cohen_kappa_score(all_labels, all_preds)

    print(f'\nTest Loss:       {test_loss:.4f}')
    print(f'Test Accuracy:   {acc:.4f}')
    print(f'Precision (M):   {prec_m:.4f}  Recall (M): {rec_m:.4f}  F1 (M): {f1_m:.4f}')
    print(f'Precision (µ):   {prec_i:.4f}  Recall (µ): {rec_i:.4f}  F1 (µ): {f1_i:.4f}')
    print(f"Cohen's Kappa:   {kappa:.4f}\n")

    # 分类报告
    print('Classification Report:')
    print(classification_report(
        all_labels, all_preds,
        target_names=class_names,
        digits=4
    ))

    # 混淆矩阵可视化
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8,6))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names
    )
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
