import os
from PIL import Image
from torch.utils.data import Dataset

class RAFDataset(Dataset):
    def __init__(self, img_dir, label_file, transform=None):
        """
        img_dir: 图像所在目录，例如 './RAF-basic/Image/train'
        label_file: 标签文件路径，例如 './RAF-basic/Label/train_label.txt'
        transform: torchvision.transforms.Compose 对象
        """
        self.img_dir = img_dir
        self.transform = transform
        # 读取标签文件，每行格式：<img_name> <label_id>
        with open(label_file, 'r') as f:
            lines = f.readlines()
        # 存成 [(img_name, label_id), ...]
        self.samples = [line.strip().split() for line in lines]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_name, label = self.samples[idx]
        img_path = os.path.join(self.img_dir, img_name + '.jpg')
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, int(label)
    