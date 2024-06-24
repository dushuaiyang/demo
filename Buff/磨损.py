import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 读取数据
data = pd.read_csv('arm2.csv')  # 替换为你的数据文件路径

data.dropna(inplace=True)
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['type'] = pd.to_numeric(data['type'], errors='coerce')
# 建立模型
X = data['type'].tolist()  # 将X转换为普通的 Python 列表
y = data['price'].tolist()  # 将y转换为普通的 Python 列表

model = LinearRegression()
model.fit(np.array(X).reshape(-1, 1), y)  # 将X转换为二维数组

# 绘制散点图和拟合线
plt.figure(figsize=(10, 6))
plt.scatter(X, y, alpha=0.5, label='Data')

# 绘制拟合线
plt.plot(X, model.predict(np.array(X).reshape(-1, 1)), color='red', label='Linear Regression')

plt.title('Price vs type with Linear Regression Fit')
plt.xlabel('type')
plt.ylabel('Price')
plt.legend()
plt.xticks(rotation=45)  # 使x轴标签斜着显示，方便查看
plt.grid(True)
plt.show()
