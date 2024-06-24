import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

import matplotlib.pyplot as plt

import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import tensorflow as tf
import random
import os

# 随机种子
random.seed(1)
tf.random.set_seed(1)

data = pd.read_csv('ob.csv', encoding='utf-8')
data.drop(columns=['时间'], inplace=True)
# print(data.head())

# 提取特征和目标变量
X = data.drop(columns=['价格'])
y = data['价格']

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

#  使用Sequential函数构造多层感知机
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    Dense(1)
])

# 编译模型 optimizer用来调整权重的算法。adam是(自适应矩估计)  模型评估的指标
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# 训练模型
history = model.fit(X_train, y_train, epochs=500, batch_size=32, validation_data=(X_test, y_test))
# 获取每一层的权重和偏置项
for layer in model.layers:
    weights = layer.get_weights()
    if weights:
        print(f"Layer: {layer.name}")
        print(f"Weights shape: {weights[0].shape}")
        print(f"Weights values: {weights[0]}")
        print(f"Bias shape: {weights[1].shape}")
        print(f"Bias values: {weights[1]}")
        print("\n")


# 评估模型
loss, mae = model.evaluate(X_test, y_test)
print(f"测试集上的损失: {loss}, 平均绝对误差: {mae}")

# 进行预测
predictions = model.predict(X_test)

# 打印实际价格和预测价格
for i in range(10):
    print(f"实际价格: {y_test.iloc[i]}, 预测价格: {predictions[i][0]}")

plt.figure(figsize=(10, 6))

plt.plot(y_test.values, label='实际价格', color='blue')
plt.plot(predictions, label='预测价格', color='orange')

plt.title('实际价格 vs 预测价格')
plt.xlabel('样本编号')
plt.ylabel('价格')
plt.legend()
plt.grid(True)
plt.show()

#  探究什么原因对价格的影响程度
# 原始的测试集评估
baseline_loss, baseline_mae = model.evaluate(X_test, y_test)

feature_importance = np.zeros(X.shape[1])
for i in range(X.shape[1]):
    X_test_drop = np.copy(X_test)
    X_test_drop[:, i] = 0
    # 计算预测结果并评估性能
    loss_drop, mae_drop = model.evaluate(X_test_drop, y_test)
    # 计算特征 i 的 drop feature importance
    feature_importance[i] = (baseline_loss - loss_drop) / baseline_loss

# 可视化
plt.figure(figsize=(10, 6))
plt.bar(range(X.shape[1]), feature_importance, align="center")
plt.xticks(range(X.shape[1]), X.columns, rotation=90)
plt.xlabel("特征")
plt.ylabel("特征影响程度")
plt.title("不同特征对数据的影响程度")
plt.tight_layout()
plt.show()
# from sklearn.model_selection import KFold
#
# # KFold交叉验证
# kf = KFold(n_splits=5, shuffle=True, random_state=1)
#
# # 存储每个折叠的结果
# scores = []
#
# for train_index, test_index in kf.split(X_scaled):
#     X_train_cv, X_test_cv = X_scaled[train_index], X_scaled[test_index]
#     y_train_cv, y_test_cv = y.iloc[train_index], y.iloc[test_index]
#
#     # 构建模型
#     model_cv = Sequential([
#         Dense(128, activation='relu', input_shape=(X_train_cv.shape[1],)),
#         Dropout(0.5),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(1)
#     ])
#
#     # 编译模型
#     model_cv.compile(optimizer='adam', loss='mse', metrics=['mae'])
#
#     # 训练模型
#     history_cv = model_cv.fit(X_train_cv, y_train_cv, epochs=500, batch_size=32, validation_data=(X_test_cv, y_test_cv))
#
#     # 评估模型
#     loss_cv, mae_cv = model_cv.evaluate(X_test_cv, y_test_cv)
#     scores.append(mae_cv)
#
# # 打印交叉验证结果
# print("交叉验证结果:")
# for i, score in enumerate(scores):
#     print(f"折叠 {i+1} 平均绝对误差: {score}")
# print(f"平均平均绝对误差: {np.mean(scores)}")

