# train.py

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from torch.utils.data import DataLoader, random_split
from model import RAFResNet
from sklearn.metrics import accuracy_score
from tqdm import tqdm
from multiprocessing import freeze_support

def main():
    # ——— 配置 ——— #
    DATA_DIR      = './深度学习/RAF-DB/data/DATASET'
    BATCH_SIZE    = 64
    NUM_WORKERS   = 0
    NUM_CLASSES   = 7
    NUM_EPOCHS    = 20
    LR            = 1e-4
    VAL_SPLIT     = 0.1
    DEVICE        = 'cuda' if torch.cuda.is_available() else 'cpu'
    SAVE_PATH     = 'best_model.pth'

    # 早停配置
    patience = 5
    no_improve_count = 0

    # 数据变换
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]
    train_transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    test_transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    # 加载数据集
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
    val_loader   = DataLoader(
        val_ds,   batch_size=BATCH_SIZE,
        shuffle=False, num_workers=NUM_WORKERS
    )
    test_ds     = datasets.ImageFolder(
        root=os.path.join(DATA_DIR, 'test'),
        transform=test_transform
    )
    test_loader = DataLoader(
        test_ds,  batch_size=BATCH_SIZE,
        shuffle=False, num_workers=NUM_WORKERS
    )

    model     = RAFResNet(num_classes=NUM_CLASSES).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    best_val_acc = 0.0

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

        print(f'— Epoch {epoch} — '
              f'Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | '
              f' Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}')

        # 保存并更新最佳指标
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), SAVE_PATH)
            print(f'    ↑ New best model saved (val_acc={val_acc:.4f})')
            no_improve_count = 0
        else:
            no_improve_count += 1
            print(f'    — No improvement for {no_improve_count}/{patience} epochs')

        # 检查是否触发早停
        if no_improve_count >= patience:
            print(f'\nEarly stopping triggered at epoch {epoch}.')
            break

        scheduler.step()

    # 测试集评估
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
