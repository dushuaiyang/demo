import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


# 读取数据
data = pd.read_csv('ob.csv', encoding='utf-8')
data.drop(columns=['时间'], inplace=True)

# 提取特征和目标变量
X = data.drop(columns=['价格'])
y = data['价格']

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.8, random_state=42)

# 建立模型
model = Sequential([
    Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1)
])

# 编译模型
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 训练模型
history = model.fit(X_train, y_train, epochs=500, batch_size=32, validation_data=(X_test, y_test))

# 绘制测试集的实际价格和预测价格
predictions_test = model.predict(X_test)

plt.figure(figsize=(10, 6))

# 绘制实际价格
plt.plot(y_test.values, label='实际价格', color='blue')

# 绘制预测价格
plt.plot(predictions_test, label='预测价格', color='orange')

plt.title('测试集实际价格 vs 预测价格')
plt.xlabel('样本编号')
plt.ylabel('价格')
plt.legend()
plt.grid(True)
plt.show()
