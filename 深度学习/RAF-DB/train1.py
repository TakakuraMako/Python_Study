# train_with_early_stop.py

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from torchvision.transforms import (
    RandomResizedCrop, RandomHorizontalFlip, RandomRotation,
    ColorJitter, RandomErasing
)
from torch.utils.data import DataLoader, random_split
from model1 import RAFResNet
from sklearn.metrics import accuracy_score
from tqdm import tqdm
from multiprocessing import freeze_support
import matplotlib.pyplot as plt  # 用于绘图

def main():
    # —— 配置 —— #
    DATA_DIR      = './深度学习/RAF-DB/data/DATASET'
    BATCH_SIZE    = 64
    NUM_WORKERS   = 0
    NUM_CLASSES   = 7
    NUM_EPOCHS    = 20
    LR            = 1e-4
    VAL_SPLIT     = 0.1
    DEVICE        = 'cuda' if torch.cuda.is_available() else 'cpu'
    SAVE_PATH     = 'best_model.pth'

    # —— 早停配置 —— #
    patience       = 5    # 连续多少个 epoch 验证集没提升就停
    no_improve_cnt = 0

    # —— 用于记录曲线 —— #
    train_losses_history = []
    val_losses_history   = []
    train_accs_history   = []
    val_accs_history     = []

    # 统计用的均值/标准差
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]

    # —— 数据增强 & 预处理 —— #
    train_transform = transforms.Compose([
        RandomResizedCrop(224, scale=(0.8, 1.0)),
        RandomHorizontalFlip(p=0.5),
        RandomRotation(degrees=15),
        ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
        RandomErasing(p=0.5, scale=(0.02, 0.2))
    ])
    test_transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    # —— 加载数据集 —— #
    full_train = datasets.ImageFolder(
        root=os.path.join(DATA_DIR, 'train'),
        transform=train_transform
    )
    val_size   = int(VAL_SPLIT * len(full_train))
    train_size = len(full_train) - val_size
    train_ds, val_ds = random_split(full_train, [train_size, val_size])

    train_loader = DataLoader(
        train_ds, batch_size=BATCH_SIZE,
        shuffle=True,  num_workers=NUM_WORKERS
    )
    val_loader = DataLoader(
        val_ds,   batch_size=BATCH_SIZE,
        shuffle=False, num_workers=NUM_WORKERS
    )

    test_ds = datasets.ImageFolder(
        root=os.path.join(DATA_DIR, 'test'),
        transform=test_transform
    )
    test_loader = DataLoader(
        test_ds, batch_size=BATCH_SIZE,
        shuffle=False, num_workers=NUM_WORKERS
    )

    # —— 模型、损失、优化器、调度器 —— #
    model     = RAFResNet(num_classes=NUM_CLASSES, dropout_p=0.5).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR,
        weight_decay=1e-4
    )
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    best_val_acc = 0.0

    # —— 训练 & 验证 —— #
    for epoch in range(1, NUM_EPOCHS + 1):
        model.train()
        train_losses, train_preds, train_labels = [], [], []
        loop = tqdm(train_loader, desc=f'Epoch {epoch}/{NUM_EPOCHS} [Train]')
        for imgs, labels in loop:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss    = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_losses.append(loss.item())
            train_preds.extend(outputs.argmax(dim=1).cpu().numpy())
            train_labels.extend(labels.cpu().numpy())
            loop.set_postfix(loss=loss.item())

        train_loss = sum(train_losses) / len(train_losses)
        train_acc  = accuracy_score(train_labels, train_preds)
        train_losses_history.append(train_loss)
        train_accs_history.append(train_acc)

        model.eval()
        val_losses, val_preds, val_labels = [], [], []
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                outputs = model(imgs)
                loss    = criterion(outputs, labels)
                val_losses.append(loss.item())
                val_preds.extend(outputs.argmax(dim=1).cpu().numpy())
                val_labels.extend(labels.cpu().numpy())

        val_loss = sum(val_losses) / len(val_losses)
        val_acc  = accuracy_score(val_labels, val_preds)
        val_losses_history.append(val_loss)
        val_accs_history.append(val_acc)

        print(f'— Epoch {epoch} — '
              f'Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | '
              f' Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}')

        # —— 保存最佳并更新早停计数 —— #
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), SAVE_PATH)
            print(f'    ↑ New best model saved (val_acc={val_acc:.4f})')
            no_improve_cnt = 0
        else:
            no_improve_cnt += 1
            print(f'    — No improvement for {no_improve_cnt}/{patience} epochs')

        # —— 早停检查 —— #
        if no_improve_cnt >= patience:
            print(f'\nEarly stopping at epoch {epoch} (no improvement in last {patience} epochs)')
            break

        scheduler.step()

    # —— 绘制训练曲线 —— #
    epochs = range(1, len(train_losses_history) + 1)

    plt.figure()
    plt.plot(epochs, train_losses_history, label='Train Loss')
    plt.plot(epochs, val_losses_history,   label='Val Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Loss Curve')
    plt.savefig('loss_curve.png')
    plt.show()

    plt.figure()
    plt.plot(epochs, train_accs_history, label='Train Acc')
    plt.plot(epochs, val_accs_history,   label='Val Acc')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Accuracy Curve')
    plt.savefig('acc_curve.png')
    plt.show()

    # —— 测试集评估 —— #
    print('\n==> Load best model for testing')
    model.load_state_dict(torch.load(SAVE_PATH))
    model.eval()
    test_preds, test_labels = [], []
    with torch.no_grad():
        for imgs, labels in tqdm(test_loader, desc='Testing'):
            imgs = imgs.to(DEVICE)
            outputs = model(imgs)
            test_preds.extend(outputs.argmax(dim=1).cpu().numpy())
            test_labels.extend(labels.numpy())

    test_acc = accuracy_score(test_labels, test_preds)
    print(f'\nTest Accuracy: {test_acc:.4f}')

if __name__ == '__main__':
    freeze_support()
    main()
