import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 加载数据集
(X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()
print("训练集与测试集形状",X_train.shape, X_test.shape)
# (60000, 28, 28) (10000, 28, 28)
# 60000个训练样本，每个样本是一个28*28的图片

# 数据预处理
## 归一化
## 每个像素点的值是0-255之间的整数，将其归一化到0-1之间
X_train = X_train / 255.0
X_test = X_test / 255.0

# 构建模型
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 编译模型
model.compile(
    optimizer='adam', #默认学习率learning_rate=0.001
    loss='sparse_categorical_crossentropy', #损失函数
    metrics=['accuracy'] #评估指标 准确率
)

# 训练模型
history = model.fit(X_train, Y_train, epochs=10, validation_split=0.2, batch_size=64)
# 每个 epoch 的 steps = 48000 / 64 = 750

# 评估模型
# test_loss, test_acc = model.evaluate(X_test, Y_test)
print("验证集最终准确率:", history.history['val_accuracy'][-1])

# 绘制准确率曲线
plt.plot(history.history['accuracy'], label='训练集准确率')
plt.plot(history.history['val_accuracy'], label='验证集准确率')
plt.xticks(range(0, 10))
plt.yticks(np.linspace(min(min(history.history['accuracy']), min(history.history['val_accuracy'])), 1, 11))
plt.title('准确率曲线')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()